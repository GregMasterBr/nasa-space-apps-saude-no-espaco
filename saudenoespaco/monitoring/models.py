from django.db import models
from saudenoespaco.astronaut.models import ResearchSubject
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class EmotionalCheckIn(models.Model):

    MOOD_CHOICES = [
        ('EXCELLENT', 'Excelente'),
        ('GOOD', 'Bem'),
        ('NEUTRAL', 'Neutro'),
        ('BAD', 'Mal'),
        ('VERY_BAD', 'Muito mal'),
    ]

    subject = models.ForeignKey(
        ResearchSubject,
        on_delete=models.CASCADE,
        related_name='emotional_checkins',
        verbose_name='Participante'
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        verbose_name='Humor'
    )

    stress_level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Nível de estresse',
        help_text='Escala de 1 a 5'
    )

    fatigue_level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],        
        verbose_name='Nível de fadiga',
        help_text='Escala de 1 a 5'
    )

    emotions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Emoções percebidas'
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do registro'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Check-in emocional'
        verbose_name_plural = 'Check-ins emocionais'
        
        constraints = [
            models.CheckConstraint(
                check=Q(stress_level__gte=1, stress_level__lte=5),
                name='stress_level_between_1_and_5'
            ),
            models.CheckConstraint(
                check=Q(fatigue_level__gte=1, fatigue_level__lte=5),
                name='fatigue_level_between_1_and_5'
            ),
        ]        

    def __str__(self):
        return f'{self.subject.subject_code} - {self.get_mood_display()}'