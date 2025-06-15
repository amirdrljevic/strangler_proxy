from django.http import HttpResponse

def health_check(request):
    return HttpResponse("Proxy service is up and healthy.", content_type="text/plain")
