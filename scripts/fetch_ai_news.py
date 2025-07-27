#!/usr/bin/env python3
"""
AI News Fetcher - What actually happened in AI today
Using OpenAI Responses API with real web search for accurate, cited results.
"""

import os
import json
import time
from datetime import datetime, timedelta
import argparse
import yaml
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AINewsFetcher:
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY required - get one from platform.openai.com")
        self.client = OpenAI(api_key=self.openai_api_key)
    
    def fetch_news(self, date: str) -> dict:
        """Use OpenAI Responses API with web search to find real AI news."""
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        readable_date = date_obj.strftime('%B %d, %Y')
        day_name = date_obj.strftime('%A')
        
        try:
            print(f"🌐 OpenAI searching the web for AI news from {readable_date}...")
            
            # Get recent stories to avoid duplicates
            recent_stories = self._get_recent_stories(7)
            recent_stories_text = ""
            if recent_stories:
                recent_stories_text = "\n\nRECENTLY COVERED STORIES (avoid these):\n"
                for story in recent_stories[-10:]:  # Last 10 to keep it manageable
                    recent_stories_text += f"- {story['title']} ({story['source']})\n"
            
            # Define 4 focused categories
            categories = [
                {
                    "name": "Product Launches & Company News",
                    "search_focus": "AI product launches, company announcements, new AI tools and apps, startup news, major tech company updates",
                    "examples": "New AI and generative AI models, startup funding, new AI applications",
                    "freshness": "prioritize articles published TODAY or within the last 24 hours"
                },
                {
                    "name": "Research & Academic Developments", 
                    "search_focus": "AI new research papers, arXiv preprints, conference presentations (e.g. NeurIPS, CVPR), and breakthroughs in AI models, training methods, or evaluation",
                    "examples": "research breakthroughs, transformer model advancements, multimodal papers, new benchmarks, interpretability tools, peer-reviewed research",
                    "freshness": "include recent papers, conference announcements, and arXiv preprints from the past week"
                },
                {
                    "name": "Business & Industry Trends",
                    "search_focus": "Funding rounds, mergers, acquisitions, layoffs, regulatory filings, major hires or leadership changes in AI companies",
                    "examples": "Series A/B/C funding for AI startups, acquisitions by Big Tech, layoffs at AI firms, IPO rumors, executive moves",
                    "freshness": "focus on announcements from the last 24-48 hours"
                },
                {
                    "name": "Useful Tools & Apps",
                    "search_focus": "AI tools, apps, courses, tutorials, useful tech tools, useful apps, courses or resources to learn AI and coding",
                    "examples": "AI tools, apps, courses, tutorials, useful tech tools, useful apps",
                    "freshness": "include recent releases and updates from the past few days"
                }
            ]
            
            all_stories = []
            
            # Make 4 focused calls
            for i, category in enumerate(categories, 1):
                print(f"🔍 Category {i}/4: {category['name']}")
                
                try:
                    response = self.client.responses.create(
                        model="gpt-4o",
                        tools=[{"type": "web_search_preview"}],
                        input=f"""
Search the web for CURRENT AI and technology news from {readable_date} ({day_name}).
FOCUS: {category['name']}
Search specifically for: {category['search_focus']}
Examples: {category['examples']}

FRESHNESS REQUIREMENTS:
- {category['freshness']}
- Focus on fresh, relevant developments rather than strict time limits

CONTENT REQUIREMENTS:
- Find 1-2 high-quality stories in this specific category
- Focus on {category['search_focus']}
- CRITICAL: Ensure source diversity - avoid getting stories from the same publication
- Each story should come from a different publication when possible
- Focus on quality and accuracy over quantity
- AVOID DUPLICATES: Do not include stories similar to recently covered ones

{recent_stories_text}

Return a JSON response with 1-2 stories:

{{
    "stories": [
        {{
            "title": "Concise headline, catchy and engaging",
            "summary": "What happened, why it matters, impact on the industry, interesting, captivating, and engaging",
            "url": "Direct URL to the news article",
            "source": "Publication name",
            "publication_date": "Publication date",
            "category": "{category['name']}"
        }}
    ]
}}

IMPORTANT: 
- Include stories from diverse sources: TechCrunch, The Verge, Ars Technica, Bloomberg, Wired, VentureBeat, Engadget, MIT Technology Review, CNBC, WSJ, and other reputable sources in English
- NO wikipedia articles as sources
- Avoid getting stories from the same publication
- ONLY include real articles with actual URLs - never make up or hallucinate content
- If you can't find good stories in this category, return an empty stories array
- Make sure the stories are different from recently covered ones"""
                    )
                    
                    # Extract the response content
                    response_content = ""
                    for output_item in response.output:
                        if hasattr(output_item, 'content') and output_item.type == 'message':
                            for content_item in output_item.content:
                                if hasattr(content_item, 'text'):
                                    response_content += content_item.text
                    
                    if response_content:
                        try:
                            # Extract JSON
                            if '```json' in response_content:
                                json_start = response_content.find('```json') + 7
                                json_end = response_content.find('```', json_start)
                                json_content = response_content[json_start:json_end].strip()
                            elif '{' in response_content and '}' in response_content:
                                json_start = response_content.find('{')
                                json_end = response_content.rfind('}') + 1
                                json_content = response_content[json_start:json_end]
                            else:
                                print(f"   ⚠️  No JSON found in response for category {i}")
                                continue
                            
                            category_data = json.loads(json_content)
                            if 'stories' in category_data:
                                stories_count = len(category_data['stories'])
                                all_stories.extend(category_data['stories'])
                                print(f"   ✅ Found {stories_count} stories")
                                if stories_count == 0:
                                    print(f"   ℹ️  Category {category['name']} returned empty stories array")
                            else:
                                print(f"   ⚠️  No 'stories' key found in response for category {i}")
                                
                        except json.JSONDecodeError as e:
                            print(f"   ❌ JSON parsing error in category {i}: {e}")
                            print(f"   Response preview: {response_content[:200]}...")
                            continue
                    else:
                        print(f"   ❌ No response content for category {i}")
                        
                except Exception as e:
                    print(f"   ❌ API error for category {i}: {e}")
                    continue
                
                # Small delay between calls
                time.sleep(1)
            
            if len(all_stories) == 0:
                print("❌ No stories found across all categories")
                return self._fallback_response(date)
            
            # Generate engaging summary from the stories
            summary = self._generate_summary(all_stories, readable_date)
            
            # Save stories to tracking file
            self._save_story_tracking(all_stories, date)
            
            print(f"✅ Total: {len(all_stories)} stories from {len(set(story.get('source', '') for story in all_stories))} different sources")
            
            return {
                "summary": summary,
                "stories": all_stories
            }
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._fallback_response(date)
    
    def _generate_summary(self, stories: list, date: str) -> str:
        """Generate an engaging summary from the fetched stories."""
        try:
            print("📝 Generating engaging summary...")
            
            # Prepare stories for summary generation
            stories_text = ""
            for i, story in enumerate(stories, 1):
                stories_text += f"{i}. {story.get('title', '')} ({story.get('source', '')})\n"
                stories_text += f"   {story.get('summary', '')}\n\n"
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You're writing a daily AI news digest. Keep it:
                        - Chill and natural, not overly enthusiastic or corporate
                        - Interesting and informative without being cringy
                        - Focus on what's actually cool or important
                        - Connect dots between stories when it makes sense
                        - Keep it to 2-3 sentences
                        - Sound like a knowledgeable friend sharing interesting tech news"""
                    },
                    {
                        "role": "user",
                        "content": f"""Based on these AI and tech stories from {date}, write a chill 2-3 sentence summary:

{stories_text}

Write something interesting and natural, not overly hyped."""
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            print(f"   ✅ Summary generated: {summary}")
            return summary
            
        except Exception as e:
            print(f"   ❌ Summary generation failed: {e}")
            # Fallback to simple summary
            return f"Today's AI news covers {len(stories)} key developments across different areas."
    
    def _get_recent_stories(self, days_back: int = 7) -> list:
        """Get stories from the last N days to avoid duplicates."""
        recent_stories = []
        try:
            # Check if tracking file exists
            if os.path.exists("_ai_news/story_tracking.json"):
                with open("_ai_news/story_tracking.json", 'r', encoding='utf-8') as f:
                    tracking_data = json.load(f)
                
                cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
                
                for entry in tracking_data:
                    if entry.get('date', '') >= cutoff_date:
                        recent_stories.append({
                            'title': entry.get('title', ''),
                            'source': entry.get('source', '')
                        })
                
                print(f"📋 Found {len(recent_stories)} recent stories to avoid duplicates")
                
        except Exception as e:
            print(f"⚠️  Could not load recent stories: {e}")
        
        return recent_stories
    
    def _save_story_tracking(self, stories: list, date: str):
        """Save stories to tracking file for future duplicate detection."""
        try:
            os.makedirs("_ai_news", exist_ok=True)
            
            # Load existing tracking data
            tracking_data = []
            if os.path.exists("_ai_news/story_tracking.json"):
                with open("_ai_news/story_tracking.json", 'r', encoding='utf-8') as f:
                    tracking_data = json.load(f)
            
            # Add new stories
            for story in stories:
                tracking_data.append({
                    'date': date,
                    'title': story.get('title', ''),
                    'source': story.get('source', '')
                })
            
            # Keep only last 30 days of data to manage file size
            cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            tracking_data = [entry for entry in tracking_data if entry.get('date', '') >= cutoff_date]
            
            # Save updated tracking data
            with open("_ai_news/story_tracking.json", 'w', encoding='utf-8') as f:
                json.dump(tracking_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved {len(stories)} stories to tracking file")
            
        except Exception as e:
            print(f"⚠️  Could not save story tracking: {e}")
    
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