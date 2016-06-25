from django import forms

class NameForm(forms.Form):
    zipcode    = forms.CharField(label='', widget=forms.TextInput(attrs={'margin-top': '10px', 'id':'inputZip', 'class':'form-control', 
	'placeholder':'Enter your zipcode', 'required':'', 'autofocus':''   }), max_length=6)
    condition  = forms.CharField(label='', widget=forms.TextInput(attrs={'margin-top': '10px', 'id':'inputCondition', 'class':'form-control', 
	'placeholder':'Enter your condition', 'required':'', 'autofocus':''   }), max_length=100)

#, 'placeholder':'Enter your conditions here or use our syptoms check above'
