from django.core.management.base import BaseCommand
from saudenoespaco.astronaut.models import Astronaut


class Command(BaseCommand):

    help = 'Importa os integrantes da tripulação da missão Inspiration4'

    def handle(self, *args, **options):

        astronauts = [

            {
                'full_name': 'Jared Isaacman',
                'nationality': 'Estados Unidos',
                'biography': (
                    'Comandante da missão Inspiration4. '
                    'Empresário e piloto, liderou a primeira missão '
                    'orbital totalmente civil.'
                ),
            },

            {
                'full_name': 'Hayley Arceneaux',
                'nationality': 'Estados Unidos',
                'biography': (
                    'Oficial médica da missão Inspiration4. '
                    'Assistente médica no St. Jude Children’s '
                    'Research Hospital.'
                ),
            },

            {
                'full_name': 'Sian Proctor',
                'nationality': 'Estados Unidos',
                'biography': (
                    'Piloto da missão Inspiration4. '
                    'Geocientista, educadora e exploradora.'
                ),
            },

            {
                'full_name': 'Chris Sembroski',
                'nationality': 'Estados Unidos',
                'biography': (
                    'Especialista de missão da Inspiration4. '
                    'Profissional da área aeroespacial e veterano '
                    'da Força Aérea dos Estados Unidos.'
                ),
            },

        ]

        profile_url = 'https://inspiration4.com/crew/'

        source_url = 'https://www.spacex.com/launches/inspiration4/'

        created_count = 0
        updated_count = 0

        for data in astronauts:

            astronaut, created = Astronaut.objects.update_or_create(

                full_name=data['full_name'],

                agency='',

                defaults={
                    'nationality': data['nationality'],
                    'biography': data['biography'],
                    'profile_url': profile_url,
                    'source_url': source_url,
                }

            )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Astronauta cadastrado: {astronaut.full_name}'
                    )
                )

            else:
                updated_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f'Astronauta atualizado: {astronaut.full_name}'
                    )
                )

        self.stdout.write('')

        self.stdout.write(
            self.style.SUCCESS(
                'Importação finalizada!'
            )
        )

        self.stdout.write(
            f'Novos cadastros: {created_count}'
        )

        self.stdout.write(
            f'Registros atualizados: {updated_count}'
        )