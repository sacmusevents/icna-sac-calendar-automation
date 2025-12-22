# 🚀 Complete Setup Guide

Follow these steps to get your automation hub running in under 10 minutes.

## Prerequisites

- A GitHub account (free) - [Sign up here](https://github.com/join)
- That's it! No credit card, no server, no coding required.

## Step-by-Step Setup

### Step 1: Fork This Repository (2 minutes)

1. Make sure you're logged into GitHub
2. Click the **"Fork"** button at the top-right of this repository page
3. Click **"Create fork"**
4. Wait for GitHub to copy the repository to your account

### Step 2: Enable GitHub Actions (1 minute)

1. Go to your forked repository (it should be at `github.com/YOUR-USERNAME/REPO-NAME`)
2. Click the **"Actions"** tab at the top
3. You'll see a message about workflows
4. Click **"I understand my workflows, go ahead and enable them"**

### Step 3: Run Your First Scrape (2 minutes)

1. Stay in the **"Actions"** tab
2. On the left sidebar, click **"Sync ICNA Events to Calendar"**
3. Click the **"Run workflow"** dropdown button (on the right)
4. Make sure **"main"** branch is selected
5. Click the green **"Run workflow"** button
6. Refresh the page after 10 seconds

You'll see a workflow run appear with a yellow dot (running) that turns green (success) or red (failed).

### Step 4: Verify It Worked (1 minute)

1. Click on the workflow run (it will have a title like "Sync ICNA Events to Calendar")
2. Click on **"scrape-and-publish"** to see the logs
3. Look for messages like:
   ```
   Scraping page 1: https://icnasac.org/up-coming-events/
   Found 10 events on page 1
   ✓ Generated calendar file: icna_events.ics
   ```
4. Go back to your repository main page
5. You should see a new file: **icna_events.ics**

🎉 If you see the file, the scraper worked!

### Step 5: Subscribe in Google Calendar (3 minutes)

1. Go back to your repository main page
2. Click on **icna_events.ics**
3. Click the **"Raw"** button (top right of the file viewer)
4. Copy the URL from your browser's address bar (should look like):
   ```
   https://raw.githubusercontent.com/YOUR-USERNAME/REPO-NAME/main/icna_events.ics
   ```

5. Open [Google Calendar](https://calendar.google.com) in a new tab
6. On the left side, find **"Other calendars"**
7. Click the **+** button next to it
8. Select **"From URL"**
9. Paste the URL you copied
10. Click **"Add calendar"**

Wait 5-10 seconds and you should see **"ICNA Sacramento Events"** appear in your calendar list!

### Step 6: Check Your Events (1 minute)

1. In Google Calendar, make sure the new calendar is checked (visible)
2. You should see ICNA events appear on your calendar
3. Click on an event to see details (title, time, location, description)

**Note**: The events appear instantly the first time. Future updates take 12-48 hours to sync.

## 🎯 What Happens Next?

Your calendar will now **automatically update** every Monday at 9 AM Pacific time:

```
Monday 9 AM
  ↓
Scraper runs
  ↓  
Fetches latest events
  ↓
Updates icna_events.ics
  ↓
Google Calendar syncs (12-48 hours later)
```

## 🛠️ Customization

### Change the Schedule

Want it to run daily instead of weekly?

1. Go to your repository
2. Click `.github/workflows/sync-calendar.yml`
3. Click the pencil icon (Edit this file)
4. Find this line:
   ```yaml
   - cron: '0 17 * * 1'
   ```
5. Change it to (for daily at 6 AM Pacific):
   ```yaml
   - cron: '0 14 * * *'
   ```
6. Click **"Commit changes"**

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

### Run Manually Anytime

1. Go to **"Actions"** tab
2. Click **"Sync ICNA Events to Calendar"**
3. Click **"Run workflow"** → **"Run workflow"**

### Add Email Notifications

Want to be notified when the scraper runs?

1. Go to your repository **Settings**
2. Click **"Notifications"** (left sidebar)
3. Under **"Actions"**, enable **"Send notifications for failed workflows"**

You'll get an email if something breaks.

## 🔍 Troubleshooting

### "The file icna_events.ics doesn't exist"

**Solution**: The workflow hasn't run yet. Go to Actions tab and manually trigger it.

### "Workflow failed"

**Solution**: 
1. Click on the failed workflow run
2. Click on "scrape-and-publish"
3. Look for red error messages
4. Common issues:
   - Website changed structure → Need to update scraper code
   - Network timeout → Just re-run the workflow

### "Google Calendar says URL is invalid"

**Solution**: Make sure you're using the **Raw** URL that starts with `raw.githubusercontent.com`

### "Events aren't updating"

**Solution**: Google Calendar refreshes slowly (12-48 hours). You can:
1. Wait patiently
2. Unsubscribe and re-subscribe to force immediate refresh
3. Or download the ICS file and import manually for instant updates

## 📚 Next Steps

Now that you have your first automation running:

1. **Star this repository** so you can find it easily later
2. **Explore the code** in `scrape_icna_events.py` (even if you don't code)
3. **Add more automations** using the template in the main README
4. **Customize the schedule** to your needs
5. **Share with friends** who might find it useful

## 💡 Pro Tips

1. **GitHub Actions shows you everything**: Always check the Actions tab to see what's happening
2. **Manual triggers are your friend**: Use "Run workflow" to test changes immediately
3. **Logs are detailed**: Expand each step in the workflow to see exactly what happened
4. **Start simple**: Get one automation working before adding more

## 🆘 Need Help?

- **Check the logs**: 90% of issues show up in the workflow logs
- **Re-run the workflow**: Sometimes it just needs another try
- **Open an issue**: Use the Issues tab to ask for help

---

**Congratulations!** 🎊 You now have a fully automated calendar sync running on GitHub Actions.

Welcome to the world of automation! 🤖
