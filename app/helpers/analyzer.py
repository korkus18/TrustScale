from app.models.post import Post
from app.models.result import Result, CategoryAnalysis, Commentary
from app.helpers.scraper import Scraper
import aiohttp
import asyncio
import os
import json
from typing import Optional, Dict, Any, List


class Analyzer:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }

    async def _call_openai_api(self, prompt: str) -> Optional[str]:
        """Asynchronously calls OpenAI API with the given prompt

        Args:
            prompt (str): The prompt to send to OpenAI API

        Returns:
            Optional[str]: The response from OpenAI API or None if there's an error
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.openai_api_url,
                    headers=self.headers,
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        print(f"Error calling OpenAI API: {response.status}")
                        return None
        except Exception as e:
            print(f"Exception while calling OpenAI API: {str(e)}")
            return None

    def _create_analysis_prompt(self, post: Post) -> str:
        """Creates a prompt for OpenAI API based on the Instagram post data

        Args:
            post (Post): The Instagram post data

        Returns:
            str: The formatted prompt for OpenAI API
        """
        prompt = f"""You are an expert in social media content evaluation.

Your task is to analyze an Instagram post consisting of an image and a caption.  
Evaluate the post in four categories:

1. **Engagement** – How engaging is the post for its audience?  
2. **Quality** – Is the post visually and linguistically well-made?  
3. **Relevance** – Is the post relevant to its niche or topic?  
4. **Audience Behavior** – How likely is the audience to interact with the post?

Post Information:
Author: {post.author.username} ({post.author.full_name})
Caption: {post.caption}
Hashtags: {', '.join(post.hashtags)}
Likes: {post.like_count}
Comments: {post.comment_count}
Location: {post.location.name if post.location else 'Not specified'}
Media Type: {'Video' if post.is_video else 'Image'}

For each category, provide:

- `"score"`: a number from 1 to 100 (realistic use of the full range)
- `"commentary"`: three fields:
  - `"positive"` – One short sentence describing what works well
  - `"neutral"` – One short sentence suggesting possible improvement
  - `"negative"` – One short sentence pointing out what doesn't work
- `"pros"`: 2–3 clear bullet points summarizing strengths
- `"cons"`: 2–3 clear bullet points summarizing weaknesses
- `"tips"`: 2–3 specific, practical suggestions for improving this category

Be direct, constructive, and avoid vague or generic advice.

Return only a valid JSON object in the following format:

{{
  "engagement": {{
    "score": 0,
    "commentary": {{
      "positive": "",
      "neutral": "",
      "negative": ""
    }},
    "pros": [],
    "cons": [],
    "tips": []
  }},
  "quality": {{
    "score": 0,
    "commentary": {{
      "positive": "",
      "neutral": "",
      "negative": ""
    }},
    "pros": [],
    "cons": [],
    "tips": []
  }},
  "relevance": {{
    "score": 0,
    "commentary": {{
      "positive": "",
      "neutral": "",
      "negative": ""
    }},
    "pros": [],
    "cons": [],
    "tips": []
  }},
  "audience_behavior": {{
    "score": 0,
    "commentary": {{
      "positive": "",
      "neutral": "",
      "negative": ""
    }},
    "pros": [],
    "cons": [],
    "tips": []
  }}
}}

Do not include any explanation or extra text."""
        return prompt

    def _parse_analysis_response(self, response: str) -> tuple[Dict[str, CategoryAnalysis], int, List[str], List[str], str]:
        """Parses the OpenAI API response into the required format

        Args:
            response (str): The raw response from OpenAI API

        Returns:
            tuple[Dict[str, CategoryAnalysis], int, List[str], List[str], str]: 
                Category analyses, average score, overall pros, overall cons, and detail
        """
        try:
            # Parse the JSON response
            analysis = json.loads(response)
            
            # Convert each category to CategoryAnalysis objects
            category_analyses = {}
            all_pros = []
            all_cons = []
            
            for category_name, category_data in analysis.items():
                commentary = Commentary(
                    positive=category_data["commentary"]["positive"],
                    neutral=category_data["commentary"]["neutral"],
                    negative=category_data["commentary"]["negative"]
                )
                
                category_analyses[category_name] = CategoryAnalysis(
                    score=category_data["score"],
                    commentary=commentary,
                    pros=category_data["pros"],
                    cons=category_data["cons"],
                    tips=category_data["tips"]
                )
                
                all_pros.extend(category_data["pros"])
                all_cons.extend(category_data["cons"])
            
            # Calculate average score
            average_score = sum(cat.score for cat in category_analyses.values()) // 4
            
            # Create detailed analysis
            detail = []
            for category_name, category_data in category_analyses.items():
                detail.append(f"{category_name.title()} Analysis:")
                detail.append(f"Score: {category_data.score}")
                detail.append("Commentary:")
                detail.append(f"Positive: {category_data.commentary.positive}")
                detail.append(f"Neutral: {category_data.commentary.neutral}")
                detail.append(f"Negative: {category_data.commentary.negative}")
                detail.append("Tips:")
                for tip in category_data.tips:
                    detail.append(f"- {tip}")
                detail.append("")
            
            return category_analyses, average_score, all_pros, all_cons, "\n".join(detail)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            raise ValueError("Failed to parse analysis response")
        except Exception as e:
            print(f"Error processing analysis response: {str(e)}")
            raise ValueError("Failed to process analysis response")

    async def run(self, post: Post) -> Result:
        """Asynchronously analyzes an Instagram post using OpenAI API

        Args:
            post (Post): The Instagram post to analyze

        Returns:
            Result: The analysis result with detailed category analysis
        """
        prompt = self._create_analysis_prompt(post)
        analysis = await self._call_openai_api(prompt)
        
        if not analysis:
            raise ValueError("Failed to get analysis from OpenAI API")

        try:
            category_analyses, average_score, overall_pros, overall_cons, detail = self._parse_analysis_response(analysis)
            
            return Result(
                engagement=category_analyses["engagement"],
                quality=category_analyses["quality"],
                relevance=category_analyses["relevance"],
                audience_behavior=category_analyses["audience_behavior"],
                average_score=average_score,
                overall_pros=overall_pros,
                overall_cons=overall_cons,
                detail=detail
            )
        except Exception as e:
            raise ValueError(f"Failed to create result: {str(e)}")
