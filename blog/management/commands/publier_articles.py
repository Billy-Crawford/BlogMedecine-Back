# blog/management/commands/publier_articles.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Article, AbonneNewsletter
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Publie les articles planifiés et envoie la newsletter"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        articles = Article.objects.filter(
            statut='brouillon',
            date_publication__lte=now
        )

        for article in articles:
            article.statut = 'publie'
            article.save()
            self.stdout.write(f"Article publié : {article.titre}")

        publies = Article.objects.filter(
            statut='publie',
            newsletter_envoyee=False
        )

        for article in publies:
            abonnés = AbonneNewsletter.objects.all()
            emails = [a.email for a in abonnés]

            if emails:
                send_mail(
                    subject=f"📰 Nouveau post sur le blog : {article.titre}",
                    message=f"Un nouvel article est publié : {article.titre}\n\n"
                            f"Lisez-le ici : https://votre-site.com/articles/{article.slug}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=emails,
                    fail_silently=False,
                )

                article.newsletter_envoyee = True
                article.save()
                self.stdout.write(f"Newsletter envoyée pour : {article.titre}")
