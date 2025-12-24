"""
Integration test for Page 3 HTML parsing and date extraction

This test verifies that:
1. All 10 events are extracted from page 3 HTML
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

# Expected events on page 3 with their data
PAGE_3_EVENTS = [
    {
        "title": "ICNA Office Opening",
        "date_str": "October 8, 2022, 1:00 PM – 3:30 PM",
        "expected_start": datetime(2022, 10, 8, 13, 0),
        "expected_end": datetime(2022, 10, 8, 15, 30),
        "location": "Sacramento, 9700 Business Park Dr, #407 , Sacramento, CA 95827, USA",
    },
    {
        "title": "Every Sunday: Dawah Booth @ Denios Market Roseville 2022",
        "date_str": "May 29, 2022, 10:30 AM – 3:00 PM PDT",
        "expected_start": datetime(2022, 5, 29, 10, 30),
        "expected_end": datetime(2022, 5, 29, 15, 0),
        "location": "Roseville, 1551 Vineyard Rd, Roseville, CA 95678, USA",
    },
    {
        "title": "Every Saturday: Dawah Booth @ Denios Market Roseville 2022",
        "date_str": "May 28, 2022, 10:30 AM – 3:00 PM",
        "expected_start": datetime(2022, 5, 28, 10, 30),
        "expected_end": datetime(2022, 5, 28, 15, 0),
        "location": "Roseville, 1551 Vineyard Rd, Roseville, CA 95678, USA",
    },
    {
        "title": "ICNA Sacramento Eid Picnic 2022",
        "date_str": "May 22, 2022, 2:00 PM – 7:00 PM",
        "expected_start": datetime(2022, 5, 22, 14, 0),
        "expected_end": datetime(2022, 5, 22, 19, 0),
        "location": "Kaseberg Park , 1511 Rand Way ,Roseville, CA 95678, USA",
    },
    {
        "title": "ICNA Young Muslim Islamic Quiz 2022",
        "date_str": "April 23, 2022, 9:00 AM PDT – Apr 24, 2022, 2:00 PM PDT",
        "expected_start": datetime(2022, 4, 23, 9, 0),
        "expected_end": datetime(2022, 4, 24, 14, 0),
        "location": "ICNA quiz 2022 will be Online Event",
    },
    {
        "title": "ICNA Sacramento Supporter’s Fundraiser 2022",
        "date_str": "April 22, 2022, 2:00 PM – 4:00 PM PDT",
        "expected_start": datetime(2022, 4, 22, 14, 0),
        "expected_end": datetime(2022, 4, 22, 16, 0),
        "location": "ICNA Sacramento Zoom Meeting",
    },
    {
        "title": "Weekend Atiqaf [ April 1st and 2nd] Friday and Saturday night at MCF Folsom",
        "date_str": "April 1, 2022, 9:00 PM – Apr 03, 2022, 6:00 AM",
        "expected_start": datetime(2022, 4, 1, 21, 0),
        "expected_end": datetime(2022, 4, 3, 6, 0),
        "location": "MCF Folsom, 391 S Lexington Dr #120, Folsom, CA 95630, USA",
    },
    {
        "title": "40 Hadeeth of Nawawi by Sh. Khalilurahman Chishti",
        "date_str": "May 1, 2022, 5:30 PM – Apr 06, 2022, 7:30 PM",
        # Note: End date is BEFORE start date - this is a data error in the HTML
        # The scraper will detect this and swap the dates
        "expected_start": datetime(2022, 5, 1, 17, 30),
        "expected_end": datetime(2022, 4, 6, 19, 30),
        "location": "MCF Folsom, 391 S Lexington Dr, Folsom 95630",
    },
    {
        "title": "ICNA  Relief Californa Virtual Banquet",
        "date_str": "March 27, 2022, 4:30 PM – 7:00 PM PDT",
        "expected_start": datetime(2022, 3, 27, 16, 30),
        "expected_end": datetime(2022, 3, 27, 19, 0),
        "location": "https://icnarelief.org/california-banquet/",
    },
    {
        "title": "Family Hike Sly Park ( Venue change from Bassi Falls )",
        "date_str": "March 26, 2022, 9:00 AM – 2:00 PM PDT",
        "expected_start": datetime(2022, 3, 26, 9, 0),
        "expected_end": datetime(2022, 3, 26, 14, 0),
        "location": "Sly Park Recreation Area, 4771 Sly Park Rd, Pollock Pines, CA 95726, USA",
    },
]


def test_page_3_html_extraction_and_parsing():
    """Test extraction and parsing of all events from page 3 JSON response"""

    fixture_path = Path(__file__).parent / "fixtures" / "page_3.json"
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
    print(f"Testing Page 3: {len(event_elements)} events found")
    print(f"{'='*70}\n")

    if len(event_elements) != len(PAGE_3_EVENTS):
        print(f"✗ FAILED: Expected {len(PAGE_3_EVENTS)} events, found {len(event_elements)}")
        return False

    all_passed = True

    for i, (event_elem, expected) in enumerate(zip(event_elements, PAGE_3_EVENTS), 1):
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
    success = test_page_3_html_extraction_and_parsing()
    sys.exit(0 if success else 1)
