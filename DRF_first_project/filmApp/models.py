from django.db import models

class Aktyor(models.Model):
    J = (
        ('Male', 'Male'),
        ('Famale', 'Famale')
    )
    ism = models.CharField(max_length=50)
    davlat = models.CharField(max_length=50, blank=True, null=True)
    jins = models.CharField(max_length=10, choices=J, blank=True, null=True)
    tugilgan_sana = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.ism

class Kino(models.Model):
    J = (
        ('Fantastik', 'Fantastik'),
        ('Ilmiy', 'Ilmiy'),
        ('Tarixiy', 'Tarixiy'),
        ('Badiiy', 'Badiiy'),
        ('Komediya', 'Komediya')
    )
    nom = models.CharField(max_length=100)
    janr = models.CharField(max_length=20, choices=J, blank=True, null=True)
    yil = models.DateField(blank=True, null=True)
    aktyorlar = models.ManyToManyField(Aktyor)
    def __str__(self):
        return self.nom

class Tarif(models.Model):
    nom = models.CharField(max_length=50)
    davomiylik = models.CharField(max_length=100)
    narx = models.CharField(max_length=50)
    def __str__(self):
        return self.nom