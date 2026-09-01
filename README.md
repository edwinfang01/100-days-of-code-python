# Python Pro Bootcamp: Intermediate & Advanced Projects

This repository tracks my progress through the **100 Days of Code: The Complete Python Pro Bootcamp** by Dr. Angela Yu. 

## 🎯 My Learning Path
I have focused this repository on the **Intermediate and Advanced** sections of the course (starting from **Day 25**), as I had already mastered the basic fundamentals of Python. 

My current focus is on:
- **Data Handling:** Working with CSV and JSON files using Pandas.
- **GUI Applications:** Building interactive software with Tkinter.
- **Web Development & Scraping:** Structuring web pages with HTML5/CSS3 and harvesting data using Beautiful Soup.
- **Problem Solving:** Implementing complex logic and OOP principles.

---

## 🚀 Projects Log

| Day | Project | Status | Key Concepts |
| :---: | :--- | :---: | :--- |
| 25 | U.S. States Game | ✅ Done | `Pandas`, CSV reading, Coordinate systems. |
| 26 | NATO Alphabet | ✅ Done | List & Dictionary Comprehensions. |
| 27 | Mile to Km Converter | ✅ Done | `Tkinter`, `*args`, `**kwargs`. |
| 28 | Pomodoro App | ✅ Done | UI Timers, `after()` method. |
| 29-30 | **Password Manager** | ✅ Done | **Day 29:** UI & File I/O. **Day 30:** JSON data & Exception handling (`try/except`). |
| 31 | **Flash Card App** | ✅ Done | UI Layout, French-English translation logic. |
| 32 | Automated Birthday Wisher | ✅ Done | smtplib, datetime, Environment Variables, Security. |
| 33 | ISS Overhead Notifier | ✅ Done | Working with APIs (`requests`), JSON parsing, API parameters, and `smtplib` for automated alerts. |
| 34 | Quizzler App | ✅ Done | Class-based UI development, API calls with parameters, **Type Hinting**, and HTML unescaping for text data. |
| 35 | Rain Alert (WhatsApp) | ✅ Done | API calls, JSON slicing. **[See Automated Bot Version 🤖](https://github.com/edwinfang01/automated-day-35-rain-alert)** |
| 36 | Stock Trading News Alert | ✅ Done | Integration of multiple APIs (Stock + News), percentage change logic, and automated WhatsApp/SMS alerts. |
| 37 | Habit Tracker | ✅ Done | Advanced HTTP Requests (POST/PUT/DELETE) & Headers. <br> [![Habit Graph](https://pixe.la/v1/users/yaboiamai/graphs/graph1.svg)](https://pixe.la/v1/users/yaboiamai/graphs/graph1.html) |
| 38 | Workout Tracker (NLP) | ✅ Done | **Natural Language Processing (NLP)** to structure workout data, Google Sheets API integration (Sheety API), and secure Bearer Token authentication. |
| 39-40 | **Flight Club Capstone** | ✅ Done | Advanced **OOP**, API Orchestration (SerpApi + Sheety), **Data Caching**, and Multi-channel Broadcasting (Email + WhatsApp). |
| 41 | Top 3 Animes Website | ✅ Done | HTML5 foundations: Heading hierarchy, paragraphs, and horizontal rules. |
| 42 | HTML Forms & Tables | ✅ Done | Intermediate HTML: Creating complex data tables and building interactive user forms. |
| 43 | Personal Website (CSS Intro) | ✅ Done | Introduction to CSS: Inline, internal, and external styling, selectors, and text formatting. |
| 44 | Portfolio Website (CSS Intermediate) | ✅ Done | CSS Positioning, the Box Model, layouts, and static web deployment. |
| 45 | Top 100 Movies Scraper | ✅ Done | **Web Scraping** with `BeautifulSoup` & `requests`. Adapted code to target the live, modern Empire Online website layout. |
| 46 | Musical Time Machine | ✅ Done | **Spotify API (Spotipy)**, Web Scraping (Billboard Hot 100), and **`requests_cache`** to optimize network requests.
| 47 | Automated Amazon Price Tracker | ✅ Done | Web Scraping (BeautifulSoup), automated email alerts (smtplib), and **localization via Cookies** (USD/en_US) handling.
| 48 | Cookie Clicker Bot | ✅ Done | **Selenium WebDriver**, browser automation, interaction with dynamic elements, and real-time game logic.
| 49 | Snack and Lift | ✅ Done | **Selenium WebDriver**, advanced web flow automation, and multi-page navigation.


💡 Decision & Problem Solving:
- **Day 35:** I pivoted from Twilio SMS to the Twilio WhatsApp API due to regional limitations with trial SMS services. I successfully configured the Twilio Sandbox to receive automated weather alerts directly on my phone.
- **Day 45:** The course's archived Wayback Machine link for the Empire article was broken. I investigated the live Empire Online website, analyzed its updated DOM structure, and rewrote the parsing logic to scrape the top 100 movies from their current live page.
- **Day 46 (Performance Optimization):** To avoid redundant network requests to the Billboard website during testing, I integrated `requests_cache`. This caches HTTP responses locally, speeding up execution and preventing potential IP rate-limiting.
- **Day 47 (Localization & Scraping Fix):** When scraping Amazon from my local region, prices defaulted to Dominican Pesos (DOP) or altered the DOM structure. I resolved this by injecting explicit localization cookies (`"i18n-prefs": "USD"` and `"lc-main": "en_US"`) into the request headers to consistently force the US/English store interface.


---

## 🛠️ Current Tech Stack
- **Language:** Python 3.x
- **Libraries & Frameworks:** Pandas, Tkinter, BeautifulSoup4, Requests.
- **Web Foundations:** HTML5, CSS3.
- **Focus:** Object-Oriented Programming (OOP) & Web Scraping.

## ⚙️ How to Run
1. Clone the repository.
2. Navigate to the specific day's folder.
3. Install dependencies: `pip install -r requirements.txt` (if applicable).
4. Run `python main.py` or open the `.html` files in a browser for web days.

---
*Note: This repository is updated regularly as I progress through the challenges.*
