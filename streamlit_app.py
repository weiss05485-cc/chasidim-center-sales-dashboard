import streamlit as st
from playwright.sync_api import sync_playwright

def get_data_mobile_mode(user, pwd):
    try:
        with sync_playwright() as p:
            # אנחנו משתמשים בזהות של אייפון - לפעמים זה עוקף חסימות שולחן עבודה
            iphone = p.devices['iPhone 13']
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(**iphone)
            page = context.new_page()
            
            st.write("📱 מנסה לגשת בגרסת מובייל...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle")
            
            # צילום מסך כדי לראות אם עקפנו
            page.screenshot(path="mobile_test.png")
            st.image("mobile_test.png", caption="מה שהדפדפן רואה עכשיו")
            
            if "Cloudflare" in page.content():
                return None, "עדיין חסום. Cloudflare מזהה אותנו."
            
            # אם הגענו לכאן ויש שדות - נמשיך
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            
            return page.content(), "success"
    except Exception as e:
        return None, str(e)

st.title("RNET - ניסיון עקיפת חסימה")
if st.button("נסה להתחבר כטלפון"):
    data, status = get_data_mobile_mode("Hasnew", "hasnew123")
    st.write(status)
