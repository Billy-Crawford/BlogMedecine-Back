from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import (
    ArticleViewSet, AdminArticleViewSet,  # ← Ajouté ici
    CategorieViewSet, CommentaireViewSet,
    LikeDislikeViewSet, AbonneNewsletterViewSet,
    ArticleDetailView, AdminDashboardStatsView
)

router = DefaultRouter()

# 🟢 Routes publiques
router.register('articles', ArticleViewSet, basename='public-article')
router.register('categories', CategorieViewSet)
router.register('commentaires', CommentaireViewSet)
router.register('reactions', LikeDislikeViewSet)
router.register('abonne-newsletter', AbonneNewsletterViewSet)

# 🔒 Routes admin (ViewSet dédié)
router.register('admin/articles', AdminArticleViewSet, basename='admin-article')

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/dashboard/stats/', AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
]
