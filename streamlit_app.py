import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="בדיקת חיבור RNET", layout="wide")
st.title("🚀 בדיקת חיבור למערכת RNET")

def fetch_sales(username, password):
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    
    # הוספת "זהות" של דפדפן רגיל כדי שלא יחסמו אותנו
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    })

    login_url = "https://app.rnetpos.com/Account/Login"
    
    try:
        st.write("מנסה לגשת לדף הכניסה עם זהות של דפדפן...")
        r = session.get(login_url, verify=False, timeout=15)
        
        # בדיקה אם קיבלנו תוכן בכלל
        if r.status_code != 200:
            return None, f"השרת של RNET החזיר שגיאה: {r.status_code}"

        soup = BeautifulSoup(r.text, 'html.parser')
        
        # חיפוש הטוקן - ננסה למצוא אותו בצורה גמישה יותר
        token_element = soup.find('input', {'name': '__RequestVerificationToken'})
        
        if not token_element:
            # אם לא מצאנו, נדפיס מה כן מצאנו כדי להבין מה קורה
            st.write("לא נמצא טוקן. בודק אם יש הודעת חסימה...")
            if "Cloudflare" in r.text or "Captcha" in r.text:
                return None, "המערכת חסומה על ידי הגנת בוטים (Cloudflare). נצטרך שיטה אחרת."
            return None, "לא נמצא טוקן אבטחה בדף."
            
        token = token_element['value']
        st.write("טוקן נמצא! מנסה להתחבר...")

        payload = {
            "UserName": username,
            "Password": password,
            "__RequestVerificationToken": token,
            "RememberMe": "false"
        }
        
        login_response = session.post(login_url, data=payload, verify=False, timeout=15)
        
        if "Login" in login_response.url:
             return None, "שם משתמש או סיסמה לא נכונים."

        sales_r = session.get("https://app.rnetpos.com/sales", verify=False, timeout=15)
        return sales_r.text, "success"
        
    except Exception as e:
        return None, f"שגיאה: {str(e)}"

if st.button("התחל משיכת נתונים"):
    html_data, status = fetch_sales("Hasnew", "hasnew123")
    
    if status == "success":
        st.success("הצלחנו!")
        st.code(html_data[:1000])
    else:
        st.error(status)
