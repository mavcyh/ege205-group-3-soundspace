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

def send_confirmation_booking_email(temporary_password, start_datetime, end_datetime, instrument_names, recipient):
    
    subject = "SoundSpace Booking Details"
    
    instruments_booked_html = ""
    instruments_booked_plaintext = ""
    if len(instrument_names) == 0:
        instruments_booked_html = '<p style="font-size: 15px">None</p>'
        instruments_booked_plaintext = "None"
    else:
        for instrument_name in instrument_names:
            instruments_booked_html += f'<p style="font-size: 15px">{instrument_name}</p>\n'
            instruments_booked_plaintext += f"{instrument_name}\n"
    
    html = f"""\
    <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <!--[if mso]>
    <noscript>
        <xml>
        <o:OfficeDocumentSettings>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style>
        table, td, div, h1, p {{font-family: Arial, sans-serif;}}
    </style>
    </head>
    <body style="margin:0;padding:0;">
    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:white;">
        <tr>
        <td align="center" style="padding:0;">
            <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
            <tr>
                <td align="left" style="background:#ffffff;"> 
                <img src="cid:logo" alt="soundspace_logo" width="250" style="height:auto;display:block;margin:auto;padding:50px 0 20px;" />
                </td>
            </tr>
            <tr>
                <td>
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                    <td>
                        <h1 style="text-align:center;font-size:28px;color:rgb(241, 150, 86);padding-bottom:10px;">Thank you for booking with us!</h1>
                        <p style="font-size:14px;text-align:center;">Please use the following <span style="font-weight:bold;">temporary password</span><br>during your session to unlock the <span style="font-weight:bold;">music studio:</span></p>
                    </td>
                    </tr>
                    <tr>
                    <td>
                        <p style="text-align:center;font-weight:bold;font-size:50px;">{temporary_password}</p>
                    </td>
                    </tr>
                    <tr style="text-align:center;">
                        <td>
                            <h2>Order Summary</h2>
                            <p style="font-size:15px;padding-left:40px;padding-right:40px;">Thank you for booking with SoundSpace!<br>Below are the details of your booking:</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:15px;display:inline-block;margin-right:20px;"><span style="font-weight:bold;">Start Datetime: </span>{start_datetime}</p>
                            <p style="font-size:15px;display:inline-block;margin-left:20px;"><span style="font-weight:bold;">End Datetime: </span>{end_datetime}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="text-align:center;padding-bottom:20px;">
                            <p><b>Instruments booked:</b></p>
                            {instruments_booked_html}
                        </td>
                    </tr>
                </table>
                </td>
            </tr>
            <tr>
                <td style="padding:20px 30px;background:black">
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                    <td style="padding:0;" align="left">
                        <p style="margin:0;font-size:12px;font-family:Arial,sans-serif;color:white">
                        &copy; SoundSpace 2024. All rights reserved.
                        </p>
                    </td>                
                    </tr>
                </table>
                </td>
            </tr>
            </table>
        </td>
        </tr>
    </table>
    </body>
    </html>
    """
    
    images = [["logo", "src/assets/soundspace-logo.jpg"]]
    
    plaintext = f"""\
    Thank you for booking with SoundSpace!
    Please use the following temporary password during your session to unlock the music studio: {temporary_password}
    
    Start Datetime: {start_datetime}
    End Datetime: {end_datetime}
    
    Instruments booked:
    {instruments_booked_plaintext}
    """
    
    send_email(subject, html, images, plaintext, recipient)