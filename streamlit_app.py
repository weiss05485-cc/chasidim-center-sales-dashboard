import streamlit as st
import pandas as pd

# הגדרות דף רחב
st.set_page_config(page_title="RNET Dashboard", layout="wide")

st.title("📊 דאשבורד מכירות RNET")
st.markdown("---")

# כפתור העלאת קובץ
uploaded_file = st.file_uploader("העלה קובץ אקסל או CSV שייצאת מ-RNET", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    try:
        filename = uploaded_file.name.lower()
        df = None

        # לוגיקה לקריאת הקובץ לפי סוג וקידוד
        if filename.endswith('.csv'):
            # ניסיון קריאה של CSV עם מפרידים שונים וקידוד עברי
            for separator in [',', ';', '\t']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='cp1255', sep=separator)
                    if len(df.columns) > 1: # אם זיהה יותר מעמודה אחת, זה המפריד הנכון
                        break
                except:
                    continue
            
            # אם עדיין לא הצליח, ניסיון אחרון עם UTF-8
            if df is None or len(df.columns) <= 1:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            # קריאת אקסל (תומך ב-XLS ו-XLSX)
            df = pd.read_excel(uploaded_file)

        if df is not None:
            # ניקוי עמודות ריקות ורווחים
            df = df.dropna(how='all', axis=1)
            df.columns = df.columns.str.strip()

            st.success(f"✅ הקובץ נטען בהצלחה! נמצאו {len(df)} שורות.")

            # זיהוי עמודות (סה"כ ותאריך)
            total_col = next((c for c in df.columns if 'סה"כ' in c or 'סכום' in c or 'Total' in c), None)
            date_col = next((c for c in df.columns if 'תאריך' in c or 'Date' in c), None)

            # תצוגת מדדים (KPI)
            st.subheader("📌 נתונים מרכזיים")
            m1, m2, m3 = st.columns(3)
            
            if total_col:
                # המרה למספר (למקרה שיש פסיקים או שקלים בטקסט)
                df[total_col] = pd.to_numeric(df[total_col].astype(str).str.replace(',', '').str.replace('₪', ''), errors='coerce')
                total_val = df[total_col].sum()
                m1.metric("סה-כ מכירות", f"₪{total_val:,.2f}")
                m2.metric("כמות עסקאות", len(df))
                m3.metric("ממוצע לעסקה", f"₪{(total_val/len(df)):,.2f}" if len(df)>0 else "0")

            # גרף מכירות
            if date_col and total_col:
                st.markdown("---")
                st.subheader("📈 גרף מכירות יומי")
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
                df = df.dropna(subset=[date_col])
                daily_sales = df.groupby(date_col)[total_col].sum()
                st.line_chart(daily_sales)

            # הצגת הטבלה
            with st.expander("👁️ צפייה בנתונים הגולמיים"):
                st.dataframe(df, use_container_width=True)
        else:
            st.error("לא הצלחנו לקרוא נתונים מהקובץ. נסה לשמור אותו כ-Excel רגיל.")

    except Exception as e:
        st.error(f"שגיאה בניתוח הקובץ: {e}")
else:
    st.info("👋 המערכת מחכה לקובץ. ייצא דוח מ-RNET והעלה אותו כאן.")
