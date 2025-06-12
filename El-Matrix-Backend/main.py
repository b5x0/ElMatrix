import os
import json
import random
from flask import Flask, request, jsonify
import google.generativeai as genai

# --- Initialization ---
app = Flask(__name__)

try:
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    raise ValueError("GEMINI_API_KEY not found in Replit Secrets. Please set it.")

# --- Prompt Engineering (UPDATED with final language & link rules) ---
PROMPT_TEMPLATE = """
You are a creative cybersecurity expert designing content for "Sahbi Game," an educational game in Tunisia.

**CRITICAL RULES:**
1.  **Output Format:** You MUST respond with a single, valid JSON object and nothing else. Do not use markdown like ```json.
2.  **Explanation Language:** The `explanationHint`, `explanationRight`, and `explanationWrong` fields MUST be written in **English**. They should be clear and educational.
3.  **Content Language:** The `content` field (the message itself) MUST be written in the following style: **{content_language_style}**.
4.  **Fake Links:** When a scam involves a link, create a realistic-looking but FAKE URL (e.g., `bit-ly/promo-bonus`, `tunisiana-support.info`, `poste-tn-livraison.com`). **Do not just write `[link]` or `[URL]`.**
5.  **Realism:** Scenarios should be culturally relevant to Tunisia (names, places, situations).

---
**INSTRUCTIONS FOR THIS SCENARIO:**
*   **Generate a {request_type_instruction}**
*   **Difficulty:** {difficulty}

---
**JSON OUTPUT STRUCTURE:**
{{
    "type": "SMS",
    "name": "Sender Name/Number",
    "content": "The full text of the message in the requested content language style.",
    "correctAnswer": "Deny" or "Trust",
    "explanationHint": "A helpful hint (in English).",
    "explanationRight": "Positive feedback for a correct answer (in English).",
    "explanationWrong": "An educational explanation for a wrong answer (in English)."
}}

---
Now, generate the new scenario.
"""

# --- API Endpoint (UPDATED) ---
@app.route('/generate-scenario', methods=['POST'])
def generate_scenario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request: No JSON body"}), 400

        difficulty = data.get('difficulty', 'Rookie')
        request_type = data.get('requestType', 'scam')

        # REVERTED: Removed "Derja" from the options. It will now only choose between French styles.
        content_styles = ("Formal French", "Informal French")
        selected_style = random.choice(content_styles)

        if request_type == 'legitimate':
            request_type_instruction = "LEGITIMATE, normal, and trustworthy message. The 'correctAnswer' MUST be 'Trust'."
        else: # scam
            request_type_instruction = "SCAM message. The 'correctAnswer' MUST be 'Deny'."

        prompt = PROMPT_TEMPLATE.format(
            content_language_style=selected_style,
            request_type_instruction=request_type_instruction,
            difficulty=difficulty
        )

        print(f"Generating a '{request_type}' scenario in '{selected_style}' for difficulty: {difficulty}...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        response_text = response.text.strip().replace("```json", "").replace("```", "")
        scenario_json = json.loads(response_text)

        print("Successfully generated and parsed scenario.")
        return jsonify(scenario_json)

    except json.JSONDecodeError:
        print(f"ERROR: Gemini returned malformed JSON: {response.text}")
        return jsonify({"error": "Failed to parse AI response. Retrying may work."}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# To run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)