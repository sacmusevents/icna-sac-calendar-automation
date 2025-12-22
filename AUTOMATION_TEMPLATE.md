# 📝 Template: Adding New Automations

Use this template to add more scrapers and automations to your hub.

## Example: News Scraper

### 1. Create the Scraper Script

Create `scrape_news.py`:

```python
#!/usr/bin/env python3
"""
News Scraper Example
Scrapes news articles from a website
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class NewsScraper:
    def __init__(self):
        self.base_url = "https://example-news-site.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_articles(self):
        """Scrape articles from the news site"""
        response = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # Update these selectors based on your target website
        for article in soup.find_all('article', class_='news-item'):
            title = article.find('h2').get_text(strip=True)
            link = article.find('a')['href']
            date = article.find('time')['datetime']
            
            articles.append({
                'title': title,
                'url': link,
                'date': date,
                'scraped_at': datetime.now().isoformat()
            })
        
        return articles
    
    def save_to_json(self, articles, filename='news.json'):
        """Save articles to JSON file"""
        with open(filename, 'w') as f:
            json.dump(articles, f, indent=2)
        
        print(f"✓ Saved {len(articles)} articles to {filename}")

def main():
    scraper = NewsScraper()
    articles = scraper.scrape_articles()
    scraper.save_to_json(articles)

if __name__ == "__main__":
    main()
```

### 2. Create the Workflow

Create `.github/workflows/scrape-news.yml`:

```yaml
name: Scrape News Daily

on:
  # Run every day at 6 AM Pacific (2 PM UTC)
  schedule:
    - cron: '0 14 * * *'
  
  # Allow manual trigger
  workflow_dispatch:

jobs:
  scrape-news:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install requests beautifulsoup4
    
    - name: Run news scraper
      run: |
        python scrape_news.py
    
    - name: Commit results
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git add news.json
        git diff --staged --quiet || git commit -m "Update news - $(date +'%Y-%m-%d')"
        git push
    
    - name: Generate summary
      run: |
        echo "## 📰 News Scraper Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Articles Found**: $(jq '. | length' news.json)" >> $GITHUB_STEP_SUMMARY
```

### 3. Update README

Add a section to your main README:

```markdown
## 📰 News Scraper

Scrapes daily news articles and saves them to `news.json`.

**Schedule**: Every day at 6 AM Pacific  
**Output**: `news.json`
```

### 4. Test It

1. Commit both files to your repository
2. Go to Actions tab
3. Find "Scrape News Daily" workflow
4. Click "Run workflow"

## Common Automation Patterns

### Pattern 1: Scrape → Store → Notify

Good for: Price tracking, job boards, real estate

```yaml
- name: Run scraper
  run: python scrape.py

- name: Check for changes
  run: |
    if [ "$(git diff data.json)" ]; then
      echo "NEW_ITEMS=true" >> $GITHUB_ENV
    fi

- name: Send notification
  if: env.NEW_ITEMS == 'true'
  run: |
    # Send email, Slack message, etc.
```

### Pattern 2: Scrape → Transform → Publish

Good for: Data aggregation, report generation

```yaml
- name: Scrape data
  run: python scrape.py

- name: Transform data
  run: python transform.py

- name: Generate report
  run: python generate_report.py

- name: Publish to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
```

### Pattern 3: Multi-Source Aggregation

Good for: Combining multiple sources

```yaml
- name: Scrape source 1
  run: python scrape_source1.py

- name: Scrape source 2
  run: python scrape_source2.py

- name: Merge results
  run: python merge_data.py

- name: Publish combined data
  run: python publish.py
```

## Useful GitHub Actions

### Send Email Notifications

```yaml
- name: Send email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: New items found!
    body: Check the repository for updates
    to: you@example.com
    from: GitHub Actions
```

### Upload to Google Drive

```yaml
- name: Upload to Google Drive
  uses: adityak74/google-drive-upload-git-action@main
  with:
    credentials: ${{ secrets.GOOGLE_DRIVE_CREDENTIALS }}
    filename: data.json
    folderId: YOUR_FOLDER_ID
```

### Post to Slack

```yaml
- name: Post to Slack
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: 'YOUR_CHANNEL_ID'
    slack-message: 'Scraper found new items!'
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

## Tips for Success

1. **Start Simple**: Get one scraper working before adding complexity
2. **Use Artifacts**: Store temporary files as artifacts for debugging
3. **Log Everything**: Add `echo` statements to see what's happening
4. **Handle Errors**: Add `|| true` to continue on errors
5. **Test Locally**: Run scripts on your computer first
6. **Version Control**: Commit working versions before changing
7. **Use Secrets**: Never hardcode passwords/API keys

## Debugging

### View Detailed Logs

```yaml
- name: Debug step
  run: |
    echo "Current directory: $(pwd)"
    echo "Files: $(ls -la)"
    echo "Environment: $(env)"
```

### Enable Debug Logging

Go to repository Settings → Secrets → New repository secret:
- Name: `ACTIONS_STEP_DEBUG`
- Value: `true`

### Download Artifacts

```yaml
- name: Upload debug info
  uses: actions/upload-artifact@v4
  with:
    name: debug-logs
    path: |
      *.log
      *.json
```

## Need Help?

- GitHub Actions docs: https://docs.github.com/en/actions
- Workflow syntax: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- Community actions: https://github.com/marketplace?type=actions

Happy automating! 🤖
