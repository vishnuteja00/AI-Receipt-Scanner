import easyocr
import streamlit as st
import re
from PIL import Image
import numpy as np
import pandas as pd
import ssl

# Bypass SSL Verification issues
ssl._create_default_https_context = ssl._create_unverified_context

# Page Config
st.set_page_config(page_title="AI Receipt Scanner", layout="wide")

@st.cache_resource
def load_model():
    return easyocr.Reader(['en'])

reader = load_model()

# UPGRADE 1: Added "Category" to our database
if 'expense_db' not in st.session_state:
    st.session_state.expense_db = pd.DataFrame(columns=["Date", "Merchant/Details", "Category", "Amount (₹)"])

st.title("🧾 Smart AI Receipt Analyzer & Expense Tracker")
st.write("An advanced OCR system designed for automated financial document data extraction.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Upload Section")
    uploaded_file = st.file_uploader("Upload a receipt image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Target Document", use_container_width=True)
        
        with st.spinner("Processing document using Deep Learning..."):
            image_np = np.array(image)
            result = reader.readtext(image_np, detail=0)
            full_text = " ".join(result)
            
            # --- AI Regex Extraction Engines ---
            total_pattern = re.search(r'(?:Total|Payable|Net|Amount|Anount)[^\d]*(\d+[.,]\d{2})', full_text, re.IGNORECASE)
            detected_amount = total_pattern.group(1) if total_pattern else "0.00"
            
            date_pattern = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', full_text)
            detected_date = date_pattern.group(1) if date_pattern else "Not Found"

            # UPGRADE 2: Basic NLP Auto-Categorization
            text_lower = full_text.lower()
            if any(word in text_lower for word in ['restaurant', 'food', 'swiggy', 'zomato', 'cafe', 'bread', 'sugar', 'bakery']):
                auto_category = "Food & Dining"
            elif any(word in text_lower for word in ['hospital', 'pharmacy', 'clinic', 'medical', 'tablet', 'drug']):
                auto_category = "Medical"
            elif any(word in text_lower for word in ['uber', 'petrol', 'diesel', 'taxi', 'auto', 'transport', 'fuel']):
                auto_category = "Transport"
            else:
                auto_category = "Shopping / General"

with col2:
    st.header("📊 AI Extraction Verification")
    if uploaded_file is not None:
        st.success("Analysis Complete!")
        
        st.subheader("Edit/Verify Extracted Data:")
        verified_date = st.text_input("Detected Date", value=detected_date)
        verified_merchant = st.text_input("Merchant Name / Details", value="General Store")
        
        # Determine the default index for the dropdown based on AI prediction
        category_options = ["Food & Dining", "Medical", "Transport", "Shopping / General", "Other"]
        default_index = category_options.index(auto_category) if auto_category in category_options else 3
        verified_category = st.selectbox("Expense Category", category_options, index=default_index)
        
        verified_amount = st.text_input("Detected Total Amount (₹)", value=detected_amount)
        
        if st.button("💾 Save to Expense Log"):
            new_row = pd.DataFrame([{
                "Date": verified_date, 
                "Merchant/Details": verified_merchant, 
                "Category": verified_category,
                "Amount (₹)": float(verified_amount.replace(',', ''))
            }])
            st.session_state.expense_db = pd.concat([st.session_state.expense_db, new_row], ignore_index=True)
            st.toast("Saved successfully!")

# --- Expense History Log Dashboard ---
st.markdown("---")
st.header("📈 Visual Expense Dashboard")

if not st.session_state.expense_db.empty:
    # Show the table
    st.dataframe(st.session_state.expense_db, use_container_width=True)
    
    # UPGRADE 3: Data Visualization! 
    st.subheader("💰 Spending Breakdown by Category")
    
    # Group the data by category and sum the amounts
    chart_data = st.session_state.expense_db.groupby("Category")["Amount (₹)"].sum().reset_index()
    # Set the index so Streamlit draws the chart correctly
    chart_data = chart_data.set_index("Category")
    
    # Draw a beautiful bar chart
    st.bar_chart(chart_data, color="#ff4b4b")
    
    csv = st.session_state.expense_db.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Logs as CSV", data=csv, file_name="Expense_Report.csv", mime="text/csv")
else:
    st.info("No documents logged yet. Upload a receipt above and click 'Save to Expense Log'.")