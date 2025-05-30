import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

referent = os.getenv('REF')
addressee = os.getenv('ADD')
password = os.getenv('PASS')
subject = 'Relatório de pedidos'
body = 'Segue em anexo o relatório de pedidos'

msg = EmailMessage()
msg['From'] = referent
msg['To'] = addressee
msg['Subject'] = subject
msg.set_content(body)

files = [
    'deliveries_avg.xlsx',
    'deliveries_count.xlsx',
]

for file in files:
    with open(f'excel/files/{file}', 'rb') as f:
        content = f.read()
        msg.add_attachment(
            content,
            maintype='application', 
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            filename=file
        )

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(referent, password)
    smtp.send_message(msg)

print('Email enviado com sucesso!')
