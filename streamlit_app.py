import streamlit as st
import os
import subprocess
import sys

# התקנת דפדפן אם חסר
if 'browser_installed' not in st.session_state:
    with st.spinner("מתקין רכיבי דפדפן..."):
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        st.session_state['browser_installed'] = True

from playwright.sync_api import sync_playwright

st.title("📊 RNET - משיכת נתונים")

def get_data(user, pwd):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 720})
            page = context.new_page()
            
            st.write("🌐 פותח את עמוד הכניסה...")
            # נותנים לו יותר זמן להיטען
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="domcontentloaded", timeout=60000)
            
            st.write("⌨️ מחפש שדות כניסה ומזין פרטים...")
            # מחכה שהשדה יופיע על המסך לפני שהוא מנסה להקליד
            page.wait_for_selector('input', timeout=20000)
            
            # ניסיון להקליד לפי סוג השדה (יותר אמין משם)
            page.get_by_placeholder("Username").fill(user)
            page.get_by_placeholder("Password").fill(pwd)
            
            st.write("🖱️ מבצע התחברות...")
            # לחיצה על הכפתור שנראה כמו "Login" או "כניסה"
            page.get_by_role("button").first.click()
            
            st.write("⏳ מחכה לטעינת נתונים (עשוי לקחת זמן)...")
            # מחכה 10 שניות שהדף יתחלף
            page.wait_for_timeout(10000)
            
            # עובר ישירות לדף המכירות
            page.goto("https://app.rnetpos.com/sales", wait_until="networkidle")
            
            html = page.content()
            browser.close()
            return html, "success"
    except Exception as e:
        return None, str(e)

if st.button("הפעל משיכת נתונים"):
    with st.spinner("הדפדפן עובד..."):
        res, status = get_data("Hasnew", "hasnew123")
        if status == "success":
            st.success("הצלחנו!")
            st.text_area("הנתונים שהתקבלו:", res[:2000], height=300)
        else:
            st.error(f"שגיאה: {status}")
