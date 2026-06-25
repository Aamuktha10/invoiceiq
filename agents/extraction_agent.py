import os
import base64
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class ExtractionAgent:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        print(f"GROQ_API_KEY loaded: {bool(api_key)}")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    def _read_file_as_base64(self, filepath):
        with open(filepath, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        ext = filepath.rsplit(".", 1)[-1].lower()
        media_type_map = {
            "pdf": "application/pdf",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg"
        }
        return data, media_type_map.get(ext, "image/jpeg")

    def extract(self, filepath):
        b64_data, media_type = self._read_file_as_base64(filepath)

        prompt = """You are an invoice data extraction specialist.
Analyze this invoice image and extract fields.
Respond ONLY with a valid JSON object, nothing else, no markdown.

{
  "vendor": "Company name",
  "amount": 1234.56,
  "currency": "INR",
  "date": "YYYY-MM-DD",
  "invoice_number": "INV-001",
  "line_items": [{"description": "Item", "quantity": 1, "unit_price": 100.0, "total": 100.0}],
  "tax": 0.0,
  "payment_terms": "Net 30",
  "confidence": 0.95
}

If a field cannot be found, use null. Amount must be a number."""

        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{b64_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        raw = response.choices[0].message.content.strip()
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)