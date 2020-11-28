import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent
import config

class Mailer:
    def __init__(self):
        self.__sg = SendGridAPIClient(config.send_grid_api_key)

    def send_email_base(self, from_email, to_emails, subject, html_content):
        message = Mail(from_email=From(from_email),
               to_emails=[To(to_email) for to_email in to_emails],
               subject=Subject(subject),
               html_content=HtmlContent(html_content))
        return self.__sg.send(message)

    def send_email_to_me(self, subject, html_content):
        return self.send_email_base(
                from_email='nanazhoushop@gmail.com',
                to_emails=['nanazhouh@gmail.com'],
                subject=subject,
                html_content=html_content) 

    def send_email(self, product, action, timestamp):
        time = '{} PT'.format(timestamp.strftime("%Y-%m-%d, %H:%M:%S"))
        pattern = product['pattern']
        color = product['color']
        url = product['url']
        has_image = False
        if len(product['images']) > 0:
            has_image = True
            image = product['images'][0]

        subject = 'Hermes US {} {} - {} at {}'.format(action, pattern, color, time)
        if has_image:
            html_content = '''
                <div>
                    <a href='{}' style='font-size:14px; font-weight:bold; color:black; text-decoration: none;'>
                        {} - {}
                    </a>
                </div>
                <br/>
                <div>
                    <a href='{}'><img src='{}' /></a>
                </div>
            '''.format(url, pattern, color, url, image)
        else:
            html_content = '''
                <div>
                    <a href='{}' style='font-size:14px; font-weight:bold; color:black; text-decoration: none;'>
                        {} - {}
                    </a>
                </div>
            '''.format(url, pattern, color)

        self.send_email_to_me(subject=subject, html_content=html_content)
