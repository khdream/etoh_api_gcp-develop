from appellation.urls import router
from bottle.views import (
    BottleViewSet,
    BottlePhotoViewSet,
    BottlePriceViewSet,
    NoteGuideViewSet,
    RangeViewSet,
    WineBottleViewSet,
    WineMakerViewSet,
    WineMakerProfileViewSet,
    StockListViewSet,
    StockViewSet,
    WareHouseViewSet,
)


router.register(r'bottle', BottleViewSet, basename='bottle')
router.register(r'wine_bottle', WineBottleViewSet, basename='wine_bottle')
router.register(r'wine_maker', WineMakerViewSet, basename='wine_maker')
router.register(r'wine_maker_profile', WineMakerProfileViewSet,
                basename='wine_maker_profile')
router.register(r'note_guide', NoteGuideViewSet, basename='note_guide')
router.register(r'bottle_price', BottlePriceViewSet, basename='bottle_price')
router.register(r'bottle_photo', BottlePhotoViewSet, basename='bottle_photo')

router.register(r'scale', RangeViewSet, basename='scale')
router.register(r'stock_list', StockListViewSet, basename='stock_list')
router.register(r'warehouse', WareHouseViewSet, basename='warehouse')
router.register(r'stock', StockViewSet, basename='stock')