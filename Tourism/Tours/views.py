from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from provider.views import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_destination(request):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        if request.method == 'POST':
            form = DestinationForm(request.POST, request.FILES)
            if form.is_valid():
                destination = form.save(commit=False)
                destination.provider = user.provider_names
                destination.save()
                # return redirect('destination_detail', pk=destination.pk)
                return redirect('Provider:provider_profile')
        else:
            form = DestinationForm()
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        return render(request, 'Tours/add_destination.html', {'form': form,'img' : provider_image.avatar.url})
    else:
        return redirect('Provider:provider_login')


def manage_destinations(request):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        destination_list = Destination.objects.all().reverse()
        paginator = Paginator(destination_list, 10)  # Show 10 destinations per page
        page = request.GET.get('page')
        try:
            destinations = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            destinations = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            destinations = paginator.page(paginator.num_pages)
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        context = {'destinations': destinations,
                'img' : provider_image.avatar.url}
        return render(request, 'Tours/manage_destinations.html', context)
    else:
        return redirect('Provider:provider_login')

def destination_detail(request, destination_id):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        destination = get_object_or_404(Destination, id=destination_id)
        context = {'destination': destination,'img' : provider_image.avatar.url}
        return render(request, 'Tours/view_destinations.html', context)
    else:
        return redirect('Provider:provider_login')

def destination_edit(request, destination_id):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        destination = get_object_or_404(Destination, pk=destination_id)

        if request.method == 'POST':
            form = DestinationForm(request.POST, request.FILES, instance=destination)
            if form.is_valid():
                form.save()
                return redirect('Tour:destination_detail', destination_id=destination_id)
        else:
            form = DestinationForm(instance=destination)

        context = {'form': form, 'destination': destination,'img' : provider_image.avatar.url}
        return render(request, 'Tours/edit_destination.html', context)
    else:
        return redirect('Provider:provider_login')

def destination_delete(request, destination_id):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        destination = get_object_or_404(Destination, pk=destination_id)
        if destination:
            destination.delete()
            return redirect('Tour:manage_destinations')
        context = {'destination': destination,'img' : provider_image.avatar.url}
        return render(request, 'Tours/edit_destination.html', context)
    else:
        return redirect('Provider:provider_login')