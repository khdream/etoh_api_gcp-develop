from food_and_wine_pairing.urls import router
from rest_framework.routers import DefaultRouter
from productspec.views import (
    AromaViewSet,
    AssembleViewSet,
    CategoryLexiconViewSet,
    LexiconViewSet,
    RobeViewSet,
    VintageViewSet,
    WineProfileCDCViewSet,
    WineCDCLexiconViewSet,
)
from productspec.views import (
    DenominationWineViewSet,
    GrapeViewSet,
    GrapeAssemblyViewSet,
    GrapeProfileViewSet,
    WineCDCViewSet,
    SugarDoseViewSet
)


router = DefaultRouter()
router.register(r'grape', GrapeViewSet, basename='grape')
router.register(r'grape_profile', GrapeProfileViewSet,
                basename='grape_profile')
router.register(r'grape_assemble', GrapeAssemblyViewSet,
                basename='grape_assemble')
router.register(r'denomination_wine', DenominationWineViewSet,
                basename='denomination_wine')
router.register(r'sugar_dose', SugarDoseViewSet, basename='sugar_dose')
router.register(r'wine_cdc', WineCDCViewSet, basename='wine_cdc')

router.register(r'assemble', AssembleViewSet, basename='assemble')
router.register(r'robe', RobeViewSet, basename='robe')

router.register(r'wine_profile_cdc', WineProfileCDCViewSet,
                basename='wine_profile_cdc')
router.register(r'vintage', VintageViewSet, basename='vintage')
router.register(r'aroma', AromaViewSet, basename='aroma')
router.register(r'category_lexicon', CategoryLexiconViewSet,
                basename='category_lexicon')
router.register(r'lexicon', LexiconViewSet, basename='lexicon')
router.register(r'wine_cdc_lexicon', WineCDCLexiconViewSet,
                basename='wine_cdc_lexicon')
