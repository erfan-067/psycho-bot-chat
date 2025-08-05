"""
🤖 روان‌شناس هوشمند تلگرام
نویسنده: [behnik]
تاریخ: 2025
"""

import json
import os
import requests
from datetime import datetime
import base64
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔧 تنظیمات - اینجا کلیدهایت را وارد کن
TELEGRAM_BOT_TOKEN = "7478411640:AAEokvaXD4Ey7UdqHrfZBtNivF2lr8_GtqU"  # از BotFather
Gemini_API_KEY = "AIzaSyCKzDUihDzAgWuSHn8dP6iTGeE6m4-lsAI"  # از console.groq.com
GITHUB_USERNAME = "erfan-067"         # نام کاربری GitHub
GITHUB_REPO = "psycho-bot-chat"             # نام repository
GITHUB_TOKEN = "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"         # GitHub Personal Access Token

# 📝 تنظیم لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class PsychologyBot:
    def __init__(self):
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.github_api = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents"
        
    def get_ai_response(self, user_message, user_history=[]):
        """دریافت پاسخ هوشمندانه از Groq AI"""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # ساخت پیام‌های سیستم + تاریخچه
        messages = [
            {
                "role": "system", 
                "content": """شما یک روان‌شناس حرفه‌ای و دلسوز هستید که به زبان فارسی پاسخ می‌دهید.

ویژگی‌های شما:
- با همدلی و گرمی صحبت می‌کنید
- راهکارهای عملی و علمی ارائه می‌دهید
- از زبان ساده و قابل فهم استفاده می‌کنید
- امید و انگیزه القا می‌کنید
- محدودیت‌های خود را می‌شناسید

مهم: اگر مشکل خیلی جدی است، توصیه کنید با روان‌شناس حضوری مشورت کند."""
            }
        ]
        
        # اضافه کردن تاریخچه (آخرین 3 مکالمه)
        for conv in user_history[-3:]:
            messages.append({"role": "user", "content": conv.get("user_message", "")})
            messages.append({"role": "assistant", "content": conv.get("ai_response", "")})
        
        # پیام جدید کاربر
        messages.append({"role": "user", "content": user_message})
        
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content']
                return ai_response
            else:
                logger.error(f"Groq API Error: {response.status_code}")
                return "متأسفم، الان کمی مشکل فنی دارم. لطفاً چند دقیقه دیگر دوباره امتحان کن. 🔧"
        except requests.exceptions.Timeout:
            return "درخواست زیادی طول کشید. لطفاً دوباره تلاش کن. ⏰"
        except Exception as e:
            logger.error(f"Error in AI response: {e}")
            return "مشکلی در سیستم پیش اومده. چند لحظه صبر کن و دوباره امتحان کن. 🛠️"
    
    def load_user_history(self, user_id):
        """بارگذاری تاریخچه کاربر از GitHub"""
        filename = f"conversations/{user_id}.json"
        try:
            response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{filename}")
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []
    
    def save_conversation(self, user_id, user_message, ai_response, user_name=""):
        """ذخیره مکالمه در GitHub"""
        filename = f"conversations/{user_id}.json"
        
        # اطلاعات مکالمه جدید
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "user_name": user_name,
            "user_message": user_message,
            "ai_response": ai_response,
            "message_length": len(user_message),
            "response_length": len(ai_response)
        }
        
        try:
            # بارگذاری تاریخچه قبلی
            existing_conversations = self.load_user_history(user_id)
            
            # اضافه کردن مکالمه جدید
            existing_conversations.append(conversation_data)
            
            # حفظ فقط آخرین 50 مکالمه (بهینه‌سازی فضا)
            if len(existing_conversations) > 50:
                existing_conversations = existing_conversations[-50:]
            
            # تبدیل به JSON و رمزگذاری
            json_content = json.dumps(existing_conversations, ensure_ascii=False, indent=2)
            encoded_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
            
            # دریافت SHA فایل (برای آپدیت)
            sha = None
            try:
                file_response = requests.get(f"{self.github_api}/{filename}", 
                                           headers={"Authorization": f"token {GITHUB_TOKEN}"})
                if file_response.status_code == 200:
                    sha = file_response.json().get('sha')
            except:
                pass
            
            # آپلود به GitHub
            github_data = {
                "message": f"💬 Update conversation for user {user_id} at {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "content": encoded_content
            }
            
            if sha:
                github_data["sha"] = sha
            
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            
            response = requests.put(f"{self.github_api}/{filename}", headers=headers, json=github_data)
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Conversation saved for user {user_id}")
                return True
            else:
                logger.error(f"❌ GitHub save failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error saving conversation: {e}")
            return False

# 🤖 ایجاد نمونه ربات
psych_bot = PsychologyBot()

def start(update: Update, context: CallbackContext) -> None:
    """پیام شروع ربات"""
    user = update.effective_user
    welcome_message = f"""
🌟 سلام {user.first_name} عزیز!

من یک روان‌شناس هوشمند هستم و اینجام تا بهت کمک کنم. 💙

🔹 **چطور کار می‌کنم؟**
- هر سوال یا مشکلی داری، راحت بنویس
- پاسخ‌های علمی و عملی بهت می‌دم
- تمام مکالمات ما محرمانه است

🔹 **چه کمکی می‌تونم بکنم؟**
- کاهش اضطراب و استرس
- بهبود روابط
- افزایش اعتماد به نفس
- مدیریت احساسات
- راهنمایی در تصمیم‌گیری

💡 **یادت باشه**: من مکمل مشاوره حضوری هستم، نه جایگزین!

حالا بگو، چطور می‌تونم کمکت کنم؟ 😊
    """
    update.message.reply_text(welcome_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """راهنمای استفاده"""
    help_text = """
🆘 **راهنمای استفاده**

🔸 **دستورات:**
- /start - شروع مجدد
- /help - این راهنما
- /stats - آمار مکالمات شما

🔸 **نحوه استفاده:**
فقط پیام خودت را بنویس و ارسال کن!

🔸 **مثال‌ها:**
- "احساس غمگینی می‌کنم"
- "چطور اعتماد به نفسم را بالا ببرم؟"
- "با همکارانم مشکل دارم"

🔸 **نکات مهم:**
✅ صادقانه صحبت کن
✅ جزئیات بیشتر = کمک بهتر
✅ صبور باش (پردازش کمی طول می‌کشه)

❤️ اینجام تا کمکت کنم!
    """
    update.message.reply_text(help_text)

def stats(update: Update, context: CallbackContext) -> None:
    """نمایش آمار کاربر"""
    user_id = update.effective_user.id
    history = psych_bot.load_user_history(user_id)
    
    if not history:
        update.message.reply_text("هنوز مکالمه‌ای نداشتیم! بیا شروع کنیم 😊")
        return
    
    total_messages = len(history)
    first_chat = history[0]['timestamp'][:10] if history else "نامشخص"
    last_chat = history[-1]['timestamp'][:10] if history else "نامشخص"
    
    stats_text = f"""
📊 **آمار مکالمات شما**

💬 تعداد مکالمات: {total_messages}
📅 اولین مکالمه: {first_chat}
🕐 آخرین مکالمه: {last_chat}

🌟 از اینکه به من اعتماد کردی ممنونم!
همیشه اینجام که کمکت کنم 💙
    """
    update.message.reply_text(stats_text)

def handle_message(update: Update, context: CallbackContext) -> None:
    """پردازش پیام‌های کاربر"""
    user = update.effective_user
    user_message = update.message.text
    
    # نمایش پیام "در حال تایپ..."
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # بارگذاری تاریخچه کاربر
    user_history = psych_bot.load_user_history(user.id)
    
    # دریافت پاسخ از AI
    ai_response = psych_bot.get_ai_response(user_message, user_history)
    
    # ذخیره مکالمه
    save_success = psych_bot.save_conversation(
        user_id=user.id,
        user_message=user_message, 
        ai_response=ai_response,
        user_name=user.first_name or ""
    )
    
    # ارسال پاسخ
    update.message.reply_text(ai_response)
    
    # لاگ
    logger.info(f"💬 User {user.id} ({user.first_name}): {user_message[:50]}...")
    logger.info(f"🤖 Bot response saved: {save_success}")

def error_handler(update: Update, context: CallbackContext) -> None:
    """مدیریت خطاها"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        update.message.reply_text(
            "متأسفم، مشکلی پیش اومده! 😅
"
            "لطفاً دوباره امتحان کن یا چند دقیقه صبر کن."
        )

def main():
    """اجرای اصلی ربات"""
    
    # بررسی کلیدها
    if "YOUR_TELEGRAM_TOKEN_HERE" in TELEGRAM_BOT_TOKEN:
        print("❌ لطفاً کلیدهای API را در فایل bot.py وارد کنید!")
        return
    
    # ساخت ربات
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    # اضافه کردن هندلرها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error_handler)
    
    # شروع ربات
    print("🤖 ربات روان‌شناس شروع شد!")
    print(f"📊 Username: @{updater.bot.username}")
    print("🔄 در حال گوش دادن...")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
