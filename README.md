# AI Financial Advisor 💰

A full-stack, mildly gentle AI Financial Advisor built for the Gemma 4 Good Hackathon. 

This application takes user spending data, processes it through a Pandas backend, and uses advanced prompt engineering and output parsing with the `gemma-4-31b-it` model to provide empathetic, actionable financial advice.

## Tech Stack
* Frontend: HTML, CSS, JavaScript
* Backend: Python, Flask, Pandas
* AI Engine: Google Generative AI (Gemma 4)

## How to Run Locally

1. Clone this repository.
2. Install the required dependencies:
   `pip install -r requirements.txt`
3. Get a Google AI Studio API Key and paste it into line 5 of `app.py`.
4. Run the Flask server:
   `python app.py`
5. Open your browser and go to `http://127.0.0.1:5000`