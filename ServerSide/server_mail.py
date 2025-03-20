import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
sys.path.append('.')
from DB_Connect import  pull_products_for_mail,delete_Size




def send_email(product,size,mail,name,price):
    sender_email = ""
    try:
        # Gmail SMTP sunucusuna bağlanma
        smtp_server = ""
        smtp_port = 587

        smtp_user = sender_email  # Gönderen e-posta adresi
        smtp_password = ""  # Uygulama şifresi

        # E-posta mesajını oluşturma
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = mail
        msg['Subject'] = f"Zarasify"

        round_price = round(price,2)
        body = f"Beklediğiniz {name} ürününün {size} bedeni {round_price}TL'ye mevcuttur. \n Link:  {product} \n\n"
        # E-posta içeriğini ekleyin
        msg.attach(MIMEText(body, 'plain'))
        
    
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Güvenli bağlantı
            server.login(smtp_user, smtp_password)  # Gmail hesabına giriş
            text = msg.as_string()  # E-posta mesajını string formatına çevirme
            server.sendmail(sender_email, mail, text)  # E-posta gönderme

        print(f"E-posta başarıyla gönderildi: {mail}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


# connectdb()

def start():
    print("Mail başladı")
    filtered = pull_products_for_mail()

    if filtered != []:
        for i in filtered:
            send_email(i[0],i[1],i[2],i[5],i[6])
            delete_Size(i[3],i[4])
            

    print(filtered)

# close_Connection()