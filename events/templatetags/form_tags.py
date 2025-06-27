from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

# Fișierul form_tags.py definește un filtru personalizat în Django Template Language,
# care ne permite să adăugăm clase CSS câmpurilor din formular direct în template, fără să modificăm forms.py.

