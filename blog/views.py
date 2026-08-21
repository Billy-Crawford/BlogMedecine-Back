from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveAPIView
from .models import Article, Categorie, Commentaire, LikeDislike, AbonneNewsletter
from .serializers import (
    ArticleSerializer, CategorieSerializer, CommentaireSerializer,
    LikeDislikeSerializer, AbonneNewsletterSerializer, AdminArticleSerializer, CommentaireCreateSerializer,
    CommentaireReadSerializer
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(statut="publie")  # ← Par défaut, on ne montre que les articles publiés
    serializer_class = ArticleSerializer
    lookup_field = 'slug'  # ← Utiliser le slug dans l’URL
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre', 'categorie__nom']

    def get_queryset(self):
        # Permet de filtrer dynamiquement via ?statut=xxx
        statut = self.request.query_params.get('statut')
        if statut:
            return Article.objects.filter(statut=statut)
        return Article.objects.filter(statut="publie")  # ← Par défaut : que les publiés


class AdminArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = AdminArticleSerializer
    permission_classes = [IsAdminUser]


class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.filter(statut="publie")
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("DONNÉES REÇUES :", request.data)
        return super().create(request, *args, **kwargs)


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentaireCreateSerializer
        return CommentaireReadSerializer

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip=ip)



class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip=ip)


class AbonneNewsletterViewSet(viewsets.ModelViewSet):
    queryset = AbonneNewsletter.objects.all()
    serializer_class = AbonneNewsletterSerializer
    permission_classes = [AllowAny]


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        articles_publies = Article.objects.filter(
            statut='publie'
        ).count()

        commentaires = Commentaire.objects.count()

        categories = Categorie.objects.count()

        return Response({
            'articles_publies': articles_publies,
            'commentaires': commentaires,
            'categories': categories,
        })

