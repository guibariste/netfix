
# il reste plus qu'a faire les services les plus demandes et pas crash quand on est pas log

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User
from django.core.exceptions import ObjectDoesNotExist
from .models import Service,Service_Request
from .forms import CreateNewService,RequestServiceForm
from django.contrib.auth.decorators import login_required





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
@login_required
def service_list(request):
    
    # user_id = request.user.id
    # user = User.objects.get(id=user_id)
        
    # if user.is_company:
    
    #  services = Service.objects.filter(company_id=user_id).order_by("-date")
    # elif user.is_customer:
    services = Service.objects.all().order_by("-date")
    # else :
    #    crrer une redirection vers la connexion
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})



def get_company_name(user_id):
    try:
        company = User.objects.get(id=user_id)
        field_value = company.username
        return field_value
    except Company.DoesNotExist:
        return None

def service_field(request,field):
    print(field)
    try:

        services = Service.objects.filter(field__iexact=field)
        # for service in services:
        # print(service.name)
        # Effectuez les opérations souhaitées avec l'objet "service"
        return render(request, 'services/list.html', {'services': services, })
    except ObjectDoesNotExist:
        # Gérez le cas où l'objet "Service" n'existe pas
        print("existe pas")
        
        return redirect('/')
     
     
def create(request):
    # il faut aussi s'occuper de all/in one pour la liste deroulante
    user_id = request.user.id
    field_value = get_field_value(user_id)
    print(field_value)
    if request.method == 'POST':
        form = CreateNewService(request.POST, user_id=user_id)
        if form.is_valid():
         cleaned_data = form.cleaned_data
        name=(cleaned_data['name'])
        description=(cleaned_data['description'])
        price_hour=(cleaned_data['price_hour'])
        field=(cleaned_data['field'])
        name_company=get_company_name(user_id)
        service = Service.objects.create(name=name,description=description,price_hour=price_hour, field=field,name_company= name_company,  company_id=user_id)
        service.save()
        return redirect('/')
    else:
       form = CreateNewService(user_id=user_id)

    context = {'form': form, 'field_value': field_value}
    return render(request, 'services/create.html', context=context)

def request_service(request, id):
    # Get the service object with the given id
    service = Service.objects.get(id=id)
    # If the form is submitted
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = RequestServiceForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            data = form.cleaned_data
            print(data)

            # Here you can save the form data to the database, for example:
            requestService = Service_Request.objects.create(user_id=request.user.id,service_id=service.id, adress=data['adress'], nbre_hour=data['nbre_hour'],price_hour=service.price_hour,service_name=service.name,name_company=service.name_company,total_price=service.price_hour*data["nbre_hour"],field =service.field)
            requestService.save()
            return redirect('/')
    # If the form is not submitted
    else:
        # Create a new form instance
        form = RequestServiceForm()
    # Render the request_service.html template with the service and the form instances
    return render(request, 'services/request_service.html', {'service': service, 'form': form})