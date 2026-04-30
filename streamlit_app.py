import streamlit as st
import pandas as pd
import io

# הגדרות דף
st.set_page_config(page_title="RNET Sales Dashboard", layout="wide")

st.title("📊 דאשבורד מכירות RNET")
st.markdown("---")

# כפתור העלאת קובץ - תומך בכל הפורמטים ש-RNET מוציאה
uploaded_file = st.file_uploader("העלה את הקובץ שייצאת מ-RNET (Excel או CSV)", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    try:
        # בדיקת סוג הקובץ וקריאה בהתאם
        filename = uploaded_file.name.lower()
        
        if filename.endswith('.csv'):
            # ניסיון קריאה של CSV עם קידוד עברית נפוץ בתוכנות ישנות
            df = pd.read_csv(uploaded_file, encoding='cp1255')
        elif filename.endswith('.xls'):
            # קריאת אקסל ישן (דורש xlrd שבדרך כלל מותקן בסטנדרט של Streamlit)
            df = pd.read_excel(uploaded_file)
        else:
            # קריאת אקסל חדש
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ הקובץ '{filename}' נטען בהצלחה!")
        st.markdown("---")

        # ניקוי שמות העמודות (הסרת רווחים מיותרים)
        df.columns = df.columns.str.strip()

        # תצוגת מדדים מרכזיים (KPI)
        # ננסה למצוא עמודת 'סה"כ' או 'סכום'
        total_col = next((c for c in df.columns if 'סה"כ' in c or 'סכום' in c), None)
        date_col = next((c for c in df.columns if 'תאריך' in c), None)

        col1, col2, col3 = st.columns(3)
        
        if total_col:
            total_sales = df[total_col].sum()
            with col1:
                st.metric("סה-כ מכירות", f"₪{total_sales:,.2f}")
            with col2:
                st.metric("כמות עסקאות", len(df))
            with col3:
                avg_sale = df[total_col].mean()
                st.metric("ממוצע לעסקה", f"₪{avg_sale:,.2f}")

        # תצוגת גרף מכירות לפי תאריך (אם קיים)
        if date_col and total_col:
            st.subheader("📈 מגמת מכירות")
            # המרת תאריך לפורמט תקין
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
            sales_by_date = df.groupby(date_col)[total_col].sum()
            st.line_chart(sales_by_date)

        # הצגת הטבלה המלאה בסוף
        with st.expander("לצפייה בנתונים הגולמיים"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"שגיאה בניתוח הקובץ: {e}")
        st.info("טיפ: אם האקסל לא נטען, נסה לשמור אותו במחשב כ-CSV ולהעלות שוב.")

else:
    st.info("👋 ברוך הבא! ייצא דוח מכירות מ-RNET והעלה אותו כאן כדי לראות את הנתונים.")
