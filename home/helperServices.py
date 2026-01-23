import hmac
import hashlib,jwt,datetime
from django.conf import settings
from django.core.mail import send_mail

# Generate hash passsword
def generate_hash_password(password):
    hashpassword = hmac.new(settings.SECRET_KEY.encode(),password.encode(),hashlib.sha256).hexdigest()
    return hashpassword

# Send verification mail
def send_verification_mail(email,token):
    subject="Account Verification for CodeOne"
    message = (
        f"Hello,\n\n"
        f"Thank you for signing up.\n\n"
        f"To complete your registration, please verify your email address by clicking the link below:\n\n"
        f"http://127.0.0.1:8000/verify/?token={token}\n\n"
        f"If the link does not open, copy and paste it into your browser.\n\n"
        f"If you did not create this account, you can safely ignore this email.\n\n"
        f"Regards,\n"
        f"Team"
        )
    from_email = settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list)
    

# Function to generate token
def generate_token(email,role,userId):
        payload = {
        "email" : email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
        "role":role,
        "userId":userId
        }
        token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
        return token

# Function to verify user token
def cheack_valid_token(token):
    try:
        userdata = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
        return {"valid":True,"data":userdata}
    except jwt.ExpiredSignatureError:
        return {"valid":False,"error":"TOKEN_EXPIRED"}
    except jwt.InvalidTokenError:
        return {"valid":False,"error":"Invalid token"}
