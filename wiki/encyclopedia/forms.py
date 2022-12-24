from django import forms

class search(forms.Form):
    
    """
    Recieve search query
    """
    q = forms.CharField(max_length=250, label="q")

class createPage(forms.Form):

    """
    Form to create New Entry, Should be used on CreatePage template
    """
    title = forms.CharField(max_length=250, label="title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'px-2 w-auto h-max rounded-lg ring-2 ring-violet-500 text-semibold text-xl text-black',"height": "500px"}), label="content")

class edit(forms.Form):
    """ 
    It takes title as a input
    """
    rcvTitle =  forms.CharField(max_length=250)
    

