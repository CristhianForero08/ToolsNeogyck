from django.shortcuts import render
from .forms import SearchForm
from .models import SearchQuery
from .selenium_scraper import search_google

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            url = form.cleaned_data['url']
            country = form.cleaned_data['country']
            language = form.cleaned_data['language']
            email = form.cleaned_data['email']
            accept_terms = form.cleaned_data['accept_terms']

            # Obtener los primeros 100 resultados
            urls = search_google(keyword, country, language)
            
            # Determinar la posición de la URL, si está presente en los primeros 100 resultados
            try:
                position = urls.index(url) + 1  # Si se encuentra, la posición será index + 1
            except ValueError:
                position = None  # Si no se encuentra la URL, posición será None

            # Guardar la consulta en la base de datos
            SearchQuery.objects.create(
                keyword=keyword,
                url=url,
                position=position,
                country=country,
                language=language,
                email=email,
                accept_terms=accept_terms
            )

            # Preparar mensaje de resultado
            if position is None:
                message = "La página no se encontró en los primeros 100 resultados."
            else:
                message = None

            # Mostrar los primeros 20 resultados de la búsqueda
            top_20_urls = urls[:20]

            return render(request, 'results.html', {
                'urls': top_20_urls, 
                'position': position, 
                'message': message
            })
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
