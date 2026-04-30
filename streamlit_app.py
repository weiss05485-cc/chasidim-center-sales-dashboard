import streamlit as st
import pandas as pd

st.set_page_config(page_title="RNET Dashboard", layout="wide")
st.title("📊 דאשבורד מכירות RNET - העלאת קובץ")

# כפתור להעלאת הקובץ שייצאת מהתוכנה
uploaded_file = st.file_uploader("גרור לכאן את קובץ האקסל שייצאת מ-RNET", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        # קריאת האקסל
        df = pd.read_excel(uploaded_file)
        
        st.success("✅ הקובץ נטען בהצלחה!")
        
        # תצוגת נתונים בסיסית (לפי העמודות שראינו בתוכנה)
        st.subheader("סיכום נתונים מהיר:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("סה-כ מכירות (ברוטו)", f"₪{df['סה-כ'].sum():,.2f}")
        with col2:
            st.metric("כמות עסקאות", len(df))
        with col3:
            st.metric("ממוצע לעסקה", f"₪{df['סה-כ'].mean():,.2f}")

        # גרף מכירות לפי תאריך
        st.line_chart(df.set_index('תאריך')['סה-כ'])
        
    except Exception as e:
        st.error(f"שגיאה בניתוח הקובץ: {e}. וודא שזה הקובץ המקורי שייצאת מהתוכנה.")
else:
    st.info("אנא ייצא את הדוח מהתוכנה (אייקון האקסל) והעלה אותו לכאן.")
