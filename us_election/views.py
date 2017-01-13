from django.shortcuts import render


def documentation(request):
    context = {}
    return render(request, 'documentation.html', context)
