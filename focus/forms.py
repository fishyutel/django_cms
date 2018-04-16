from django import forms

class LoginForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'uid','placeholder':'username'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'pwd','placeholder':'CMSpassword'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))