import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import asyncio
from datetime import datetime

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# بارگذاری متغیرها
load_dotenv()

class PsychologyBot:
    def __init__(self):
        # تنظیم Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # آمار کاربران
        self.user_stats = {}
        
        logger.info("✅ Gemini API configured successfully!")

    async def get_ai_response(self, user_message: str, user_id: int) -> str:
        """دریافت پاسخ از Gemini"""
        try:
            # پرامپت روان‌شناسی
            psychology_prompt = f"""
شما یک روان‌شناس حرفه‌ای و دلسوز هستید. به زبان فارسی پاسخ دهید.

اصول مهم:
- همدلی و درک نشان دهید
- راهکارهای عملی ارائه دهید  
- از زبان صمیمی و حمایتی استفاده کنید
- در موارد جدی، مراجعه به متخصص را پیشنهاد دهید
- پاسخ حداکثر 200 کلمه باشد

پیام کاربر: {user_message}

پاسخ روان‌شناسی:
"""

            # درخواست به Gemini (async wrapper)
            response = await asyncio.to_thread(
                self.model.generate_content, 
                psychology_prompt
            )
            
            if response and response.text:
                logger.info(f"✅ AI response generated for user {user_id}")
                return response.text.strip()
            else:
                return "متاسفم، نتوانستم پاسخ مناسبی تولید کنم. لطفاً دوباره تلاش کنید."
                
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            return "عذرخواهی می‌کنم، در حال حاضر مشکل فنی داریم. لطفاً کمی بعد تلاش کنید. 🔧"

    def update_stats(self, user_id: int):
        """آپدیت آمار کاربر"""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                'messages': 0, 
                'start_date': datetime.now().strftime('%Y-%m-%d')
            }
        
        self.user_stats[user_id]['messages'] += 1

# ایجاد instance بات
psychology_bot = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستور /start"""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name or "کاربر"
    
    welcome_message = f"""
🌟 سلام {first_name} عزیز!

من یک دستیار روان‌شناسی هوشمند هستم که با هوش مصنوعی Google Gemini کار می‌کنم.

🤝 **چطور کمکتان کنم؟**
- احساسات و مشکلاتتان را با من در میان بگذارید
- راهکارهای عملی برای بهبود روحیه دریافت کنید
- در مورد استرس، اضطراب، غم و... صحبت کنید

📋 **دستورات:**
/help - راهنمای کامل
/stats - آمار پیام‌هایتان

💚 آماده شنیدن شما هستم...
"""
    
    try:
        await update.message.reply_text(welcome_message)
        psychology_bot.update_stats(user_id)
        logger.info(f"✅ Start command sent to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Error in start command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای استفاده"""
    help_text = """
📖 **راهنمای استفاده:**

🔹 **چطور کار می‌کنم؟**
فقط پیام بفرستید و من با تکنیک‌های روان‌شناسی پاسخ می‌دهم.

🔹 **موضوعات قابل بحث:**
- استرس و اضطراب
- افسردگی و غم  
- مشکلات روابط
- اعتماد به نفس
- مدیریت عصبانیت
- مسائل خانوادگی
- مشکلات کاری

🔹 **مثال‌هایی از پیام‌ها:**
- "استرس کاری زیادی دارم"
- "احساس تنهایی می‌کنم"  
- "با همسرم مشکل دارم"
- "اعتماد به نفسم پایینه"

⚠️ **توجه مهم:** 
در موارد جدی حتماً با روان‌شناس واقعی مشورت کنید.

💪 آماده کمک به شما هستم!
"""
    
    try:
        await update.message.reply_text(help_text)
        logger.info(f"✅ Help sent to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in help command: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار کاربر"""
    user_id = update.effective_user.id
    
    if user_id in psychology_bot.user_stats:
        stats = psychology_bot.user_stats[user_id]
        stats_text = f"""
📊 **آمار شما:**

💬 تعداد پیام‌ها: {stats['messages']}
📅 شروع استفاده: {stats['start_date']}
🤖 مدل AI: Google Gemini Pro

🎯 هر چه بیشتر از من استفاده کنید، بهتر می‌توانم کمکتان کنم!

💡 **نکته:** برای بهترین نتیجه، سوالات مفصل بپرسید.
"""
    else:
        stats_text = """
📊 **آمار شما:**

💬 تعداد پیام‌ها: 0
📅 این اولین بار است که از من استفاده می‌کنید!
🤖 مدل AI: Google Gemini Pro

🚀 شروع کنید و از خدمات روان‌شناسی من بهره‌مند شوید.
"""
    
    try:
        await update.message.reply_text(stats_text)
        logger.info(f"✅ Stats sent to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Error in stats command: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام‌های کاربر"""
    user_id = update.effective_user.id
    user_message = update.message.text
    first_name = update.effective_user.first_name or "کاربر"
    
    logger.info(f"📨 Message from {user_id} ({first_name}): {user_message[:50]}...")
    
    try:
        # نمایش در حال تایپ
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )
        
        # دریافت پاسخ AI
        ai_response = await psychology_bot.get_ai_response(user_message, user_id)
        
        # ارسال پاسخ
        await update.message.reply_text(ai_response)
        
        # آپدیت آمار
        psychology_bot.update_stats(user_id)
        
        logger.info(f"✅ Response sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Error handling message from {user_id}: {e}")
        
        # پیام خطا برای کاربر
        error_message = """
😔 متاسفم، خطایی رخ داد. 

🔧 **راه‌حل‌های ممکن:**
- کمی صبر کنید و دوباره تلاش کنید
- پیام کوتاه‌تری بفرستید
- از /help برای راهنمایی استفاده کنید

💪 مشکل موقتی است و زود حل می‌شود!
"""
        try:
            await update.message.reply_text(error_message)
        except:
            pass

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاهای کلی"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """اجرای اصلی بات"""
    global psychology_bot
    
    print("🔄 Starting Psychology AI Bot...")
    
    # بررسی API Keys
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
        print("📝 Add your token to .env file: TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in .env file!")
        print("📝 Add your key to .env file: GEMINI_API_KEY=your_key_here")
        return
    
    print("✅ API Keys loaded successfully!")
    
    try:
        # ایجاد instance بات
        psychology_bot = PsychologyBot()
        
        # ساخت Application
        app = Application.builder().token(telegram_token).build()
        
        # اضافه کردن handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("stats", stats_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        print("✅ Bot handlers configured successfully!")
        print("🚀 Starting bot polling...")
        print("📱 Go to Telegram and send /start to your bot!")
        print("⏹️  Press Ctrl+C to stop the bot")
        print("-" * 50)
        
        # شروع polling
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Critical error starting bot: {e}")
        print("🔧 Check your .env file and API keys")

if __name__ == '__main__':
    main()
