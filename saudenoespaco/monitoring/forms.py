
from django import forms
from .models import EmotionalCheckIn


class EmotionalCheckInForm(forms.ModelForm):

    EMOTION_CHOICES = [
        ('Feliz', '😊 Feliz'),
        ('Calmo', '😌 Calmo'),
        ('Motivado', '🚀 Motivado'),
        ('Ansioso', '😟 Ansioso'),
        ('Estressado', '😣 Estressado'),
        ('Triste', '😢 Triste'),
        ('Irritado', '😠 Irritado'),
        ('Solitário', '🥺 Solitário'),
        ('Cansado', '😴 Cansado'),
        ('Preocupado', '😰 Preocupado'),
    ]

    emotions = forms.MultipleChoiceField(
        choices=EMOTION_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = EmotionalCheckIn

        fields = [
            'mood',
            'stress_level',
            'fatigue_level',
            'emotions',
            'notes',
        ]

        widgets = {
            'mood': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'stress_level': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5,
                    'placeholder': '1 a 5'
                }
            ),

            'fatigue_level': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5,
                    'placeholder': '1 a 5'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Compartilhe como está se sentindo...'
                }
            ),
        }

