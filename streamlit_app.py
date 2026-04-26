import streamlit as st
import os

# התקנת הדפדפן אם הוא חסר
if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    st.info("מתקין רכיבי דפדפן בפעם הראשונה... זה ייקח רגע.")
    os.system("playwright install chromium")

from playwright.sync_api import sync_playwright

st.title("📊 RNET - משיכת נתונים")

def get_data(user, pwd):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # יצירת זהות דפדפן בלי הספריה הבעייתית
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            st.write("🌐 פותח את עמוד הכניסה...")
            page.goto("https://app.rnetpos.com/Account/Login", wait_until="networkidle")
            
            st.write("⌨️ מזין פרטים...")
            page.fill('input[name="UserName"]', user)
            page.fill('input[name="Password"]', pwd)
            
            st.write("🖱️ מתחבר...")
            page.click('button[type="submit"]')
            
            # מחכה 5 שניות לטעינת הדף שאחרי הלוגין
            page.wait_for_timeout(5000)
            
            # מעבר לדף המכירות (ליתר ביטחון)
            page.goto("https://app.rnetpos.com/sales")
            page.wait_for_timeout(3000)
            
            html = page.content()
            browser.close()
            return html, "success"
    except Exception as e:
        return None, str(e)

if st.button("הפעל משיכה"):
    res, status = get_data("Hasnew", "hasnew123")
    if status == "success":
        st.success("הצלחנו!")
        st.code(res[:1000])
    else:
        st.error(f"שגיאה: {status}")
