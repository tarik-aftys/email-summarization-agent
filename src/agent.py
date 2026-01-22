import json
import os
import requests
from datetime import date

HF_API_KEY = os.getenv("HF_API_KEY") 
HF_API_URL = "https://api-inference.huggingface.co/models"
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-3B-Instruct") 
 
SYSTEM_PROMPT = """
You are an Email Summarization Agent.
 
Your job:
1. Summarize the email in 2–3 sentences
2. Extract key points
3. Extract action items (who should do what)
4. Identify deadlines
5. Classify urgency: Low, Medium, or High
 
Return ONLY valid JSON with this schema:
 
{
  "sender": "",
  "subject": "",
  "date": "",
  "summary": "",
  "key_points": [],
  "action_items": [],
  "deadlines": [],
  "urgency": ""
}
"""
 
def read_email(path="email.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def summarize_email(email_text):
    headers = {
        "Content-Type": "application/json"
    }
    
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"
    
    prompt = f"""<|im_start|>system{SYSTEM_PROMPT}<|im_end|>
                 <|im_start|>userEmail à résumer:{email_text},Répondez UNIQUEMENT avec un JSON valide selon le schéma demandé.<|im_end|>
                 <|im_start|>assistant"""
    
    data = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.2,
            "max_new_tokens": 500,
            "return_full_text": False
        }
    }
    
    api_url = f"{HF_API_URL}/{HF_MODEL}"
    
    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            response_text = result[0].get("generated_text", "")
        elif isinstance(result, dict):
            response_text = result.get("generated_text", "")
        else:
            response_text = str(result)
        
        if not response_text:
            raise ValueError("Hugging Face n'a pas retourné de réponse")
                
        if "<|im_end|>" in response_text:
            response_text = response_text.split("<|im_end|>")[0].strip()
        elif "<|eot_id|>" in response_text:
            response_text = response_text.split("<|eot_id|>")[-1].strip()
        
        try:
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "sender": "",
                "subject": "",
                "date": "",
                "summary": response_text[:200] if response_text else "Résumé non disponible",
                "key_points": [],
                "action_items": [],
                "deadlines": [],
                "urgency": "Medium"
            }
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erreur lors de l'appel à Hugging Face: {str(e)}") from e
 
def save_outputs(data, outputs_dir="outputs"):

    os.makedirs(outputs_dir, exist_ok=True)
    
    with open(os.path.join(outputs_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open(os.path.join(outputs_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"Email Summary ({date.today()})\n")
        f.write("SUMMARY:\n")
        f.write(data["summary"] + "\n\n")
 
        f.write("KEY POINTS:\n")
        for p in data["key_points"]:
            f.write(f"- {p}\n")
 
        f.write("\nACTION ITEMS:\n")
        for a in data["action_items"]:
            f.write(f"- {a}\n")
 
        f.write("\nDEADLINES:\n")
        for d in data["deadlines"]:
            f.write(f"- {d}\n")
 
        f.write(f"\nURGENCY: {data['urgency']}\n")
 
