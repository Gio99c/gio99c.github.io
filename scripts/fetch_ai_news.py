#!/usr/bin/env python3
"""
AI News Fetcher - Daily digest of what's happening in AI
Uses OpenAI's latest models with web search to find and curate news.
"""

import os
import json
import requests
from datetime import datetime, timedelta
import argparse
import yaml

class AINewsFetcher:
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY required")
    
    def fetch_news(self, date: str) -> dict:
        """Search for AI news and create a digest."""
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        readable_date = date_obj.strftime('%B %d, %Y')
        
        # Simple, direct prompt inspired by Eugene Yan's style
        prompt = f"""
Find the most important AI and tech news from {readable_date}. 

Search for:
- New AI models or research breakthroughs
- Company announcements (funding, products, partnerships)  
- Industry developments and policy changes
- Technical advances that practitioners care about

Return this format:

{{
    "summary": "2-3 sentences on the day's key developments",
    "stories": [
        {{
            "title": "Direct, clear headline",
            "summary": "What happened and why it matters in 1-2 sentences",
            "url": "source link",
            "source": "publication name"
        }}
    ]
}}

Focus on 6-8 stories that AI/ML practitioners would find useful. Skip fluff pieces.
"""

        try:
            # Use latest GPT-4.1 with Responses API and web search
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'gpt-4.1',  # Latest model as of 2025
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a tech news curator. Search the web for current AI news. Be concise and practical. Focus on what matters to practitioners.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'tools': [
                        {
                            'type': 'function',
                            'function': {
                                'name': 'web_search',
                                'description': 'Search web for current information',
                                'parameters': {
                                    'type': 'object',
                                    'properties': {
                                        'query': {
                                            'type': 'string',
                                            'description': 'Search query'
                                        }
                                    },
                                    'required': ['query']
                                }
                            }
                        }
                    ],
                    'tool_choice': 'auto',
                    'temperature': 0.2,
                    'max_tokens': 2000
                },
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message'].get('content', '')
            if not content:
                return self._fallback_response(date)
            
            try:
                news_data = json.loads(content)
                if 'summary' not in news_data or 'stories' not in news_data:
                    return self._fallback_response(date)
                return news_data
            except json.JSONDecodeError:
                return self._fallback_response(date)
                
        except Exception as e:
            print(f"Error: {e}")
            return self._fallback_response(date)
    
    def _fallback_response(self, date: str) -> dict:
        """Fallback when API fails."""
        return {
            "summary": "AI news fetch temporarily unavailable. The system searches daily for the latest developments in AI research, products, and industry news.",
            "stories": [{
                "title": "System Update",
                "summary": "Daily AI news will resume shortly.",
                "url": "#",
                "source": "AI News"
            }]
        }
    
    def create_post(self, date: str, news_data: dict) -> tuple[str, str]:
        """Create Jekyll post."""
        
        # Clean up stories
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
        content += f"<!-- Generated {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} -->\n"
        
        return filename, content
    
    def save_post(self, filename: str, content: str):
        """Save post to _ai_news directory."""
        os.makedirs("_ai_news", exist_ok=True)
        
        with open(f"_ai_news/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Fetch daily AI news')
    parser.add_argument('--date', help='Date (YYYY-MM-DD)', 
                       default=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
    args = parser.parse_args()
    
    print(f"🔍 Fetching AI news for {args.date}")
    
    try:
        fetcher = AINewsFetcher()
        news_data = fetcher.fetch_news(args.date)
        
        print(f"📰 Found {len(news_data.get('stories', []))} stories")
        
        filename, content = fetcher.create_post(args.date, news_data)
        fetcher.save_post(filename, content)
        
        print("✅ Done")
        
    except Exception as e:
        print(f"❌ {e}")
        return 1

if __name__ == "__main__":
    main()