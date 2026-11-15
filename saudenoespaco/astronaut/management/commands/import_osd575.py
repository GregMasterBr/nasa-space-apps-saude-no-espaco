
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

    help = 'Importa os resultados do CMP do estudo OSD-575.'

    CSV_DIR = (
        Path(settings.BASE_DIR)
        / 'data'
        / 'raw'
        / 'inspiration4'
        / 'OSD-575'
    )

    STUDY_CODE = 'OSD-575'

    SOURCE_URL = (
        'https://osdr.nasa.gov/bio/repo/data/studies/OSD-575'
    )

    # Estrutura: nome do parâmetro, coluna do resultado,
    # coluna da referência mínima, coluna da referência máxima,
    # unidade.

    PARAMETERS = [
        (
            'ALBUMIN',
            'albumin_value_gram_per_deciliter',
            'albumin_range_min_gram_per_deciliter',
            'albumin_range_max_gram_per_deciliter',
            'g/dL',
        ),
        (
            'ALBUMIN TO GLOBULIN RATIO',
            'albumin_to_globulin_ratio_value',
            'albumin_to_globulin_ratio_range_min',
            'albumin_to_globulin_ratio_range_max',
            '',
        ),
        (
            'ALKALINE PHOSPHATASE',
            'alkaline_phosphatase_value_units_per_liter',
            'alkaline_phosphatase_range_min_units_per_liter',
            'alkaline_phosphatase_range_max_units_per_liter',
            'U/L',
        ),
        (
            'ALT',
            'alt_value_units_per_liter',
            'alt_range_min_units_per_liter',
            'alt_max_units_per_liter',
            'U/L',
        ),
        (
            'AST',
            'ast_value_units_per_liter',
            'ast_range_min_units_per_liter',
            'ast_max_units_per_liter',
            'U/L',
        ),
        (
            'TOTAL BILIRUBIN',
            'total_bilirubin_value_milligram_per_deciliter',
            'total_bilirubin_range_min_milligram_per_deciliter',
            'total_bilirubin_range_max_milligram_per_deciliter',
            'mg/dL',
        ),
        (
            'BUN TO CREATININE RATIO',
            'bun_to_creatinine_ratio_value',
            'bun_to_creatinine_ratio_range_min',
            'bun_to_creatinine_ratio_range_max',
            '',
        ),
        (
            'CALCIUM',
            'calcium_value_milligram_per_deciliter',
            'calcium_range_min_milligram_per_deciliter',
            'calcium_range_max_milligram_per_deciliter',
            'mg/dL',
        ),
        (
            'CARBON DIOXIDE',
            'carbon_dioxide_value_millimol_per_liter',
            'carbon_dioxide_range_min_millimol_per_liter',
            'carbon_dioxide_range_max_millimol_per_liter',
            'mmol/L',
        ),
        (
            'CHLORIDE',
            'chloride_value_millimol_per_liter',
            'chloride_range_min_millimol_per_liter',
            'chloride_range_max_millimol_per_liter',
            'mmol/L',
        ),
        (
            'CREATININE',
            'creatinine_value_milligram_per_deciliter',
            'creatinine_range_min_milligram_per_deciliter',
            'creatinine_range_max_milligram_per_deciliter',
            'mg/dL',
        ),
        (
            'EGFR AFRICAN AMERICAN',
            'egfr_african_american_value_milliliter_per_minute_per_1.73_meter_squared',
            'egfr_african_american_range_min_milliliter_per_minute_per_1.73_meter_squared',
            'egfr_african_american_range_max_milliliter_per_minute_per_1.73_meter_squared',
            'mL/min/1.73m²',
        ),
        (
            'EGFR NON AFRICAN AMERICAN',
            'egfr_non_african_american_value_milliliter_per_minute_per_1.73_meter_squared',
            'egfr_non_african_american_range_min_milliliter_per_minute_per_1.73_meter_squared',
            'egfr_non_african_american_range_max_milliliter_per_minute_per_1.73_meter_squared',
            'mL/min/1.73m²',
        ),
        (
            'GLOBULIN',
            'globulin_value_gram_per_deciliter',
            'globulin_range_min_gram_per_deciliter',
            'globulin_range_max_gram_per_deciliter',
            'g/dL',
        ),
        (
            'GLUCOSE',
            'glucose_value_milligram_per_deciliter',
            'glucose_range_min_milligram_per_deciliter',
            'glucose_range_max_milligram_per_deciliter',
            'mg/dL',
        ),
        (
            'POTASSIUM',
            'potassium_value_millimol_per_liter',
            'potassium_range_min_millimol_per_liter',
            'potassium_range_max_millimol_per_liter',
            'mmol/L',
        ),
        (
            'TOTAL PROTEIN',
            'total_protein_value_gram_per_deciliter',
            'total_protein_range_min_gram_per_deciliter',
            'total_protein_range_max_gram_per_deciliter',
            'g/dL',
        ),
        (
            'SODIUM',
            'sodium_value_millimol_per_liter',
            'sodium_range_min_millimol_per_liter',
            'sodium_range_max_millimol_per_liter',
            'mmol/L',
        ),
        (
            'UREA NITROGEN (BUN)',
            'urea_nitrogen_bun_value_milligram_per_deciliter',
            'urea_nitrogen_bun_range_min_milligram_per_deciliter',
            'urea_nitrogen_bun_range_max_milligram_per_deciliter',
            'mg/dL',
        ),
    ]

    MISSING_VALUES = {'', 'NA', 'N/A', 'NAN', 'NULL'}

    def parse_decimal(self, raw_value, line_number, column_name):

        value = str(raw_value or '').strip()

        if value.upper() in self.MISSING_VALUES:
            return None

        try:
            return Decimal(value)
        except InvalidOperation:
            raise CommandError(
                f'Valor inválido na linha {line_number}, '
                f'coluna {column_name}: {value}'
            )

    def find_csv_file(self):

        if not self.CSV_DIR.exists():
            raise CommandError(
                f'Diretório não encontrado: {self.CSV_DIR}'
            )

        files = list(self.CSV_DIR.glob('*.csv'))

        metabolic_files = [
            file for file in files
            if 'metabolic' in file.name.lower()
            or 'cmp' in file.name.lower()
        ]

        if len(metabolic_files) == 1:
            return metabolic_files[0]

        if len(files) == 1:
            return files[0]

        if not files:
            raise CommandError(
                f'Nenhum CSV encontrado em: {self.CSV_DIR}'
            )

        names = '\n'.join(file.name for file in files)

        raise CommandError(
            'Mais de um CSV encontrado. Deixe somente o arquivo '
            f'do CMP na pasta ou ajuste o importador:\n{names}'
        )

    def handle(self, *args, **options):

        csv_path = self.find_csv_file()

        self.stdout.write(f'Arquivo encontrado: {csv_path.name}')

        try:
            mission = Mission.objects.get(name='Inspiration4')
        except Mission.DoesNotExist:
            raise CommandError(
                'Missão Inspiration4 não encontrada.'
            )

        created_count = 0
        updated_count = 0
        skipped_count = 0
        sample_count = 0

        with csv_path.open(
            mode='r',
            encoding='utf-8-sig',
            newline=''
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            required_columns = {'Sample Name'}

            for parameter in self.PARAMETERS:
                required_columns.update(parameter[1:4])

            missing_columns = (
                required_columns - set(reader.fieldnames or [])
            )

            if missing_columns:
                raise CommandError(
                    'Colunas ausentes no CSV:\n'
                    + '\n'.join(sorted(missing_columns))
                )

            with transaction.atomic():

                for line_number, row in enumerate(reader, start=2):

                    sample_name = row['Sample Name'].strip()

                    try:
                        subject_code, sample_type, timepoint = (
                            sample_name.split('_', 2)
                        )
                    except ValueError:
                        raise CommandError(
                            f'Nome de amostra inválido na linha '
                            f'{line_number}: {sample_name}'
                        )

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

                    sample_count += 1

                    for (
                        parameter_name,
                        value_column,
                        min_column,
                        max_column,
                        unit,
                    ) in self.PARAMETERS:

                        value = self.parse_decimal(
                            row[value_column],
                            line_number,
                            value_column
                        )

                        # Sem resultado não criamos registro.
                        if value is None:
                            skipped_count += 1
                            continue

                        reference_min = self.parse_decimal(
                            row[min_column],
                            line_number,
                            min_column
                        )

                        reference_max = self.parse_decimal(
                            row[max_column],
                            line_number,
                            max_column
                        )

                        record, created = (
                            HealthRecord.objects.update_or_create(

                                subject=subject,
                                study_code=self.STUDY_CODE,
                                parameter=parameter_name,
                                timepoint=timepoint,

                                defaults={
                                    'value': value,
                                    'reference_min': reference_min,
                                    'reference_max': reference_max,
                                    'unit': unit,
                                    'test_type': 'CMP',
                                    'sex': '',
                                    'collection_date': None,
                                    'sample_type': sample_type.capitalize(),
                                    'source_url': self.SOURCE_URL,
                                }
                            )
                        )

                        if created:
                            created_count += 1
                        else:
                            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                '\nImportação do OSD-575 concluída!'
            )
        )

        self.stdout.write(f'Arquivo: {csv_path.name}')
        self.stdout.write(f'Amostras processadas: {sample_count}')
        self.stdout.write(f'Registros criados: {created_count}')
        self.stdout.write(f'Registros atualizados: {updated_count}')
        self.stdout.write(f'Resultados ausentes ignorados: {skipped_count}')
        self.stdout.write(
            f'Total de registros válidos: '
            f'{created_count + updated_count}'
        )
