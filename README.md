# 🤖 روان‌شناس هوشمند تلگرام

ربات هوشمند روان‌شناسی با استفاده از Groq AI و GitHub برای ذخیره‌سازی

## 🏗️ ساختار پروژه

psycho-bot-database/
├── README.md              # راهنمای پروژه  
├── conversations/         # پوشه مکالمات کاربران
│   ├── placeholder.txt   # فایل نگهدارنده پوشه
│   └── [user_id].json    # فایل‌های مکالمه (خودکار ساخته می‌شود)
├── bot.py                # کد اصلی ربات
└── requirements.txt      # کتابخانه‌های مورد نیاز

## ⚡ راه‌اندازی سریع

### 1. کلیدهای مورد نیاز:
- **Telegram Bot Token**: از @BotFather
- **Groq API Key**: از console.groq.com (رایگان)
- **GitHub Token**: از GitHub Settings > Developer settings

### 2. نصب:
```bash
pip install -r requirements.txt

### 3. اجرا:
bash
python bot.py

## 📊 ویژگی‌ها

- ✅ پاسخ‌های روان‌شناسی حرفه‌ای
- ✅ ذخیره خودکار مکالمات در GitHub
- ✅ رایگان (Groq AI)
- ✅ امن و محرمانه
- ✅ قابل توسعه

## 🔧 تنظیمات

فایل `bot.py` را ویرایش کنید و کلیدهای API را وارد کنید:

python
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"

## 📱 استفاده

1. ربات را در تلگرام پیدا کنید
2. /start بزنید
3. سوال یا مشکل خود را بنویسید
4. پاسخ تخصصی دریافت کنید

---

💡 **توجه**: این ربات جایگزین مشاوره حضوری نیست و صرفاً راهنمایی اولیه ارائه می‌دهد.


### **گام 3: ذخیره تغییرات**
💾 نهایی کردن:
1. پایین صفحه، قسمت "Commit changes"
2. عنوان: "Add project structure to README"
3. توضیحات: "Added file structure and setup guide"
4. روی "Commit changes" کلیک کن


---

## **🎨 نتیجه نهایی در GitHub:**

وقتی کسی به repository شما مراجعه کند، این ساختار را در صفحه اصلی می‌بیند:

📋 نمایش در GitHub:
┌─────────────────────────────────────┐
│ 🤖 روان‌شناس هوشمند تلگرام          │
│                                     │
│ ## 🏗️ ساختار پروژه                 │
│                                     │
│ psycho-bot-database/               │
│ ├── README.md                      │
│ ├── conversations/                 │
│ │   ├── placeholder.txt           │
│ │   └── [user_id].json           │
│ ├── bot.py                        │
│ └── requirements.txt              │
│                                     │
│ ## ⚡ راه‌اندازی سریع                │
│ ...                                 │
└─────────────────────────────────────┘


---

## **🎯 هدف این ساختار:**

### **برای کاربران:**
👥 فوائد:
✅ فهم سریع پروژه
✅ راهنمای نصب واضح  
✅ توضیح فایل‌ها
✅ نحوه استفاده


### **برای توسعه‌دهندگان:**
👨‍💻 فوائد:
✅ ساختار منطقی
✅ مستندسازی کامل
✅ قابل نگهداری
✅ حرفه‌ای به نظر می‌رسد


**آیا این واضح شد؟ آیا می‌خواهید مرحله بعد (دریافت API کلیدها) را شرح دهم؟** 🔑
