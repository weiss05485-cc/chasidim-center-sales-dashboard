import streamlit as st
import os
import subprocess
import sys

# התקנת דפדפן
if 'browser_installed' not in st.session_state:
    with st.spinner("מכין את הדפדפן..."):
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        st.session_state['browser_installed'] = True

from playwright.sync_api import sync_playwright

st.title("📊 RNET - ניתוח חסימות")

def get_data_debug(user, pwd):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 720})
            page = context.new_page()
            
            st.write("🌐 ניסיון גישה לאתר...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle", timeout=60000)
            
            # צילום מסך כדי להבין מה קורה
            page.screenshot(path="debug_screen.png")
            st.image("debug_screen.png", caption="זה מה שהדפדפן רואה ברגע זה")
            
            # בדיקה אם יש בכלל שדות
            inputs = page.query_selector_all("input")
            if not inputs:
                return None, "לא נמצאו שדות כניסה בדף. כנראה יש חסימת בוטים (Cloudflare)."

            st.write("⌨️ מזין פרטים...")
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            page.click('button[type="submit"]')
            
            page.wait_for_timeout(5000)
            page.goto("https://app.rnetpos.com/sales")
            
            html = page.content()
            browser.close()
            return html, "success"
    except Exception as e:
        return None, str(e)

if st.button("הפעל בדיקה מצולמת"):
    with st.spinner("הדפדפן סורק את האתר..."):
        res, status = get_data_debug("Hasnew", "hasnew123")
        if status == "success":
            st.success("הצלחנו!")
            st.code(res[:500])
        else:
            st.error(f"סטטוס: {status}")
