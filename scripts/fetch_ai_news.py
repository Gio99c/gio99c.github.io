#!/usr/bin/env python3
"""
AI News Fetcher - What actually happened in AI today
Using OpenAI Responses API with real web search for accurate, cited results.
"""

import os
import json
import requests
from datetime import datetime
import argparse
import yaml
from urllib.parse import urlparse
import time
from openai import OpenAI

class AINewsFetcher:
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY required - get one from platform.openai.com")
        self.client = OpenAI(api_key=self.openai_api_key)
    
    def verify_url_accessible(self, url: str) -> bool:
        """Verify that a URL is accessible and returns a valid response."""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except:
            try:
                # Fallback to GET request if HEAD fails
                response = requests.get(url, timeout=10, allow_redirects=True)
                return response.status_code == 200
            except:
                return False
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL for source verification."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return ""
    
    def verify_source_matches_domain(self, claimed_source: str, url: str) -> bool:
        """Verify that the claimed source matches the URL domain."""
        domain = self.extract_domain(url)
        if not domain:
            return False
        
        claimed_lower = claimed_source.lower()
        
        # Common source-to-domain mappings
        source_mappings = {
            'techcrunch': 'techcrunch.com',
            'the verge': 'theverge.com',
            'verge': 'theverge.com',
            'reuters': 'reuters.com',
            'bloomberg': 'bloomberg.com',
            'wired': 'wired.com',
            'ars technica': 'arstechnica.com',
            'venturebeat': 'venturebeat.com',
            'engadget': 'engadget.com',
            'openai': 'openai.com',
            'anthropic': 'anthropic.com',
            'google': 'blog.google',
            'microsoft': 'blogs.microsoft.com',
            'meta': 'ai.meta.com',
            'arxiv': 'arxiv.org',
            'nature': 'nature.com',
            'science': 'science.org',
            'mit technology review': 'technologyreview.com',
            'ai news': 'artificialintelligence-news.com'
        }
        
        # Check if claimed source matches domain
        expected_domain = source_mappings.get(claimed_lower)
        if expected_domain:
            return expected_domain in domain
        
        # Fallback: check if source name appears in domain
        source_words = claimed_lower.replace(' ', '').replace('-', '')
        return source_words in domain.replace('.', '').replace('-', '')
    
    def fetch_news(self, date: str) -> dict:
        """Use OpenAI Responses API with web search to find real AI news."""
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        readable_date = date_obj.strftime('%B %d, %Y')
        day_name = date_obj.strftime('%A')
        
        try:
            print(f"🌐 OpenAI searching the web for AI news from {readable_date}...")
            
            # Use OpenAI Responses API with web search tool
            response = self.client.responses.create(
                model="gpt-4o",
                tools=[
                    {
                        "type": "web_search_preview"
                    }
                ],
                input=f"""Search the web for CURRENT AI and technology news from {readable_date} ({day_name}).

CRITICAL REQUIREMENTS:
- Search ONLY legitimate news websites: TechCrunch, The Verge, Ars Technica, Reuters, Bloomberg, Wired, VentureBeat, Engadget, MIT Technology Review, etc.
- Find articles published TODAY ({readable_date}) or within the last 24-48 hours
- EXCLUDE Wikipedia, LinkedIn posts, personal blogs, arXiv papers
- Focus on BREAKING NEWS and recent announcements

Search specifically for:
- Company product launches and announcements  
- Funding rounds and acquisitions announced today
- AI model releases and updates
- Industry partnerships announced recently
- Policy/regulatory news from government sources
- Earnings reports and business developments

Return a JSON response in TLDR newsletter style:

{{
    "summary": "Today's key AI/tech developments in 1-2 sentences - what practitioners need to know",
    "stories": [
        {{
            "title": "Concise headline focused on the key development",
            "summary": "TLDR-style: What happened, why it matters, impact on the industry. Keep it practical and skip the fluff.",
            "url": "Direct URL to the actual news article from a legitimate publication",
            "source": "Publication name (TechCrunch, Reuters, etc.)",
            "publication_date": "Actual publication date from the article"
        }}
    ]
}}

QUALITY FILTERS:
- Only include URLs from established tech/business news sites
- Skip Wikipedia, LinkedIn, personal blogs, academic papers
- Prioritize breaking news from {readable_date}
- If no news from today, search for "AI news last 24 hours" or "AI news this week"
- Write summaries like TLDR newsletter: direct, practical, no marketing speak

Search now for current AI/tech news from legitimate sources."""
            )
            
            # DEBUG: Log the full OpenAI API response
            print("🔍 DEBUG: Full OpenAI API response:")
            print(response)
            print("=" * 80)
            
            print("🔍 Processing OpenAI response with web search citations...")
            
            # Extract the response content from Responses API format
            # Look for the message content in the output
            response_content = ""
            for output_item in response.output:
                if hasattr(output_item, 'content') and output_item.type == 'message':
                    for content_item in output_item.content:
                        if hasattr(content_item, 'text'):
                            response_content += content_item.text
            
            # DEBUG: Log the extracted content
            print("🔍 DEBUG: Extracted content from OpenAI:")
            print(f"Content: {response_content}")
            print("=" * 80)
            
            if not response_content:
                print("❌ No content returned from OpenAI")
                return self._fallback_response(date)
            
            print("🔍 Processing and validating results...")
            
            # Extract JSON from OpenAI response
            try:
                if '```json' in response_content:
                    json_start = response_content.find('```json') + 7
                    json_end = response_content.find('```', json_start)
                    json_content = response_content[json_start:json_end].strip()
                elif '{' in response_content and '}' in response_content:
                    json_start = response_content.find('{')
                    json_end = response_content.rfind('}') + 1
                    json_content = response_content[json_start:json_end]
                else:
                    print("❌ No JSON found in OpenAI response")
                    return self._fallback_response(date)
                
                news_data = json.loads(json_content)
                
                if 'summary' not in news_data or 'stories' not in news_data:
                    print("❌ Invalid JSON structure from OpenAI")
                    return self._fallback_response(date)
                
                # Practical validation - focus on basic quality checks
                validated_stories = []
                for i, story in enumerate(news_data.get('stories', []), 1):
                    print(f"📋 Checking story {i}: {story.get('title', 'Untitled')[:60]}...")
                    
                    url = story.get('url', '')
                    source = story.get('source', '')
                    title = story.get('title', '')
                    summary = story.get('summary', '')
                    
                    # Basic validation checks
                    issues = []
                    
                    # 1. Check URL format
                    if not url or url == '#' or 'http' not in url or len(url) < 15:
                        issues.append("Invalid URL")
                    
                    # 2. Filter out non-news sources
                    domain = self.extract_domain(url)
                    excluded_domains = [
                        'wikipedia.org', 'linkedin.com', 'arxiv.org', 'github.com',
                        'reddit.com', 'twitter.com', 'x.com', 'medium.com',
                        'substack.com', 'blogspot.com', 'wordpress.com'
                    ]
                    
                    if any(excluded in domain for excluded in excluded_domains):
                        issues.append(f"Excluded source domain: {domain}")
                    
                    # 3. Check for legitimate news sources
                    legitimate_domains = [
                        'techcrunch.com', 'theverge.com', 'arstechnica.com', 'reuters.com',
                        'bloomberg.com', 'wired.com', 'venturebeat.com', 'engadget.com',
                        'technologyreview.com', 'cnbc.com', 'wsj.com', 'ft.com',
                        'bbc.com', 'cnn.com', 'axios.com', 'theinformation.com',
                        'semafor.com', 'artificialintelligence-news.com'
                    ]
                    
                    if not any(legit in domain for legit in legitimate_domains):
                        print(f"   ⚠️  Non-standard news source: {domain}")
                        # Don't reject, just warn
                    
                    # 4. Check if we have basic content
                    if not title or len(title) < 10:
                        issues.append("Missing/short title")
                    
                    if not summary or len(summary) < 20:
                        issues.append("Missing/short summary")
                    
                    if not source:
                        issues.append("Missing source")
                    
                    # 5. Try to verify URL is accessible (but don't fail on this)
                    url_accessible = self.verify_url_accessible(url) if url and 'http' in url else False
                    
                    # 6. Check source-domain matching (but allow some flexibility)
                    source_matches = self.verify_source_matches_domain(source, url) if url and source else False
                    
                    # Decision logic - be more lenient
                    if len(issues) > 2:
                        print(f"   ❌ Too many issues: {', '.join(issues)}")
                        continue
                    
                    if not url_accessible:
                        print(f"   ⚠️  URL may not be accessible: {url}")
                        # Don't reject - just warn
                    
                    if not source_matches and source.lower() != 'unknown':
                        print(f"   ⚠️  Source '{source}' may not match domain: {self.extract_domain(url)}")
                        # Don't reject - just warn
                    
                    # Accept the story if it passes basic checks
                    print(f"   ✅ Story accepted")
                    validated_stories.append(story)
                    
                    # Small delay
                    time.sleep(0.2)
                
                if len(validated_stories) == 0:
                    print("❌ No stories passed basic validation")
                    return self._fallback_response(date)
                
                print(f"✅ {len(validated_stories)} stories validated and ready")
                
                news_data['stories'] = validated_stories
                return news_data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")
                print(f"Content preview: {response_content[:200]}...")
                return self._fallback_response(date)
                
        except Exception as e:
            if "openai" in str(type(e)).lower():
                print(f"❌ OpenAI API error: {e}")
            else:
                print(f"❌ Unexpected error: {e}")
            return self._fallback_response(date)
    
    def _fallback_response(self, date: str) -> dict:
        """Fallback when OpenAI web search fails."""
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        readable_date = date_obj.strftime('%B %d, %Y')
        
        return {
            "summary": f"Unable to fetch AI news for {readable_date}. The search system encountered technical difficulties. Please check back later for daily AI and tech news updates.",
            "stories": [{
                "title": "News Search Temporarily Unavailable",
                "summary": "The automated news search system is experiencing technical issues. Daily AI news updates will resume shortly.",
                "url": "https://platform.openai.com/",
                "source": "System Status"
            }]
        }
    
    def create_post(self, date: str, news_data: dict) -> tuple[str, str]:
        """Create Jekyll post with the news."""
        
        stories = []
        for story in news_data.get('stories', []):
            stories.append({
                'title': story.get('title', 'Untitled'),
                'summary': story.get('summary', ''),
                'url': story.get('url', '#'),
                'source': story.get('source', 'Unknown')
            })
        
        frontmatter = {
            'date': date,
            'summary': news_data.get('summary', 'Daily AI news digest'),
            'stories': stories
        }
        
        filename = f"{date}-ai-news-digest.md"
        
        content = "---\n"
        content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        content += "---\n\n"
        content += f"<!-- Generated with OpenAI web search {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} -->\n"
        
        return filename, content
    
    def save_post(self, filename: str, content: str):
        """Save post to _ai_news directory."""
        os.makedirs("_ai_news", exist_ok=True)
        
        with open(f"_ai_news/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Fetch AI news using OpenAI web search')
    parser.add_argument('--date', help='Date (YYYY-MM-DD)', 
                       default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    
    print(f"🔍 Fetching AI news for {args.date}")
    
    try:
        fetcher = AINewsFetcher()
        news_data = fetcher.fetch_news(args.date)
        
        story_count = len(news_data.get('stories', []))
        print(f"📰 Found {story_count} stories")
        
        filename, content = fetcher.create_post(args.date, news_data)
        fetcher.save_post(filename, content)
        
        print("✅ Done")
        
    except Exception as e:
        print(f"❌ {e}")
        return 1

if __name__ == "__main__":
    main()