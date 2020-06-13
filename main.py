import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template
from pathlib import Path

def get_data():
    try:
        page = requests.get("https://rate.bot.com.tw/xrt/quote/ltm/USD", timeout=5)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        raw_data = soup.select("tbody tr")[:4]
        return [(e.get_text().split("\n")[1], float(e.get_text().split("\n")[4])) for e in raw_data]

    except requests.exceptions.HTTPError as e: 
            print ("HTTP Error:", e) 

    except requests.exceptions.ConnectionError as e: 
            print ("Error Connecting:", e) 

    except requests.exceptions.Timeout as e: 
            print ("Timeout Error:", e) 

    except requests.exceptions.RequestException as e:
        print ("Request exception: ", e)

def analyze_data(data):
    for i in range(1, len(data)):
        if data[i-1][1] > data[i][1]:
            return False
    return True 
    
def send_notification():
    with open("secret.txt", "r") as rf:
        fr,to,password = rf.readlines()

        content = MIMEMultipart()
        content["subject"] = "$$$ Dollar goes down! $$$"
        content["from"] = fr.replace("\n", "")
        content["to"] = to.replace("\n", "")
        body = Template(Path("email.html").read_text())
        content.attach(MIMEText(body.substitute({"user": "Alvin"}), "html"))

        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(fr.replace("\n", ""), password.replace("\n", ""))
                smtp.send_message(content)
                print("sent")
            
            except Exception as e:
                print("Error message: ", e)
    

# if analyze_data(get_data()):
#     send_notification()

send_notification()