from django import forms
from .models import Comment
# from .models import Category
from .models import Event
from django.core.exceptions import ValidationError
from django.utils import timezone


# Ce facem mai jos::
# Folosim ModelForm pentru modelul Event
# Validăm titlul să nu fie gol
# Validăm descrierea să aibă minim 20 caractere
# În metoda clean validăm relația între datele de start și end, plus să fie dată viitoare start_date
# ---------------------------------------------------------------------------------------------------------------------------------------------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'location', 'start_date', 'end_date', 'description', 'image', 'website_url']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Titlul evenimentului nu poate fi gol sau doar spații.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) < 20:
            raise ValidationError("Descrierea trebuie să aibă cel puțin 20 de caractere.")
        return description

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Data de început nu poate fi după data de sfârșit.")
            if start_date < timezone.localdate():
                raise ValidationError("Data de început trebuie să fie azi sau în viitor.")
            

# ---------------------------------------------------------------------------------------------------------------------------------------------   

class EventSearchForm(forms.Form):
    name = forms.CharField(
        label='Titlu',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    location = forms.CharField(
        label='Locație',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    start_date = forms.DateField(
        label='Data de început',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    description = forms.CharField(
        label='Descriere',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    STATUS_CHOICES = [
        ('all', 'Toate'),
        ('upcoming', 'Viitoare'),
        ('ongoing', 'În curs'),
    ]
    status = forms.ChoiceField(
        label='Stare',
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    


# ---------------------------------------------------------------------------------------------------------------------------------------------       
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Comentariu',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'maxlength': 500,
            'class': 'form-control',  # 👈 Bootstrap class aici
        }),
        max_length=500,
        help_text='Maxim 500 caractere.'
    )

    class Meta:
        model = Comment
        fields = ['content']
