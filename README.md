# AI-Receipt-Scanner
An AI-powered web app that uses Deep Learning (EasyOCR) to automatically scan receipts, extract total amounts, and visualize personal expense data.

## 📌 Project Overview
This is a full-stack AI web application built with Python and Streamlit. It uses Deep Learning-based Optical Character Recognition (OCR) to automatically read physical supermarket bills, restaurant receipts, and invoices. 

Instead of manual data entry, the AI extracts the date, categorizes the expense, and logs the total amount into an interactive financial dashboard.

## 🚀 Features
* **AI Computer Vision:** Utilizes `EasyOCR` to accurately read messy and blurry text from physical receipts.
* **Smart Data Extraction:** Custom Regular Expressions (Regex) handle OCR typos to perfectly capture currency amounts and dates.
* **Auto-Categorization:** Uses basic NLP to read merchant items and automatically tag expenses as "Food", "Medical", "Transport", etc.
* **Interactive Dashboard:** Built with `Streamlit` to visualize spending breakdowns using dynamic bar charts.
* **Data Export:** Users can download their logged expense history as a clean CSV file.

## 💻 Tech Stack
* **Frontend/UI:** Streamlit
* **AI/Deep Learning:** EasyOCR, OpenCV (Headless)
* **Data Processing:** Python, Pandas, NumPy, Regex (re)

## 🌐 Live Demo
You can test the AI directly in your browser here: **[Insert Your Streamlit Cloud Link Here]**

## 🛠️ How to Run Locally
1. Clone this repository.
2. Install the required libraries:
   `pip install -r requirements.txt`
3. Run the application:
   `python -m streamlit run app.py`
