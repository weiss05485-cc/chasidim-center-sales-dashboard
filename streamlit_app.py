import streamlit as st
import pandas as pd
import pyodbc # ספריה לחיבור למסדי נתונים

st.set_page_config(page_title="RNET Live Dashboard", layout="wide")
st.title("🚀 דאשבורד RNET - נתונים בזמן אמת")

# פרטי השרת מהתמונה והמשתמש שנתת
SERVER = '51.17.219.56'
DATABASE = 'HasidimNEW' # מהתמונה image_e5382b.png
USERNAME = '780'
PASSWORD = '21060'

@st.cache_data(ttl=600) # מרענן נתונים כל 10 דקות
def load_live_data():
    # מחרוזת התחברות ל-SQL Server
    conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    
    # שאילתת SQL למשיכת מכירות (דוגמה, צריך לוודא שמות טבלאות מול RNET)
    query = "SELECT * FROM SalesTable WHERE SaleDate >= CAST(GETDATE() AS DATE)" 
    
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    with st.spinner('מתחבר לשרת RNET...'):
        df = load_live_data()
    
    st.success("✅ מחובר לנתונים חיים!")
    
    # כאן נשים את הגרפים והמדדים שבנינו קודם
    st.metric("מכירות היום", len(df))
    st.dataframe(df)

except Exception as e:
    st.error(f"לא הצלחתי להתחבר ישירות לשרת: {e}")
    st.info("ייתכן שהשרת חסום לחיבורים חיצוניים. בינתיים אפשר להמשיך עם העלאת אקסלים.")
