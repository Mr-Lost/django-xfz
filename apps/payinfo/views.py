from django.shortcuts import render


def payinfo_index(request):
    return render(request, 'payinfo/payinfo.html')
