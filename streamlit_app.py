import streamlit as st
import pandas as pd

# הגדרות דף רחב
st.set_page_config(page_title="RNET Sales Dashboard", layout="wide")

st.title("📊 דאשבורד מכירות RNET - גרסה מלאה")
st.markdown("---")

# כפתור העלאת קובץ
uploaded_file = st.file_uploader("העלה קובץ אקסל או CSV שייצאת מ-RNET", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    try:
        filename = uploaded_file.name.lower()
        df = None

        # לוגיקה לקריאת הקובץ
        if filename.endswith('.csv'):
            # ניסיון קריאה של CSV עם מפרידים שונים וקידוד עברי (cp1255)
            for separator in [',', ';', '\t']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='cp1255', sep=separator)
                    if len(df.columns) > 1:
                        break
                except:
                    continue
        else:
            # קריאת אקסל - מנגנון דילוג על שורות ריקות (skiprows)
            # אנחנו סורקים את 10 השורות הראשונות כדי למצוא את הכותרות
            for i in range(10):
                uploaded_file.seek(0)
                temp_df = pd.read_excel(uploaded_file, skiprows=i)
                # אם מצאנו עמודה שהיא לא "Unnamed", סימן שהגענו לכותרות
                if any(col for col in temp_df.columns if not str(col).startswith('Unnamed')):
                    df = temp_df
                    break

        if df is not None:
            # ניקוי עמודות ריקות ורווחים בשמות
            df = df.dropna(how='all', axis=1)
            df.columns = df.columns.str.strip()

            st.success(f"✅ הקובץ '{filename}' עובד! נמצאו {len(df)} שורות.")

            # זיהוי עמודות (סה"כ ותאריך) - מחפש שמות נפוצים ב-RNET
            total_col = next((c for c in df.columns if any(word in str(c) for word in ['סה"כ', 'סכום', 'ברוטו', 'Total'])), None)
            date_col = next((c for c in df.columns if any(word in str(c) for word in ['תאריך', 'Date'])), None)

            # תצוגת מדדים (KPI)
            st.subheader("📌 נתונים מרכזיים")
            m1, m2, m3 = st.columns(3)
            
            if total_col:
                # ניקוי פורמט כספי (הסרת ₪ ופסיקים) והמרה למספר
                df[total_col] = pd.to_numeric(df[total_col].astype(str).str.replace(',', '').str.replace('₪', '').str.replace(' ', ''), errors='coerce')
                total_val = df[total_col].sum()
                m1.metric("סה-כ מכירות", f"₪{total_val:,.2f}")
                m2.metric("כמות עסקאות", len(df))
                m3.metric("ממוצע לעסקה", f"₪{(total_val/len(df)):,.2f}" if len(df)>0 else "0")
            else:
                st.warning("⚠️ לא מצאתי עמודת 'סה-כ'. וודא שהכותרות בטבלה למטה תקינות.")

            # גרף מכירות יומי
            if date_col and total_col:
                st.markdown("---")
                st.subheader("📈 מגמת מכירות")
                # המרה לתאריך עם תמיכה בפורמט ישראלי (יום ראשון)
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
                df = df.dropna(subset=[date_col, total_col])
                daily_sales = df.groupby(date_col)[total_col].sum()
                st.line_chart(daily_sales)

            # הצגת הטבלה המלאה לעיון
            with st.expander("👁️ לצפייה בטבלה המלאה (כדי לוודא שהכותרות זוהו)"):
                st.dataframe(df, use_container_width=True)
        else:
            st.error("❌ לא הצלחתי למצוא טבלה תקינה בקובץ. נסה לשמור אותו כ-Excel רגיל.")

    except Exception as e:
        st.error(f"🔥 שגיאה בניתוח הקובץ: {e}")
else:
    st.info("👋 מחכה לקובץ שלך. ייצא דוח מ-RNET (עדיף באקסל) והעלה אותו כאן.")
