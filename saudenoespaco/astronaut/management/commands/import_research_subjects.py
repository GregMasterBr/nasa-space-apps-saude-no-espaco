
from django.core.management.base import BaseCommand, CommandError

from saudenoespaco.astronaut.models import (
    Mission,
    ResearchSubject,
)


class Command(BaseCommand):

    help = 'Importa os participantes científicos da Inspiration4'

    def handle(self, *args, **options):

        try:
            mission = Mission.objects.get(
                name='Inspiration4'
            )

        except Mission.DoesNotExist:
            raise CommandError(
                'A missão Inspiration4 não foi encontrada. '
                'Execute primeiro import_inspiration4.'
            )

        subjects = [
            {
                'subject_code': 'C001',
                'description': (
                    'Participante científico anonimizado '
                    'da missão Inspiration4.'
                ),
            },
            {
                'subject_code': 'C002',
                'description': (
                    'Participante científico anonimizado '
                    'da missão Inspiration4.'
                ),
            },
            {
                'subject_code': 'C003',
                'description': (
                    'Participante científico anonimizado '
                    'da missão Inspiration4.'
                ),
            },
            {
                'subject_code': 'C004',
                'description': (
                    'Participante científico anonimizado '
                    'da missão Inspiration4.'
                ),
            },
        ]

        source_url = (
            'https://osdr.nasa.gov/bio/repo/data/missions/'
            'SpaceX%20Inspiration4'
        )

        created_count = 0
        updated_count = 0

        for data in subjects:

            subject, created = (
                ResearchSubject.objects.update_or_create(

                    mission=mission,

                    subject_code=data['subject_code'],

                    defaults={
                        'description': data['description'],
                        'source_url': source_url,
                    }

                )
            )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Participante cadastrado: '
                        f'{subject.subject_code}'
                    )
                )

            else:
                updated_count += 1

                self.stdout.write(
                    f'Participante atualizado: '
                    f'{subject.subject_code}'
                )

        self.stdout.write('')

        self.stdout.write(
            self.style.SUCCESS(
                'Importação dos participantes finalizada!'
            )
        )

        self.stdout.write(
            f'Novos participantes: {created_count}'
        )

        self.stdout.write(
            f'Participantes atualizados: {updated_count}'
        )
