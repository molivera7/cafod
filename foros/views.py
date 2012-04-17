import operator
import thread
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from forms import *
from models import *
from tagging.models import Tag
from tagging.models import TaggedItem


# Create your views here.

def lista_foro(request):
    discusiones = Foros.objects.all().order_by('-creacion')


    return render_to_response('index.html', locals(), 
    	           context_instance=RequestContext(request))

@login_required
def ver_foro(request, foro_id):
    discusion = get_object_or_404(Foros, id=foro_id)   

    if request.method == 'POST':
        form = AporteForm(request.POST)

        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.foro = discusion
            form_uncommited.save()

            return HttpResponseRedirect('/foros/ver/%d' % discusion.id)
    else:
        form = AporteForm()
    return render_to_response('foros/ver_foro.html', RequestContext(request, locals()))

@login_required
def comentario_foro(request, aporte_id):
    aporte = get_object_or_404(Aportes, id=aporte_id)

    if request.method == 'POST':
        form1 = ComentarioForm(request.POST)
        if form1.is_valid():
            form1_uncommited = form1.save(commit=False)
            form1_uncommited.usuario = request.user
            form1_uncommited.aporte = aporte
            form1_uncommited.save()
            return HttpResponseRedirect('/foros/ver/%d' % aporte.foro_id)
    else:
        form1 = ComentarioForm()
    return render_to_response('foros/comentario.html', RequestContext(request, locals()))

@login_required
def crear_foro(request):
    if request.method == 'POST':
        form = ForosForm(request.POST)
        form2 = ImagenForm(request.POST, request.FILES)
        form3 = DocumentoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()

            form2_uncommitd = form2.save(commit=False)
            form2_uncommitd.content_object = form_uncommited
            form2_uncommitd.save()

            form3_uncommitd = form3.save(commit=False)
            form3_uncommitd.content_object = form_uncommited
            form3_uncommitd.save()

            form4_uncommitd = form4.save(commit=False)
            form4_uncommitd.content_object = form_uncommited
            form4_uncommitd.save()

            form5_uncommitd = form5.save(commit=False)
            form5_uncommitd.content_object = form_uncommited
            form5_uncommitd.save()

            return HttpResponseRedirect('/foros')
            
    else:
        form = ForosForm()
        form2 = ImagenForm()
        form3 = DocumentoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render_to_response('foros/crear_foro.html', RequestContext(request, locals()))

@login_required
def editar_foro(request, id):
    foro = get_object_or_404(Foros, id=id)
    if request.method == 'POST':
        form = ForosForm(request.POST, instance=foro)
        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()
            return HttpResponseRedirect('/foros')
            
    else:
        form = ForosForm(instance=foro)
    return render_to_response('foros/crear_foro.html', RequestContext(request, locals()))

@login_required
def borrar_foro(request, id):
    foro = get_object_or_404(Foros, id=id)
    if foro.user == request.user or request.user.is_superuser:
        foro.delete()
        return redirect('/foros')
    else:
        return redirect('/')