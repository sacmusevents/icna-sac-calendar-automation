# 🤖 Personal Automation Hub

Automated scrapers and integrations that run on GitHub Actions. Currently syncing ICNA Sacramento events to your calendar.

## 📅 ICNA Events Calendar

Automatically scrapes events from [icnasac.org](https://icnasac.org/up-coming-events/) and generates an ICS calendar feed you can subscribe to.

### ⚡ Quick Start - Subscribe to Calendar

**Option 1: Google Calendar (Recommended)**
1. Copy this URL:
   ```
   https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO-NAME/main/icna_events.ics
   ```
2. Open [Google Calendar](https://calendar.google.com)
3. Click the **+** next to "Other calendars" (left sidebar)
4. Select **"From URL"**
5. Paste the URL and click **"Add calendar"**

**Note**: Google Calendar refreshes subscribed calendars every 12-48 hours. Changes won't appear instantly.

**Option 2: Import Manually**
1. Download `icna_events.ics` from this repo
2. Import it into any calendar app (Google Calendar, Outlook, Apple Calendar, etc.)

### 🔄 How It Works

```
Every Monday at 9 AM Pacific
    ↓
GitHub Actions runs scraper
    ↓
Scrapes icnasac.org/up-coming-events
    ↓
Generates icna_events.ics file
    ↓
Commits to this repository
    ↓
Your calendar auto-updates (within 12-48 hours)
```

### 🛠️ Setup Instructions

#### 1. Fork This Repository

Click the "Fork" button at the top right of this page.

#### 2. Enable GitHub Actions

1. Go to your forked repo
2. Click **"Actions"** tab
3. Click **"I understand my workflows, go ahead and enable them"**

#### 3. Update the Calendar URL

Edit this README and replace `YOUR-USERNAME/YOUR-REPO-NAME` with your actual GitHub username and repo name.

#### 4. Test the Automation

1. Go to **"Actions"** tab
2. Click **"Sync ICNA Events to Calendar"** workflow
3. Click **"Run workflow"** button
4. Select **"main"** branch
5. Click **"Run workflow"**

Wait 1-2 minutes and check if `icna_events.ics` was created in your repo.

### 📊 Features

✅ **Automated Scraping**: Runs every Monday at 9 AM  
✅ **Smart Date Parsing**: Handles various date formats  
✅ **Timezone Aware**: Converts PDT/PST correctly  
✅ **Event Details**: Includes title, time, location, description, URL  
✅ **Error Handling**: Continues even if some events fail  
✅ **Execution Logs**: See what happened in each run  

### 🔧 Customization

#### Change Schedule

Edit `.github/workflows/sync-calendar.yml`:

```yaml
schedule:
  - cron: '0 17 * * 1'  # Every Monday 9 AM Pacific (5 PM UTC)
```

Common schedules:
- Every day at 6 AM Pacific: `'0 14 * * *'`
- Every Sunday at noon Pacific: `'0 20 * * 0'`
- Twice a week (Mon & Thu): `'0 17 * * 1,4'`

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

#### Change Event Source

Edit `scrape_icna_events.py` and update `base_url` in the `__init__` method.

### 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── sync-calendar.yml       # GitHub Actions workflow
├── scrape_icna_events.py           # Main scraper script
├── requirements.txt                # Python dependencies
├── icna_events.ics                 # Generated calendar (auto-updated)
└── README.md                       # This file
```

### 🔍 Logs and Debugging

#### View Execution Logs

1. Go to **"Actions"** tab
2. Click on the latest workflow run
3. Click on **"scrape-and-publish"** job
4. Expand each step to see detailed logs

#### Common Issues

**Problem**: No events showing up  
**Solution**: Check the Actions logs for errors. The website structure might have changed.

**Problem**: Calendar not updating in Google  
**Solution**: Google Calendar can take 12-48 hours to refresh. Be patient.

**Problem**: "Permission denied" error  
**Solution**: Make sure GitHub Actions is enabled in your repo settings.

### 📈 Adding More Automations

This repo is designed to be a hub for all your automation needs. Here's how to add more scrapers:

#### Example: Add a News Scraper

1. Create `scrape_news.py` in the root directory
2. Create `.github/workflows/sync-news.yml` 
3. Copy the pattern from `sync-calendar.yml`
4. Update the schedule and script name

All your automations will show up in the Actions tab!

### 🎯 Future Enhancements

Some ideas for extending this:

- [ ] Add email notifications with event summaries
- [ ] Filter events by category/keyword
- [ ] Export to multiple formats (JSON, CSV)
- [ ] Add event reminders
- [ ] Integrate with Notion/Airtable
- [ ] Create a web dashboard to view all automations

### 🤝 Contributing

This is a personal automation hub, but feel free to:
- Open issues for bugs
- Suggest improvements
- Share your own automation scripts

### 📝 License

MIT License - Feel free to use this for your own automation needs!

---

## 🚀 Other Automation Ideas

This same pattern works for:

- **Job Boards**: Scrape job listings
- **Real Estate**: Track new property listings
- **Deals/Sales**: Monitor price drops
- **News**: Aggregate articles from multiple sources
- **Social Media**: Backup your posts
- **RSS Feeds**: Convert to different formats
- **Weather**: Daily forecast summaries
- **Sports**: Game schedules and scores

The sky's the limit! 🌟

---

**Last Updated**: Auto-generated by GitHub Actions  
**Next Run**: Check the Actions tab
