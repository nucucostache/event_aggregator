from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event, Registration, Comment
from django.utils import timezone
from datetime import timedelta

#-----------------------------------------------------------------------------------------------------
# Test Event
class EventModelTest(TestCase):
    def setUp(self):
        # Creăm un utilizator pentru organizator
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_event_creation(self):
        # Creăm un eveniment
        event = Event.objects.create(
            title='Test Eveniment',
            description='Descriere test pentru eveniment.',
            start_date=timezone.now().date() + timedelta(days=1),  # mâine
            end_date=timezone.now().date() + timedelta(days=2),    # poimâine
            location='Test Location',
            organizer=self.user,
        )
        # Verificăm dacă titlul evenimentului este corect
        self.assertEqual(event.title, 'Test Eveniment')
        # Verificăm dacă organizatorul este utilizatorul creat
        self.assertEqual(event.organizer.username, 'testuser')
        # Verificăm că metoda __str__ returnează titlul corect cu datele
        self.assertIn('Test Eveniment', str(event))
        

#-----------------------------------------------------------------------------------------------------
# Test Registration
class RegistrationModelTest(TestCase):
    def setUp(self):
        # Creăm un utilizator pentru organizator și un utilizator participant
        self.organizer = User.objects.create_user(username='organizer', password='12345')
        self.participant = User.objects.create_user(username='participant', password='12345')

        # Creăm un eveniment organizat de organizer
        self.event = Event.objects.create(
            title='Test Eveniment',
            description='Descriere test pentru eveniment.',
            start_date=timezone.now().date() + timedelta(days=1),  # mâine
            end_date=timezone.now().date() + timedelta(days=2),    # poimâine
            location='Test Location',
            organizer=self.organizer,
        )

    def test_registration_creation(self):
        # Creăm o înregistrare a participantului la eveniment
        registration = Registration.objects.create(
            user=self.participant,
            event=self.event
        )
        # Verificăm dacă utilizatorul din înregistrare este corect
        self.assertEqual(registration.user.username, 'participant')
        # Verificăm dacă evenimentul este corect asociat
        self.assertEqual(registration.event.title, 'Test Eveniment')
        # Verificăm dacă metoda __str__ returnează string-ul corect
        self.assertIn('participant înscris la Test Eveniment', str(registration))

#-----------------------------------------------------------------------------------------------------
# Test Comment
class CommentModelTest(TestCase):
    def setUp(self):
        # Creăm un utilizator și un eveniment pentru test
        self.user = User.objects.create_user(username='commentuser', password='12345')
        self.event = Event.objects.create(
            title='Eveniment Comentariu',
            description='Descriere test eveniment comentariu.',
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=2),
            location='Locatie Test',
            organizer=self.user,
        )

    def test_comment_creation(self):
        # Creăm un comentariu legat de eveniment și utilizator
        comment = Comment.objects.create(
            event=self.event,
            user=self.user,
            content='Acesta este un comentariu de test.',
        )
        # Verificăm conținutul comentariului
        self.assertEqual(comment.content, 'Acesta este un comentariu de test.')
        # Verificăm legătura cu evenimentul
        self.assertEqual(comment.event.title, 'Eveniment Comentariu')
        # Verificăm legătura cu utilizatorul
        self.assertEqual(comment.user.username, 'commentuser')
        # Verificăm că metoda __str__ returnează string-ul așteptat
        expected_str = f"Comentariu de la {self.user.username} la {self.event.title}"
        self.assertEqual(str(comment), expected_str)

