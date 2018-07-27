from django.shortcuts import render


def test(request):
    test = 1

    return render(request, 'base.html', {"test": test})