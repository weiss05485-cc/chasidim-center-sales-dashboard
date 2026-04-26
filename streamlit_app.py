import streamlit as st
import os
import subprocess
import sys

st.set_page_config(page_title="RNET Sales Dashboard", layout="wide")

# פונקציה להתקנת דפדפן בצורה אגרסיבית
def install_playwright():
    try:
        # התקנת הדפדפן הספציפי של Playwright
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return True
    except Exception as e:
        st.error(f"שגיאה בהתקנת הדפדפן: {e}")
        return False

st.title("📊 RNET - משיכת נתונים")

# בדיקה והתקנה ראשונית
if 'browser_installed' not in st.session_state:
    with st.spinner("מתקין רכיבי דפדפן בשרת (חד-פעמי)..."):
        if install_playwright():
            st.session_state['browser_installed'] = True
            st.success("הדפדפן הותקן בהצלחה!")

from playwright.sync_api import sync_playwright

def get_data(user, pwd):
    try:
        with sync_playwright() as p:
            # הפעלה עם הגדרה שמתעלמת משגיאות נתיב
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            st.write("🌐 מתחבר ל-RNET...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle", timeout=60000)
            
            st.write("⌨️ מזין פרטים...")
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            
            st.write("🖱️ מבצע התחברות...")
            page.click('button[type="submit"]')
            
            # המתנה לטעינת עמוד המכירות
            st.write("⏳ שואב נתוני מכירות...")
            page.wait_for_timeout(7000) 
            
            # אם הוא לא עבר אוטומטית, נכריח אותו לעבור למכירות
            if "sales" not in page.url:
                page.goto("https://app.rnetpos.com/sales", wait_until="networkidle")
            
            html = page.content()
            browser.close()
            return html, "success"
    except Exception as e:
        return None, str(e)

# כפתור הפעלה
if st.button("הפעל משיכת נתונים"):
    res, status = get_data("Hasnew", "hasnew123")
    if status == "success":
        st.success("בינגו! הנתונים נמשכו.")
        # כאן אנחנו מציגים את הקוד כדי לדעת מה קיבלנו
        st.text_area("קוד הנתונים שהתקבל:", res[:2000], height=300)
    else:
        st.error(f"שגיאה: {status}")
