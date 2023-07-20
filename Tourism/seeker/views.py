from django.shortcuts import render, get_object_or_404
from .accounts import *
from Tours.models import *
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from provider.render import Render

# Create your views here.

def index(request):
    destinations = Destination.objects.all()
    countries = state_data.objects.all()[:10]
    cities = city_data.objects.all()[:10]
    context = {'destinations': destinations,'countries':countries,'cities':cities}
    return render(request, "index.html", context)

def seeker_destination_detail(request, destination_id):
    if request.session.get('seeker') != None:
        epl = request.session.get('seeker')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Seeker:seeker_login')
        user = User.objects.get(username=epl['username'])
        seeker_profile_user = Seeker_Profile_Model.objects.get(user=user.seeker_names.seeker_profile_model)
        if seeker_profile_user.avatar is None:
            seeker_image = None
        else:
            seeker_image = seeker_profile_user
        destination = get_object_or_404(Destination, id=destination_id)
        context = {'destination': destination,'img' : seeker_image.avatar.url}
        return render(request, 'Seeker/seeker_tour/seeker_view_destination.html', context)
    else:
        destination = get_object_or_404(Destination, id=destination_id)
        context = {'destination': destination}
        return render(request, 'Seeker/seeker_tour/seeker_view_destination.html', context)

def trip_quotation(request, destination_id):
    if request.session.get('seeker') != None:
        epl = request.session.get('seeker')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Seeker:seeker_login')
        user = User.objects.get(username=epl['username'])
        print(user)
        seeker_profile_user = Seeker_Profile_Model.objects.get(user=user.seeker_names.seeker_profile_model)
        if seeker_profile_user.avatar is None:
            seeker_image = None
        else:
            seeker_image = seeker_profile_user
        destination = get_object_or_404(Destination, id=destination_id)
        print(destination)
        if request.method == 'POST':
            form = TripQuotationForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['departure_date']
                adults = form.cleaned_data['number_of_adults']
                child = form.cleaned_data['number_of_children']
                notes = form.cleaned_data['notes']
                trip_quotation = TripQuotation(customer=user.seeker_names,destination=destination,departure_date = date,number_of_adults = adults,number_of_children = child,notes = notes)
                trip_quotation.save()
                messages.success(request, 'Your trip quotation has been submitted successfully.')
                return redirect('Seeker:requested_quotes')
            else:
                messages.error(request,"Form is invalid")
        else:
            form = TripQuotationForm()
        return render(request, 'Seeker/seeker_tour/trip_quotation.html', {'form': form, 'destination': destination,'img' : seeker_image.avatar.url})
    else:
        return redirect('Seeker:seeker_login')

def requested_quotes(request):
    if request.session.get('seeker') != None:
        epl = request.session.get('seeker')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Seeker:seeker_login')
        user = User.objects.get(username=epl['username'])
        print(user)
        seeker_profile_user = Seeker_Profile_Model.objects.get(user=user.seeker_names.seeker_profile_model)
        if seeker_profile_user.avatar is None:
            seeker_image = None
        else:
            seeker_image = seeker_profile_user
        user_quotes = TripQuotation.objects.filter(customer=user.seeker_names)
        return render(request, 'Seeker/seeker_tour/requested_quotes.html', {'user_quotes': user_quotes,'img' : seeker_image.avatar.url})
    else:
        return redirect('Seeker:seeker_login')

def requested_quotes_data(request,id):
    if request.session.get('seeker') != None:
        epl = request.session.get('seeker')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Seeker:seeker_login')
        user = User.objects.get(username=epl['username'])
        user_quotes = TripQuotation.objects.get(pk=id)
        try:
            job = Provide_TripQuotation.objects.get(trip_quotation=user_quotes)
        except:
            job = None
        try:
            hotel = Add_hotel_data.objects.filter(trip_quotation=job.trip_quotation).last()
        except:
            hotel = None
        return Render.render('requested_quotes_data.html', {'i':job,'j':hotel})
    else:
        return redirect('Seeker:seeker_login')

def search_destinations(request):
    query = request.GET.get('q')
    # Filter jobs by query and/or category
    jobs = Destination.objects.all()
    category_id = request.GET.get('category')

    if query:
        jobs = Destination.objects.filter(name__icontains =query) | Destination.objects.filter(description__icontains =query) | Destination.objects.filter(city__city__icontains=query) | Destination.objects.filter(country__state__icontains=query)

    if category_id:
        jobs = Destination.filter(category__name__icontains=category_id)

    # Pagination
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    countries = state_data.objects.all()

    return render(request, 'search_results.html', {'destinations': page_obj, 'query': query, 'countries': countries})

def search_cat(request, category_id):
    # Retrieve jobs for the selected category
    job_category = state_data.objects.get(pk=category_id)
    job_list = Destination.objects.filter(country=job_category)
    paginator = Paginator(job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Top job categories
    countries = state_data.objects.all()

    return render(request, 'search_results.html', {'destinations': page_obj, 'countries': countries})


from django.urls import reverse

def contact(request):
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            subject = 'Thank you for contacting us'
            message = f'Dear {contact.name},\nThank you for contacting us. We will get back to you as soon as possible.'
            email_from = settings.EMAIL_HOST_USER
            email_to = [contact.email, ]
            send_mail(subject, message, email_from, email_to)
            return redirect('Seeker:index')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form,'previous_page': previous_page})

def aboutus(request):
   previous_page = request.META.get('HTTP_REFERER')
   context = {
        'previous_page': previous_page
        }
   return render(request,'aboutus.html',context)