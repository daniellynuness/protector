import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    """
    Classe para enviar e-mails sobre tentativas de login bloqueadas.
    Esta classe utiliza o servidor SMTP do Gmail para enviar e-mails.
    """
    @staticmethod
    def enviar_email(destinatario, mensagem):
        """
        Envia um e-mail de notificação sobre tentativas de login bloqueadas.
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