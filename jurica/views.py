# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from jurica.forms import RegisterForm, LoginForm, EditForm, LoginAdminForm
from django.contrib import messages
from jurica.models import Responden,Jawaban
from django import forms
from jurica.MyCustomBackend import MyCustomBackend
from django.contrib.auth.decorators import login_required
from jurica.decorators import tesdeco, ifselesai, ifblmselesai, ifsudahmulai, decoadmin
# Create your views here.
def register(request):
	template = loader.get_template('register.html')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			ne = form.save(commit=False)
			ne.group=getGroup()
			ne.save()
			messages.success(request, 'Pendaftaran berhasil. Silahkan login menggunakan email '+form.cleaned_data.get('email'))
			return redirect('masuk')
	else:
		form = RegisterForm()
	return HttpResponse(template.render({'form': form}, request))

def login(request):
	template = loader.get_template('login.html')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			# form.save()
			mcb=MyCustomBackend()
			r = mcb.authenticate(form.cleaned_data.get('email'))
			if r:
				request.session['id_responden'] = r.id_responden
				if r.stage >0:
					return redirect('pertanyaan')
				else:
					return redirect('/')
			else:
				messages.error(request, 'Email tidak valid')
				return redirect('masuk')
	else:
		form = LoginForm()
	
	# return render(request, 'login.html', {'form': form})
	return HttpResponse(template.render({'form': form}, request))

def loginadmin(request):
	template = loader.get_template('loginadmin.html')
	if request.method == 'POST':
		form = LoginAdminForm(request.POST)
		if form.is_valid():
			# form.save()
			mcb=MyCustomBackend()
			if  mcb.authenticateadmin(form.cleaned_data.get('username'),form.cleaned_data.get('password')):
				request.session['admin'] = 1
				return redirect('admin')
			else:
				messages.error(request, 'Tidak bisa masuk')
				return redirect('masukadmin')
	else:
		form = LoginAdminForm()
	
	# return render(request, 'login.html', {'form': form})
	return HttpResponse(template.render({'form': form}, request))

@tesdeco
def logout(request):
	request.session.flush()
	return redirect('/')

@decoadmin
def logoutadmin(request):
	request.session.flush()
	return redirect('admin')

@tesdeco
def information(request):
	template = loader.get_template('v_informasi.html')
	context = {
		'page': 'Informasi',
		'data': 'Main',
		'dataresponden': Responden.objects.get(id_responden=request.session['id_responden']),
    }

	return HttpResponse(template.render(context, request))


@tesdeco
@ifblmselesai
def finish(request):
	template = loader.get_template('v_selesai.html')
	r = Responden.objects.get(id_responden=request.session['id_responden'])
	context = {
		'page': 'Selesai',
		'data': 'Main',
		'dataresponden': r,
    }
	# print(r.status)
	return HttpResponse(template.render(context, request))

@decoadmin
def admin(request):
	# template = loader.get_template('baseadmin.html')
	# context = {
	# 	'page': 'Admin',
 #    }
	# return HttpResponse(template.render(context, request))
	return redirect('responden')

@tesdeco
@ifselesai
@ifsudahmulai
def questionnaire(request):
	if request.method == 'POST':
		# print request.POST
		failedcounter=0
		contain_last_question=False
		for x in request.POST:
		 	if 'q-' in x:
		 		# print x+' = '+request.POST.get(x)
		 		failedcounter+=submitanswer(request.session['id_responden'], int(x.replace('q-','')),request.POST.get(x))
		 		if str(x) == 'q-19':
		 			contain_last_question=True
		r = Responden.objects.get(id_responden=request.session['id_responden'])

		if failedcounter:
			r.failedcounter+=1
			r.score-= 25
			if r.failedcounter<3:
				messages.error(request, 'Jawaban anda salah, masih ada '+str(3-r.failedcounter)+' kesempatan tersisa.')
			else:
				r.end=timezone.now()
				r.status=3
				messages.error(request, 'Tidak dapat melanjutkan.')
		else:
			r.failedcounter=0
			if contain_last_question:
				r.end=timezone.now()
				r.status=2
		r.save()
		if not r.failedcounter:
			r.stage+=1
			r.save()
		
	lists={}
	template = loader.get_template('v_pertanyaan.html')
	context = {
		'page': 'Pertanyaan',
		'data': 'Main',
		'list123': [1,2,3],
		'list14': [1,4],
		'list25': [2,5],
		'list36': [3,6],
		'dataresponden': Responden.objects.get(id_responden=request.session['id_responden']),
    }

	if request.method == 'POST':
		return redirect('pertanyaan')
	else:
		return HttpResponse(template.render(context, request))

from django.utils import timezone
@tesdeco
def start(request):
	r= Responden.objects.get(id_responden=request.session['id_responden'])
	if not r.stage:
		r.start=timezone.now()
		r.stage=1
		r.save()
	return redirect('pertanyaan')

import operator
def getGroup():
	g={}
	g[1]=0
	g[2]=0
	g[3]=0
	g[4]=0
	g[5]=0
	g[6]=0
	rS = Responden.objects.all()
	for r in rS:
		g[r.group]+=1

	# print(g)

	return min(g.items(), key=operator.itemgetter(1))[0]

def submitanswer(id_r, quest,val):
	isfailed= 0
	anz = [[0 for x in range(15)] for y in range(7)]
	
	anz[1]=[0,1,1,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	anz[2]=[0,1,1,1,2,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
	anz[3]=[0,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
	anz[4]=[0,1,1,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	anz[5]=[0,1,1,1,2,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
	anz[6]=[0,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]

	j = Jawaban()
	j.id_pertanyaan=quest
	j.jawaban=val
	r = Responden.objects.get(id_responden=id_r)
	j.responden=r

	group=r.group

	# print 'group='+str(group)+'| q='+str(quest)+'| result='+str(anz[group][quest])

	if anz[group][quest] is 0:
		r.save()
	elif str(anz[group][quest]) == val:
		r.save()
	else:
		j.nilai= -25
		isfailed= 1
		r.save()

	j.save()
	return isfailed

@decoadmin
def responden(request):
	# print('ini responden')
	template = loader.get_template('a_responden.html')
	context = {'page': 'Responden',}
	return HttpResponse(template.render(context, request))

@decoadmin
def addresponden(request):
	template = loader.get_template('a_responden_edit.html')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			ne = form.save(commit=False)
			ne.group=getGroup()
			ne.save()
			messages.success(request, 'Berhasil mendaftarkan responden baru #'+str(ne.id_responden))
			return redirect('responden')
	else:
		form = RegisterForm()
	return HttpResponse(template.render({'form': form,'page': 'Tambah Responden'}, request))

@decoadmin
def editresponden(request):
	# instance = Responden.objects.get(id_responden=request.GET['id'])
	instance = get_object_or_404(Responden, id_responden=request.GET['id'])
	template = loader.get_template('a_responden_edit.html')
	if request.method == 'POST':
		form = EditForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Berhasil merubah responden #'+str(request.GET['id']))
			return redirect('responden')
	else:
		form = EditForm(instance=instance)
	return HttpResponse(template.render({'form': form,'page': 'Ubah Responden'}, request))

@decoadmin
def detailresponden(request):
	template = loader.get_template('a_responden_detail.html')
	instance = get_object_or_404(Responden, id_responden=request.GET['id'])
	jawabans = Jawaban.objects.filter(responden=instance)
	context = {'page': 'Detail Responden','responden':instance,'jawabans':jawabans}
	return HttpResponse(template.render(context, request))

@decoadmin
def resetresponden(request):
	instance = get_object_or_404(Responden, id_responden=request.GET['id'])
	template = loader.get_template('a_responden_reset.html')
	context = {'page': 'Detail Responden','responden':instance}
	
	if request.method == 'POST':
		jaw = Jawaban.objects.filter(responden=instance)
		jaw.delete()
		instance.status= 1
		instance.score= 100
		instance.stage= 0
		instance.failedcounter= 0
		instance.start= None
		instance.end= None
		instance.save()
		messages.success(request, 'Berhasil mereset responden #'+str(request.POST['reset']))
		return redirect('responden')
	else:
		return HttpResponse(template.render(context, request))
		
@decoadmin
def removeresponden(request):
	instance = get_object_or_404(Responden, id_responden=request.GET['id'])
	template = loader.get_template('a_responden_hapus.html')
	context = {'page': 'HapusResponden', 'responden':instance}
	if request.method == 'POST':
		jaw = Jawaban.objects.filter(responden=instance)
		jaw.delete()
		instance.delete()
		messages.success(request, 'Berhasil menghapus responden #'+str(request.POST['hapus']))
		return redirect('responden')
	else:
		return HttpResponse(template.render(context, request))

@decoadmin
def exportexcel(request):
	responden_aktif= Responden.objects.filter(status=1).count()
	responden_sukses= Responden.objects.filter(status=2).count()
	responden_gagal= Responden.objects.filter(status=3).count()
	responden_total= Responden.objects.count()
	template = loader.get_template('a_exportexcel.html')
	context = {
		'page': 'Export Excel',
		'responden_aktif': responden_aktif,
		'responden_sukses': responden_sukses,
		'responden_gagal': responden_gagal,
		'responden_total': responden_total,
	}
	return HttpResponse(template.render(context, request))

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone

@csrf_exempt
@decoadmin
def table_responden(request):
	response_data = {}

	ord= '-id_responden'
	if request.POST.get("sort[id]", ""):
		ord= '-id_responden' if request.POST.get("sort[id]", "")=='desc' else 'id_responden'
	elif request.POST.get("sort[nama]", ""):
		ord= '-nama' if request.POST.get("sort[nama]", "")=='desc' else 'nama'
	elif request.POST.get("sort[status]", ""):
		ord= '-status' if request.POST.get("sort[status]", "")=='desc' else 'status'
	elif request.POST.get("sort[penyelesaian]", ""):
		ord= '-stage' if request.POST.get("sort[penyelesaian]", "")=='desc' else 'stage'
	elif request.POST.get("sort[daftar]", ""):
		ord= '-created_at' if request.POST.get("sort[daftar]", "")=='desc' else 'created_at'
	elif request.POST.get("sort[group]", ""):
		ord= '-group' if request.POST.get("sort[group]", "")=='desc' else 'group'
	# elif request.POST.get("sort[category]", ""):
	# 	ord= '-category' if request.POST.get("sort[category]", "")=='desc' else 'category'
	# elif request.POST.get("sort[tags]", ""):
	# 	ord= '-tags' if request.POST.get("sort[tags]", "")=='desc' else 'tags'
	data_posts= Responden.objects.filter(nama__icontains=request.POST.get("searchPhrase", "")).all().order_by(ord) 
	response_data['total'] = data_posts.count()
	current= (int(request.POST.get("current", "1"))*int(request.POST.get("rowCount", "10")))-int(request.POST.get("rowCount", "10"))
	rowcount=  (str(response_data['total']) if request.POST.get("rowCount", "10") == '-1' else current+int(request.POST.get("rowCount", "10")))
	response_data['current'] = int(request.POST.get("current", "0"))
	response_data['rowCount'] = int(request.POST.get("rowCount", "10"))
	# print('rowCounta '+str(int(request.POST.get("rowCount", "10"))))
	# print('currenta '+str(int(request.POST.get("current", "0"))))
	# print('current '+str(current))
	# print('rowcount '+str(rowcount))
	data = serializers.serialize("python", data_posts[int(current) : int(rowcount)])
	rows=[]
	rowscount=0
	
	for x in data:
		dt={}
		dt['id']=x['pk']
		dt['nama']=x['fields']['nama']
		clas= 'primary' if x['fields']['status']==1 else ('success' if x['fields']['status']==2 else ('danger' if x['fields']['status']==3 else "-"))
		clas2= 'blue' if x['fields']['status']==1 else ('green' if x['fields']['status']==2 else ('red' if x['fields']['status']==3 else "-"))
		progress=int(float(x['fields']['stage'])/5*100)
		dt['status']= '<span class="badge bg-'+clas2+'">'+('Aktif' if x['fields']['status']==1 else ('Selesai' if x['fields']['status']==2 else ('Gugur' if x['fields']['status']==3 else "Tidak Aktif")))+'</span>'
		dt['penyelesaian']='<div class="progress progress active"><div class="progress-bar progress-bar-'+clas+' progress-bar-striped" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100" style="width: '+str(progress)+'%"><strong>'+str(progress)+'%</strong></div>'
		dt['daftar']=x['fields']['created_at'].strftime("%d %B %Y %H:%M:%S")
		asd='<div class="progress progress-sm active"><div class="progress-bar progress-bar-'+clas+' progress-bar-striped" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100" style="width: '+str(progress)+'%">'+str(progress)+'%</div>'
		dt['group']=x['fields']['group']
		dt['email']=x['fields']['email']
		dt['stage']=str(x['fields']['stage'])+'/5'
		# dt['tags']=x['fields']['tags']
		# dt['category']=x['fields']['category']
		rows.append(dt)
		rowscount += 1
		pass
	response_data['rows']=rows
	return JsonResponse(response_data, safe=False)


import xlwt
@decoadmin
def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report Studi Akuntansi.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Responden')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'nama', 'email', 'nomor_hp', 'jenis_kelamin', 'usia', 'pendidikan', 'program', 'semester', 'masa_kerja', 'status', 'score']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Responden.objects.all().values_list('id_responden', 'nama', 'email', 'nomor_hp', 'jenis_kelamin', 'usia', 'pendidikan', 'program', 'semester', 'masa_kerja', 'status', 'score')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response