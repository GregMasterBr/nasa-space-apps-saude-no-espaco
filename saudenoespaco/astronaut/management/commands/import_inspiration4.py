
from django.core.management.base import BaseCommand, CommandError

from saudenoespaco.astronaut.models import (
    Astronaut,
    Mission,
    MissionAssignment,
)


class Command(BaseCommand):

    help = 'Importa a missão Inspiration4 e sua tripulação'

    def handle(self, *args, **options):

        mission, created = Mission.objects.update_or_create(

            name='Inspiration4',

            defaults={
                'agency': 'SpaceX',

                'description': (
                    'Primeira missão orbital totalmente civil, '
                    'realizada pela SpaceX em setembro de 2021. '
                    'A tripulação realizou uma jornada orbital '
                    'de aproximadamente três dias, participando '
                    'também de atividades científicas e pesquisas '
                    'relacionadas à saúde humana no espaço.'
                ),

                'launch_date': '2021-09-16',

                'landing_date': '2021-09-18',

                'status': 'COMPLETED',

                'official_url': 'https://inspiration4.com/',
            }

        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    'Missão cadastrada: Inspiration4'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Missão atualizada: Inspiration4'
                )
            )

        crew = [

            {
                'name': 'Jared Isaacman',
                'role': 'Comandante',
            },

            {
                'name': 'Hayley Arceneaux',
                'role': 'Oficial médica',
            },

            {
                'name': 'Sian Proctor',
                'role': 'Piloto',
            },

            {
                'name': 'Chris Sembroski',
                'role': 'Especialista de missão',
            },

        ]

        created_count = 0
        updated_count = 0

        for member in crew:

            try:
                astronaut = Astronaut.objects.get(
                    full_name=member['name'],
                    agency=''
                )

            except Astronaut.DoesNotExist:
                raise CommandError(
                    f"Astronauta não encontrado: {member['name']}"
                )

            assignment, assignment_created = (
                MissionAssignment.objects.update_or_create(

                    astronaut=astronaut,

                    mission=mission,

                    defaults={
                        'role': member['role'],
                        'crew_type': 'PRIMARY',
                    }

                )
            )

            if assignment_created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Tripulante associado: {astronaut.full_name}'
                    )
                )

            else:
                updated_count += 1

                self.stdout.write(
                    f'Tripulante atualizado: {astronaut.full_name}'
                )

        self.stdout.write('')

        self.stdout.write(
            self.style.SUCCESS(
                'Importação da Inspiration4 finalizada!'
            )
        )

        self.stdout.write(
            f'Novas participações: {created_count}'
        )

        self.stdout.write(
            f'Participações atualizadas: {updated_count}'
        )
