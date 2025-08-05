"""
🤖 روان‌شناس هوشمند تلگرام
استفاده از Groq AI + GitHub برای ذخیره‌سازی
"""

import json
import os
import requests
from datetime import datetime
import base64

# ⚙️ تنظیمات - این بخش‌ها را تغییر دهید
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
GITHUB_REPO = "psycho-bot-database"
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"  # اختیاری

class PsychBot:
    def __init__(self):
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.github_api = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents"
        
    def get_ai_response(self, user_message):
        """دریافت پاسخ هوشمندانه از Groq"""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [
                {
                    "role": "system", 
                    "content": "شما یک روان‌شناس حرفه‌ای هستید. با همدلی و علم پاسخ دهید."
                },
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 400,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.groq_url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return "متأسفم، الان مشکل فنی دارم. لطفاً بعداً تلاش کن."
        except:
            return "خطا در اتصال. دوباره امتحان کن."
    
    def save_conversation(self, user_id, user_message, ai_response):
        """ذخیره مکالمه در GitHub"""
        filename = f"conversations/{user_id}.json"
        
        # ساخت اطلاعات مکالمه
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response
        }
        
        try:
            # خواندن فایل قبلی (اگر وجود دارد)
            try:
                response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{filename}")
                if response.status_code == 200:
                    existing_conversations = response.json()
                else:
                    existing_conversations = []
            except:
                existing_conversations = []
            
            # اضافه کردن مکالمه جدید
            existing_conversations.append(conversation_data)
            
            # تبدیل به JSON و encode کردن برای GitHub
            json_content = json.dumps(existing_conversations, ensure_ascii=False, indent=2)
            encoded_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
            
            # آپلود به GitHub
            github_data = {
                "message": f"Update conversation for user {user_id}",
                "content": encoded_content
            }
            
            headers = {}
            if GITHUB_TOKEN:
                headers["Authorization"] = f"token {GITHUB_TOKEN}"
            
            requests.put(f"{self.github_api}/{filename}", headers=headers, json=github_data)
            
        except Exception as e:
            print(f"خطا در ذخیره: {e}")

# 🚀 اجرای ربات
if __name__ == "__main__":
    print("🤖 ربات روان‌شناس آماده است!")
    print("📝 لطفاً کلیدهای API را در فایل وارد کنید")
    
    # اینجا کد اصلی تلگرام ربات اضافه می‌شود
    bot = PsychBot()
