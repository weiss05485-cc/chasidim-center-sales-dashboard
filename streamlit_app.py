import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="דאשבורד מכירות RNET", layout="wide")

st.title("📊 מערכת מעקב מכירות RNET")

def fetch_sales(username, password):
    session = requests.Session()
    login_url = "https://app.rnetpos.com/Account/Login"
    
    try:
        # 1. קבלת דף הכניסה וה-Token
        r = session.get(login_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_element = soup.find('input', {'name': '__RequestVerificationToken'})
        
        if not token_element:
            return None, "לא ניתן היה למצוא טוקן אבטחה בדף."
            
        token = token_element['value']
        
        # 2. התחברות
        payload = {
            "UserName": username,
            "Password": password,
            "__RequestVerificationToken": token,
            "RememberMe": "false"
        }
        
        login_response = session.post(login_url, data=payload)
        
        if "Login" in login_response.url:
            return None, "שם משתמש או סיסמה שגויים."

        # 3. משיכת דף המכירות
        sales_r = session.get("https://app.rnetpos.com/sales")
        return sales_r.text, "success"
        
    except Exception as e:
        return None, f"שגיאה טכנית: {str(e)}"

# ממשק משתמש
col1, col2 = st.columns(2)
with col1:
    user = st.text_input("שם משתמש RNET", value="Hasnew")
with col2:
    pwd = st.text_input("סיסמה RNET", value="hasnew123", type="password")

if st.button("משוך נתונים מהקופה"):
    with st.spinner("מתחבר ל-RNET..."):
        data, status = fetch_sales(user, pwd)
        
        if status == "success":
            st.success("התחברות הצליחה!")
            st.write("---")
            st.subheader("נתונים גולמיים שהתקבלו:")
            st.code(data[:1000], language='html')
        else:
            st.error(status)
