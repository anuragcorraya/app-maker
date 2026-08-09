# 🚀 MADDOX MODZ — AI Native Android App Maker

MADDOX MODZ হলো একটি **Termux-based AI Android App Maker**।

এর মূল উদ্দেশ্য হলো—তুমি শুধু একটি **App Prompt** দেবে, আর configured AI সেই prompt অনুযায়ী একটি native Android project তৈরি, build এবং error হলে repair করার workflow চালাবে।

## ✨ Main Features

* 🤖 Python-based AI adapter system
* 🔌 OpenRouter-compatible AI integration
* 🧠 Multiple AI adapter support
* 🔄 AI fallback / adapter switching architecture
* 🛠️ AI self-healing build workflow
* 📱 Native Android project generation
* 💻 Live terminal output
* 📂 Automatic project storage
* 🖼️ Optional app logo
* 🎬 Optional splash screen
* 🔥 Optional Firebase configuration
* 📦 Gradle APK build
* 📲 APK installer handoff
* 🕘 Recent projects
* 🤖 AI status management
* 🐙 GitHub automation
* 🔐 Environment-variable based API key support

---

# 📱 Requirements

তোমার Android ফোনে থাকতে হবে:

* Termux
* Internet
* Python 3
* Git
* OpenJDK
* Gradle / Android build toolchain
* GitHub account

> **Recommended:** Termux-এর official/current build ব্যবহার করো।

---

# ⚡ Quick Setup

Termux খুলে প্রথমে:

```bash
termux-setup-storage
```

Android permission চাইলে **Allow** চাপো।

তারপর:

```bash
pkg update -y
pkg upgrade -y
```

Required packages:

```bash
pkg install python git openjdk-17 wget curl unzip zip nano -y
```

---

# 📥 Clone MADDOX

GitHub repository:

```text
https://github.com/anuragcorraya/app-maker
```

Clone করতে:

```bash
cd ~
git clone https://github.com/anuragcorraya/app-maker.git
```

Project folder:

```bash
cd app-maker
```

ফাইলগুলো দেখো:

```bash
ls
```

এখানে `main.py` থাকা উচিত।

---

# 🐍 Check Python

```bash
python --version
```

Git:

```bash
git --version
```

Java:

```bash
java -version
```

সবগুলো version দেখালে basic environment প্রস্তুত।

---

# 📦 Install Python Dependencies

যদি repository-তে `requirements.txt` থাকে:

```bash
pip install -r requirements.txt
```

যদি `requirements.txt` না থাকে, তাহলে repository-এর `main.py` যে modules import করে সেগুলো অনুযায়ী dependencies install করতে হবে।

---

# ▶️ Run MADDOX

Project folder-এর ভিতর থেকে:

```bash
python main.py
```

অথবা:

```bash
python3 main.py
```

---

# 🖥️ Main Menu

MADDOX চালু হলে:

```text
+----------------------------------+
|                                  |
|           MADDOX MODZ            |
|                                  |
|  [1] new app    [2] add ai       |
|  [3] recents    [4] ais          |
|                                  |
| Status: AI Engine Ready          |
|                                  |
+----------------------------------+
```

---

# 🤖 1. Add AI

প্রথমবার MADDOX চালানোর সময় আগে AI configure করতে হবে।

Main Menu:

```text
[2] add ai
```

তারপর:

```text
[1] Add Python Script
```

AI-এর নাম দাও:

```text
OpenRouter AI
```

এরপর compatible Python AI adapter paste করো।

Script paste করার পরে:

```text
__MADDOX_END__
```

লিখে Enter দাও।

MADDOX Python script-এর syntax check করে সেটি AI directory-তে save করবে।

---

# 🧠 AI Adapter কী?

AI adapter হলো একটি Python script যেটা MADDOX এবং AI provider-এর মধ্যে bridge হিসেবে কাজ করে।

Architecture:

```text
MADDOX
   │
   ▼
Python AI Adapter
   │
   ▼
AI API
   │
   ▼
Generated Android Code
   │
   ▼
MADDOX Project Folder
```

---

# 🔑 OpenRouter API Key

API key সরাসরি Python source code-এ hard-code না করাই ভালো।

Environment variable ব্যবহার করো:

```bash
export OPENROUTER_API_KEY="YOUR_API_KEY"
```

Python:

```python
import os

api_key = os.getenv("OPENROUTER_API_KEY")
```

> ⚠️ API key কখনো GitHub repository-তে upload করো না।

---

# ⭐ 2. Activate AI

AI যোগ করার পরে:

```text
[2] add ai
```

তারপর:

```text
[4] Activate AI
```

তোমার AI select করো।

Status:

```text
OpenRouter AI [ACTIVE]
```

---

# 📱 3. Create New App

Main Menu:

```text
[1] new app
```

MADDOX ধাপে ধাপে তথ্য চাইবে।

### App Name

উদাহরণ:

```text
Maddox Calculator
```

### Package Name

```text
com.maddox.calculator
```

### App Logo

উদাহরণ:

```text
/sdcard/Download/logo.png
```

না চাইলে Enter।

### Splash Screen

উদাহরণ:

```text
/sdcard/Download/splash.png
```

না চাইলে Enter।

### SDK

উদাহরণ:

```text
[1] API 30
[2] API 31
[3] API 33
[4] API 34
[5] API 35
```

### Firebase

`google-services.json` configuration প্রয়োজন হলে দেওয়া যাবে।

না লাগলে Enter।

### AI Prompt

এখানে app-এর idea লিখবে।

উদাহরণ:

```text
Create a modern native Android calculator
with calculation history, dark mode and a clean UI.
```

---

# 🤖 AI Generation

Prompt দেওয়ার পরে active AI adapter চালু হবে।

Expected workflow:

```text
Prompt
   ↓
AI API
   ↓
AI generates Android code
   ↓
Project files created
   ↓
Gradle project prepared
```

Terminal-এ live progress দেখতে পারবে:

```text
[+] AI writing native Android code...
[+] Creating MainActivity
[+] Creating AndroidManifest
[+] Creating Gradle files
[+] Creating resources
```

---

# 🛠️ Self-Healing

Build করার সময় error হলে MADDOX error capture করবে।

Example:

```text
[✗] Build error detected.
```

তারপর AI repair pass:

```text
AI self-healing pass 1
```

Build error AI-কে পাঠানো হবে:

```text
Build Error:
error: ...
```

AI existing project inspect করে fix করার চেষ্টা করবে।

তারপর:

```text
[✓] AI repair completed.
Rebuilding...
```

Build আবার চলবে।

---

# 📦 APK Build

Successful build:

```text
[✓] Code compiled with zero errors!
[✓] APK ready
```

এরপর:

```text
[1] Install App
[2] Back
```

`Install App` select করলে Android installer open করার চেষ্টা করবে।

---

# 📂 Project Storage

MADDOX projectগুলো সাধারণত:

```text
/sdcard/MaddoxApps/
```

এর ভিতরে রাখবে।

Structure:

```text
MaddoxApps/
│
├── projects/
│   ├── MaddoxCalculator/
│   ├── MyNotes/
│   └── WeatherApp/
│
├── ais/
│   ├── openrouter_ai.py
│   └── another_ai.py
│
├── logs/
│
└── .maddox/
    └── config.json
```

---

# 🕘 Recents

Main Menu:

```text
[3] recents
```

এখানে তৈরি করা projects দেখতে পারবে।

Example:

```text
[1] MaddoxCalculator
[2] MyNotes
[3] WeatherApp
```

Project select করলে:

```text
[1] Files
[2] Build APK
[3] GitHub Push
[4] Open Folder
[5] Delete Project
[6] Back
```

---

# 🤖 AI Status

Main Menu:

```text
[4] ais
```

এখানে AI adapter status দেখা যাবে।

Example:

```text
OpenRouter AI
Status: ACTIVE

Gemini AI
Status: READY
```

---

# 🐙 GitHub Automation

Project তৈরি হওয়ার পরে GitHub repository-তে push করা যাবে।

Project select:

```text
[3] GitHub Push
```

Repository URL:

```text
https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

MADDOX Git commands চালানোর চেষ্টা করবে:

```bash
git init
git add .
git commit
git remote add origin
git push
```

---

# 🔐 Git Configuration

প্রথমবার Git ব্যবহার করলে:

```bash
git config --global user.name "YOUR_GITHUB_USERNAME"
```

Email:

```bash
git config --global user.email "YOUR_EMAIL"
```

GitHub authentication-এর জন্য GitHub-এর supported authentication method ব্যবহার করো।

> GitHub password বা token source code-এ রাখবে না।

---

# 🔒 Android Permissions

MADDOX-এর generated Android app-এ **শুধু প্রয়োজনীয় permission** থাকা উচিত।

Examples:

| Feature       | Permission                                         |
| ------------- | -------------------------------------------------- |
| Internet/API  | `INTERNET`                                         |
| Camera        | `CAMERA`                                           |
| Microphone    | `RECORD_AUDIO`                                     |
| Location      | `ACCESS_COARSE_LOCATION` / `ACCESS_FINE_LOCATION`  |
| Notifications | `POST_NOTIFICATIONS`                               |
| Photos/Media  | Android version অনুযায়ী প্রয়োজনীয় media permission |

Storage access-এর জন্য Termux:

```bash
termux-setup-storage
```

> Modern Android-এ সব app-এর জন্য broad storage permission প্রয়োজন হয় না। প্রয়োজন অনুযায়ী Android-এর system picker/API ব্যবহার করা উচিত।

---

# 🔄 Update MADDOX

GitHub থেকে latest code নিতে:

```bash
cd ~/app-maker
git pull
```

তারপর:

```bash
python main.py
```

---

# 🧪 Dependency Check

MADDOX-এর dependency check:

```text
[8] Dependencies
```

অথবা manually:

```bash
python --version
git --version
java -version
```

---

# ❗ Troubleshooting

## Python not found

```bash
pkg install python -y
```

## Git not found

```bash
pkg install git -y
```

## Java not found

```bash
pkg install openjdk-17 -y
```

## Storage সমস্যা

```bash
termux-setup-storage
```

## main.py পাওয়া যাচ্ছে না

```bash
cd ~/app-maker
ls
```

তারপর:

```bash
git pull
```

## Permission denied

```bash
chmod +x main.py
```

তারপর:

```bash
python main.py
```

---

# ⚠️ Important: Android Build Toolchain

MADDOX-এর Python script চালানো এবং **native Android APK build করা আলাদা বিষয়**।

Python চালানোর জন্য:

```text
Python
```

যথেষ্ট হতে পারে।

কিন্তু APK build করার জন্য প্রয়োজন হতে পারে:

```text
Java
Android SDK
Android build tools
Gradle
Android SDK platform
```

তাই শুধু:

```bash
python main.py
```

চালালেই যেকোনো Termux installation-এ APK build নিশ্চিত হবে—এমন নয়।

---

# 🔥 Full Workflow

```text
Install Termux
       ↓
termux-setup-storage
       ↓
Install Python/Git/Java
       ↓
Clone GitHub repository
       ↓
python main.py
       ↓
Add AI
       ↓
Python AI Script
       ↓
Activate AI
       ↓
New App
       ↓
Enter App Prompt
       ↓
AI Generates Android Code
       ↓
Save Project
       ↓
Gradle Build
       ↓
      Error?
      /   \
    Yes    No
     ↓      ↓
 AI Repair  APK
     ↓      ↓
 Rebuild   Install
     ↓
    APK
     ↓
 GitHub Push
```

---

# 📌 Repository

**MADDOX MODZ GitHub Repository:**

```text
https://github.com/anuragcorraya/app-maker
```

Clone:

```bash
git clone https://github.com/anuragcorraya/app-maker.git
```

Run:

```bash
cd app-maker
python main.py
```

---

# 👨‍💻 Developer

**MADDOX MODZ**

AI-powered native Android app generation workflow.

---

# 📄 License

এই repository ব্যবহার করার আগে repository-তে থাকা license file দেখুন। License না থাকলে code reuse বা redistribution-এর ক্ষেত্রে repository owner's permission প্রয়োজন হতে পারে.
