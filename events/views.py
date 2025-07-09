from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Registration, Comment
from .forms import EventSearchForm
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from users.decorators import organizer_required, user_required

from django.contrib import messages
from .forms import EventForm, CommentForm   
from django.http import HttpResponseForbidden
from django.utils.timezone import now

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Event
from .serializers import EventSerializer

from django.utils import timezone

from django.views.decorators.http import require_POST



#--------------------------------------------------------------------------------------------------------------------------------------
def event_list(request):
    form = EventSearchForm(request.GET)
    events = Event.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        location = form.cleaned_data.get('location')
        date = form.cleaned_data.get('date')
        keyword = form.cleaned_data.get('keyword')
        status = form.cleaned_data.get('status')
        category = form.cleaned_data.get('category')

        if name:
            events = events.filter(title__icontains=name)
        if location:
            events = events.filter(location__icontains=location)
        if date:
            events = events.filter(start_date__gte=date)
        if keyword:
            events = events.filter(description__icontains=keyword)

        today = now().date()
        if status == 'upcoming':
            events = events.filter(start_date__gt=today)
        elif status == 'ongoing':
            events = events.filter(start_date__lte=today, end_date__gte=today)

        if category:
            events = events.filter(category=category)

    return render(request, 'events/events_list.html', {
        'form': form,
        'events': events
    })

#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    is_registered = Registration.objects.filter(user=request.user, event=event).exists()
    registered_users = Registration.objects.filter(event=event).select_related('user')
    comments = event.comments.order_by('-created_at')  # cele mai noi primele

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.event = event
            new_comment.save()
            messages.success(request, "Comentariul tău a fost adăugat.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        comment_form = CommentForm()

    context = {
        'event': event,
        'is_registered': is_registered,
        'registered_users': registered_users,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'events/event_detail.html', context)


#--------------------------------------------------------------------------------------------------------------------------------------   
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    registration, created = Registration.objects.get_or_create(user=user, event=event)
    if created:
        messages.success(request, f"Te-ai înscris cu succes la evenimentul '{event.title}'.")
    else:
        messages.info(request, f"Deja ești înscris la acest eveniment.")

    return redirect('events:event_detail', event_id=event.id)  # presupunem că ai view de detaliu eveniment 
    
#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
@organizer_required  # să fie accesibil doar organizatorilor
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # asociezi evenimentul cu userul curent
            event.save()
            messages.success(request, "Evenimentul a fost creat cu succes!")
            return redirect('events:event_list')  # sau dashboard, după preferințe
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {
        'form': form,
        'edit_mode': False,
    })

#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
@organizer_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Verifică dacă utilizatorul este organizatorul evenimentului
    if event.organizer != request.user:
        return HttpResponseForbidden("Nu ai permisiunea să editezi acest eveniment.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Evenimentul a fost actualizat cu succes.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'edit_mode': True,
        'event': event,
    })

#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration = Registration.objects.filter(user=request.user, event=event)
    if registration.exists():
        registration.delete()
        messages.success(request, f"Te-ai dezabonat de la evenimentul '{event.title}'.")
    else:
        messages.info(request, "Nu erai înscris la acest eveniment.")
    return redirect('events:event_detail', event_id=event.id)

#--------------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def upcoming_events_api(request):
    today = now().date()
    events = Event.objects.filter(start_date__gte=today).order_by('start_date')

    # filtrare opțională după interval (vezi 7.4)
    start = request.GET.get('start')
    end = request.GET.get('end')
    if start:
        events = events.filter(start_date__gte=start)
    if end:
        events = events.filter(end_date__lte=end)

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
def my_events(request):
    today = timezone.now().date()
    filter_option = request.GET.get('filter', 'all')

    if request.user.userprofile.role == 'organizer':
        events = Event.objects.filter(organizer=request.user)
        if filter_option == 'future':
            events = events.filter(start_date__gte=today)
        elif filter_option == 'past':
            events = events.filter(end_date__lt=today)
        # altfel, 'all', păstrăm toate
        title = "Evenimente create de mine"
    else:
        registrations = Registration.objects.filter(user=request.user).select_related('event')
        events = [reg.event for reg in registrations]
        if filter_option == 'future':
            events = [e for e in events if e.start_date >= today]
        elif filter_option == 'past':
            events = [e for e in events if e.end_date < today]
        title = "Evenimente la care sunt înscris"

    return render(request, 'events/my_events.html', {
        'events': events,
        'title': title,
        'filter_option': filter_option,
    })


#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
@user_required
def user_dashboard(request):
    # Preluăm evenimentele la care userul este înscris
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    events = [reg.event for reg in registrations]

    return render(request, 'events/user_dashboard.html', {
        'events': events,
        'title': 'Evenimentele mele înscrise',
    })

#--------------------------------------------------------------------------------------------------------------------------------------    
@login_required
@organizer_required
@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Verifică dacă utilizatorul este organizatorul evenimentului
    if event.organizer != request.user:
        return HttpResponseForbidden("Nu ai permisiunea să ștergi acest eveniment.")

    event.delete()
    messages.success(request, "Evenimentul a fost șters cu succes.")
    return redirect('events:dashboard_organizator')


#--------------------------------------------------------------------------------------------------------------------------------------
@login_required
@organizer_required
def organizer_dashboard(request):
    # Acum doar organizatorii autentificați pot accesa
    # Aici poți prelua evenimentele organizatorului, ex:
    # events = Event.objects.filter(organizer=request.user)
    events = Event.objects.filter(organizer=request.user)  # presupunem că ai câmp organizer în modelul Event
    return render(request, 'events/dashboard.html', {'events': events})