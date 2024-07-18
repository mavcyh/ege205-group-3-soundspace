from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib, ssl

context = ssl.create_default_context()

def send_email(subject, html, images, plaintext, recipient):
    sender = "ege205.group.3.soundspace@gmail.com"
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(plaintext, "plain"))
    alternative.attach(MIMEText(html, "html"))
    msg.attach(alternative)
    
    for image_data in images:
        image_cid = image_data[0]
        image_path = image_data[1]
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name=image_path) 
            image.add_header('Content-ID', f"<{image_cid}>")
            image.add_header('Content-Disposition', 'inline', filename=image_path)
            file_extension = image_path.split(".")[-1]
            if file_extension == "jpg" or file_extension == "jpeg":
                image.add_header('Content-Type', 'image/jpeg')
            elif file_extension == "png":
                image.add_header('Content-Type', 'image/png')
            elif file_extension == "bmp":
                image.add_header('Content-Type', 'image/bmp')
            elif file_extension == "svg":
                image.add_header('Content-Type', 'image/svg+xml')
            msg.attach(image)
            
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp_server:
        smtp_server.login(sender, "ckuujfhqvoibxbkj")
        smtp_server.sendmail(sender, recipient, msg.as_string())