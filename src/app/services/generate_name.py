from fastapi import HTTPException
from google import genai
from typing import List

from src.app.config.config import settings


def generate_names(project_description: str) -> List[str]:
    prompt = f"""
        Generate 3 creative and catchy names for a project with the following description:

        {project_description}

        The names should be:

        1. Concise (1-3 words)
        2. Relevant to the project's purpose
        3. Memorable and easy to pronounce
        4. Evocative of innovation, simplicity, and power.

        Provide the 3 names in a JSON object like this:
        {{
            "name1": "...",
            "name2": "...",
            "name3": "..."
        }}
    """

    try:
        client = genai.Client(api_key=settings.GEMINI_API)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=prompt
        )
        if response:
            import json

            try:
                cleaned = (
                    response.text.strip().replace("```json", "").replace("```", "")
                )
                cleaned = json.loads(cleaned)
                return cleaned
            except Exception:
                raise HTTPException(
                    status_code=500, detail="Invalid JSON returned by Gemini"
                )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate names: Empty response from Gemini",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating names: {e}")
