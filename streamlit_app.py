import streamlit as st
import pandas as pd
import requests
import io
import urllib3

# השתקת אזהרות ה-SSL בעקבות השימוש ב-verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# הגדרות דף
st.set_page_config(page_title="RNET Live Dashboard", layout="wide")

st.title("🚀 דאשבורד RNET - עדכון אוטומטי")
st.markdown("---")

# פרטי הגישה מהתמונה 111_11.JPG
USER = "Hasnew"
PASS = "hasnew123"
BASE_URL = "https://app.rnetpos.com"

def get_rnet_data():
    session = requests.Session()
    
    # כתובות האתר
    login_url = f"{BASE_URL}/Account/Login" 
    # כתובת הייצוא (זו הכתובת הנפוצה, אם לא עובד נצטרך לדייק אותה מהדפדפן)
    data_url = f"{BASE_URL}/Sales/ExportToExcel" 
    
    # "זהות" של דפדפן כדי שהאתר לא יחסום את הבוט
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    # נתוני ההתחברות
    login_data = {
        "UserName": USER,
        "Password": PASS,
        "RememberMe": "false"
    }
    
    try:
        # שלב 1: התחברות (עם ביטול אימות SSL כדי לפתור את השגיאה שקיבלת)
        login_res = session.post(login_url, data=login_data, headers=headers, verify=False, timeout=20)
        
        if login_res.status_code != 200:
            st.error(f"שגיאה בהתחברות לאתר. קוד: {login_res.status_code}")
            return None

        # שלב 2: משיכת הנתונים
        data_res = session.get(data_url, headers=headers, verify=False, timeout=30)
        
        if data_res.status_code == 200:
            # קריאת האקסל מהזיכרון
            # משתמשים ב-skiprows כדי למצוא את הטבלה האמיתית במידה ויש שורות ריקות למעלה
            file_stream = io.BytesIO(data_res.content)
            
            # ניסיון לקרוא ולזהות כותרות (עד 10 שורות ראשונות)
            df = pd.read_excel(file_stream)
            for i in range(1, 10):
                if any(col for col in df.columns if not str(col).startswith('Unnamed')):
                    break
                file_stream.seek(0)
                df = pd.read_excel(file_stream, skiprows=i)
            
            return df
        else:
            st.error(f"התחברתי בהצלחה, אך לא הצלחתי להוריד את הקובץ. קוד שגיאה: {data_res.status_code}")
            st.info("ייתכן וכתובת הורדת האקסל באתר השתנתה.")
            return None

    except Exception as e:
        st.error(f"שגיאה בתקשורת: {e}")
        return None

# כפתור הפעלה
if st.button("🔄 משוך נתונים מ-RNET עכשיו"):
    with st.spinner("מתחבר לחשבון Hasnew ושואב נתונים..."):
        df = get_rnet_data()
        
        if df is not None:
            st.success(f"נמשכו {len(df)} שורות בהצלחה!")
            
            # ניקוי בסיסי
            df.columns = df.columns.str.strip()
            
            # הצגת מדדים בסיסיים
            st.markdown("### 📌 סיכום נתונים")
            total_col = next((c for c in df.columns if any(w in str(c) for w in ['סה"כ', 'סכום', 'Total'])), None)
            
            if total_col:
                # המרה למספר (ניקוי ₪ ופסיקים)
                df[total_col] = pd.to_numeric(df[total_col].astype(str).str.replace(',', '').str.replace('₪', '').str.replace(' ', ''), errors='coerce')
                
                c1, c2, c3 = st.columns(3)
                c1.metric("סה-כ מכירות", f"₪{df[total_col].sum():,.2f}")
                c2.metric("כמות עסקאות", len(df))
                c3.metric("ממוצע לעסקה", f"₪{df[total_col].mean():,.2f}")
            
            # הצגת הטבלה
            st.markdown("---")
            st.subheader("🔍 נתונים גולמיים מהאתר")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.warning("לא נמצאו נתונים להצגה. וודא שהחשבון מחובר ושיש מכירות בדוח.")

st.markdown("---")
st.caption("מקור נתונים: app.rnetpos.com | משתמש: Hasnew")
