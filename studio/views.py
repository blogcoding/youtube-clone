from django.shortcuts import render


def StudioIndexView(request):
    return render(request, 'studio/index.html', {})
