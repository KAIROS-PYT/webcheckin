# web-check-in automated
# 🛫 Indigo Web Check-in Automation (`indigo.py`)

## 📌 Overview

This script automates the **IndiGo Airlines web check-in** process using [Playwright](https://playwright.dev/). It intelligently detects form fields (PNR and Last Name), fills them in, and attempts to click the submit button — making it ideal for automating routine check-ins or diagnosing form issues.

## 🚀 Features

- Opens the IndiGo web check-in page
- Detects and interacts with dynamic content and iframes
- Locates PNR and Last Name input fields using intelligent keyword matching
- Attempts multiple input methods (fill, click+fill, type)
- Locates and clicks the submit button
- Provides extensive console logging for debugging
- Keeps the browser open for 60 seconds for manual inspection

## 🧠 Why This Script?

> Unlike naive web automation, this script:
- Handles iframes
- Dynamically inspects all inputs for potential PNR/Name matches
- Attempts various fallback methods to fill fields
- Provides diagnostic output at each step

---

## 🛠️ Requirements

- Python 3.7+
- [Playwright for Python](https://playwright.dev/python/)

### Install dependencies:
```bash
pip install playwright
playwright install

