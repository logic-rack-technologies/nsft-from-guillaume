from django import forms

from company.models import Company
from company.utilities import CommonFormHelper


class CompanyUpdateForm(forms.ModelForm):
    """
    The models forms are like the generic class based views which enables us
    to get the work done directly from the model
    We specify the models and their fields
    we can exclude fields as well
    """

    class Meta:
        model = Company
        fields = ["rpps", "adeli", "email", "first_name",
                  "last_name", "date_of_birth"]
        exclude = ["slug"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["date_of_birth"] = forms.DateField(required=False,
                                                       widget=forms.DateInput(
                                                            attrs={'type': "date",
                                                                   'data-date-container': "#datepicker1",
                                                                   'data-provide': "datepicker",
                                                                   'class': "form-control ",
                                                                   'id': 'datepicker1'
                                                                   }
                                                       ))
