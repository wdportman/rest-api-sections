import requests, os


class Mailgun:
    # added for local testing:
    # os.environ.setdefault('MAILGUN_API_KEY', 'api_key')
    # os.environ.setdefault('MAILGUN_DOMAIN', 'domain name')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)

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
