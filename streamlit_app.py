import streamlit as st
import pandas as pd
import requests
import urllib3

# ביטול אזהרות אבטחה
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="RNET Auto-Controller", layout="wide")
st.title("🤖 השתלטות אוטומטית על נתוני RNET")

# פרטי הגישה שלך
USER = "Hasnew"
PASS = "hasnew123"
BASE_URL = "https://app.rnetpos.com"

def fetch_raw_sales():
    session = requests.Session()
    
    # הגדרות שגורמות לבוט להיראות כמו דפדפן אמיתי
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    })

    try:
        # 1. שלב ההתחברות (Login)
        login_payload = {"UserName": USER, "Password": PASS, "RememberMe": "false"}
        login_res = session.post(f"{BASE_URL}/Account/Login", data=login_payload, verify=False)
        
        if login_res.status_code != 200:
            st.error("ההתחברות לאתר נכשלה.")
            return None

        # 2. שלב "ההשתלטות" - בקשת הנתונים הגולמיים
        # אנחנו מנסים לפנות לנתיב שבו האתר שומר את נתוני המכירות הגולמיים
        # הערה: הנתיב הזה משתנה מאתר לאתר, זהו ניסיון לפי המבנה של RNET
        sales_api_url = f"{BASE_URL}/Sales/GetSalesList" 
        
        # פרמטרים של תאריכים (לפי מה שראינו בתמונה 03.05.2026)
        params = {
            'fromDate': '2026-05-01',
            'toDate': '2026-05-03',
            'branchId': '0' # 0 בדרך כלל אומר "כל הסניפים"
        }

        response = session.get(sales_api_url, params=params, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            # אם הנתונים הגיעו בפורמט JSON, נהפוך אותם לטבלה
            if 'data' in data:
                return pd.DataFrame(data['data'])
            return pd.DataFrame(data)
        else:
            st.error(f"האתר סירב למסור נתונים גולמיים. קוד שגיאה: {response.status_code}")
            return None

    except Exception as e:
        st.error(f"שגיאה בתקשורת: {e}")
        return None

if st.button("🚀 הפעל השתלטות ומשיכת נתונים"):
    with st.spinner("מבצע כניסה לאתר ושואב מכירות..."):
        df = fetch_raw_sales()
        
        if df is not None and not df.empty:
            st.success("הצלחתי! הנה נתוני המכירות הגולמיים:")
            st.dataframe(df)
        else:
            st.warning("הבוט נכנס לאתר אבל לא מצא טבלת מכירות.")
            st.info("באתרים מאובטחים כמו RNET, לפעמים חייבים להשתמש בדפדפן אמיתי (Playwright) שמותקן על המחשב שלך.")
