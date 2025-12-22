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
from typing import List, Dict, Optional
import sys

class ICNAEventsScraper:
    def __init__(self):
        self.base_url = "https://icnasac.org/up-coming-events/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timezone = pytz.timezone('America/Los_Angeles')
        
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
            
            # Handle multi-day events
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
                    # Different day
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
                
                if not end_dt:
                    # Default to 1 hour duration
                    end_dt = start_dt + timedelta(hours=1)
                
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
        
        return None
    
    def scrape_page(self, page_num: int = 1) -> List[Dict]:
        """Scrape a single page of events"""
        url = self.base_url if page_num == 1 else f"{self.base_url}page/{page_num}/"
        
        print(f"Scraping page {page_num}: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            events = []
            
            # Find all event cards
            event_cards = soup.find_all('div', class_='brxe-tnvmtb')
            
            print(f"Found {len(event_cards)} events on page {page_num}")
            
            for card in event_cards:
                try:
                    # Extract title
                    title_elem = card.find('h3', class_='brxe-pgsofq')
                    title = title_elem.get_text(strip=True) if title_elem else "Untitled Event"
                    
                    # Extract date/time
                    date_elem = card.find('span', class_='brxe-bnvjah')
                    date_text = ""
                    if date_elem:
                        text_span = date_elem.find('span', class_='text')
                        date_text = text_span.get_text(strip=True) if text_span else ""
                    
                    # Extract location
                    location_elem = card.find('span', class_='brxe-oacqsb')
                    location = ""
                    if location_elem:
                        text_span = location_elem.find('span', class_='text')
                        location = text_span.get_text(strip=True) if text_span else ""
                    
                    # Extract description (optional)
                    desc_elem = card.find('span', class_='brxe-henoxh')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract event URL
                    link_elem = card.find('a', class_='brxe-giwigq')
                    event_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                    
                    # Parse the date
                    date_info = self.parse_date_string(date_text) if date_text else None
                    
                    if date_info:
                        events.append({
                            'title': title,
                            'start': date_info['start'],
                            'end': date_info['end'],
                            'location': location,
                            'description': description,
                            'url': event_url
                        })
                        print(f"  ✓ {title} - {date_info['start'].strftime('%Y-%m-%d')}")
                    else:
                        print(f"  ✗ Skipped (no valid date): {title}")
                        
                except Exception as e:
                    print(f"  ✗ Error processing event: {e}")
                    continue
            
            return events
            
        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")
            return []
    
    def scrape_all_events(self, max_pages: int = 5) -> List[Dict]:
        """Scrape all events across multiple pages"""
        all_events = []
        
        for page in range(1, max_pages + 1):
            events = self.scrape_page(page)
            
            if not events:
                print(f"No events found on page {page}, stopping.")
                break
                
            all_events.extend(events)
        
        print(f"\nTotal events scraped: {len(all_events)}")
        return all_events
    
    def generate_ics(self, events: List[Dict], filename: str = "icna_events.ics"):
        """Generate ICS calendar file from events"""
        calendar = Calendar()
        
        for event_data in events:
            event = Event()
            event.name = event_data['title']
            event.begin = event_data['start']
            event.end = event_data['end']
            event.location = event_data['location']
            
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
    
    # Scrape all events
    events = scraper.scrape_all_events(max_pages=5)
    
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
