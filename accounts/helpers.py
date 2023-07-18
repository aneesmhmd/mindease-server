from django.core.mail import  send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail


def send_verification_email(request,email, user):
    domain = get_current_site(request)
    uid =  urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = 'http://' + str(domain) + 'activate' + uid + token

    
    html_message = f'''
        <html>
            <head>
                <style>                    
                    .container {{
                        background-color: white;
                        color:#242424;
                        padding: 20px;
                        border-radius: 5px;
                        display: inline-block;
                        text-align: left;
                    }}
                    
                    .link-button {{
                        display: inline-block;
                        background-color: #6366F1;
                        color: #ffffff!important;
                        text-decoration: none;
                        padding: 10px 20px;
                        border-radius: 3px;
                    }}
                    
                    a {{
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Hi from Bronet</h1>
                    <p>Follow this link to sign in to Bronet:</p>
                    <a class="link-button" href={link}">Sign In</a>
                </div>
            </body>
        </html>
        '''

    send_mail(
        "Hi from MindEase",
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False,
    )