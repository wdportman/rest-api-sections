import requests, os


class Mailgun:
    # MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    # MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)
    MAILGUN_API_KEY = 'key-842a1f8f1e0b9640ad5453c29f9d8c69'
    MAILGUN_DOMAIN = 'sandboxfa8e407562584713beb299a1a3320ad6.mailgun.org'

    @classmethod
    def send_email(cls, email, subject, text, html):
        if cls.MAILGUN_API_KEY is None or cls.MAILGUN_DOMAIN is None:
            raise EnvironmentError('Failed to load MailGun configurations.')
        return requests.post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={'from': f'{"Items-rest Service"} <do-not-reply@{cls.MAILGUN_DOMAIN}>',
                  'to': [email],
                  'subject': subject,
                  'text': text,
                  'html': html})
