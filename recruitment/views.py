from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.generic import View
import requests
from django.http import JsonResponse
from recruitment.forms import Application
import uuid
import time
import json
from django.contrib import messages



# single work responsible for getting user auth token 
# this function returns the status code & the token if the status is valid

def getToken(username, password):
    context = {
        'username': str(username),
        'password': str(password)
    }
    r = requests.post('https://recruitment.fisdev.com/api/login/', data=context)
    print(r)
    if r.status_code == 200:
        print('status code', r.status_code)
        response = r.json()
        token = response['token']
        return [r.status_code, token]
    else:
        return [r.status_code, 'invalid']






class LoginPageView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        self.email = request.POST.get('email')
        self.password = request.POST.get('password')
        self.token = getToken(self.email, self.password)
        print(self.token[0],self.token[1])
        context = {'status_code': self.token[0]}
        return JsonResponse(context)
    


class ApplicationPage(View):

    def get(self, request):
        return render(request, 'applicationPage.html')

    def post(self, request):
        request.POST = request.POST.copy()
        print(request.POST, request.FILES)
        form = Application(request.POST)
        #print(form)
        if form.is_valid():
            print(form)
            self.context = {
                "tsync_id": f"{uuid.uuid4()}", 
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "phone": form.cleaned_data['phone'],
                "full_address": form.cleaned_data['full_address'],
                "name_of_university": form.cleaned_data['name_of_university'],
                "graduation_year": form.cleaned_data['graduation_year'],
                "cgpa": form.cleaned_data['cgpa'],
                "experience_in_months": form.cleaned_data['experience_in_months'],
                "current_work_place_name": form.cleaned_data['current_work_place_name'],
                "applying_in": form.cleaned_data['applying_in'],
                "expected_salary": form.cleaned_data['expected_salary'],
                "field_buzz_reference": form.cleaned_data['field_buzz_reference'],
                "github_project_url": form.cleaned_data['github_project_url'],
                # "cv_file": request.FILES['cv_pdf_file'],
                "cv_file":{
                    # "cv_file": request.FILES['cv_pdf_file'],
                    "tsync_id": f"{uuid.uuid4()}",
                },
                "on_spot_update_time": int(time.time()*1000.0),
                "on_spot_creation_time": int(time.time()*1000.0)
            }
            get_token = getToken('aveechakra@gmail.com','v1ChJro65')
            #"Content-type": "APPLICATION/JSON",
            self.headers = {"Content-type": "APPLICATION/JSON","Authorization": "Token {}".format(get_token[1])}
            self.r = requests.post('https://recruitment.fisdev.com/api/v0/recruiting-entities/', headers =self.headers ,data=json.dumps(self.context))
            self.getJsonResponseData = self.r.json()
            print(self.getJsonResponseData)
            print(self.getJsonResponseData['cv_file'])
            self.cvFileId = self.getJsonResponseData['cv_file']['id']
            self.fileUploadUrl= "https://recruitment.fisdev.com/api/file-object/{}/".format(self.cvFileId)
            self.getCv = request.FILES['cv_pdf_file']
            self.files = {'file': self.getCv.read(), 'boundary':''}
            self.cvUploadHeaders = {'content-type': 'multipart/form-data;boundary=uuuhrfanfrufiavee71','Authorization':'token {}'.format(get_token[1])}
            self.response = requests.put(self.fileUploadUrl, headers = self.cvUploadHeaders, files = self.files)
            print('file upload ',self.response.content)
            message = 'Form submitted to Fieldbuzz'
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            for field in form:
                for error in field.errors:
                    messages.warning(
                        request, "%s : %s" % (field.name, error))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


