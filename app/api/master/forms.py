from django import forms


class DateRangeForm(forms.Form):
    """ Form for choosing start and end date"""

    start = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    end = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
