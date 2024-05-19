from django import forms

from users.models import Company

def get_field_value(user_id):
    try:
        company = Company.objects.get(user_id=user_id)
        field_value = company.field
        if field_value != 'All in One':
            return [field_value]
        else:
            return [
                'Air Conditioner', 
                'Carpentry',
                'Electricity', 
                'Gardening',
                'Home Machines',
                'House Keeping',
                'Interior Design',
                'Locks', 
                'Painting', 
                'Plumbing',
                'Water Heaters'
            ]
    except Company.DoesNotExist:
        return []


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    # field = forms.ChoiceField(choices=[], required=True)
    field = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'style': 'display:block;'}))

    def __init__(self, *args, **kwargs):
        
         
        user_id = kwargs.pop('user_id', None)
        super(CreateNewService, self).__init__(*args, **kwargs)
      
        # self.fields['field'].choices = [(str(get_field_value(user_id)), str(get_field_value(user_id)))]
        field_value = get_field_value(user_id)
        self.fields['field'].choices = [(str(value), str(value)) for value in field_value]
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

class RequestServiceForm(forms.Form):
    # adress
    # nombres d'heures  apres on doit retourner dans le profil du customer les requets precedentes
    # du coup plus un service sera demande il sera dans les services les plus demandees dans home
    # table a creer : request_service : id(user),nbre_heures,date,
    adress = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adress'}))
    nbre_hour = forms.DecimalField(
        decimal_places=1, max_digits=5, min_value=0.00)
    
