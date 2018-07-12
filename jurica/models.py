from __future__ import unicode_literals

from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from datetime import datetime, timedelta
class Responden(models.Model):
	REQUIRED_FIELDS = ('user',)
	id_responden= models.AutoField(primary_key=True)
	nama= models.CharField(max_length=100, null=False, default=None)
	email= models.EmailField(unique=True)
	nomor_hp= models.CharField(max_length=20, null=False, default=None)
	jenisKel= (
		('', '- Jenis Kelamin -'),
        (0, 'Laki-Laki'),
        (1, 'Perempuan')
    )
	jenis_kelamin= models.IntegerField(choices=jenisKel, null=False, default=None)
	usia= models.IntegerField(blank=True, null=False, default=None)
	jenisPen= (
		('', '- Jenjang Pendidikan -'),
        (0, 'S1'),
        (1, 'S2')
    )
	pendidikan= models.IntegerField(choices=jenisPen, null=False, default=None)
	jenisPro= (
		('', '- Jurusan -'),
        (0, 'Akuntansi'),
        (1, 'Manajemen')
    )
	program= models.IntegerField(choices=jenisPro, null=False, default=None)
	semester= models.IntegerField(blank=True, null=False, default=None)
	masa_kerja= models.IntegerField(blank=True, null=False, default=None)
	jStatus= (
		# (3, 'gugur'),
		# (2, 'Selesai'),
        (1, 'Aktif'),
        (0, 'Tidak Aktif'),
    )
	status= models.IntegerField(choices=jStatus, null=True, default=1)
	score= models.IntegerField(blank=True, null=True,default=100)
	stage= models.IntegerField(blank=True, null=True,default=0)
	failedcounter= models.IntegerField(blank=True, null=True,default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	start = models.DateTimeField(null=True)
	end = models.DateTimeField(null=True)
	group= models.IntegerField(null=False, default=0)
	def __str__(self):
		return self.nama

	def kesempatan(self):
		return 3-self.failedcounter

	def progress(self):
		return int(round(float(self.stage)/5*100,0))
	def scorefinal(self):
		if self.score <25:
			return 25
		else:
			return self.score
	


	def durasimengerjakan(self):
		result="Belum selesai mengerjakan"
		try:
			aaa= self.end-self.start
			d = datetime(1,1,1) + aaa
			if d.day-1 is not 0:
				result="%d Hari, %d Jam, %d Menit, %d Detik" % (d.day-1, d.hour, d.minute, d.second)
			elif d.hour is not 0:
				result="%d Jam, %d Menit, %d Detik" % (d.hour, d.minute, d.second)
			elif d.minute is not 0:
				result="%d Menit, %d Detik" % (d.minute, d.second)
			else:
				result="%d Detik" % (d.second)
		except Exception as e:
			pass
		return result

class Jawaban(models.Model):
	id_jawaban= models.AutoField(primary_key=True)
	responden= models.ForeignKey(Responden, on_delete=models.SET_NULL,null=True)
	id_pertanyaan= models.IntegerField(blank=True, null=True)
	jawaban = models.TextField(blank=True, null=True)
	nilai = models.IntegerField(blank=True, null=True)
	jStatusJaw= (
        (0, 'Salah'),
        (1, 'Benar')
    )
	status= models.IntegerField(choices=jStatusJaw, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.id_jawaban

	def namapertanyaan(self):
		p = [0 for x in range(20)]
		print(p)
		p[1]='Respon1 #1'
		p[2]='Respon1 #2'
		p[3]='Respon1 #3'
		p[4]='Respon2 #1'
		p[5]='Respon2 #2'
		p[6]='Respon2 #3'
		p[7]='Respon3 #1'
		p[8]='Respon3 #2'
		p[9]='Respon4 #1'
		p[10]='Respon4 #2'
		p[11]='Respon4 #3'
		p[12]='Respon4 #4'
		p[13]='Respon4 #5'
		p[14]='Respon4 #6'
		p[15]='Respon4 #7'
		p[16]='Respon4 #8'
		p[17]='Respon4 #9'
		p[18]='Respon4 #10'
		p[19]='Respon4 #11'

		return p[self.id_pertanyaan]


