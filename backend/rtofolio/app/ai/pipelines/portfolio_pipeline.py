import json
import os
from anthropic import Anthropic
from app.schemas.portfolio import PortfolioSchema
from app.env import CLAUDE_API_KEY

model = "claude-sonnet-4-5-20250929"

def load_portfolio_template():
    """Load the portfolio template JSON from samples directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '..', '..', 'samples', 'portfolio_v1.json')
    
    with open(template_path, 'r') as f:
        return json.load(f)

def generate_portfolio_pipeline(resume_markdown: str):
    """
    Generate a filled portfolio JSON from resume markdown.
    
    Args:
        resume_markdown: The resume content in markdown format
        
    Returns:
        dict: A filled portfolio JSON based on the template
    """
    try:
        # Load the portfolio template
        portfolio_template = load_portfolio_template()
        
        # Create the prompt for Claude
        prompt = f"""You are an expert portfolio generator. I will provide you with a resume in markdown format and a JSON template for a portfolio website.

Your task is to carefully analyze the resume and fill in ALL the empty fields in the JSON template with appropriate data extracted from the resume.

**Resume (Markdown):**
```markdown
{resume_markdown}
```

**Portfolio JSON Template:**
```json
{json.dumps(portfolio_template, indent=2)}
```

**Instructions:**
1. Fill in ALL empty string fields ("") in the JSON template with relevant data from the resume
2. For the theme section, choose appropriate style, color palette(light, dark, terminal), font(sans-serif, serif, monospace), and tone that would suit the person's profession
3. For the navbar section: extract the person's name, create relevant navigation links
4. For the hero section: create an engaging hero_text based on their professional summary, use their name, suggest a CTA
5. For skills section: extract ALL technical skills, tools, and technologies from the resume. Add icons from https://devicon.dev/
6. For experience section: extract work experience with role, company, dates, and create compelling descriptions. Do not add more than what is in the resume.
7. For projects section: extract projects from the resume with title, description, and any links mentioned. Add images from https://images.unsplash.com/. Do not add more than what is in the resume.
8. For footer section: use the person's name and create relevant social/contact links
9. If there are more items in the template than data in the resume, fill in what you can and leave the rest empty
10. If there is more data in the resume than template slots, prioritize the most important/recent items
11. Ensure all dates are properly formatted
12. Make descriptions concise but impactful
13. Return ONLY the filled JSON, no additional text or explanation
14. Return the JSON in the same format as the template, with no additional keys or fields

Return the complete filled JSON now:"""

        # Call Claude API
        client = Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            model=model,
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response text
        response_text = response.content[0].text
        
        # Parse the JSON from the response
        # Claude might wrap it in markdown code blocks, so we need to extract it
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.rfind("```")
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.rfind("```")
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text.strip()
        
        # Parse and return the JSON
        filled_portfolio = json.loads(json_str)
        return filled_portfolio
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response from Claude: {str(e)}")
    except Exception as e:
        raise e