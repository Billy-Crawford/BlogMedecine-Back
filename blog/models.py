import os.path
from datetime import datetime
from fileinput import filename

from django.db import models
from django.utils.text import slugify


class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

def article_image_upload_path(instance, filename):
    # Nettoyer le titre
    base_slug = slugify(instance.titre)

    # Extraire l'extension du fichier original
    ext = os.path.splitext(filename)[1]

    # Timestamp pour eviter les doublons
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Nouveau nom de fichier
    new_filename = f"{base_slug}_{timestamp}{ext}"

    # Dossier de destination
    return os.path.join("articles", new_filename)


class Article(models.Model):
    STATUS_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('programme', 'Programmé'),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=article_image_upload_path)
    # image = models.ImageField(upload_to='articles/')
    contenu = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="articles")
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES, default='brouillon')
    date_publication = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    newsletter_envoyee = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    texte = models.CharField(max_length=300)
    ip = models.GenericIPAddressField()
    date_creation = models.DateTimeField(auto_now_add=True)


class LikeDislike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="reactions")
    type = models.CharField(max_length=10)  # 'like' ou 'dislike'
    ip = models.GenericIPAddressField()
    date_creation = models.DateTimeField(auto_now_add=True)


class AbonneNewsletter(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
