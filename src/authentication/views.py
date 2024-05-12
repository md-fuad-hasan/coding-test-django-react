from django.contrib.auth.decorators import login_required

# Create your views here.
from django import views
from django.utils.decorators import method_decorator

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class DashboardView(views.generic.TemplateView):
    template_name = 'dashboard.html'
