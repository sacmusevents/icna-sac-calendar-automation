"""
Integration test for Page 1 HTML parsing and date extraction

This test verifies that:
1. All 10 events are extracted from page 1 HTML
2. Date strings are correctly extracted from the HTML
3. Date parsing produces correct start and end times
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import pytz
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrape_icna_events import ICNAEventsScraper

# Expected events on page 1 with their data
PAGE_1_EVENTS = [
    {
        "title": "Seerah Program",
        "date_str": "October 31, 2025, 6:00 PM – 9:00 PM PDT",
        "expected_start": datetime(2025, 10, 31, 18, 0),
        "expected_end": datetime(2025, 10, 31, 21, 0),
        "location": "Islamic Society of Placer County, 616 Church St, Roseville, CA 95678, USA",
    },
    {
        "title": "Dawah Training: Atheism and Youth",
        "date_str": "October 25, 2025, 10:00 AM – 3:00 PM PDT",
        "expected_start": datetime(2025, 10, 25, 10, 0),
        "expected_end": datetime(2025, 10, 25, 15, 0),
        "location": "Masjid Annur Islamic Center Sacramento, 6990 65th St, Sacramento, CA 95823, USA",
    },
    {
        "title": "ICNA Dawah Booth at CA State Fair 2025 [ July 11 – July 27 ]",
        "date_str": "July 11, 2025, 10:00 AM PDT – Jul 27, 2025, 10:00 PM PDT",
        "expected_start": datetime(2025, 7, 11, 10, 0),
        "expected_end": datetime(2025, 7, 27, 22, 0),
        "location": "California State Fair, 1600 Exposition Blvd, Sacramento, CA 95815, USA",
    },
    {
        "title": "Understand Salah and Quran the easy Way. [ Jun 27- 29]",
        "date_str": "June 27, 2025, 6:30 PM – Jun 29, 2025, 5:30 PM",
        "expected_start": datetime(2025, 6, 27, 18, 30),
        "expected_end": datetime(2025, 6, 29, 17, 30),
        "location": "MCF Folsom, 391 S Lexington Dr #120, Folsom, CA 95630, USA",
    },
    {
        "title": "ICNA Young Muslim Islamic Quiz 2025",
        "date_str": "April 12, 2025,  9:00 PM – 9:05 PM",  # Note extra space
        "expected_start": datetime(2025, 4, 12, 21, 0),
        "expected_end": datetime(2025, 4, 12, 21, 5),
        "location": "MCF Folsom, 391 S Lexington Dr #120, Folsom, CA 95630, USA",
    },
    {
        "title": "Ramadan Qiyam Night:",
        "date_str": "March 15, 2025,  11:30 PM – Mar 16, 2025, 7:30 AM",  # Note extra space
        "expected_start": datetime(2025, 3, 15, 23, 30),
        "expected_end": datetime(2025, 3, 16, 7, 30),
        "location": "ICNA Office: Sacramento, 9700 Business Park Dr, Suite 406, Sacramento, CA 95827, USA",
    },
    {
        "title": "ICNA Sacramento Supporter's Fundraiser Dinner 2025",
        "date_str": "February 16, 2025, 6:00 PM – 9:00 PM",
        "expected_start": datetime(2025, 2, 16, 18, 0),
        "expected_end": datetime(2025, 2, 16, 21, 0),
        "location": "Folsom Community Center [ East Room ], 52 Natoma St, Folsom, CA 95630, USA",
    },
    {
        "title": "Appreciation-Dinner2024",
        "date_str": "August 17, 2024, 7:30 PM – 9:30 PM",
        "expected_start": datetime(2024, 8, 17, 19, 30),
        "expected_end": datetime(2024, 8, 17, 21, 30),
        "location": "ICNA Office Sacramento, 9700 Business Park Dr, Suite 407, Sacramento, CA 95827, USA",
    },
    {
        "title": "Hujjaj Welcome Dinner 2024",
        "date_str": "July 20, 2024, 6:00 PM – 8:30 PM",
        "expected_start": datetime(2024, 7, 20, 18, 0),
        "expected_end": datetime(2024, 7, 20, 20, 30),
        "location": "Rancho Cordova, 11354 White Rock Rd, Rancho Cordova, CA 95742, USA",
    },
    {
        "title": "ICNA Dawah Booth at CA State Fair 2024 [ July 12 – July 28 ]",
        "date_str": "July 12, 2024, 11:00 AM PDT – Jul 28, 2024, 10:00 PM PDT",
        "expected_start": datetime(2024, 7, 12, 11, 0),
        "expected_end": datetime(2024, 7, 28, 22, 0),
        "location": "Sacramento, 1600 Exposition Blvd, Sacramento, CA 95815, USA",
    },
]


def test_page_1_html_extraction_and_parsing():
    """Test extraction and parsing of all events from page 1 HTML"""

    fixture_path = Path(__file__).parent / "fixtures" / "page_1.html"
    with open(fixture_path) as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    scraper = ICNAEventsScraper()
    tz = pytz.timezone('America/Los_Angeles')

    # Extract all event elements
    event_elements = soup.find_all('div', class_='brxe-tnvmtb')
    print(f"\n{'='*70}")
    print(f"Testing Page 1: {len(event_elements)} events found")
    print(f"{'='*70}\n")

    if len(event_elements) != len(PAGE_1_EVENTS):
        print(f"✗ FAILED: Expected {len(PAGE_1_EVENTS)} events, found {len(event_elements)}")
        return False

    all_passed = True

    for i, (event_elem, expected) in enumerate(zip(event_elements, PAGE_1_EVENTS), 1):
        # Extract title
        title_elem = event_elem.find('h3', class_='brxe-pgsofq')
        title = title_elem.get_text(strip=True) if title_elem else ""

        # Extract date string
        date_elem = event_elem.find('span', class_='brxe-bnvjah')
        date_text = ""
        if date_elem:
            text_span = date_elem.find('span', class_='text')
            date_text = text_span.get_text(strip=True) if text_span else ""

        # Extract location
        location_elem = event_elem.find('span', class_='brxe-oacqsb')
        location = ""
        if location_elem:
            text_span = location_elem.find('span', class_='text')
            location = text_span.get_text(strip=True) if text_span else ""

        # Verify title
        if title != expected["title"]:
            print(f"✗ Event {i} - Title mismatch")
            print(f"  Expected: {expected['title']}")
            print(f"  Got:      {title}")
            all_passed = False
            continue

        # Verify date string extraction
        if date_text != expected["date_str"]:
            print(f"✗ Event {i} ({title}) - Date string mismatch")
            print(f"  Expected: {expected['date_str']}")
            print(f"  Got:      {date_text}")
            all_passed = False
            continue

        # Parse date
        date_info = scraper.parse_date_string(date_text)
        if not date_info:
            print(f"✗ Event {i} ({title}) - Date parsing returned None")
            all_passed = False
            continue

        # Verify parsed times
        expected_start_tz = tz.localize(expected["expected_start"])
        expected_end_tz = tz.localize(expected["expected_end"])

        actual_start = date_info['start']
        actual_end = date_info['end']

        if actual_start != expected_start_tz or actual_end != expected_end_tz:
            print(f"✗ Event {i} ({title}) - Parsed times mismatch")
            print(f"  Date string: {date_text}")
            print(f"  Expected: {expected_start_tz.strftime('%Y-%m-%d %H:%M')} → {expected_end_tz.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Got:      {actual_start.strftime('%Y-%m-%d %H:%M')} → {actual_end.strftime('%Y-%m-%d %H:%M')}")
            all_passed = False
            continue

        # Verify location
        if location != expected["location"]:
            print(f"✗ Event {i} ({title}) - Location mismatch")
            print(f"  Expected: {expected['location']}")
            print(f"  Got:      {location}")
            all_passed = False
            continue

        print(f"✓ Event {i:2d}: {title}")
        print(f"           {date_text}")
        print(f"           → {actual_start.strftime('%Y-%m-%d %H:%M')} to {actual_end.strftime('%Y-%m-%d %H:%M')}")

    print(f"\n{'='*70}")
    if all_passed:
        print("✓ All tests PASSED!")
    else:
        print("✗ Some tests FAILED!")
    print(f"{'='*70}\n")

    return all_passed


if __name__ == "__main__":
    success = test_page_1_html_extraction_and_parsing()
    sys.exit(0 if success else 1)
