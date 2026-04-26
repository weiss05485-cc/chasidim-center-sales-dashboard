import streamlit as st
import asyncio
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

st.title("📊 RNET - חיבור באמצעות דפדפן וירטואלי")

def get_data_with_browser(user, pwd):
    with sync_playwright() as p:
        # פתיחת דפדפן כרום "חרישי"
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # הגנה מפני זיהוי בוטים
        stealth_sync(page)
        
        try:
            st.write("🌐 פותח את אתר RNET...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle")
            
            st.write("⌨️ מזין פרטי התחברות...")
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            
            # לחיצה על כפתור התחברות
            page.click('button[type="submit"]')
            
            # מחכה שהדף יטען אחרי ההתחברות
            page.wait_for_url("**/sales**", timeout=10000)
            
            st.write("✅ התחברנו! שואב נתונים...")
            content = page.content()
            
            browser.close()
            return content, "success"
            
        except Exception as e:
            browser.close()
            return None, f"שגיאה: {str(e)}"

if st.button("הפעל דפדפן ומשוך נתונים"):
    with st.spinner("הדפדפן הוירטואלי מתחיל לעבוד... זה עשוי לקחת כ-30 שניות"):
        data, status = get_data_with_browser("Hasnew", "hasnew123")
        
        if status == "success":
            st.success("הצלחנו לעקוף את החסימה!")
            st.code(data[:1000])
        else:
            st.error(status)
            st.info("אם מופיעה שגיאת Timeout, ייתכן שהאתר דורש אימות נוסף או שהשדות שונים.")
