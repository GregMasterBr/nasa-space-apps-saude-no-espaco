
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from saudenoespaco.astronaut.models import (
    Mission,
    ResearchSubject,
    HealthRecord,
)


class Command(BaseCommand):

    help = 'Importa os resultados do hemograma CBC do estudo OSD-569.'

    FILE_PATH = (
        Path(settings.BASE_DIR)
        / 'data'
        / 'raw'
        / 'inspiration4'
        / 'OSD-569'
        / 'LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv'
    )

    STUDY_CODE = 'OSD-569'

    SOURCE_URL = (
        'https://osdr.nasa.gov/geode-py/ws/studies/OSD-569/'
        'download?file=LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv'
        '&version=1'
    )

    REQUIRED_COLUMNS = [
        'ANALYTE',
        'VALUE',
        'RANGE_MIN',
        'RANGE_MAX',
        'UNITS',
        'TEST_TYPE',
        'SUBJECT_ID',
        'SEX',
        'TEST_DATE',
    ]

    def handle(self, *args, **options):

        if not self.FILE_PATH.exists():
            raise CommandError(
                f'Arquivo CSV não encontrado: {self.FILE_PATH}'
            )

        try:
            mission = Mission.objects.get(name='Inspiration4')
        except Mission.DoesNotExist:
            raise CommandError(
                'Missão Inspiration4 não encontrada. '
                'Execute primeiro o importador da missão.'
            )

        created_count = 0
        updated_count = 0

        with self.FILE_PATH.open(
            mode='r',
            encoding='utf-8-sig',
            newline=''
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            missing_columns = (
                set(self.REQUIRED_COLUMNS) - set(reader.fieldnames or [])
            )

            if missing_columns:
                raise CommandError(
                    f'Colunas ausentes no CSV: {missing_columns}'
                )

            with transaction.atomic():

                for line_number, row in enumerate(reader, start=2):

                    subject_code = row['SUBJECT_ID'].strip()

                    try:
                        subject = ResearchSubject.objects.get(
                            mission=mission,
                            subject_code=subject_code
                        )
                    except ResearchSubject.DoesNotExist:
                        raise CommandError(
                            f'Participante {subject_code} não encontrado '
                            f'na linha {line_number}.'
                        )

                    try:
                        value = Decimal(row['VALUE'])
                        reference_min = Decimal(row['RANGE_MIN'])
                        reference_max = Decimal(row['RANGE_MAX'])
                    except (InvalidOperation, TypeError):
                        raise CommandError(
                            f'Valor numérico inválido na linha {line_number}.'
                        )

                    record, created = HealthRecord.objects.update_or_create(

                        subject=subject,
                        study_code=self.STUDY_CODE,
                        parameter=row['ANALYTE'].strip(),
                        timepoint=row['TEST_DATE'].strip(),

                        defaults={
                            'value': value,
                            'reference_min': reference_min,
                            'reference_max': reference_max,
                            'unit': row['UNITS'].strip(),
                            'test_type': row['TEST_TYPE'].strip(),
                            'sex': row['SEX'].strip(),
                            'collection_date': None,
                            'sample_type': '',
                            'source_url': self.SOURCE_URL,
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                '\nImportação do OSD-569 concluída!'
            )
        )

        self.stdout.write(f'Registros criados: {created_count}')
        self.stdout.write(f'Registros atualizados: {updated_count}')
        self.stdout.write(
            f'Total processado: {created_count + updated_count}'
        )
