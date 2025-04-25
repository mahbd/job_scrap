import json
import os

from google import genai
from google.genai import types


def convert_using_gemini(web_content: str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "models/gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""Create a JSON for this model. Output in Json Format
class Job(models.Model):
title = models.CharField(max_length=200)
subtitle = models.CharField(max_length=200, blank=True, null=True)
description = models.TextField(blank=True, null=True)
requirements = models.TextField(blank=True, null=True)
company = models.CharField(max_length=200, blank=True, null=True)
location = models.CharField(max_length=200, blank=True, null=True)
salary = models.CharField(max_length=200, blank=True, null=True)
date_posted = models.DateTimeField(auto_now_add=True)
url = models.URLField(max_length=200, unique=True)
category = models.CharField(max_length=200, blank=True, null=True)
is_suitable = models.BooleanField(default=False)
job_type = models.CharField(
max_length=50,
choices=[
('FT', 'Full-time'),
('PT', 'Part-time'),
('CT', 'Contract'),
('FL', 'Freelance')
],
blank=True,
null=True
)
{web_content}
"""),
            ],
        ),

    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["title", "url"],
            properties={
                "title": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "subtitle": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "description": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "requirements": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "company": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "location": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "salary": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "date_posted": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "url": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "category": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "is_suitable": genai.types.Schema(
                    type=genai.types.Type.BOOLEAN,
                ),
                "job_type": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=["FT", "PT", "CT", "FL"],
                ),
            },
        ),
    )

    output_content = ""
    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        if chunk.text:
            output_content += chunk.text

    # Convert to JSON and return
    try:
        return json.loads(output_content)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None

