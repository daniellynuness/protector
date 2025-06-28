class EmailService:
    @staticmethod
    def enviar_email(destinatario, mensagem):
        """
        Simula o envio de um e-mail para o destinatário.
        """
        print("\n=== Simulação de Envio de E-mail ===")
        print(f"Para: {destinatario}")
        print(f"Assunto: Tentativas de Login Bloqueadas")
        print(f"Mensagem: {mensagem}")