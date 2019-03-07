from django import forms

class LinkInsertForm(forms.Form):
    links = forms.CharField(widget=forms.Textarea)


class GetPeriodLinkForm(forms.Form):
    pass