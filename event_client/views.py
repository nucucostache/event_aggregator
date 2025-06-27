from django.shortcuts import render
import requests

def api_event_list(request):
    api_url = 'http://127.0.0.1:8000/api/upcoming/'  # URL-ul API-ului tău local

    start = request.GET.get('start')
    end = request.GET.get('end')

    params = {}
    if start:
        params['start'] = start
    if end:
        params['end'] = end

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # ridică excepție dacă e cod de eroare
        events = response.json()
    except requests.RequestException:
        events = []

    return render(request, 'event_client/api_event_list.html', {
        'events': events,
        'start': start,
        'end': end,
    })


