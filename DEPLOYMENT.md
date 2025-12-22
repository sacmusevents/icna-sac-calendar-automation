# 🚀 Deployment Instructions

## What You Have

A complete GitHub Actions automation system that:
- ✅ Scrapes ICNA Sacramento events automatically
- ✅ Generates an ICS calendar file
- ✅ Updates every Monday at 9 AM Pacific
- ✅ Can be subscribed to in Google Calendar
- ✅ Includes templates for adding more automations

## Files Included

```
icna-calendar-automation/
├── .github/
│   └── workflows/
│       └── sync-calendar.yml          # GitHub Actions workflow
├── scrape_icna_events.py              # Main scraper script
├── requirements.txt                   # Python dependencies
├── icna_events.ics                    # Sample output file
├── .gitignore                         # Git ignore rules
├── README.md                          # Main documentation
├── SETUP.md                           # Detailed setup guide
├── QUICKSTART.md                      # 5-minute checklist
└── AUTOMATION_TEMPLATE.md             # Template for adding more scrapers
```

## Deployment Steps

### Option 1: Upload to GitHub (Recommended)

1. **Create a new GitHub repository**:
   - Go to https://github.com/new
   - Name: `my-automation-hub` (or any name you like)
   - Choose: Public (required for free GitHub Pages)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

2. **Upload your files**:
   - Click "uploading an existing file"
   - Drag and drop the entire `icna-calendar-automation` folder contents
   - Commit message: "Initial commit - ICNA calendar automation"
   - Click "Commit changes"

3. **Enable GitHub Actions**:
   - Go to the Actions tab
   - Click "I understand my workflows, go ahead and enable them"

4. **Test it**:
   - Go to Actions tab
   - Click "Sync ICNA Events to Calendar"
   - Click "Run workflow" → "Run workflow"
   - Wait 1-2 minutes
   - Check if `icna_events.ics` appears in your repo

### Option 2: Use Git Command Line

If you're comfortable with git:

```bash
# Navigate to the icna-calendar-automation folder
cd icna-calendar-automation

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ICNA calendar automation"

# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## After Deployment

### Get Your Calendar URL

Once the workflow runs successfully:

1. Go to your repository
2. Click on `icna_events.ics`
3. Click the "Raw" button
4. Copy the URL (should be like):
   ```
   https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/icna_events.ics
   ```

### Subscribe in Google Calendar

1. Open Google Calendar
2. Click "+" next to "Other calendars"
3. Select "From URL"
4. Paste your calendar URL
5. Click "Add calendar"

Events will appear immediately! Updates sync every 12-48 hours.

## Customization

### Change the Schedule

Edit `.github/workflows/sync-calendar.yml`:

```yaml
schedule:
  - cron: '0 17 * * 1'  # Every Monday 9 AM Pacific
```

Common schedules:
- Daily: `'0 14 * * *'`  (6 AM Pacific)
- Twice a week: `'0 17 * * 1,4'`  (Mon & Thu)
- Monthly: `'0 17 1 * *'`  (1st of month)

Use https://crontab.guru to create custom schedules.

### Add More Automations

See `AUTOMATION_TEMPLATE.md` for examples of:
- News scrapers
- Price trackers
- Job board monitors
- And more!

## Monitoring

### View Workflow Runs

Go to Actions tab to see:
- When workflows ran
- Whether they succeeded or failed
- Detailed logs of each step

### Email Notifications

To get notified of failures:

1. Go to repository Settings
2. Notifications → Actions
3. Enable "Send notifications for failed workflows"

## Troubleshooting

### "Workflow not running automatically"

- Check Actions tab → make sure workflows are enabled
- Verify the cron schedule is correct
- Wait for the scheduled time (or trigger manually)

### "Permission denied when pushing"

The workflow needs write permissions:

1. Go to Settings → Actions → General
2. Under "Workflow permissions"
3. Select "Read and write permissions"
4. Save

### "Website changed and scraper broke"

This happens when websites update their HTML structure:

1. Check the workflow logs to see the error
2. Update `scrape_icna_events.py` to match the new structure
3. Test locally if possible
4. Commit the fix

## Pro Tips

1. **Manual triggers are great for testing** - use them often
2. **Check logs when something fails** - they show exactly what went wrong
3. **Start with one automation** - get it working before adding more
4. **Use GitHub Issues** - track bugs and improvements
5. **Keep it simple** - the best automation is one that just works

## Next Steps

- [ ] Deploy to GitHub
- [ ] Subscribe to calendar
- [ ] Watch the first automated run
- [ ] Explore adding more automations
- [ ] Share with friends who might find it useful

## Support

- **Documentation**: Read the markdown files
- **Examples**: Check `AUTOMATION_TEMPLATE.md`
- **Logs**: Always check the Actions tab first
- **GitHub Actions Docs**: https://docs.github.com/en/actions

---

**You're all set!** 🎉 

Your automation hub is ready to deploy. Once it's on GitHub, it will run automatically forever (as long as GitHub Actions is free, which it is for public repos).

Enjoy your automated calendar! 📅✨
