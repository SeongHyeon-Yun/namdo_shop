from django import forms
from .models import User, ExcelUpload


class join_form(forms.Form):
    user_id = forms.CharField(max_length=50)
    password_1 = forms.CharField(widget=forms.PasswordInput, max_length=50)
    password_2 = forms.CharField(widget=forms.PasswordInput, max_length=50)
    boss_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=11)
    company_name = forms.CharField(max_length=30)
    company_number = forms.CharField(max_length=15)
    manager_name = forms.CharField(max_length=5)
    business_file = forms.FileField()
    post_code = forms.CharField(max_length=20)
    address = forms.CharField(max_length=100)
    detail_address = forms.CharField(max_length=100)
    extraAddress = forms.CharField(max_length=100)
    email_check = forms.BooleanField(required=False)
    message_check = forms.BooleanField(required=False)

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")

        if User.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError("이미 사용중인 아이디 입니다.")
        return user_id

    def clean(self):
        cleaned_data = super().clean()

        pw1 = cleaned_data.get("password_1")
        pw2 = cleaned_data.get("password_2")

        if pw1 != pw2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data


class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelUpload
        fields = ["excel_file"]

    def clean_excel_file(self):
        file = self.cleaned_data["excel_file"]
        if not file.name.endswith((".xlsx", ".xls")):
            raise forms.ValidationError("엑셀 파일만 업로드 가능합니다.")
        return file
