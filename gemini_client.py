from google import genai


class GeminiClient:

    def summarize(self, query):
        # System instruction + prompt
        prompt = f"""You are a helpful assistant that summarizes source code files.

Code:
```
{query}
```

Provide a concise summary."""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        return response.text
    
    def __init__(self) -> None:
        self.client = genai.Client()



#GEMINI_API_KEY
