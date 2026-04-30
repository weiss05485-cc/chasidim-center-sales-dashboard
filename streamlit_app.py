import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="RNET Dashboard", layout="wide")

st.title("📊 דאשבורד מכירות RNET")
st.markdown("---")

# כפתור העלאת קובץ
uploaded_file = st.file_uploader("העלה קובץ אקסל או CSV שייצאת מ-RNET", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    try:
        filename = uploaded_file.name.lower()
        
        # שלב קריאת הקובץ עם טיפול בבעיית העברית
        if filename.endswith('.csv'):
            try:
                # ניסיון ראשון: קידוד עברי סטנדרטי של חלונות
                df = pd.read_csv(uploaded_file, encoding='cp1255')
            except:
                # ניסיון שני: קידוד מודרני
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            # קריאת אקסל (XLS או XLSX)
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ הקובץ נטען בהצלחה!")
        
        # ניקוי רווחים משמות העמודות
        df.columns = df.columns.str.strip()

        # זיהוי עמודות סכום ותאריך באופן אוטומטי
        total_col = next((c for c in df.columns if 'סה"כ' in c or 'סכום' in c or 'Total' in c), None)
        date_col = next((c for c in df.columns if 'תאריך' in c or 'Date' in c), None)

        # תצוגת מדדים
        st.subheader("📊 סיכום כללי")
        m1, m2, m3 = st.columns(3)
        
        if total_col:
            total_val = pd.to_numeric(df[total_col], errors='coerce').sum()
            m1.metric("סה-כ מכירות", f"₪{total_val:,.2f}")
            m2.metric("כמות שורות בדוח", len(df))
            m3.metric("ממוצע לשורה", f"₪{(total_val/len(df)):,.2f}")

        # תצוגת גרף במידה ויש תאריך
        if date_col and total_col:
            st.markdown("---")
            st.subheader("📈 מגמת מכירות לאורך זמן")
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
            df = df.dropna(subset=[date_col])
            chart_data = df.groupby(date_col)[total_col].sum()
            st.line_chart(chart_data)

        # הצגת הטבלה
        with st.expander("לצפייה בנתונים הגולמיים"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"שגיאה בניתוח הקובץ: {e}")
        st.info("אם מדובר ב-CSV, וודא ששמרת אותו בקידוד עברי (Windows-1255).")
else:
    st.info("👋 המערכת מוכנה. ייצא דוח מהתוכנה של RNET והעלה אותו כאן.")
