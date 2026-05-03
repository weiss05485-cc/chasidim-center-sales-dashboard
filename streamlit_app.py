import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="RNET Cloud Automation", layout="wide")

# הגדרות
USER = "Hasnew"
PASS = "hasnew123"
# כאן תכניס את המפתח שתקבל מ-browserless
BROWSERLESS_TOKEN = "כאן_שמים_את_המפתח" 

st.title("🤖 השתלטות ענן אוטומטית (RNET)")

def fetch_data_via_cloud_browser():
    # פקודת "השתלטות" שנשלחת לדפדפן מרוחק
    # הקוד הזה אומר לדפדפן בענן: כנס, תתחבר, ותביא לי את הטבלה
    logic = f"""
    async ({{ page }}) => {{
        await page.goto('https://app.rnetpos.com/Account/Login');
        await page.fill('input[name="UserName"]', '{USER}');
        await page.fill('input[name="Password"]', '{PASS}');
        await page.click('button[type="submit"]');
        await page.waitForNavigation();
        
        await page.goto('https://app.rnetpos.com/sales');
        await page.waitForTimeout(5000); // מחכה שהנתונים יטענו
        
        // מושך את הנתונים מהטבלה שעל המסך
        const data = await page.evaluate(() => {{
            const rows = Array.from(document.querySelectorAll('table tr'));
            return rows.map(row => {{
                const columns = row.querySelectorAll('td');
                return Array.from(columns).map(column => column.innerText);
            }});
        }});
        return data;
    }}
    """
    
    url = f"https://production-sfo.browserless.io/function?token={BROWSERLESS_TOKEN}"
    response = requests.post(url, json={"code": logic}, headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

if st.button("🚀 הפעל השתלטות מהענן"):
    if BROWSERLESS_TOKEN == "כאן_שמים_את_המפתח":
        st.warning("עליך להירשם ל-Browserless ולשים את המפתח בקוד.")
    else:
        with st.spinner("דפדפן מרוחק משתלט על RNET..."):
            raw_data = fetch_data_via_cloud_browser()
            if raw_data:
                df = pd.DataFrame(raw_data)
                st.success("הנתונים נשאבו בהצלחה!")
                st.dataframe(df)
            else:
                st.error("ההשתלטות נכשלה. ייתכן והאתר שינה את מבנה הדף.")

st.info("💡 פתרון זה משתמש בדפדפן חיצוני בענן, כך שאין צורך להתקין כלום על המחשב שלך.")
