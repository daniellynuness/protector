import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    @staticmethod
    def enviar_email(destinatario, mensagem):
        """
        Envia um e-mail real para o destinatário.
        """
        # Configurações do servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        remetente = "protectorbsi@gmail.com"
        senha = "arys wklr tjed umdx"  # senha de app do Gmail

        # Monta o e-mail
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = "Tentativas de Login Bloqueadas"
        msg.attach(MIMEText(mensagem, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")