"""
Integration tests for ICNA Events Scraper date parsing

Test cases document the expected date formats:
1. Format A: Full date/time to full date/time (possibly different dates)
   Example: "March 15, 2025, 11:30 PM – Mar 16, 2025, 7:30 AM"

2. Format B: Full date/time to end_time only (same-day events)
   Example: "April 12, 2025, 9:00 PM – 9:05 PM"

3. Format C: Single date/time only (assumes 2-hour duration)
   Example: "April 12, 2025, 9:00 PM"
"""

import sys
import os
from datetime import datetime
import pytz

# Add parent directory to path to import scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrape_icna_events import ICNAEventsScraper

# Test cases: (date_string, expected_start, expected_end, format_type)
TEST_CASES = [
    # Format A: Full date/time to full date/time (different dates)
    (
        "March 15, 2025, 11:30 PM – Mar 16, 2025, 7:30 AM",
        datetime(2025, 3, 15, 23, 30),
        datetime(2025, 3, 16, 7, 30),
        "Format A: Overnight event (different dates)"
    ),

    # Format A: Full date/time to full date/time (same date, fully expressed)
    (
        "July 11, 2025, 10:00 AM PDT – Jul 27, 2025, 10:00 PM PDT",
        datetime(2025, 7, 11, 10, 0),
        datetime(2025, 7, 27, 22, 0),
        "Format A: Multi-day event"
    ),

    # Format B: Full date/time to end_time only
    (
        "April 12, 2025, 9:00 PM – 9:05 PM",
        datetime(2025, 4, 12, 21, 0),
        datetime(2025, 4, 12, 21, 5),
        "Format B: Same-day event (5 minute duration)"
    ),

    # Format B: With timezone
    (
        "October 31, 2025, 6:00 PM PDT – 9:00 PM PDT",
        datetime(2025, 10, 31, 18, 0),
        datetime(2025, 10, 31, 21, 0),
        "Format B: Same-day event with timezone"
    ),

    # Format C: Single date/time only (2-hour default)
    # NOTE: This format may not exist on the current website, but we should handle it
    # if it appears in the future
    (
        "December 25, 2025, 2:00 PM",
        datetime(2025, 12, 25, 14, 0),
        datetime(2025, 12, 25, 16, 0),  # 2 hours later
        "Format C: Single date/time with 2-hour default"
    ),
]


def test_date_parsing():
    """Test date parsing against known event formats"""
    scraper = ICNAEventsScraper()
    tz = pytz.timezone('America/Los_Angeles')

    passed = 0
    failed = 0

    for date_str, expected_start, expected_end, description in TEST_CASES:
        try:
            result = scraper.parse_date_string(date_str)

            if result is None:
                print(f"✗ FAILED: {description}")
                print(f"  Input: {date_str}")
                print(f"  Error: parse_date_string returned None")
                failed += 1
                continue

            # Convert to local time for comparison (parsing returns localized datetime)
            actual_start = result['start']
            actual_end = result['end']

            # Expected times localized
            expected_start_localized = tz.localize(expected_start)
            expected_end_localized = tz.localize(expected_end)

            # Check if times match
            if actual_start == expected_start_localized and actual_end == expected_end_localized:
                print(f"✓ PASSED: {description}")
                print(f"  Input: {date_str}")
                print(f"  Start: {actual_start.strftime('%Y-%m-%d %H:%M %Z')}")
                print(f"  End:   {actual_end.strftime('%Y-%m-%d %H:%M %Z')}")
                passed += 1
            else:
                print(f"✗ FAILED: {description}")
                print(f"  Input: {date_str}")
                print(f"  Expected: {expected_start_localized} → {expected_end_localized}")
                print(f"  Got:      {actual_start} → {actual_end}")
                failed += 1

        except Exception as e:
            print(f"✗ EXCEPTION: {description}")
            print(f"  Input: {date_str}")
            print(f"  Error: {e}")
            failed += 1

        print()

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print(f"{'='*60}")

    return failed == 0


if __name__ == "__main__":
    success = test_date_parsing()
    sys.exit(0 if success else 1)
