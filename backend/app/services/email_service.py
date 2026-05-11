import resend
from app.core.config import get_settings

class EmailService:
    def __init__(self):
        settings = get_settings()
        resend.api_key = settings.RESEND_API_KEY
        self.mail_from = settings.MAIL_FROM
        self.frontend_url = settings.FRONTEND_URL

    def send_password_reset_email(self, email: str, token: str):
        reset_link = f"{self.frontend_url}/reset-password?token={token}"
        
        html_content = f"""
        <html>
            <body style="font-family: sans-serif; color: #1a2e1a;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 16px;">
                    <h2 style="color: #2d4a2d;">Recuperar contraseña</h2>
                    <p>Hola,</p>
                    <p>Has solicitado restablecer tu contraseña en <strong>Creciendo App</strong>. Haz clic en el botón de abajo para continuar:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" style="background-color: #2d4a2d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 12px; font-weight: bold; display: inline-block;">
                            Restablecer contraseña
                        </a>
                    </div>
                    <p style="font-size: 0.8em; color: #666;">Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 0.8em; color: #999;">Este enlace expirará en 1 hora.</p>
                </div>
            </body>
        </html>
        """
        
        try:
            params = {
                "from": self.mail_from,
                "to": [email],
                "subject": "Restablecer tu contraseña - Creciendo App",
                "html": html_content,
            }
            resend.Emails.send(params)
        except Exception as e:
            # En producción, usarías un logger aquí
            print(f"Error enviando correo: {e}")
            raise ValueError("No se pudo enviar el correo de recuperación.")
