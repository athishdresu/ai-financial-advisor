import os
import pandas as pd
import google.generativeai as genai
from flask import Flask, jsonify, render_template, request

my_api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=my_api_key)

model = genai.GenerativeModel('gemma-4-31b-it')

app = Flask(__name__)

def financial_summary(data):
    df = pd.DataFrame(data)
    df['amount'] = pd.to_numeric(df['amount'])
    
    category_total = df.groupby('category')['amount'].sum().reset_index()
    
    summary_text = "Here is the user's spending summary:\n"
    for index, row in category_total.iterrows():
        summary_text += f"- {row['category']}: ₹{row['amount']:.2f}\n"
    
    return summary_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_finances():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded!"})
        
    file = request.files['file']
    
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower()
        live_data = df.to_dict(orient='records')
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid CSV file format!"})
    
    if not live_data or len(live_data) == 0:
        return jsonify({"status": "error", "message": "No data provided in CSV!"})
        
    summary = financial_summary(live_data)
    
    system_prompt = f"Analyze this financial data:\n{summary}\n\nYou must provide exactly two sentences: a sweet compliment, and an easy saving tip. You can write out your internal thoughts first, but you MUST put your final two sentences at the very end after the exact word FINAL_ANSWER:"

    try:
        response = model.generate_content(
            system_prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.1)
        )
        
        clean_advice = response.text.split("FINAL_ANSWER:")[-1].replace("*", "").strip()
        
    except Exception as e:
        clean_advice = "The AI Brain encountered an error processing your data. Please check the server logs."
    
    return jsonify({
        "status": "success", 
        "data_summary": summary, 
        "ai_advice": clean_advice
    })

if __name__ == '__main__':
    app.run(debug=True)
