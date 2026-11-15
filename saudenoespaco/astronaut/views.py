
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Count
from django.db import models
from .models import ResearchSubject, HealthRecord, Astronaut
import random

def astronaut_index(request):

    subjects = ResearchSubject.objects.select_related(
        'mission'
    ).order_by('subject_code')

    astronauts = Astronaut.objects.all()

    astronaut_by_code = {
        astronaut.code: astronaut
        for astronaut in astronauts
        if astronaut.code
    }

    cards = [
        {
            'subject': subject,
            'astronaut': astronaut_by_code.get(subject.subject_code),
        }
        for subject in subjects
    ]



    context = {
        'cards': cards,
    }

    return render(request, 'astronaut_index.html', context)


def dashboard(request):

    # 1. Buscar todos os participantes científicos
    subjects = ResearchSubject.objects.select_related(
        'mission'
    ).order_by('subject_code')

    # 2. Identificar o participante selecionado
    subject_code = request.GET.get('subject', 'C001')

    subject = get_object_or_404(
        ResearchSubject,
        subject_code=subject_code
    )

    # 3. Buscar os resultados laboratoriais do participante
    records = HealthRecord.objects.filter(
        subject=subject
    ).order_by(
        'study_code',
        'parameter',
        'timepoint'
    )

    # 4. Separar os resultados por estudo
    cbc_records = records.filter(study_code='OSD-569')
    cmp_records = records.filter(study_code='OSD-575')

    # 5. Preparar um resumo dos estudos
    study_summary = (
        records.values('study_code', 'test_type')
        .annotate(
            total_records=Count('id'),
            total_parameters=Count('parameter', distinct=True),
            total_timepoints=Count('timepoint', distinct=True)
        )
        .order_by('study_code')
    )

    # 6. Contabilizar os resultados

    # 7. Indicadores gerais do participante
    total_parameters = records.values(
        'parameter'
    ).distinct().count()

    total_timepoints = records.values(
        'timepoint'
    ).distinct().count()

    # 8. Resultados com intervalos de referência disponíveis
    records_with_reference = records.filter(
        reference_min__isnull=False,
        reference_max__isnull=False
    )

    # 9. Resultados fora do intervalo de referência
    out_of_range = records_with_reference.filter(
        value__lt=models.F('reference_min')
    ).count() + records_with_reference.filter(
        value__gt=models.F('reference_max')
    ).count()

    # 10. Preparar os dados para o template
    context = {
        'subjects': subjects,
        'selected_subject': subject,

        'records': records,
        'cbc_records': cbc_records,
        'cmp_records': cmp_records,

        'study_summary': study_summary,

        # Indicadores gerais
        'total_records': records.count(),
        'total_cbc': cbc_records.count(),
        'total_cmp': cmp_records.count(),
        'total_parameters': total_parameters,
        'total_timepoints': total_timepoints,
        'out_of_range': out_of_range,
        'records_with_reference': records_with_reference.count(),
    }


    # messages.add_message(
    #     request,
    #     constants.SUCCESS,
    #     'Dados do participante carregados com sucesso!'
    # )

    return render(request, 'dashboard.html', context)


def visor_astronaut(request):

    # 1. Identificar o participante
    subject_code = request.GET.get('subject', 'C001')

    subject = get_object_or_404(
        ResearchSubject,
        subject_code=subject_code
    )

    # 2. Buscar os timepoints disponíveis para o participante
    available_timepoints = list(
        HealthRecord.objects.filter(
            subject=subject
        ).exclude(
            timepoint=''
        ).values_list(
            'timepoint',
            flat=True
        ).distinct()
    )

    # 3. Ordenar os timepoints cronologicamente
    timeline_order = [
        'L-92',
        'L-44',
        'L-3',
        'R+1',
        'R+45',
        'R+82',
        'R+194'
    ]

    timepoints = sorted(
        available_timepoints,
        key=lambda item: (
            timeline_order.index(item)
            if item in timeline_order
            else len(timeline_order)
        )
    )

    # 4. Selecionar o timepoint
    selected_timepoint = request.GET.get('timepoint')

    if selected_timepoint not in timepoints:
        selected_timepoint = timepoints[-1] if timepoints else None

    # 5. Buscar os resultados do timepoint selecionado
    records = HealthRecord.objects.filter(
        subject=subject,
        timepoint=selected_timepoint
    ).order_by(
        'study_code',
        'parameter'
    ) if selected_timepoint else HealthRecord.objects.none()

    # 6. Organizar os resultados em painéis
    study_definitions = [
        {
            'code': 'OSD-569',
            'name': 'Complete Blood Count',
            'category': 'HEMATOLOGY',
        },
        {
            'code': 'OSD-575',
            'name': 'Comprehensive Metabolic Panel',
            'category': 'METABOLIC PROFILE',
        },
    ]

    visor_slides = []

    for study in study_definitions:

        study_records = list(
            records.filter(
                study_code=study['code']
            )
        )

        # Cada painel apresenta até quatro indicadores
        chunks = [
            study_records[i:i + 4]
            for i in range(0, len(study_records), 4)
        ]

        # Mesmo sem resultados, manter um painel informativo
        if not chunks:
            chunks = [[]]

        for index, chunk in enumerate(chunks):

            metrics = []

            for record in chunk:

                value = format(record.value, 'f').rstrip('0').rstrip('.')

                metrics.append({
                    'parameter': record.parameter,
                    'value': value or '0',
                    'unit': record.unit or '',
                    'reference_min': record.reference_min,
                    'reference_max': record.reference_max,
                })

            visor_slides.append({
                'study_code': study['code'],
                'study_name': study['name'],
                'category': study['category'],
                'metrics': metrics,
                'slide_part': index + 1,
                'has_data': bool(metrics),
            })

            
    fatigue_levels = [
        {
            'code': 'cool',
            'label': 'COOL',
            'description': 'LOW FATIGUE',
        },
        {
            'code': 'alert',
            'label': 'ALERT',
            'description': 'MODERATE FATIGUE',
        },
        {
            'code': 'stressed',
            'label': 'STRESSED',
            'description': 'HIGH FATIGUE',
        },
    ]

    fatigue_status = random.choice(fatigue_levels)


    # 7. Preparar os dados para o template
    context = {
        'subject': subject,
        'timepoints': timepoints,
        'selected_timepoint': selected_timepoint,
        'visor_slides': visor_slides,
        'total_records': records.count(),
        'has_records': records.exists(),
        # Mental fatigue
        'fatigue_levels': fatigue_levels,
        'fatigue_status': fatigue_status,
    }

    return render(request, 'visor.html', context)
