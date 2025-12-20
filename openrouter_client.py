import os
from openai import OpenAI

class OpenRouterClient:
  
  def summarize(self,query):
    
    completion = self.client.chat.completions.create(
  
    model="mistralai/mistral-nemo",
    messages=[
      { 'role': 'system', 
              'content': 'You are a helpful assistant that summarizes source code files.' 
            },
            {
              "role": "user",
              "content": f"'''{query}'''"
            }
          ],
      )

    return completion.choices[0].message.content

  
  def __init__(self) -> None:
      self.client = OpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key=os.getenv('OPENROUTER_API_KEY')
      )
