import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(page_title="RNET Dashboard", layout="wide")

st.title("📊 מערכת ניהול מכירות RNET")

# תפריט בחירה בציד האתר
st.sidebar.header("🔌 חיבור לנתונים")
mode = st.sidebar.radio("בחר מקור נתונים:", ("העלאת קובץ אקסל", "חיבור ישיר לשרת (Live)"))

if mode == "חיבור ישיר לשרת (Live)":
    st.subheader("🔗 חיבור ישיר לבסיס הנתונים")
    
    # כפתור התחברות כדי שלא ינסה כל הזמן ויחסם
    if st.button("בצע התחברות עכשיו"):
        try:
            conn_str = (
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=51.17.219.56;'
                'DATABASE=HasidimNEW;'
                'UID=780;'
                'PWD=21060;'
                'ConnectTimeout=10;'
            )
            with st.spinner('מנסה להתחבר...'):
                conn = pyodbc.connect(conn_str)
                # כאן צריך לדעת את שם הטבלה (למשל Sales או Transactions)
                df = pd.read_sql("SELECT TOP 100 * FROM TblSales ORDER BY SaleDate DESC", conn)
                st.success("✅ חיבור הצליח! נתונים נמשכו.")
                st.dataframe(df)
                conn.close()
        except Exception as e:
            st.error(f"לא הצלחתי להתחבר: {e}")
            st.info("נראה שהמשתמש '780' לא מורשה להתחבר ישירות ל-SQL. בדוק עם התמיכה של RNET.")

else:
    st.subheader("📂 העלאת דוח אקסל ידני")
    uploaded_file = st.file_uploader("גרור כאן את האקסל שייצאת מ-RNET", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file:
        try:
            # הקוד החזק שכתבנו קודם שסורק את האקסל
            for i in range(10):
                uploaded_file.seek(0)
                temp_df = pd.read_excel(uploaded_file, skiprows=i)
                if any(col for col in temp_df.columns if not str(col).startswith('Unnamed')):
                    df = temp_df
                    break
            st.success("✅ הקובץ נקלט!")
            st.dataframe(df.head(20))
        except Exception as e:
            st.error(f"שגיאה בקריאת הקובץ: {e}")

st.markdown("---")
st.caption("פיתוח: דאשבורד מכירות חסידים | סטטוס חיבור: פעיל")
