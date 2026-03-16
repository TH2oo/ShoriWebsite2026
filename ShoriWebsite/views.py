from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Match, Profile



def home(request):
    now = timezone.now()
    next_match = (
        Match.objects
        .filter(datetime__gt=now)
        .select_related('home_team', 'away_team')
        .first()
    )

    context = {}
    if next_match:
        context['match'] = next_match
        context['match_iso'] = next_match.datetime.isoformat()
        context['home_team'] = next_match.home_team
        context['away_team'] = next_match.away_team

    return render(request, 'home.html', context)


def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None
        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error = "Adresse e-mail ou mot de passe incorrect."
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


def application_view(request):
    errors = []
    valid_divisions = ('loisir', 'departemental', 'regional', 'pre-national', 'national')
    success = False

    if request.method == 'POST':
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        division = request.POST.get('division', 'loisir')
        postes = request.POST.getlist('poste')

        if division not in valid_divisions:
            division = 'loisir'

        if not last_name:
            errors.append("Le nom est requis.")
        if not first_name:
            errors.append("Le prenom est requis.")
        if not email:
            errors.append("L'adresse e-mail est requise.")
        if not postes:
            errors.append("Veuillez selectionner au moins un poste.")
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caracteres.")
        if password != password2:
            errors.append("Les mots de passe ne correspondent pas.")
        if User.objects.filter(email=email).exists():
            errors.append("Cette adresse e-mail est deja utilisee.")

        if not errors:
            # Pour l'instant, on simule juste l'envoi a faire
            success = True

    return render(request, 'form.html', {'errors': errors, 'success': success})

def profil_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'profil.html', {'profile': profile})

