#!/usr/bin/env python3
"""
ICNA Sacramento Events Scraper
Scrapes events from icnasac.org and generates an ICS calendar file
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ics import Calendar, Event
import pytz
import re
import hashlib
import json
from typing import List, Dict, Optional
import sys
import urllib.parse
import subprocess
from playwright.sync_api import sync_playwright

class ICNAEventsScraper:
    def __init__(self):
        self.base_url = "https://icnasac.org/up-coming-events/"
        self.rest_api_url = "https://icnasac.org/wp-json/bricks/v1/load_query_page"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timezone = pytz.timezone('America/Los_Angeles')
        self.wp_rest_nonce = None
        self.post_id = "478"
        self.query_element_id = "tnvmtb"
        self.pagination_id = "wupvnd"
        self.session = requests.Session()
        
    def parse_date_string(self, date_str: str) -> Optional[Dict]:
        """
        Parse date strings like:
        - "October 31, 2025, 6:00 PM – 9:00 PM PDT"
        - "July 11, 2025, 10:00 AM PDT – Jul 27, 2025, 10:00 PM PDT"
        - "March 15, 2025,  11:30 PM – Mar 16, 2025, 7:30 AM"
        """
        try:
            # Clean up the string
            date_str = date_str.strip()
            date_str = re.sub(r'\s+', ' ', date_str)  # Normalize whitespace

            # Handle three cases:
            # 1. Format A/B: Has a dash (date range or time range)
            # 2. Format C: Single date/time (no dash) - default to 2-hour duration
            if '–' in date_str or '—' in date_str:
                parts = re.split(r'[–—]', date_str)
                start_part = parts[0].strip()
                end_part = parts[1].strip() if len(parts) > 1 else ""
                
                # Parse start datetime
                # Remove timezone abbreviations for parsing
                start_clean = re.sub(r'\s+(PDT|PST)$', '', start_part)
                
                # Try different date formats
                formats = [
                    "%B %d, %Y, %I:%M %p",  # October 31, 2025, 6:00 PM
                    "%B %d, %Y, %I:%M%p",   # October 31, 2025, 6:00PM
                ]
                
                start_dt = None
                for fmt in formats:
                    try:
                        start_dt = datetime.strptime(start_clean, fmt)
                        break
                    except ValueError:
                        continue
                
                if not start_dt:
                    print(f"Warning: Could not parse start date: {start_part}")
                    return None
                
                # Parse end datetime
                end_dt = None
                end_clean = re.sub(r'\s+(PDT|PST)$', '', end_part)

                # End might be same day (just time) or different day
                if re.match(r'^\d{1,2}:\d{2}\s*[AP]M', end_clean.strip()):
                    # Same day, just time
                    time_match = re.search(r'(\d{1,2}):(\d{2})\s*([AP]M)', end_clean)
                    if time_match:
                        hour = int(time_match.group(1))
                        minute = int(time_match.group(2))
                        am_pm = time_match.group(3)

                        if am_pm == 'PM' and hour != 12:
                            hour += 12
                        elif am_pm == 'AM' and hour == 12:
                            hour = 0

                        end_dt = start_dt.replace(hour=hour, minute=minute)

                        # Handle overnight events
                        if end_dt < start_dt:
                            end_dt = end_dt + timedelta(days=1)
                    else:
                        raise ValueError(f"Could not extract time from time-only end: {end_part}")
                else:
                    # Different day - must have full date
                    # Handle abbreviated month format like "Mar 16, 2025, 7:30 AM"
                    for fmt in [
                        "%b %d, %Y, %I:%M %p",
                        "%B %d, %Y, %I:%M %p",
                        "%b %d, %Y, %I:%M%p",
                        "%B %d, %Y, %I:%M%p",
                    ]:
                        try:
                            end_dt = datetime.strptime(end_clean, fmt)
                            break
                        except ValueError:
                            continue

                    # If no format matched, raise exception instead of silently defaulting
                    if not end_dt:
                        raise ValueError(
                            f"End date does not match time-only pattern and could not parse as full date. "
                            f"End part: '{end_part}', Cleaned: '{end_clean}'. "
                            f"Expected format: 'HH:MM AM/PM' OR 'Month DD, YYYY, HH:MM AM/PM'"
                        )

                # Localize to Pacific timezone
                start_dt = self.timezone.localize(start_dt)
                end_dt = self.timezone.localize(end_dt)

                return {
                    'start': start_dt,
                    'end': end_dt
                }
            else:
                # Format C: Single date/time only - default to 2-hour duration
                start_clean = re.sub(r'\s+(PDT|PST)$', '', date_str)

                # Try to parse as full date with time
                for fmt in [
                    "%B %d, %Y, %I:%M %p",   # December 25, 2025, 2:00 PM
                    "%B %d, %Y, %I:%M%p",    # December 25, 2025, 2:00PM
                ]:
                    try:
                        start_dt = datetime.strptime(start_clean, fmt)
                        break
                    except ValueError:
                        continue

                if not start_dt:
                    raise ValueError(
                        f"Single date/time format could not parse. "
                        f"Input: '{date_str}'. "
                        f"Expected format: 'Month DD, YYYY, HH:MM AM/PM'"
                    )

                # Default to 2-hour duration for events with only start time
                end_dt = start_dt + timedelta(hours=2)

                # Localize to Pacific timezone
                start_dt = self.timezone.localize(start_dt)
                end_dt = self.timezone.localize(end_dt)

                return {
                    'start': start_dt,
                    'end': end_dt
                }

        except Exception as e:
            print(f"Error parsing date '{date_str}': {e}")
            return None
    
    def fetch_nonce(self):
        """Fetch the wpRestNonce from the events page and establish session cookies"""
        try:
            # Use comprehensive headers to match a real browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Referer': 'https://icnasac.org/'
            }

            response = self.session.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()

            print(f"✓ Established session, cookies: {list(self.session.cookies.keys())}")

            # Look for wpRestNonce in bricksData variable
            match = re.search(r'"wpRestNonce":"([a-f0-9]+)"', response.text)
            if match:
                self.wp_rest_nonce = match.group(1)
                print(f"✓ Fetched wpRestNonce: {self.wp_rest_nonce}")
                return True
            else:
                print("⚠ Warning: Could not find wpRestNonce in page...")
                return False
        except Exception as e:
            print(f"Error fetching nonce: {e}")
            return False

    def scrape_all_pages_with_browser(self) -> List[Dict]:
        """Scrape all pages using Playwright headless browser to handle JavaScript pagination"""
        all_events = []

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            try:
                # Navigate to the events page
                print(f"Loading page with browser: {self.base_url}")
                page.goto(self.base_url, wait_until='networkidle')

                # Wait for pagination to be rendered
                page.wait_for_selector('.brxe-pagination', timeout=10000)

                # Count total pages from pagination links
                # Look for numeric page links (2, 3, etc.) to determine total pages
                page_links = page.query_selector_all('.brxe-pagination a.page-numbers')
                print(f"Found {len(page_links)} pagination links")

                # The last numeric link (before the next arrow) tells us the max page
                total_pages = 1
                for link in page_links:
                    link_text = link.text_content().strip()
                    if link_text.isdigit():
                        total_pages = max(total_pages, int(link_text))

                print(f"Found {total_pages} pages total")

                # Scrape each page
                for page_num in range(1, min(total_pages + 1, 6)):  # Max 5 pages
                    print(f"Extracting events from page {page_num}")

                    # Get the HTML of all event cards on this page
                    events_html = page.locator('.brxe-tnvmtb').all()
                    page_events = 0

                    for event_elem in events_html:
                        event_html = event_elem.inner_html()
                        soup = BeautifulSoup(event_html, 'html.parser')

                        # Extract event details
                        title_elem = soup.find('h3', class_='brxe-pgsofq')
                        title = title_elem.get_text(strip=True) if title_elem else "Untitled Event"

                        date_elem = soup.find('span', class_='brxe-bnvjah')
                        date_text = ""
                        if date_elem:
                            text_span = date_elem.find('span', class_='text')
                            date_text = text_span.get_text(strip=True) if text_span else ""

                        location_elem = soup.find('span', class_='brxe-oacqsb')
                        location = ""
                        if location_elem:
                            text_span = location_elem.find('span', class_='text')
                            location = text_span.get_text(strip=True) if text_span else ""

                        desc_elem = soup.find('span', class_='brxe-henoxh')
                        description = desc_elem.get_text(strip=True) if desc_elem else ""

                        link_elem = soup.find('a', class_='brxe-giwigq')
                        event_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""

                        # Parse the date
                        date_info = self.parse_date_string(date_text) if date_text else None

                        if date_info:
                            start = date_info['start']
                            end = date_info['end']

                            # Validate that both start and end are properly set
                            if not start or not end:
                                print(f"  ✗ Skipped (incomplete date info): {title}")
                                print(f"     Date text: {date_text}")
                                print(f"     Start: {start}, End: {end}")
                                continue

                            # Fix invalid dates (end before start)
                            if end < start:
                                print(f"  ⚠ Warning: End date before start for '{title}', swapping dates")
                                start, end = end, start

                            all_events.append({
                                'title': title,
                                'start': start,
                                'end': end,
                                'location': location,
                                'description': description,
                                'url': event_url
                            })
                            print(f"  ✓ {title} - {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')}")
                            page_events += 1
                        else:
                            print(f"  ✗ Skipped (no valid date): {title}")
                            print(f"     Date text: {date_text}")

                    print(f"Found {page_events} events on page {page_num}")

                    # Click next page button if not on the last page
                    if page_num < total_pages:
                        next_button = page.locator('.brx-ajax-pagination .next.page-numbers')
                        print(f"  Next button count: {next_button.count()}")
                        if next_button.count() > 0:
                            print(f"  Navigating to page {page_num + 1}...")
                            try:
                                next_button.click()
                                print(f"  Waiting for new events to load...")
                                # Wait for the event cards to be replaced with new content
                                page.wait_for_timeout(2000)  # Give JavaScript time to update
                                page.wait_for_load_state('networkidle')
                                print(f"  Page {page_num + 1} loaded")
                            except Exception as e:
                                print(f"  ✗ Error clicking next button: {e}")
                                break
                        else:
                            print(f"  No next button found, stopping")
                            break

            finally:
                browser.close()

        print(f"\nTotal events scraped: {len(all_events)}")
        return all_events

    
    def generate_ics(self, events: List[Dict], filename: str = "icna_events.ics"):
        """Generate ICS calendar file from events"""
        calendar = Calendar()

        for event_data in events:
            try:
                event = Event()
                event.name = event_data['title']
                event.begin = event_data['start']
                event.end = event_data['end']
                event.location = event_data['location']

                # Validate times
                if not event.begin or not event.end:
                    print(f"Warning: Event '{event_data['title']}' has missing begin or end time")
                    print(f"  Begin: {event.begin}, End: {event.end}")
                    continue

                if event.end < event.begin:
                    print(f"Warning: Event '{event_data['title']}' has end before begin, skipping")
                    continue

                # Combine description and URL
                description_parts = []
                if event_data['description']:
                    description_parts.append(event_data['description'])
                if event_data['url']:
                    description_parts.append(f"\n\nMore info: {event_data['url']}")

                event.description = '\n'.join(description_parts)

                # Create unique identifier (deterministic hash for consistent deduplication)
                title_hash = hashlib.md5(event_data['title'].encode()).hexdigest()[:8]
                event.uid = f"{event_data['start'].strftime('%Y%m%d%H%M%S')}-{title_hash}"

                calendar.events.add(event)
            except Exception as e:
                print(f"Error creating ICS event for '{event_data['title']}': {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Write to file
        with open(filename, 'w') as f:
            f.writelines(calendar.serialize_iter())
        
        print(f"\n✓ Generated calendar file: {filename}")
        print(f"  Events included: {len(calendar.events)}")
        
        return filename

def main():
    print("=" * 60)
    print("ICNA Sacramento Events Scraper")
    print("=" * 60)
    print()

    scraper = ICNAEventsScraper()

    # Scrape all events using headless browser to handle JavaScript pagination
    events = scraper.scrape_all_pages_with_browser()

    if not events:
        print("\n⚠ No events found!")
        sys.exit(1)

    # Generate ICS file
    ics_file = scraper.generate_ics(events, "icna_events.ics")
    
    print("\n" + "=" * 60)
    print("✓ Scraping complete!")
    print("=" * 60)
    print(f"\nTo import into Google Calendar:")
    print("1. Go to Google Calendar")
    print("2. Click '+' next to 'Other calendars'")
    print("3. Select 'From URL'")
    print("4. Paste the public URL of icna_events.ics")
    print()

if __name__ == "__main__":
    main()
