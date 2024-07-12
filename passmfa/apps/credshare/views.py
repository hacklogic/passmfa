from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .models import AppCredentials
from .forms import AppCredentialsForm, ShareCredentialsForm

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from apps.authentication.views import AuthView
from .forms import UploadFileForm


import pyotp, datetime,io
import json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from PIL import Image
from pyzbar.pyzbar import decode
import base64

@csrf_exempt
def userlogout(request):
    logout(request)
    return redirect("/login")



class LoginView(AuthView):
    #template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("index")  # Replace 'index' with the actual URL name for the home page
        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        if request.method == "POST":

            username = request.POST.get("email-username")
            password = request.POST.get("password")

            if not (username and password):
                messages.error(request, "Please enter your username and password.")
                return redirect("login")

            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "Please enter a valid email.")
                    return redirect("login")
                username = user_email.username

            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, "Please ask Admin to create a new user.")
                return redirect("login")

            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                # Login the user if authentication is successful
                login(request, authenticated_user)

                # Redirect to the page the user was trying to access before logging in
                if "next" in request.POST:
                    return redirect(request.POST["next"])
                else: # Redirect to the home page or another appropriate page
                    return redirect("index")
            else:
                messages.error(request, "Please enter a valid username.")
                return redirect("login")


class IndexView2(TemplateView):
    #template_name = 'login.html'
    template_name = 'auth_login_basic.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
class IndexView(TemplateView):
    template_name = 'auth_login_basic.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if self.request.user.is_authenticated:
            credentials = AppCredentials.objects.filter(app_owner=self.request.user)
            #shared_credentials = AppCredentials.objects.filter(shared_with_users=self.request.user) | AppCredentials.objects.filter(shared_with_groups__in=self.request.user.groups.all()).distinct()

            context['credentials']=credentials

            #context['shared_credentials']=shared_credentials
        return context


class NewView(TemplateView):
    template_name = 'auth_login_basic.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if self.request.user.is_authenticated:
            credentials = AppCredentials.objects.filter(app_owner=self.request.user)
            #shared_credentials = AppCredentials.objects.filter(shared_with_users=self.request.user) | AppCredentials.objects.filter(shared_with_groups__in=self.request.user.groups.all()).distinct()

            context['credentials']=credentials

            #context['shared_credentials']=shared_credentials
        return context
@login_required
def get_otp(request, credential_id):
    # 假设我们有一个函数 `get_credential_by_id` 来获取凭据对象
    if request.user.is_authenticated:
        credentials = AppCredentials.objects.filter(app_owner=request.user).filter(id=credential_id)

        #credential = get_credential_by_id(credential_id)

        if len(credentials)==1:
            #totp = pyotp.TOTP(credentials[0].app_two_fa)  # 使用pyotp生成2FA代码
            totp = pyotp.TOTP(pyotp.random_base32())

            #totp = pyotp.TOTP('ubh3na6olofxfhvi')
            time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
            current_2fa_code = totp.now()
            return JsonResponse({"otp": current_2fa_code, "rtime": int(time_remaining)})
        else:
            totp = pyotp.TOTP(pyotp.random_base32())

            # totp = pyotp.TOTP('ubh3na6olofxfhvi')
            time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
            current_2fa_code = totp.now()
            return JsonResponse({"otp": current_2fa_code, "rtime": int(time_remaining)})
            #return JsonResponse({"otp": "error"})


def credentials_list(request):
    credentials = AppCredentials.objects.filter(app_owner=request.user)
    #shared_credentials = AppCredentials.objects.filter(shared_with_users=request.user) | AppCredentials.objects.filter(shared_with_groups__in=request.user.groups.all()).distinct()
    #return render(request, 'credentials_list.html', {'credentials': credentials, 'shared_credentials': shared_credentials})
    return render(request, 'credentials_list.html',{'credentials': credentials})


def read_qrcode(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            image = Image.open(file)

            qrcode_data = decode(image)
            if qrcode_data:
                qr = qrcode_data[0].data.decode('utf-8')
                #print(qr)
                return JsonResponse({'status':'1','qrcode': qr})
            else:
                return JsonResponse({'status':'0','qrcode': 'No QR code found'})
    return JsonResponse({'error': 'No image data provided'})

@csrf_exempt
def read_qrcode_bak(request):

    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        #print(image_data)
        if image_data:
            # 将 base64 编码的图片数据解码为图片
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # 读取二维码信息
            #qrcode_data = read_qrcode_from_image(image)
            qrcode_data = decode(image)
            if qrcode_data:
                qr = qrcode_data[0].data.decode('utf-8')
                #print(qr)
                return JsonResponse({'status':'1','qrcode': qr})
            else:
                return JsonResponse({'status':'0','qrcode': 'No QR code found'})
    return JsonResponse({'error': 'Invalid request method'})




@csrf_exempt
def add_credentials(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)

        form = AppCredentialsForm(json_data)
        if form.is_valid():
            credentials = form.save(commit=False)
            credentials.app_owner = request.user
            credentials.save()
            return JsonResponse({'success': True, 'message': 'Data saved successfully'})
            #return redirect('index')
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    else:
        form = AppCredentialsForm()
    return render(request, 'add_credentials.html', {'form': form})


@csrf_exempt
def edit_credentials(request, id):
    if request.method == 'GET':
        credentials = AppCredentials.objects.get(app_owner=request.user, id=id)
        if credentials:
            print(credentials)
            return JsonResponse({'app_name': credentials.app_name,
                                 'app_url': credentials.app_url,
                                 'app_username': credentials.app_username,
                                 'app_password': credentials.app_password,
                                 'app_two_fa': credentials.app_two_fa
                                 })
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)



class SharetomeView(TemplateView):
    template_name = 'sharetome.html'
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        #context = super().get_context_data(**kwargs)
        # Get URL parameters
        #user_id = kwargs.get('user_id1')
        #page = kwargs.get('page')

        #shared_credentials = AppCredentials.objects.filter(shared_with_users=self.request.user) | AppCredentials.objects.filter(shared_with_groups__in=self.request.user.groups.all()).distinct()

        shared_tome_credentials = AppCredentials.objects.filter(shared_with_users=self.request.user)

        credentials_with_groups = []
        groups = self.request.user.groups.all()
        for group in groups:
            print(group.name)
            credentials = AppCredentials.objects.filter(shared_with_groups = group).distinct()
            if credentials.exists():
                for credential in credentials:
                    print(credential)
                    credentials_with_groups.append({
                        'credential': credential,
                        'group': group
                    })
        print(credentials_with_groups)
        '''     
        shared_togroup_credentials = AppCredentials.objects.filter(shared_with_groups__in=self.request.user.groups.all()).distinct()
        # Prepare a list with credentials and their corresponding groups
        credentials_with_groups = []
        for credential in shared_togroup_credentials:
            #groups = credential.shared_with_groups.all()
            groups = self.request.user.groups.all()
            for group in groups:
                credentials_with_groups.append({
                    'credential': credential,
                    'group': group
                })
        '''
        for credential in shared_tome_credentials:
            print(credential)
        for credential in credentials_with_groups:
            print(credential)


        # Get GET data
        #name = self.request.GET.get('name')
        #email = self.request.GET.get('email')

        # Add URL parameters to the context
        context['share_me'] = shared_tome_credentials
        context['share_group'] = credentials_with_groups

        return context
'''
    def post(self, request, *args, **kwargs):
        # Get the POST data
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Get URL parameters
        user_id = kwargs.get('user_id')
        page = kwargs.get('page')

        # Do something with the data
        print(f'Name: {name}, Email: {email}, User ID: {user_id}, Page: {page}')

        # Return the template response
        return self.render_to_response(self.get_context_data(**kwargs))
'''


@csrf_exempt
def delete_credentials(request, id):
    if request.method == 'GET':
        credentials = AppCredentials.objects.get(app_owner=request.user, id=id)
        if credentials:
            print(credentials)

            credentials.delete()
            #return redirect('index')
            return JsonResponse({'success': True, 'message': 'Data delete successfully'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def getshare_credentials(request, id):
    if request.method == 'GET':
        #credentials = AppCredentials.objects.get(app_owner=request.user, id=id)

        shared_tome_credentials = AppCredentials.objects.filter(shared_with_users=request.user)
        shared_togroup_credentials =  AppCredentials.objects.filter(shared_with_groups__in= request.user.groups.all()).distinct()

        return JsonResponse({'success': True, 'message': 'Data delete successfully'})

    pass


@csrf_exempt
def addshare_credentials(request, id):
    if request.method == 'GET':
        credentials = AppCredentials.objects.get(app_owner=request.user, id=id)
        if credentials:
            print(credentials)
            #return redirect('index')
            return JsonResponse({'success': True, 'message': 'Data delete successfully'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)


    credentials = get_object_or_404(AppCredentials, id=id, app_owner=request.user)
    if request.method == 'POST':
        form = ShareCredentialsForm(request.POST, instance=credentials)
        if form.is_valid():
            form.save()
            return redirect('credentials_list')
    else:
        form = ShareCredentialsForm(instance=credentials)
    return render(request, 'share_credentials.html', {'form': form})


@csrf_exempt
def delshare_credentials(request,type,id):
    if request.method == 'GET':
        #now only support 1-1 share deletion, not support  1-gourp deletion
        if type ==0:
            credential = AppCredentials.objects.get(app_owner=request.user, id=id)
            credential.shared_with_users.remove(request.user)
            credential.save()
            return JsonResponse({'success': True, 'message': 'Share delete successfully'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
