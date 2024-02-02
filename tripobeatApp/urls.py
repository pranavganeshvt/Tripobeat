from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tripobeatApp'
#url patterns has list of all urls corresponding to the views and the webpages
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('home/', views.alternate_page, name = 'alternate_page'),
    path('blog/', views.blog_page, name = 'blog_page'),
    path('itineraries/', views.category_page, name = 'category_page'),
    path('itineraries/<int:itinerary_id>/', views.item_page, name = 'item_page'),
    path('itineraries/search/', views.search_result, name = 'search_result'),
    path('itineraries/add/', views.add_category, name='add_category'),
    path('itineraries/<int:itinerary_id>/delete/', views.delete_category, name = 'delete_category'),
    path('itineraries/<int:itinerary_id>/edit/', views.edit_category, name = 'edit_category'),
    path('itineraries/add_item/', views.add_item_page, name='add_item_page'),
    path('get_other_blogs/', views.get_other_blogs, name='get_other_blogs'),
    path('itineraries/<int:itinerary_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('itineraries/<int:itinerary_id>/edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
