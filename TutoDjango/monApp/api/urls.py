# from monApp.api import views
# 

# urlpatterns = [
#     path('categories/',views.CategorieAPIView.as_view(),name="api-lst-ctgrs"),
#     path('categories/<pk>/',views.CategorieDetailAPIView.as_view(),name="api-dtl-ctgr"),


#     path('produits/',views.ProduitAPIView.as_view(),name="api-lst-prdts"),
#     path('produits/<pk>/',views.ProduitDetailAPIView.as_view(),name="api-dtl-prdt"),

#     path('rayons/',views.RayonAPIView.as_view(),name="api-lst-rayons"),
#     path('rayons/<pk>/',views.RayonDetailAPIView.as_view(),name="api-dtl-rayon"),

#     path('statuts/',views.StatutAPIView.as_view(),name="api-lst-statuts"),
#     path('statuts/<pk>/',views.StatutDetailAPIView.as_view(),name="api-dtl-statut"),

#     path('contenir/',views.ContenirAPIView.as_view(),name="api-lst-contenir"),
#     path('contenir/<pk>/',views.ContenirDetailAPIView.as_view(),name="api-dtl-contenir"),
# ]

from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, ProduitViewSet, RayonViewSet, StatutViewSet, ContenirViewSet
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'rayons', RayonViewSet, basename='rayon')
router.register(r'statuts', StatutViewSet, basename='statut')
router.register(r'contenir', ContenirViewSet, basename='contenir')

urlpatterns = [ 
    path('', include(router.urls)), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]