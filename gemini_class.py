import base64

import vertexai
import vertexai.preview.generative_models as generative_models

from vertexai.generative_models import GenerativeModel, Part, FinishReason

from model import Model

class GeminiClass:
  """Prompt Google Cloud hosted Gemini family of models.

  Documentation: https://github.com/googleapis/python-aiplatform/tree/main/vertexai/generative_models
  """
  def __init__(self, model: Model):
    vertexai.init()

    self.model = GenerativeModel(model.model_version)

    self.generation_config = {
        "max_output_tokens": model.attributes['max_output_tokens'],
        "temperature": model.attributes['temperature'],
        "top_k": model.attributes['top_k'],
        "top_p": model.attributes['top_p'],
    }

    self.safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    }

  def generate(self, prompt: str) -> str:
    try:
      response = self.model.generate_content(
          prompt,
          generation_config=self.generation_config,
          safety_settings=self.safety_settings
          )
      return response.text
    except Exception as e:
      print(f"An unexpected error occurred: {e}")

    return None