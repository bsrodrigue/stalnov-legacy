from .models import Genre

def genres(request):
    genres = Genre.objects.all()
    return {
        'genres': genres,
    }
