import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="RNET BI Dashboard", layout="wide")

st.title("📊 דאשבורד מכירות RNET (חיבור API)")

# הזנת פרטי גישה (לפי התיעוד ששלחת)
with st.sidebar:
    st.header("מפתח גישה")
    token = st.text_input("הדבק כאן את ה-Security Token שלך:", type="password")
    st.info("את ה-Token ניתן לקבל ממנהל תיק הלקוח ב-RNET")

if token:
    # שליפת רשימת חנויות לפי התיעוד ששלחת
    url = "https://api.rnetpos.com/v1/stores" #
    
    # הגדרת אימות (Basic Auth) לפי התיעוד
    # משתמש: token, סיסמה: ה-token האישי
    auth = ('token', token) #

    with st.spinner("מושך נתונים מהשרת..."):
        try:
            response = requests.get(url, auth=auth, timeout=10) #
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                
                # תצוגה של החנויות (בני ברק, ירושלים וכו')
                st.success(f"נמצאו {len(df)} חנויות פעילות")
                
                # יצירת טבלה יפה
                cols_to_show = ['StoreName', 'Code', 'Status']
                st.table(df[cols_to_show])
                
            elif response.status_code == 401:
                st.error("❌ ה-Token לא תקין. וודא שהעתקת אותו נכון.")
            else:
                st.error(f"שגיאה מהשרת: {response.status_code}")
        except Exception as e:
            st.error(f"שגיאה בחיבור: {e}")
else:
    st.warning("נא להזין Security Token כדי לראות נתונים.")
