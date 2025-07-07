from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'category']

# Ce face EventSerializer:
# Transformă fiecare instanță Event în JSON
# Include doar câmpurile importante pentru listarea evenimentelor viitoare