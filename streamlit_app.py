import streamlit as st
import pandas as pd
import requests
import io

# הגדרות דף
st.set_page_config(page_title="RNET Auto-Dashboard", layout="wide")

st.title("🚀 דאשבורד RNET - עדכון אוטומטי")

# פרטי הגישה מהתמונה ששלחת
USER = "Hasnew"
PASS = "hasnew123"
BASE_URL = "https://app.rnetpos.com"

def get_rnet_data():
    session = requests.Session()
    
    # כתובות (יכול להשתנות מעט בהתאם למבנה האתר)
    login_url = f"{BASE_URL}/Account/Login" 
    data_url = f"{BASE_URL}/Sales/ExportToExcel" # הכתובת שבה מורידים את הקובץ
    
    # שלב 1: התחברות
    # אנחנו שולחים את הטופס כמו שהאתר מצפה לקבל
    login_data = {
        "UserName": USER,
        "Password": PASS,
        "RememberMe": "false"
    }
    
    try:
        # שליחת בקשת התחברות
        res = session.post(login_url, data=login_data, timeout=15)
        
        # שלב 2: משיכת הנתונים
        # כאן אנחנו מנסים להוריד את קובץ המכירות
        # (ייתכן וצריך להוסיף כאן פרמטרים של תאריכים בתוך ה-URL)
        response = session.get(data_url, timeout=20)
        
        if response.status_code == 200:
            # אם קיבלנו תוכן של אקסל, נקרא אותו ל-Dataframe
            df = pd.read_excel(io.BytesIO(response.content))
            return df
        else:
            st.error(f"התחברות הצליחה אבל לא הצלחתי למשוך את הקובץ. קוד שגיאה: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"שגיאה בתקשורת עם האתר: {e}")
        return None

# כפתור רענון
if st.button("🔄 רענן נתונים עכשיו"):
    with st.spinner("מתחבר ל-RNET ושואב נתונים..."):
        df = get_rnet_data()
        
        if df is not None:
            st.success("הנתונים עודכנו בהצלחה!")
            
            # --- כאן מתחיל הדאשבורד שלך ---
            
            # ניקוי כותרות
            df.columns = df.columns.str.strip()
            
            # מדדים (KPI)
            st.subheader("📌 סיכום מכירות")
            col1, col2 = st.columns(2)
            
            # זיהוי עמודת סכום (צריך להתאים לשם העמודה באקסל שלהם)
            total_col = next((c for c in df.columns if 'סה"כ' in str(c) or 'Total' in str(c)), None)
            
            if total_col:
                total_val = pd.to_numeric(df[total_col], errors='coerce').sum()
                col1.metric("סה-כ הכנסות", f"₪{total_val:,.2f}")
                col2.metric("מספר עסקאות", len(df))
            
            # הצגת הטבלה
            st.markdown("---")
            st.subheader("🔍 נתוני מכירות אחרונים")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.info("נסה לבדוק אם שם המשתמש והסיסמה עדיין בתוקף באתר.")

st.markdown("---")
st.caption("מערכת זו מבצעת אוטומציה מול app.rnetpos.com")
