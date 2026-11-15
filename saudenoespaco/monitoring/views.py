
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import EmotionalCheckInForm
from .models import EmotionalCheckIn


@login_required
def home_monitoring(request):

    # 1. Identificar o participante associado ao usuário
    subject = getattr(request.user, 'research_subject', None)

    # 2. Verificar se existe participante associado
    if subject is None:
        messages.error(
            request,
            'Sua conta não está vinculada a um participante científico.'
        )

        return render(request, 'index.html', {
            'subject': None,
            'form': EmotionalCheckInForm(),
            'checkins': [],
        })

    # 3. Processar o envio do formulário
    if request.method == 'POST':

        form = EmotionalCheckInForm(request.POST)

        if form.is_valid():

            checkin = form.save(commit=False)

            # Associar automaticamente ao participante autenticado
            checkin.subject = subject

            checkin.save()

            messages.success(
                request,
                'Seu check-in emocional foi registrado com sucesso!'
            )

            return redirect('home_monitoring')

    else:
        form = EmotionalCheckInForm()

    # 4. Buscar os últimos registros emocionais
    checkins = EmotionalCheckIn.objects.filter(
        subject=subject
    ).order_by('-created_at')[:10]

    # 5. Preparar os dados para o template
    context = {
        'subject': subject,
        'form': form,
        'checkins': checkins,
    }

    return render(request, 'monitoring_index.html', context)
