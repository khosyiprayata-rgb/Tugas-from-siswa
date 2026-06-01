from django.db import models

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    umur = models.IntegerField()
    tanggal_lahir = models.DateField()
    status_hadir = models.CharField(max_length=20)
    nilai_akhir = models.IntegerField() 