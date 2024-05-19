from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service,Service_Request
from django.db.models import Count


def home(request):
    service_counts = (
        Service_Request.objects
        .values('service_id')
        .annotate(count=Count('service_id'))
        .order_by('-count')
    )

    service_Mosts = []
    for item in service_counts:
        service_id = item['service_id']
        # service_count = item['count']
        service = Service.objects.get(id=service_id)
        service_Mosts.append({
            'id' : service.id,
            'nom': service.name,
            'field': service.field,
            'prix': service.price_hour,
            'company': service.name_company,
        })

    context = {'service_Mosts': service_Mosts[0:3]}
    return render(request, 'main/home.html', context)




def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
