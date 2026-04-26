import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="RNET Dashboard", layout="wide")
st.title("📊 דאשבורד מכירות RNET")

# תיבת הדבקה למה שהעתקת מה-Console
raw_cookie = st.text_input("הדבק כאן את מה שהעתקת מה-Console (Ctrl+V):", type="password")

if raw_cookie:
    url = "https://app.rnetpos.com/sales"
    
    # הגדרת ה-Headers עם כל הקוקיז שהדבקת
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': raw_cookie  # כאן אנחנו משתמשים בכל השורה שהעתקת
    }

    with st.spinner("מתחבר ל-RNET..."):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200 and "Login" not in response.url:
                st.success("✅ הצלחנו! המערכת מחוברת.")
                
                # תצוגה ראשונית של הקוד כדי שאוכל לעזור לך לעצב
                st.subheader("נתונים גולמיים מהשרת:")
                st.code(response.text[:2000])
            else:
                st.error("❌ ההתחברות נכשלה. וודא שאתה מחובר לאתר RNET בדפדפן לפני העתקת הקוד.")
        except Exception as e:
            st.error(f"שגיאה: {e}")
