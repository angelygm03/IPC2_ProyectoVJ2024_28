from django import forms


class LoginForm(forms.Form):
    iduser = forms.CharField(label='iduser')
    password = forms.CharField(widget=forms.PasswordInput(), label='password')

class FileForm(forms.Form):
    file = forms.FileField(label='file')

class AddCartForm(forms.Form):
    product_id = forms.CharField(label='product_id')
    user_id = forms.CharField(label='user_id')