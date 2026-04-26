import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="בדיקת חיבור RNET", layout="wide")

st.title("🚀 בדיקת חיבור למערכת RNET")
st.info("אם אתה רואה את ההודעה הזו, האתר עובד תקין. עכשיו נסה להתחבר.")

def fetch_sales(username, password):
    # ביטול אזהרות SSL
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    login_url = "https://app.rnetpos.com/Account/Login"
    
    try:
        # 1. ניסיון טעינת דף כניסה
        st.write("מנסה לגשת לדף הכניסה...")
        r = session.get(login_url, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        token_element = soup.find('input', {'name': '__RequestVerificationToken'})
        if not token_element:
            return None, "שגיאה: לא נמצא טוקן אבטחה בדף (RNET שינו משהו?)"
            
        token = token_element['value']
        
        # 2. שליחת פרטי התחבורה
        payload = {
            "UserName": username,
            "Password": password,
            "__RequestVerificationToken": token,
            "RememberMe": "false"
        }
        
        st.write("שולח פרטי התחברות...")
        login_response = session.post(login_url, data=payload, verify=False, timeout=10)
        
        # בדיקה אם נשארנו בדף הלוגין (סימן שנכשל)
        if "Login" in login_response.url and login_response.status_code == 200:
             return None, "שם משתמש או סיסמה לא נכונים במערכת RNET."

        # 3. משיכת נתונים
        st.write("מתחבר לדף המכירות...")
        sales_r = session.get("https://app.rnetpos.com/sales", verify=False, timeout=10)
        return sales_r.text, "success"
        
    except Exception as e:
        return None, f"שגיאה בתקשורת: {str(e)}"

# כפתור הפעלה
if st.button("התחל משיכת נתונים"):
    # כאן השתמשתי בפרטים שנתת לי קודם
    html_data, status = fetch_sales("Hasnew", "hasnew123")
    
    if status == "success":
        st.success("בינגו! הצלחנו להיכנס.")
        st.subheader("תוכן ראשוני מהאתר:")
        st.code(html_data[:1000], language='html')
    else:
        st.error(status)
