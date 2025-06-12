import os
import json
import mimetypes
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# --- Initialization ---
app = Flask(__name__)

try:
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    raise ValueError(
        "GEMINI_API_KEY not found in Replit Secrets. Please set it.")

# --- The AI's "Brain": Prompt Engineering ---
PROMPT_TEMPLATE = """
You are "El Moufatteche," a world-class digital forensics expert. Your primary goal is **objective accuracy**. Your reputation depends on correctly identifying forgeries AND correctly verifying legitimate documents. Do not be overly suspicious; a false alarm is a critical failure.

**TASK:**
Perform a neutral forensic analysis on the provided document/image based on the user's specified document type. Objectively assess both its positive (authentic) and negative (suspicious) features.

**CRITICAL RULES:**
1.  **Output Format:** Your response MUST be a single, valid JSON object and nothing else.
2.  **Status:** The 'status' must accurately reflect your findings: "VERIFIED LEGITIMATE", "HIGHLY SUSPICIOUS", "FORGERY DETECTED", or "INCONCLUSIVE".
3.  **Document Reference:** Generate a plausible but FAKE reference number (e.g., ID-TN-12345678, CHQ-2025-0608).
4.  **Checks and Scores:** Provide a `title`, `reason`, and `score` from 0-100. For legitimate documents, the reasons should praise authentic features.
5.  **Tailored Analysis:** Base your checks on the specific 'Document Type' provided below.

---
**USER-PROVIDED CONTEXT:**
*   Document Type: {doc_type}

---
**ANALYSIS CHECKLISTS (Guide):**
*   **'National ID Card':** 'Image Quality', 'Font Consistency', 'Security Features' (holograms), 'National Emblem', 'Background Image', 'ID Number Plausibility'.
*   **'Financial Document' (Cheque):** 'Paper Quality', 'Watermark Presence', 'Bank Authentication' (MICR), 'Signature Validity', 'Amount Consistency', 'Date Validity'.
*   **'Screenshot':** 'UI Element Consistency', 'Timestamp Plausibility', 'Profile Picture Quality', 'Message Tone', 'Pixel Inconsistencies'.
*   **'Legal Document':** 'Official Seal/Stamp', 'Font & Formatting Consistency', 'Signature Authenticity', 'Paper Aging/Wear'.

---
**EXAMPLE 1: A SUSPICIOUS DOCUMENT**
{{
  "status": "HIGHLY SUSPICIOUS",
  "documentReference": "ID-TN-FAKE-001",
  "summary": "The ID card shows multiple signs of digital manipulation and lacks key security features.",
  "checks": [
    {{ "title": "Image Quality", "reason": "The photograph's edges are unnaturally sharp, suggesting it was digitally pasted onto the document.", "score": 25 }},
    {{ "title": "Font Consistency", "reason": "The font used for the name does not match the standard font used on official Tunisian IDs.", "score": 30 }},
    {{ "title": "Security Features", "reason": "No visible holographic overlay or microprinting, which are standard on authentic cards.", "score": 10 }}
  ]
}}

**EXAMPLE 2: A LEGITIMATE DOCUMENT**
{{
  "status": "VERIFIED LEGITIMATE",
  "documentReference": "ID-TN-AUTH-987",
  "summary": "The document appears authentic, with all security features present and consistent formatting.",
  "checks": [
    {{ "title": "Security Features", "reason": "Holographic overlay is present and reacts correctly to light (based on image sheen). Microprinting is visible upon close inspection.", "score": 98 }},
    {{ "title": "Font Consistency", "reason": "All fonts are crisp, well-aligned, and consistent with official document standards.", "score": 100 }},
    {{ "title": "Image Quality", "reason": "The primary photograph is well-integrated with the background, showing no signs of digital alteration.", "score": 95 }}
  ]
}}
---
Now, perform your objective analysis on the provided file.
"""


# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Receives the uploaded file and returns the AI analysis."""
    if 'document' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['document']
    doc_type = request.form.get('doc_type', 'Unknown Document')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Read the file's bytes and determine its MIME type
            file_bytes = file.read()
            mime_type, _ = mimetypes.guess_type(file.filename)
            if mime_type is None:
                # Fallback for unknown types
                mime_type = 'application/octet-stream'

            # Prepare the prompt for Gemini
            prompt = PROMPT_TEMPLATE.format(doc_type=doc_type)

            # Create the content payload for Gemini
            model = genai.GenerativeModel(
                'gemini-1.5-flash-latest')  # Use a powerful vision model
            response = model.generate_content(
                [prompt, {
                    'mime_type': mime_type,
                    'data': file_bytes
                }])

            # Clean and parse the JSON response
            response_text = response.text.strip().replace("```json",
                                                          "").replace(
                                                              "```", "")
            analysis_json = json.loads(response_text)

            return jsonify(analysis_json)

        except json.JSONDecodeError:
            print(f"ERROR: Gemini returned malformed JSON: {response.text}")
            return jsonify({"error": "AI response was not valid JSON."}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify(
                {"error": f"An internal server error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
