import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(page_title="RNET Live Dashboard", layout="wide")
st.title("🚀 דאשבורד RNET - נתונים בזמן אמת")

# פרטי השרת
SERVER = '51.17.219.56'
DATABASE = 'HasidimNEW'
USERNAME = '780'
PASSWORD = '21060'

@st.cache_data(ttl=600)
def load_live_data():
    # בלינוקס (Streamlit Cloud) משתמשים בדרייבר FreeTDS או ODBC Driver 17/18
    # ננסה את הפורמט הכי נפוץ שעובד ב-Cloud
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
        f'Timeout=30;'
    )
    
    conn = pyodbc.connect(conn_str)
    # נסה למשוך נתונים מטבלת המכירות (כאן צריך לוודא את שם הטבלה המדויק ב-RNET)
    query = "SELECT TOP 100 * FROM Sales" 
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    with st.spinner('מנסה להתחבר לבסיס הנתונים של RNET...'):
        df = load_live_data()
    
    st.success("✅ מחובר בהצלחה!")
    st.dataframe(df)

except Exception as e:
    st.error(f"לא הצלחתי להתחבר ישירות לשרת: {e}")
    st.info("💡 טיפ: אם מופיעה שגיאת Timeout, ייתכן שהשרת שלכם חוסם חיבורים מחו-ל.")
