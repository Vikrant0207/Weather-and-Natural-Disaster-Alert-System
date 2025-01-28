import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# Constants
OPENWEATHER_API_KEY = "NA"           #Enter openweather api key   
TWILIO_ACCOUNT_SID = "NA"            #Enter twilio account sid       
TWILIO_AUTH_TOKEN = "NA"             #Enter twilio authentication token      
FROM_PHONE = "NA"                    #Enter the developer's temp number                                
TO_PHONE = "NA"                      #Enter twilio registered phone number to receive alert                         
SMTP_SERVER = "smtp.gmail.com"                                     
EMAIL_PORT = 587
EMAIL_ADDRESS = "NA"                 #Enter twilio registered  email to receive email alerts      
EMAIL_PASSWORD = "NA"                                   

# Fetch weather data
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

# Analyze weather and set alerts
def analyze_weather(data):
    alerts = []
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']

    if "rain" in weather or "storm" in weather:
        alerts.append("Heavy rain or storm detected! FLOOD ALERT!!!")
    if wind_speed > 20:  # Adjust threshold for your needs
        alerts.append(f"High wind speed detected: {wind_speed} m/s! CYCLONE ALERT!!")
    if temp < 0:
        alerts.append("Freezing temperature detected! AVALANCHE ALERT!!!")
    if temp > 30:
        alerts.append("Heatwave conditions detected! FIRE ALERT!!!")

    return alerts

# Send email alert
def send_email_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Or a recipient email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()
        print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Send SMS alert (optional)
def send_sms_alert(body):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=FROM_PHONE,
            to=TO_PHONE
        )
        print(f"SMS alert sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Main function
def main():
    city = input("Enter your city: ")
    try:
        weather_data = fetch_weather_data(city)
        alerts = analyze_weather(weather_data)

        if alerts:
            alert_message = "\n".join(alerts)
            print("Alerts:")
            print(alert_message)
            send_email_alert("Weather Alert", alert_message)
            send_sms_alert(alert_message)  # Uncomment if using Twilio
        else:
            print("No significant weather alerts.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
