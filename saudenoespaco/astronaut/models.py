
from django.db import models


class Astronaut(models.Model):

    full_name = models.CharField(
        max_length=150,
        verbose_name='Nome completo'
    )

    agency = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Agência espacial'
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nacionalidade'
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Ocupação'
    )

    biography = models.TextField(
        blank=True,
        verbose_name='Biografia'
    )

    photo_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Caminho da fotografia'
    )

    profile_url = models.URLField(
        blank=True,
        verbose_name='Perfil oficial'
    )

    source_url = models.URLField(
        blank=True,
        verbose_name='Fonte dos dados'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    code = models.CharField(
        max_length=4,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Código do participante'
    )


    class Meta:
        ordering = ['full_name']
        verbose_name = 'Astronauta'
        verbose_name_plural = 'Astronautas'

        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'agency'],
                name='unique_astronaut_per_agency'
            )
        ]

    def __str__(self):
        return self.full_name


class Mission(models.Model):

    STATUS_CHOICES = [
        ('PLANNED', 'Planejada'),
        ('IN_PROGRESS', 'Em andamento'),
        ('COMPLETED', 'Concluída'),
        ('CANCELLED', 'Cancelada'),
    ]

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nome da missão'
    )

    agency = models.CharField(
        max_length=100,
        default='SpaceX',
        verbose_name='Agência responsável'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    launch_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de lançamento'
    )

    landing_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de retorno'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED',
        verbose_name='Situação'
    )

    official_url = models.URLField(
        blank=True,
        verbose_name='Página oficial'
    )

    astronauts = models.ManyToManyField(
        Astronaut,
        through='MissionAssignment',
        related_name='missions',
        verbose_name='Astronautas'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Missão'
        verbose_name_plural = 'Missões'

    def __str__(self):
        return self.name


class MissionAssignment(models.Model):

    CREW_TYPE_CHOICES = [
        ('PRIMARY', 'Tripulação principal'),
        ('BACKUP', 'Tripulação reserva'),
    ]

    astronaut = models.ForeignKey(
        Astronaut,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Astronauta'
    )

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Missão'
    )

    role = models.CharField(
        max_length=100,
        verbose_name='Função na missão'
    )

    crew_type = models.CharField(
        max_length=20,
        choices=CREW_TYPE_CHOICES,
        default='PRIMARY',
        verbose_name='Tipo de participação'
    )

    class Meta:
        ordering = ['mission', 'astronaut']

        constraints = [
            models.UniqueConstraint(
                fields=['astronaut', 'mission'],
                name='unique_astronaut_mission'
            )
        ]

        verbose_name = 'Participação em missão'
        verbose_name_plural = 'Participações em missões'

    def __str__(self):
        return f'{self.astronaut} - {self.mission}'


class ResearchSubject(models.Model):

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='research_subjects',
        verbose_name='Missão'
    )

    user = models.OneToOneField(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='research_subject',
        verbose_name='Usuário de acesso'
    )

    subject_code = models.CharField(
        max_length=50,
        verbose_name='Código do participante'
    )

    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descrição'
    )

    source_url = models.URLField(
        blank=True,
        verbose_name='Fonte dos dados'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['subject_code']

        constraints = [
            models.UniqueConstraint(
                fields=['mission', 'subject_code'],
                name='unique_subject_per_mission'
            )
        ]

        verbose_name = 'Participante de pesquisa'
        verbose_name_plural = 'Participantes de pesquisa'

    def __str__(self):
        return f'{self.mission} - {self.subject_code}'


class HealthRecord(models.Model):

    subject = models.ForeignKey(
        ResearchSubject,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name='Participante'
    )

    study_code = models.CharField(
        max_length=50,
        verbose_name='Código do estudo'
    )

    parameter = models.CharField(
        max_length=150,
        verbose_name='Parâmetro analisado'
    )

    value = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        verbose_name='Resultado'
    )


    reference_min = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        null=True,
        blank=True,
        verbose_name='Referência mínima'
    )

    reference_max = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        null=True,
        blank=True,
        verbose_name='Referência máxima'
    )

    sex = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Sexo registrado na fonte'
    )

    test_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Tipo do exame'
    )


    unit = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Unidade de medida'
    )

    collection_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data da coleta'
    )

    timepoint = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Momento da coleta'
    )

    sample_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tipo de amostra'
    )

    source_url = models.URLField(
        blank=True,
        verbose_name='Fonte dos dados'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['collection_date', 'parameter']

        indexes = [
            models.Index(
                fields=['study_code', 'parameter'],
                name='health_study_param_idx'
            )
        ]

        verbose_name = 'Registro de saúde'
        verbose_name_plural = 'Registros de saúde'

    def __str__(self):
        return f'{self.subject} - {self.parameter}'


class FamilyContact(models.Model):

    astronaut = models.ForeignKey(
        'Astronaut',
        on_delete=models.CASCADE,
        related_name='family_contacts',
        verbose_name='Astronauta'
    )

    name = models.CharField(
        max_length=150,
        verbose_name='Nome do familiar'
    )

    relationship = models.CharField(
        max_length=100,
        verbose_name='Grau de parentesco'
    )

    photo_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Caminho da fotografia'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Contato principal'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Contato ativo'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Contato familiar'
        verbose_name_plural = 'Contatos familiares'

    def __str__(self):
        return f'{self.name} - {self.astronaut.full_name}'


class CommunicationCall(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        MISSED = 'MISSED', 'Missed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    astronaut = models.ForeignKey(
        'Astronaut',
        on_delete=models.CASCADE,
        related_name='communication_calls',
        verbose_name='Astronauta'
    )

    contact = models.ForeignKey(
        FamilyContact,
        on_delete=models.PROTECT,
        related_name='calls',
        verbose_name='Contato familiar'
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data agendada'
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Início da chamada'
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fim da chamada'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name='Status'
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chamada de comunicação'
        verbose_name_plural = 'Chamadas de comunicação'

    def __str__(self):
        return f'{self.astronaut.full_name} - {self.contact.name}'


class CommunicationChecklist(models.Model):

    class ChecklistType(models.TextChoices):
        PRE_CALL = 'PRE_CALL', 'Pre-call'
        POST_CALL = 'POST_CALL', 'Post-call'
        DAILY = 'DAILY', 'Daily Wellness'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    astronaut = models.ForeignKey(
        'Astronaut',
        on_delete=models.CASCADE,
        related_name='communication_checklists',
        verbose_name='Astronauta'
    )

    call = models.ForeignKey(
        CommunicationCall,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checklists',
        verbose_name='Chamada relacionada'
    )

    checklist_type = models.CharField(
        max_length=20,
        choices=ChecklistType.choices,
        verbose_name='Tipo de checklist'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de conclusão'
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Checklist de comunicação'
        verbose_name_plural = 'Checklists de comunicação'

    def __str__(self):
        return f'{self.astronaut.full_name} - {self.get_checklist_type_display()}'


class CommunicationChecklistItem(models.Model):

    checklist = models.ForeignKey(
        CommunicationChecklist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Checklist'
    )

    description = models.CharField(
        max_length=255,
        verbose_name='Descrição do item'
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name='Concluído'
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Item do checklist'
        verbose_name_plural = 'Itens do checklist'

    def __str__(self):
        return self.description
