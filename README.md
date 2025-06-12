# El MatriX - Your AI Friend in the Fight Against Scams

**Tagline:** Sometimes, you have to be “nesnes” like Beji to discover the truth.

![El MatriX Feature](El-Matrix-Doc-Verification/static/moufatteche.png) 
<!-- Make sure this path is correct if you change the folder names -->

## Elevator Pitch

Cyber scams are an emerging threat in Tunisia, where victims lose their life savings and peace of mind, and conventional awareness campaigns are not effective at reaching the most at-risk populations. Our solution, El MatriX, is an experiential learning game that reinvents scam prevention from a boring lecture to an empowering experience. Rather than merely studying threats, users learn by doing through experiential learning: recognizing suspicious indicators in real-life, AI-generated scenarios in a secure, gamified setting. Using Google's Gemini, El MatriX generates culturally specific Tunisian scams that adapt according to emerging trends in the real world, thereby making the training continually applicable. The core loop is straightforward and compelling: play the game, get points, and spend the points to call upon "El Moufatteche," our real-world AI assistant, to help analyze suspicious messages or documents that you encounter. El MatriX is not just a game; it is an interactive training field that transforms potential victims into aware defenders, thereby forging a more secure digital Tunisia, one player at a time.

## Core Features

-   **Roblox Educational Game:** An interactive game where players face AI-generated scam scenarios and learn to identify red flags in a safe environment.
-   **Dynamic AI Scenarios:** A Python backend powered by Google Gemini generates an endless supply of realistic and culturally relevant scam messages in French, keeping the content fresh and up-to-date with emerging threats.
-   **"El Moufatteche" Document Verifier:** A standalone web application that uses Gemini's multimodal capabilities to analyze user-uploaded images (IDs, cheques, screenshots) and provide a detailed forensic report on their legitimacy.
-   **Mercy & Points System:** An intelligent points system that rewards correct answers and provides "mercy rounds" for players struggling, ensuring a positive and encouraging learning curve.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E77D3?style=for-the-badge&logo=google&logoColor=white)
![Roblox (Luau)](https://img.shields.io/badge/Roblox-000000?style=for-the-badge&logo=roblox&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Replit](https://img.shields.io/badge/Hosted_on-Replit-F26207?style=for-the-badge&logo=replit&logoColor=white)


## Project Structure

The repository is organized into two main components:

-   **/El-Matrix-Doc-Verification:** Contains the Python Flask server that communicates with the Roblox game. It receives requests for new scenarios and uses the Gemini API to generate dynamic scam/legitimate text messages.
-   **/El-Matrix-Backend:** Contains the standalone Flask web application for document verification. This includes the HTML, CSS, and JavaScript for the frontend, and the Python backend for handling file uploads and multimodal analysis with Gemini.

## Setup and Installation

To run these projects, you will need a Replit account and a Google Gemini API key.

1.  **Create a Replit Account:** Sign up at [Replit.com](https://replit.com).
2.  **Get a Gemini API Key:** Obtain your API key from [Google AI Studio](https://ai.google.dev/studio).
3.  **Clone the Repository (Optional):** You can clone this repository to your local machine or directly to Replit.
4.  **Set up Each Backend:**
    -   Create a new **Flask** Repl for each backend (`El-Matrix-Backend` and `El-Matrix-Doc-Verification`).
    -   Upload the respective files into each Repl.
    -   In the "Secrets" tab of each Repl, create a new secret with the key `GEMINI_API_KEY` and paste your API key as the value.
    -   Click "Run". The server will start, and a public URL will be provided.

## Key AI Concepts Implemented

Our approach focuses on **Prompt Engineering** and **In-Context Learning** to guide the Gemini model effectively without traditional fine-tuning.

-   **System Prompting:** We provide the AI with a detailed "persona" (e.g., "El Moufatteche, a world-class forensics expert") and a strict set of rules. This ensures consistent tone, output format (JSON), and behavior.
-   **In-Context Learning & Bias Correction:** For the document verifier, we initially faced a "suspicion bias." We corrected this by providing the AI with two examples directly in the prompt: one for a fake document and one for a legitimate one. This taught the AI to be more objective and recognize authentic features, significantly reducing false positives.

## Future Improvements

-   **Difficulty Scaling:** Fully integrate the difficulty selection to provide more complex scams for advanced players.
-   **Dialect Fine-Tuning:** Explore fine-tuning a model on a dataset of Tunisian "Derja" to provide hyper-realistic Arabic scam messages.
-   **Real-Time Browser Extension:** Develop an "El Moufatteche" browser extension that can analyze suspicious links and web pages in real-time.
-   **Expanded Scam Types:** Add new modules for email phishing, voice note scams (vishing), and QR code scams.
