from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import forms

# Create your views here.

def index(request):

    form = forms.FormName()

    if request.method == "POST":

        form = forms.FormName(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['file']
            file_data = csv_file.read().decode("utf-8")
            request.session['csv_data'] = [s.split('\t') for s in file_data.splitlines()]
            request.session['user'] = form.cleaned_data['user']

            print(f'"VALIDATION SUCCESS!"')
            print("Name: "+ form.cleaned_data['user'])

            return HttpResponseRedirect(reverse('display'))

        else:
            print("ERROR")
            print(form.errors)
    else:
        print("Not a POST request")

    return render(request, 'basicapp/index.html', {'form': form})

def display_page_view(request):

    data = request.session.get('csv_data', 0)
    user = request.session.get('user', 0)

    if data != 0 and user != 0:
        output = '<ol>'
        for x, line in enumerate(data):
            if x == 0:
                continue
            elif line[0] == '':
                continue
            else:
                output += "<li><a href='http://thradiology.dyndns.org:3333/studyList?searchID=" + line[0] + "' target='_blank' rel='noopener'>"
                output += line[1] + '</a>. '
                output += line[2] + '</li> '
        output += '</ol>'

    return render(request, 'basicapp/display_page.html', {'data': data, 'output': output, 'user': user})

