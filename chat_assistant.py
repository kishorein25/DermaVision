# ==============================================================================
# DermaVision: Stage 5 - Interactive Dermatology Chat Assistant
# Powered by Local Ollama (llama3.2:1b) with Medical Report Context
# ==============================================================================

import requests
import json
from typing import Dict, Any, List

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"

class DermaChatAssistant:
    def __init__(self, model_name: str = MODEL_NAME, api_url: str = OLLAMA_CHAT_URL):
        self.model_name = model_name
        self.api_url = api_url

    def answer_question(
        self,
        user_question: str,
        diagnosis_context: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Answers user follow-up questions regarding their diagnosis report.
        """
        c_name = diagnosis_context.get("condition_name", "Skin Condition")
        region = diagnosis_context.get("region", "Skin")
        category = diagnosis_context.get("category", "General")
        confidence = diagnosis_context.get("confidence", 95.0)

        system_instruction = (
            f"You are DermaVision AI, an empathetic, certified clinical dermatology assistant.\n"
            f"The patient has been evaluated for an image of their {region}.\n"
            f"Current Diagnosis: {c_name} (Category: {category}, Confidence: {confidence}%).\n"
            f"Guidelines:\n"
            f"1. Provide compassionate, clear, scientifically accurate answers.\n"
            f"2. Explain safe at-home skincare practices, hygiene, and when to seek urgent clinical care.\n"
            f"3. Always remind the patient to consult a licensed dermatologist before taking prescription medications.\n"
            f"4. Keep answers concise, practical, and easy to understand."
        )

        messages = [{"role": "system", "content": system_instruction}]

        if conversation_history:
            for turn in conversation_history[-6:]:
                messages.append(turn)

        messages.append({"role": "user", "content": user_question})

        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "max_tokens": 400
                }
            }
            res = requests.post(self.api_url, json=payload, timeout=10.0)
            if res.status_code == 200:
                data = res.json()
                return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            # Fallback response
            pass

        # Intelligent local fallback response
        return (
            f"Regarding your query on **{c_name}** ({region}):\n\n"
            f"• **Gentle Care:** Keep the area clean using lukewarm water and a fragrance-free mild cleanser. Avoid picking, scratching, or aggressive scrubbing.\n"
            f"• **Barrier Protection:** Apply a gentle barrier moisturizer and broad-spectrum sunscreen.\n"
            f"• **Medical Advice:** Because individual skin sensitivities vary, please consult a certified dermatologist before starting active medicinal treatments."
        )


if __name__ == "__main__":
    chat = DermaChatAssistant()
    sample_context = {
        "condition_name": "Acne Vulgaris",
        "region": "Face",
        "category": "disease",
        "confidence": 96.5
    }
    reply = chat.answer_question("Can I apply aloe vera on this?", sample_context)
    print("DermaChatAssistant Response:\n", reply)
