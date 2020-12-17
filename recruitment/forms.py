from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
import uuid
import json
import time

class Application(forms.Form):
    tsync_id = uuid.uuid4()
    name = forms.CharField(max_length=256)
    email = forms.EmailField(max_length=256)
    phone = forms.CharField(max_length=14)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=256)
    graduation_year = forms.IntegerField(max_value=2020, min_value=2015)
    cgpa = forms.IntegerField(required=False)
    experience_in_months = forms.IntegerField(max_value=100, min_value=0,  required=False)
    current_work_place_name = forms.CharField(max_length=256,  required=False)
    applying_in = forms.CharField(max_length=50)
    expected_salary = forms.IntegerField(max_value=60000, min_value=15000)
    field_buzz_reference = forms.CharField(max_length=256,  required=False)
    github_project_url = forms.URLField(max_length=512)
    cv_file = {"tsync_id": uuid.uuid4()}
    on_spot_update_time = int(time.time()*1000.0)
    on_spot_creation_time = int(time.time()*1000.0)
    