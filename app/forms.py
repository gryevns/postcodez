from django import forms


MAX_POSTCODES = 5000


class PostcodeForm(forms.Form):
    postcodes = forms.CharField(
        label='Postcodes',
        widget=forms.Textarea(attrs={
            'class' : 'form-control',
        }),
    )
    clean = forms.BooleanField(
        label='Clean',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'checked': 'checked',
        }),
    )

    def clean_postcodes(self):
        postcodes = self.cleaned_data['postcodes']
        postcodes = postcodes.replace(',', '\n')
        postcodes = set([s.strip().upper().replace(' ', '') for s in postcodes.splitlines()])
        postcodes = [postcode for postcode in postcodes if len(postcode) < 8]
        if len(postcodes) > MAX_POSTCODES:
            raise forms.ValidationError(
                'Too many postcodes! More than {} unqiue postcodes entered.'.format(MAX_POSTCODES)
            )
        return postcodes
