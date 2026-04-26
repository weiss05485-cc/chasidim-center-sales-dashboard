def fetch_sales(username, password):
    # שורה זו משתיקה את האזהרה המציקה שתופיע בגלל ביטול ה-SSL
    requests.packages.urllib3.disable_warnings()
    
    session = requests.Session()
    login_url = "https://app.rnetpos.com/Account/Login"
    
    try:
        # 1. קבלת דף הכניסה וה-Token (הוספנו verify=False)
        r = session.get(login_url, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_element = soup.find('input', {'name': '__RequestVerificationToken'})
        
        if not token_element:
            return None, "לא ניתן היה למצוא טוקן אבטחה בדף."
            
        token = token_element['value']
        
        # 2. התחברות (הוספנו verify=False)
        payload = {
            "UserName": username,
            "Password": password,
            "__RequestVerificationToken": token,
            "RememberMe": "false"
        }
        
        login_response = session.post(login_url, data=payload, verify=False)
        
        if "Login" in login_response.url:
            return None, "שם משתמש או סיסמה שגויים."

        # 3. משיכת דף המכירות (הוספנו verify=False)
        sales_r = session.get("https://app.rnetpos.com/sales", verify=False)
        return sales_r.text, "success"
        
    except Exception as e:
        return None, f"שגיאה טכנית: {str(e)}"
