import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="RNET Sales Analysis", layout="wide")

# עיצוב כותרת
st.title("📊 דאשבורד מכירות RNET")
st.markdown(f"**מקור הנתונים:** [app.rnetpos.com/sales](https://app.rnetpos.com/sales)")
st.info("הורד את הדוח מהאתר של RNET כקובץ Excel או CSV והעלה אותו כאן למטה.")

# כפתור העלאה
uploaded_file = st.file_uploader("בחר קובץ שייצאת מ-RNET", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    try:
        filename = uploaded_file.name.lower()
        
        # קריאת הקובץ
        if filename.endswith('.csv'):
            # טיפול בעברית של CSV
            try:
                df = pd.read_csv(uploaded_file, encoding='cp1255')
            except:
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            # קריאת אקסל ודילוג אוטומטי על שורות כותרת ריקות
            df = pd.read_excel(uploaded_file)
            for i in range(1, 10):
                if any(col for col in df.columns if not str(col).startswith('Unnamed')):
                    break
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file, skiprows=i)

        # ניקוי בסיסי
        df = df.dropna(how='all', axis=1)
        df.columns = df.columns.str.strip()

        # זיהוי עמודות (סכום ותאריך)
        total_col = next((c for c in df.columns if any(w in str(c) for w in ['סה"כ', 'סכום', 'Total'])), None)
        date_col = next((c for c in df.columns if any(w in str(c) for w in ['תאריך', 'Date'])), None)

        if total_col:
            # המרה למספר
            df[total_col] = pd.to_numeric(df[total_col].astype(str).str.replace(',', '').str.replace('₪', '').str.replace(' ', ''), errors='coerce')
            
            # תצוגת מדדים בראש הדף
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            total_sum = df[total_col].sum()
            
            with col1:
                st.metric("סה-כ מכירות", f"₪{total_sum:,.2f}")
            with col2:
                st.metric("כמות עסקאות", len(df))
            with col3:
                st.metric("ממוצע לעסקה", f"₪{(total_sum/len(df)):,.2f}" if len(df) > 0 else "0")

            # גרף מכירות
            if date_col:
                st.subheader("📈 מגמת מכירות")
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
                df = df.dropna(subset=[date_col, total_col])
                daily = df.groupby(date_col)[total_col].sum()
                st.line_chart(daily)

        # הצגת הטבלה
        with st.expander("👁️ לצפייה בנתונים הגולמיים"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"שגיאה בניתוח הקובץ: {e}")
else:
    st.write("---")
    st.markdown("### 💡 איך זה עובד?")
    st.write("1. כנס לכתובת של RNET.")
    st.write("2. בצע חיפוש/סינון של המכירות שאתה רוצה.")
    st.write("3. לחץ על כפתור הייצוא (Excel או CSV).")
    st.write("4. גרור את הקובץ לכאן ותקבל ניתוח מלא ברגע.")
