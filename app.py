from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']
        email = request.form['email']

        num = number[1:] if number.startswith('011') else number
        credentials = f"{email}:{password}"
        auth = base64.b64encode(credentials.encode()).decode()
        xauth = f"Basic {auth}"

        url = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"
        headers = {
            "applicationVersion": "2",
            "applicationName": "MAB",
            "Accept": "text/xml",
            "Authorization": xauth,
            "APP-BuildNumber": "964",
            "APP-Version": "27.0.0",
            "OS-Type": "Android",
            "OS-Version": "12",
            "APP-STORE": "GOOGLE",
            "Is-Corporate": "false",
            "Content-Type": "text/xml; charset=UTF-8",
            "User-Agent": "okhttp/5.0.0-alpha.11",
            "ADRUM_1": "isMobile:true",
            "ADRUM": "isAjax:true",
            "Host": "mab.etisalat.com.eg:11003"
        }

        data = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
        <loginRequest>
            <deviceId>1234567890</deviceId>
            <firstLoginAttempt>true</firstLoginAttempt>
            <modelType>Android</modelType>
            <osVersion>12</osVersion>
            <platform>Android</platform>
            <udid>abcdef123456</udid>
        </loginRequest>"""

        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            if "true" in response.text.lower():
                cookie = response.headers.get("Set-Cookie", "").split(";")[0]
                bearer = response.headers.get("auth", "")

                redeem_url = 'https://mab.etisalat.com.eg:11003/Saytar/rest/servicemanagement/submitOrderV2'
                redeem_headers = {
                    'applicationVersion': '2',
                    'applicationName': 'MAB',
                    'Accept': 'text/xml',
                    'Cookie': cookie,
                    'Language': 'ar',
                    'APP-BuildNumber': '10493',
                    'APP-Version': '30.1.0',
                    'OS-Type': 'Android',
                    'OS-Version': '7.1.2',
                    'APP-STORE': 'GOOGLE',
                    'auth': "Bearer " + bearer,
                    'Is-Corporate': 'false',
                    'Content-Type': 'text/xml; charset=UTF-8',
                    'User-Agent': 'okhttp/5.0.0-alpha.11',
                    'ADRUM_1': 'isMobile:true',
                    'ADRUM': 'isAjax:true',
                    'Host': 'mab.etisalat.com.eg:11003'
                }

                redeem_data = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
                <submitOrderRequest>
                    <mabOperation></mabOperation>
                    <msisdn>{num}</msisdn>
                    <operation>REDEEM</operation>
                    <productName>DOWNLOAD_GIFT_1_SOCIAL_UNITS</productName>
                </submitOrderRequest>"""

                redeem_response = requests.post(redeem_url, headers=redeem_headers, data=redeem_data, timeout=10)

                if "true" in redeem_response.text.lower():
                    result = " تم إضافة 500 ميجا"
                else:
                    result = "تم تسجيل الدخول، لكن فشل تفعيل الهدية"
            else:
                result = "فشل تسجيل الدخول. تحقق من البيانات."
        except Exception as e:
            result = f"حدث خطأ: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)