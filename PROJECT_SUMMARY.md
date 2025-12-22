# 📦 ICNA Calendar Automation - Project Summary

## What This Does

Automatically syncs events from icnasac.org to your Google Calendar using GitHub Actions.

```
┌─────────────────────────────────────────────────────────┐
│                  ICNASAC.ORG                            │
│           https://icnasac.org/up-coming-events/         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ Every Monday 9 AM
                        │ (or manual trigger)
                        ↓
┌─────────────────────────────────────────────────────────┐
│              GITHUB ACTIONS WORKFLOW                     │
│  1. Runs Python scraper                                 │
│  2. Extracts all events (title, date, location, etc)    │
│  3. Generates ICS calendar file                         │
│  4. Commits to repository                               │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ Updates icna_events.ics
                        ↓
┌─────────────────────────────────────────────────────────┐
│                 GITHUB REPOSITORY                        │
│  📄 icna_events.ics (auto-updated)                      │
│  Public URL: raw.githubusercontent.com/...              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ Subscribe via URL
                        │ (updates every 12-48 hours)
                        ↓
┌─────────────────────────────────────────────────────────┐
│               YOUR GOOGLE CALENDAR                       │
│  ✓ All ICNA events automatically appear                │
│  ✓ Includes dates, times, locations, descriptions      │
│  ✓ Updates automatically when new events are added     │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ Fully Automated
- Runs every Monday at 9 AM Pacific
- No manual intervention needed
- Set it and forget it

### ✅ Zero Cost
- GitHub Actions free tier (2,000 minutes/month)
- No servers, no hosting fees
- No credit card required

### ✅ Easy to Customize
- Change schedule with one line
- Add more scrapers easily
- Template included for new automations

### ✅ Smart Scraping
- Handles pagination (multiple pages)
- Parses various date formats
- Timezone aware (PDT/PST)
- Includes all event details

### ✅ Reliable
- Error handling built-in
- Logs everything
- Can manually trigger anytime
- Email notifications on failure

## Technical Details

### Technologies Used
- **Python 3.11**: Scraping and data processing
- **GitHub Actions**: Automation runtime
- **BeautifulSoup4**: HTML parsing
- **ics library**: ICS file generation
- **Git**: Version control and deployment

### Data Flow
1. **Scraper** fetches HTML from icnasac.org
2. **Parser** extracts event information
3. **Generator** creates ICS calendar format
4. **Git** commits the file to repository
5. **Google Calendar** syncs from raw GitHub URL

### Frequency
- **Default**: Weekly (Monday 9 AM Pacific)
- **Customizable**: Daily, hourly, or custom schedule
- **Manual**: Can trigger anytime from Actions tab

## File Structure

```
icna-calendar-automation/
│
├── 📄 scrape_icna_events.py
│   └── Main scraper logic (200+ lines)
│       ├── Scrapes all event pages
│       ├── Parses dates/times
│       ├── Handles timezones
│       └── Generates ICS file
│
├── ⚙️ .github/workflows/sync-calendar.yml
│   └── GitHub Actions workflow (60 lines)
│       ├── Scheduled trigger
│       ├── Manual trigger
│       ├── Python setup
│       ├── Dependency installation
│       └── Git commit/push
│
├── 📋 requirements.txt
│   └── Python dependencies
│
├── 📅 icna_events.ics
│   └── Sample output file
│
├── 📖 Documentation Files
│   ├── README.md              (Main overview)
│   ├── SETUP.md               (Step-by-step setup)
│   ├── QUICKSTART.md          (5-minute checklist)
│   ├── DEPLOYMENT.md          (How to deploy)
│   └── AUTOMATION_TEMPLATE.md (Add more scrapers)
│
└── ⚙️ .gitignore
    └── Python and temp files
```

## Setup Requirements

### Must Have
- ✅ GitHub account (free)
- ✅ Google Calendar account (free)
- ✅ 10 minutes of time

### Don't Need
- ❌ Server or hosting
- ❌ Credit card
- ❌ Programming experience
- ❌ Google Cloud project
- ❌ API keys or credentials

## Usage Scenarios

### Primary Use Case
Keep track of ICNA Sacramento events automatically without manual calendar updates.

### Additional Use Cases
Use the same pattern for:
- 📰 News aggregation
- 💼 Job board monitoring
- 🏠 Real estate listings
- 💰 Price tracking
- 📊 Data collection
- 🎫 Event monitoring from multiple sources

## Performance

### Resource Usage
- **Execution time**: ~30-60 seconds per run
- **GitHub Actions minutes**: <1 minute per run
- **Monthly usage**: ~4 minutes (weekly runs)
- **Storage**: <1 MB

### Scalability
- ✅ Can handle 100+ events easily
- ✅ Multiple pages of results
- ✅ Can run multiple scrapers in parallel
- ✅ Free tier supports ~2,000 runs per month

## Limitations

### Google Calendar Sync
- Updates take 12-48 hours to appear
- This is a Google limitation, not the scraper
- Workaround: Import manually for instant updates

### Website Changes
- If icnasac.org changes their HTML structure, scraper needs updating
- Logs will show errors when this happens
- Template provided for easy fixes

### GitHub Actions
- 2,000 free minutes per month
- Public repositories only for free tier
- Workflows timeout after 6 hours (way more than needed)

## Maintenance

### Required Maintenance
- ✅ None! It runs automatically

### Optional Maintenance
- Check Actions tab weekly to verify runs
- Update scraper if website structure changes
- Add more automations as needed

## Success Metrics

After deployment, you should see:
- ✅ Workflow runs automatically every Monday
- ✅ icna_events.ics file updates in repository
- ✅ Events appear in Google Calendar
- ✅ Green checkmarks in Actions tab

## Troubleshooting

### Common Issues
1. **No events showing**: Check Actions logs
2. **Workflow not running**: Enable Actions in repo settings
3. **Calendar not updating**: Wait 48 hours or re-subscribe

### Debug Steps
1. Check the Actions tab for errors
2. Review the workflow logs
3. Manually trigger the workflow
4. Verify the ICS file was generated

## Future Enhancements

### Possible Improvements
- [ ] Email digest of upcoming events
- [ ] Filter events by category
- [ ] Multi-source event aggregation
- [ ] Export to multiple formats (JSON, CSV)
- [ ] Web dashboard for all automations
- [ ] Slack/Discord notifications
- [ ] Integration with task managers

## Support & Resources

### Documentation
- README.md - Overview and features
- SETUP.md - Detailed setup guide
- QUICKSTART.md - 5-minute checklist
- DEPLOYMENT.md - How to deploy
- AUTOMATION_TEMPLATE.md - Add more scrapers

### External Resources
- GitHub Actions Docs: https://docs.github.com/en/actions
- Cron Schedule Helper: https://crontab.guru
- ICS Format Spec: https://icalendar.org

## Credits

Built using:
- Python ecosystem (requests, BeautifulSoup, ics)
- GitHub Actions (free automation)
- Open source libraries

## License

MIT License - Free to use, modify, and distribute

---

## Quick Commands

### Test Locally (if you have Python)
```bash
pip install -r requirements.txt
python scrape_icna_events.py
```

### Deploy to GitHub
1. Create new repository on GitHub
2. Upload all files
3. Enable GitHub Actions
4. Run workflow manually to test

### Get Calendar URL
```
https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/icna_events.ics
```

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Status**: Production Ready ✅
