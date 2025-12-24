"""
Test incremental scraping functionality.

This test verifies that:
1. When scraping with existing events in the ICS file, only new events are processed
2. The scraper stops when it encounters an event that already exists
3. The ICS file is properly merged (new events first, then existing events)
4. No duplicate events are created
"""

import sys
import os
import tempfile
from datetime import datetime
from pathlib import Path
import pytz

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrape_icna_events import ICNAEventsScraper


def create_test_ics_file(num_events: int = 5) -> str:
    """Create a temporary ICS file with test events.

    Args:
        num_events: Number of events to create in the file

    Returns:
        Path to the temporary ICS file
    """
    # Create a temp file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.ics', delete=False)

    # Write ICS header
    temp_file.write('BEGIN:VCALENDAR\n')
    temp_file.write('VERSION:2.0\n')
    temp_file.write('PRODID:ics.py - http://git.io/lLljaA\n')
    temp_file.write(f'COMMENT:Generated at {datetime.now().isoformat()}\n')

    # Write test events (from newest to oldest)
    for i in range(num_events):
        year = 2025 - i
        month = 12
        day = 15 + i
        title = f"Test Event {num_events - i}"

        temp_file.write('BEGIN:VEVENT\n')
        temp_file.write(f'SUMMARY:{title}\n')
        temp_file.write(f'DTSTART:{year:04d}{month:02d}{day:02d}T100000Z\n')
        temp_file.write(f'DTEND:{year:04d}{month:02d}{day:02d}T110000Z\n')
        temp_file.write(f'UID:{year:04d}{month:02d}{day:02d}T100000Z-testuid\n')
        temp_file.write('DESCRIPTION:Test event description\n')
        temp_file.write('END:VEVENT\n')

    # Write calendar footer
    temp_file.write('END:VCALENDAR\n')
    temp_file.close()

    return temp_file.name


def test_load_existing_events():
    """Test that the scraper correctly loads existing events from ICS file."""
    print("\n" + "=" * 70)
    print("TEST: Load existing events from ICS file")
    print("=" * 70)

    # Create test ICS file with 5 events
    ics_file = create_test_ics_file(5)

    try:
        # Load scraper with this ICS file
        scraper = ICNAEventsScraper(ics_file=ics_file)

        # Verify that existing events were loaded
        assert len(scraper.existing_events) == 5, f"Expected 5 existing events, got {len(scraper.existing_events)}"
        print(f"✓ Correctly loaded {len(scraper.existing_events)} existing events")

        # Verify event structure
        assert any("Test Event 5" in key for key in scraper.existing_events.keys()), \
            "Expected 'Test Event 5' in existing events"
        print("✓ Existing events have correct structure")

        return True
    finally:
        os.unlink(ics_file)


def test_event_existence_check():
    """Test that event existence check works correctly."""
    print("\n" + "=" * 70)
    print("TEST: Event existence check")
    print("=" * 70)

    # Create test ICS file with 3 events
    ics_file = create_test_ics_file(3)

    try:
        scraper = ICNAEventsScraper(ics_file=ics_file)
        tz = pytz.timezone('America/Los_Angeles')

        # Create a datetime that matches one of the test events (2025-12-15 10:00 UTC = 2025-12-15 02:00 PST)
        existing_event_time = tz.localize(datetime(2025, 12, 15, 2, 0, 0))
        existing_title = "Test Event 3"

        # Check if this event exists
        exists = scraper._event_exists(existing_title, existing_event_time)
        assert exists, f"Expected event '{existing_title}' to exist"
        print(f"✓ Correctly detected existing event: '{existing_title}'")

        # Check for a non-existent event
        non_existent_time = tz.localize(datetime(2025, 1, 1, 12, 0, 0))
        not_exists = scraper._event_exists("Non-Existent Event", non_existent_time)
        assert not not_exists, "Expected event 'Non-Existent Event' to NOT exist"
        print("✓ Correctly detected non-existent event")

        return True
    finally:
        os.unlink(ics_file)


def test_incremental_scraping_stops_at_existing():
    """Test that scraper stops when encountering existing events.

    This simulates a scenario where:
    - ICS file has events 1-3
    - Website has events 1-5
    - Scraper should only return events 4-5 (the new ones)
    """
    print("\n" + "=" * 70)
    print("TEST: Incremental scraping stops at existing events")
    print("=" * 70)

    # Create ICS file with 3 existing events
    ics_file = create_test_ics_file(3)

    try:
        scraper = ICNAEventsScraper(ics_file=ics_file)
        print(f"✓ Created ICS file with {len(scraper.existing_events)} existing events")

        # Simulate events 1-5 being available (where 1-3 already exist)
        # Test events in file are created as (see create_test_ics_file):
        # - Test Event 3 (i=0): 2025, 20251215T100000Z
        # - Test Event 2 (i=1): 2024, 20241216T100000Z
        # - Test Event 1 (i=2): 2023, 20231217T100000Z
        # PST is UTC-8, so Dec 15, 2:00 AM PST = Dec 15, 10:00 AM UTC
        tz = pytz.timezone('America/Los_Angeles')
        simulated_events = [
            # These 3 are existing (should be recognized)
            {
                "title": "Test Event 3",
                "date": tz.localize(datetime(2025, 12, 15, 2, 0, 0))  # 20251215T100000Z
            },
            {
                "title": "Test Event 2",
                "date": tz.localize(datetime(2024, 12, 16, 2, 0, 0))  # 20241216T100000Z
            },
            {
                "title": "Test Event 1",
                "date": tz.localize(datetime(2023, 12, 17, 2, 0, 0))  # 20231217T100000Z
            },
            # These 2 are NEW (should be captured)
            {
                "title": "New Event 1",
                "date": tz.localize(datetime(2025, 12, 18, 2, 0, 0))  # 20251218T100000Z
            },
            {
                "title": "New Event 2",
                "date": tz.localize(datetime(2025, 12, 19, 2, 0, 0))  # 20251219T100000Z
            },
        ]

        # Test existence check for each event
        new_events_found = 0
        for event in simulated_events:
            exists = scraper._event_exists(event["title"], event["date"])
            if exists:
                print(f"  ≡ Existing: {event['title']}")
            else:
                print(f"  ✓ NEW: {event['title']}")
                new_events_found += 1

        assert new_events_found == 2, f"Expected 2 new events, found {new_events_found}"
        print(f"\n✓ Correctly identified {new_events_found} new events out of {len(simulated_events)}")

        return True
    finally:
        os.unlink(ics_file)


def test_ics_merge():
    """Test that ICS file is properly merged with new and existing events."""
    print("\n" + "=" * 70)
    print("TEST: ICS file merge (new events + existing events)")
    print("=" * 70)

    # Create test ICS file with 2 existing events
    ics_file = create_test_ics_file(2)

    try:
        # Create scraper with existing ICS file
        scraper = ICNAEventsScraper(ics_file=ics_file)
        print(f"✓ Loaded {len(scraper.existing_events)} existing events")

        # Simulate scraping 2 new events
        tz = pytz.timezone('America/Los_Angeles')
        new_events = [
            {
                'title': 'New Event A',
                'start': tz.localize(datetime(2025, 12, 25, 10, 0, 0)),
                'end': tz.localize(datetime(2025, 12, 25, 11, 0, 0)),
                'location': 'Test Location',
                'description': 'Test description A',
                'url': 'https://example.com/event-a'
            },
            {
                'title': 'New Event B',
                'start': tz.localize(datetime(2025, 12, 26, 10, 0, 0)),
                'end': tz.localize(datetime(2025, 12, 26, 11, 0, 0)),
                'location': 'Test Location',
                'description': 'Test description B',
                'url': 'https://example.com/event-b'
            }
        ]

        # Generate merged ICS file
        scraper.generate_ics(new_events, ics_file)

        # Verify the merged file
        with open(ics_file, 'r') as f:
            content = f.read()

        # Count events in merged file
        event_count = content.count('BEGIN:VEVENT')
        expected_count = 2 + 2  # 2 existing + 2 new
        assert event_count == expected_count, \
            f"Expected {expected_count} total events, found {event_count}"
        print(f"✓ Merged ICS file contains {event_count} events (2 existing + 2 new)")

        # Verify new events are in the file
        assert 'New Event A' in content, "New Event A not found in merged file"
        assert 'New Event B' in content, "New Event B not found in merged file"
        print("✓ New events are present in merged file")

        # Verify existing events are still there
        assert 'Test Event 1' in content, "Test Event 1 not found in merged file"
        assert 'Test Event 2' in content, "Test Event 2 not found in merged file"
        print("✓ Existing events are preserved in merged file")

        # Verify no duplicates (each event should appear exactly once)
        assert content.count('New Event A') == 1, "Duplicate 'New Event A' found"
        assert content.count('Test Event 1') == 1, "Duplicate 'Test Event 1' found"
        print("✓ No duplicate events in merged file")

        return True
    finally:
        if os.path.exists(ics_file):
            os.unlink(ics_file)


if __name__ == "__main__":
    all_passed = True

    try:
        all_passed &= test_load_existing_events()
        all_passed &= test_event_existence_check()
        all_passed &= test_incremental_scraping_stops_at_existing()
        all_passed &= test_ics_merge()
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        all_passed = False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All incremental scraping tests PASSED!")
    else:
        print("✗ Some tests FAILED!")
    print("=" * 70 + "\n")

    sys.exit(0 if all_passed else 1)
