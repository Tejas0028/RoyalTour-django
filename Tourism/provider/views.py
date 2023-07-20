from django.shortcuts import render,get_object_or_404,redirect
from .accounts import *
from .models import *
from .forms import *
from seeker.models import *
from Tours.models import Destination
from .render import Render


def destination_quotes(request):
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
        trips = Destination.objects.filter(provider=user.provider_names)
        quotes = TripQuotation.objects.filter(destination__in=trips)
        users = list(set([quote.customer for quote in quotes]))
        return render(request, 'Provider/provider_tours/destination_quotes.html', {'quotes': quotes, 'users': users,'img' : provider_image.avatar.url})
    else:
        return redirect('Provider:provider_login')

def provide_quote(request, trip_quotation_id):
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
        trip_quotation = get_object_or_404(TripQuotation, pk=trip_quotation_id)
        try:
            quote = Provide_TripQuotation.objects.get(trip_quotation=trip_quotation, provider=provider_profile_user)
            form = ProviderProvideQuoteForm(request.POST or None, instance=quote)
        except Provide_TripQuotation.DoesNotExist:
            form = ProviderProvideQuoteForm(request.POST or None)

        if form.is_valid():
            price = form.cleaned_data['price']
            hotel = form.cleaned_data['including_hotel']
            activity = form.cleaned_data['including_extra_activities']
            note = form.cleaned_data['notes']
            quote, created = Provide_TripQuotation.objects.get_or_create(
                trip_quotation=trip_quotation,
                provider=provider_profile_user,
                defaults={
                    'including_hotel': hotel,
                    'including_extra_activities': activity,
                    'price': price,
                    'notes': note,
                }
            )
            if not created:
                quote.including_hotel = hotel
                quote.including_extra_activities = activity
                quote.price = price
                quote.notes = note
                quote.save()

            if hotel == False:
                email = User.objects.get(username=trip_quotation.customer)
                subject = f'Quatation for the {trip_quotation.destination} Trip'
                message = f'Hello {trip_quotation.customer.seeker_profile_model.user},\nHere is your trip Quotation details from {provider_profile_user}\nDestination Name: {trip_quotation.destination}\nPrice: {price}\nIncluding Hotel: {hotel}\nIncluding Extra Activities: {activity}\nNotes: {note}'
                email_from = settings.EMAIL_HOST_USER
                email_to = [email.email, ]
                send_mail(subject, message, email_from, email_to)
                return redirect('Provider:destination_quotes')
            else:
                return redirect('Provider:add_hotel_data',trip_quotation_id=trip_quotation_id)

        return render(request, 'Provider/provider_tours/provide_quote.html', {'form': form, 'trip_quotation': trip_quotation,'img' : provider_image.avatar.url})
    else:
        return redirect('Provider:provider_login')

def MyReport(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])

    job_data = Destination.objects.filter(provider=user.provider_names)
    return Render.render('reports.html', {'job_data':job_data})

def MyServiceReport(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)

    provider_names = user.provider_names
    job = Provide_TripQuotation.objects.filter(provider=provider_names.provider_profile_model)
    # job_data = Provide_TripQuotation.objects.filter(job__in=job)
    return Render.render('MyServiceReport.html', {'job_data':job})

def add_hotel_data(request, trip_quotation_id):
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

        trip_quotation = get_object_or_404(TripQuotation, id=trip_quotation_id)
        provide_quote = get_object_or_404(Provide_TripQuotation, trip_quotation=trip_quotation)

        if not provide_quote.including_hotel:
            return redirect('Provider:destination_quotes')

        if request.method == 'POST':
            form = AddHotelDataForm(request.POST)
            if form.is_valid():
                hotel_name = form.cleaned_data['hotel_name']
                room_type = form.cleaned_data['room_type']
                notes = form.cleaned_data['notes']
                number_of_rooms = form.cleaned_data['number_of_rooms']
                hotel_data = form.save(commit=False)
                hotel_data.trip_quotation = trip_quotation
                hotel_data.save()
                email = User.objects.get(username=trip_quotation.customer)
                subject = f'Quotation for the {trip_quotation.destination} Trip'
                message = f'Hello {trip_quotation.customer.seeker_profile_model.user},\n\nHere is your trip Quotation details from {provider_profile_user}:\n\nDestination Name: {trip_quotation.destination}\nPrice: {provide_quote.price}\nIncluding Hotel: {provide_quote.including_hotel}\nIncluding Extra Activities: {provide_quote.including_extra_activities}\nNotes: {provide_quote.notes}\n\nHotel Details:\nHotel Name: {hotel_name}\nRoom Type: {room_type}\nNumber of Rooms assigned: {number_of_rooms}\nExtra notes: {notes}\n\nThank you for choosing us!\n\nBest regards,\n{provider_profile_user}'
                email_from = settings.EMAIL_HOST_USER
                email_to = [email.email,]
                send_mail(subject, message, email_from, email_to)
                messages.success(request,"Hotel data added successfully")
                return redirect('Provider:destination_quotes')
        else:
            form = AddHotelDataForm()

        return render(request, 'Provider/provider_tours/add_hotel_data.html', {'form': form,'img' : provider_image.avatar.url, 'trip_quotation': trip_quotation})
    else:
        return redirect('Provider:provider_login')