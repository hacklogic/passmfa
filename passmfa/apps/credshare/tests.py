#from django.test import TestCase

# Create your tests here.
import pyotp




#ubh3na6olofxfhvi
#ubh 3na 6ol ofx fhvi
#otpauth://totp/GitHub:John?secret=ubh3na6olofxfhvi&issuer=GitHub
'''
import pyotp, datetime
totp = pyotp.TOTP("ubh3na6olofxfhvi")
totp = pyotp.parse_uri("otpauth://totp/GitHub:John?secret=ubh3na6olofxfhvi&issuer=GitHub")


print(totp.now())
time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
print(datetime.datetime.now().timestamp())
print(time_remaining)

# 创建 TOTP 实例
refresh_time = totp.interval
print(refresh_time)

'''
'''
from PIL import Image
from pyzbar.pyzbar import decode
#data = decode(Image.open('QR_E0DA474F-36F6-474C-9E26-6CF8D3D749EA.png'))
data = decode(Image.open('testqr.png'))

print(data)
print(data[0].data.decode('utf-8'))
'''


from .apps import credshare

#from .models import AppCredentials
'''
credentials = AppCredentials.objects.get(id=18)
print(credentials)
user = User.objects.get(id=2)
credentials.shared_with_users.add(user)

gp = Group.objects.get(id=1)
credentials.shared_with_groups.add(gp)
'''