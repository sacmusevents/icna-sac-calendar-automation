"""
Integration test for Page 2 HTML parsing and date extraction

This test verifies that:
1. All 10 events are extracted from page 2 HTML
2. Date strings are correctly extracted from the HTML
3. Date parsing produces correct start and end times
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import pytz
from bs4 import BeautifulSoup
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrape_icna_events import ICNAEventsScraper

# Expected events on page 2 with their data
PAGE_2_EVENTS = [
    {
        "title": "Eid Milan 2024",
        "date_str": "April 24, 2024, 7:30 PM – 10:00 PM",
        "expected_start": datetime(2024, 4, 24, 19, 30),
        "expected_end": datetime(2024, 4, 24, 22, 0),
        "location": "ICNA Sacramento Office, 9700 Business Park Dr, Sacramento, CA 95827, USA",
    },
    {
        "title": "QiyamNight",
        "date_str": "April 5, 2024,  11:55 PM – Apr 06, 2024, 6:00 AM",
        "expected_start": datetime(2024, 4, 5, 23, 55),
        "expected_end": datetime(2024, 4, 6, 6, 0),
        "location": "ICNA Sacramento Office , 9700 Business Park Dr, Sacramento, CA 95827, USA",
    },
    {
        "title": "ICNA Sacramento Annual Fundraiser Dinner 2024",
        "date_str": "March 2, 2024, 6:00 PM – 9:00 PM",
        "expected_start": datetime(2024, 3, 2, 18, 0),
        "expected_end": datetime(2024, 3, 2, 21, 0),
        "location": "Folsom Community Center [ West Room ], 52 Natoma St, Folsom, CA 95630, USA",
    },
    {
        "title": "ICNA Tarbiyah Retreat 2023",
        "date_str": "September 9, 2023,  8:00 AM – 6:00 PM PDT",
        "expected_start": datetime(2023, 9, 9, 8, 0),
        "expected_end": datetime(2023, 9, 9, 18, 0),
        "location": "Livermore, 7000 Del Valle Rd, Livermore, CA 94550, USA",
    },
    {
        "title": "ICNA Dawah Booth at CA State Fair 2023 [ July 14 – July 30 ]",
        "date_str": "July 14, 2023, 11:00 AM PDT – Jul 30, 2023, 10:00 PM PDT",
        "expected_start": datetime(2023, 7, 14, 11, 0),
        "expected_end": datetime(2023, 7, 30, 22, 0),
        "location": "Sacramento, 1600 Exposition Blvd, Sacramento, CA 95815, USA",
    },
    {
        "title": "Every Weekend : Dawah Booth @ Arden Fair Mall",
        "date_str": "July 9, 2023, 12:00 PM – 6:00 PM",
        "expected_start": datetime(2023, 7, 9, 12, 0),
        "expected_end": datetime(2023, 7, 9, 18, 0),
        "location": "Arden Fair Mall, 1689 Arden Way, Sacramento, CA 95815, USA",
    },
    {
        "title": "Every Saturday : Dawah Booth @ Galleria Mall Roseville",
        "date_str": "July 8, 2023, 1:00 PM – 6:30 PM PDT",
        "expected_start": datetime(2023, 7, 8, 13, 0),
        "expected_end": datetime(2023, 7, 8, 18, 30),
        "location": "Galleria Mall , 1151 Galleria Blvd, Roseville, CA 95678, USA",
    },
    {
        "title": "ICNA Sacramento Eid Picnic 2023",
        "date_str": "May 7, 2023, 2:00 PM – 7:00 PM PDT",
        "expected_start": datetime(2023, 5, 7, 14, 0),
        "expected_end": datetime(2023, 5, 7, 19, 0),
        "location": "Kaseberg Park, 1151 Rand Way, Roseville, CA 95678, USA",
    },
    {
        "title": "ICNA Sacramento Annual Supporter’s Dinner",
        "date_str": "March 4, 2023, 5:30 PM – 9:00 PM PST",
        "expected_start": datetime(2023, 3, 4, 17, 30),
        "expected_end": datetime(2023, 3, 4, 21, 0),
        "location": "Sacramento, 4545 College Oak Dr, Sacramento, CA 95841, USA",
    },
    {
        "title": "Qiyam Program",
        "date_str": "February 25, 2023, 7:00 PM – 11:00 PM PST",
        "expected_start": datetime(2023, 2, 25, 19, 0),
        "expected_end": datetime(2023, 2, 25, 23, 0),
        "location": "ICNA Office , 9700 Business Park Dr, Sacramento, CA 95827, USA",
    },
]


def test_page_2_html_extraction_and_parsing():
    """Test extraction and parsing of all events from page 2 JSON response"""

    fixture_path = Path(__file__).parent / "fixtures" / "page_2.json"
    with open(fixture_path) as f:
        data = json.load(f)

    # Extract HTML from the JSON response (this is how the scraper processes it)
    html = data["html"]
    soup = BeautifulSoup(html, 'html.parser')
    scraper = ICNAEventsScraper()
    tz = pytz.timezone('America/Los_Angeles')

    # Extract all event elements
    event_elements = soup.find_all('div', class_='brxe-tnvmtb')
    print(f"\n{'='*70}")
    print(f"Testing Page 2: {len(event_elements)} events found")
    print(f"{'='*70}\n")

    if len(event_elements) != len(PAGE_2_EVENTS):
        print(f"✗ FAILED: Expected {len(PAGE_2_EVENTS)} events, found {len(event_elements)}")
        return False

    all_passed = True

    for i, (event_elem, expected) in enumerate(zip(event_elements, PAGE_2_EVENTS), 1):
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
    success = test_page_2_html_extraction_and_parsing()
    sys.exit(0 if success else 1)
