from django.utils.text import slugify
from rest_framework import serializers
from .models import Article, Categorie, Commentaire, LikeDislike, AbonneNewsletter

# --- Catégorie
class CategorieSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)  # ← important !

    class Meta:
        model = Categorie
        fields = '__all__'

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['nom'])
        return super().create(validated_data)


# --- Commentaire
class CommentaireSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()  # On affiche des infos utiles sur l'article

    class Meta:
        model = Commentaire
        fields = ['id', 'article', 'texte', 'ip', 'date_creation']
        read_only_fields = ['ip', 'date_creation']

    def get_article(self, obj):
        return {
            'id': obj.article.id,
            'titre': obj.article.titre
        }

class CommentaireCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['article', 'texte']


class CommentaireReadSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = ['id', 'article', 'texte', 'ip', 'date_creation']
        read_only_fields = ['ip', 'date_creation']

    def get_article(self, obj):
        return {
            'id': obj.article.id,
            'titre': obj.article.titre
        }


# --- Article
class ArticleSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all(), write_only=True, source='categorie')
    commentaires = CommentaireSerializer(many=True, read_only=True)  # ⬅ inclus les commentaires ici

    class Meta:
        model = Article
        fields = [
            'id', 'titre', 'slug', 'image', 'contenu',
            'categorie', 'categorie_id',
            'statut', 'date_publication', 'date_creation',
            'commentaires'
        ]

# class AdminArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
#
#         def create(selfself, validated_data):
#             #genere automatiquement le slug a partir du titre
#             titre = validated_data.get('titre', '')
#             validated_data['slug'] = slugify(titre)
#             return super().create(validated_data)


class AdminArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'slug': {'required': False},  # 👈 on dit que ce champ n'est pas requis
        }

    def create(self, validated_data):
        if 'slug' not in validated_data and 'titre' in validated_data:
            validated_data['slug'] = slugify(validated_data['titre'])

        return super().create(validated_data)


# --- Like / Dislike
class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['id', 'article', 'type', 'ip', 'date_creation']

# --- Newsletter
class AbonneNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonneNewsletter
        fields = ['id', 'email', 'date_inscription']
