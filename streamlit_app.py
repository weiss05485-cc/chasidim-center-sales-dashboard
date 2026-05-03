import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup # ספרייה לקריאת תוכן של דפי אינטרנט
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="RNET Dashboard", layout="wide")
st.title("📊 דאשבורד מכירות RNET (נתוני מסך)")

# פרטי הגישה
USER = "Hasnew"
PASS = "hasnew123"
BASE_URL = "https://app.rnetpos.com"

def scrape_rnet_screen():
    session = requests.Session()
    login_url = f"{BASE_URL}/Account/Login"
    sales_url = f"{BASE_URL}/sales" # הדף שרואים בתמונה
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    login_data = { "UserName": USER, "Password": PASS, "RememberMe": "false" }
    
    try:
        # 1. התחברות
        session.post(login_url, data=login_data, headers=headers, verify=False, timeout=20)
        
        # 2. כניסה לדף המכירות
        res = session.get(sales_url, headers=headers, verify=False, timeout=20)
        
        # 3. ניתוח דף ה-HTML (Scraping)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # חיפוש כל הנתונים שמופיעים ברשימה בתמונה
        data_points = {}
        
        # אנחנו מחפשים שורות שמכילות טקסט ומספרים עם סימן ₪
        # הקוד הזה סורק את כל ה"אלמנטים" בדף ומחפש התאמות
        for item in soup.find_all(['div', 'span', 'li']):
            text = item.get_text().strip()
            if "₪" in text:
                # ניקוי הטקסט כדי להפריד בין השם (למשל 'בני ברק') למספר
                clean_text = text.replace('₪', '').strip()
                # ננסה למצוא את התווית שקרובה למספר הזה
                parent_text = item.parent.get_text()
                
                if "בני ברק" in parent_text: data_points["בני ברק"] = clean_text
                if "ירושלים" in parent_text: data_points["ירושלים"] = clean_text
                if 'ס"כ מכירות' in parent_text: data_points['ס"כ מכירות'] = clean_text
                if "עסקה ממוצעת" in parent_text or "ממוצעת" in parent_text: data_points["ממוצע"] = clean_text

        return data_points
    except Exception as e:
        st.error(f"שגיאה בשליפת נתוני מסך: {e}")
        return None

if st.button("🔄 עדכן נתונים מהמסך"):
    results = scrape_rnet_screen()
    
    if results:
        st.success("הנתונים נשלפו מהאתר!")
        
        # תצוגה יפה של הנתונים מהתמונה
        col1, col2, col3 = st.columns(3)
        
        col1.metric("סך מכירות", f"₪{results.get('ס\"כ מכירות', '0')}")
        col2.metric("בני ברק", f"₪{results.get('בני ברק', '0')}")
        col3.metric("ירושלים", f"₪{results.get('ירושלים', '0')}")
        
        # הצגת הטבלה המלאה של מה שמצאנו
        st.write("### פירוט מלא:")
        st.json(results)
    else:
        st.warning("לא הצלחתי למצוא את הנתונים בדף. וודא שהאתר פתוח ומציג נתונים.")
