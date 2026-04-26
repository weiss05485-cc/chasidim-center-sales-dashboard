import streamlit as st
import os

# פקודה להתקנת הדפדפן בתוך השרת של Streamlit אם הוא חסר
if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    os.system("playwright install chromium")

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

st.title("📊 RNET - חיבור דפדפן וירטואלי")

def get_data_with_browser(user, pwd):
    with sync_playwright() as p:
        # הפעלת הדפדפן
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth_sync(page)
        
        try:
            st.write("🌐 פותח את אתר RNET...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle", timeout=60000)
            
            st.write("⌨️ מזין פרטי התחברות...")
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            
            st.write("🖱️ לוחץ על התחברות...")
            page.click('button[type="submit"]')
            
            # מחכה שהכתובת תשתנה לעמוד המכירות
            st.write("⏳ מחכה לטעינת נתוני המכירות...")
            page.wait_for_timeout(5000) # מחכה 5 שניות לביטחון
            
            content = page.content()
            browser.close()
            return content, "success"
            
        except Exception as e:
            browser.close()
            return None, f"שגיאה: {str(e)}"

# כפתור הפעלה
if st.button("הפעל דפדפן ומשוך נתונים"):
    with st.spinner("הדפדפן עובד ברקע... זה עשוי לקחת דקה"):
        data, status = get_data_with_browser("Hasnew", "hasnew123")
        
        if status == "success":
            st.success("הצלחנו!")
            # אם יש טבלה, ננסה להציג אותה
            st.text_area("תוצאה גולמית (HTML):", data[:2000], height=300)
        else:
            st.error(status)
