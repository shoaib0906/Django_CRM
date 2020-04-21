from django.urls import path

from . import views
urlpatterns = [
path('login/',views.loginPage ,name ="login"),
path('logout/',views.logoutUser ,name ="logout"),
path('user-profile',views.userprofile,name="user-profile"),
path('register/',views.registration ,name ="register"),
path('user-settings/',views.user_settings,name="user-settings"),

 	path('',views.home ,name="home"),
    path('Products/',views.products ,name ="Products"),
    path('Customers/<str:pk_id>',views.customers,name="Customers"),
    path('create_order/<str:pk>',views.create_order,name="create_order"),
    path('update_order/<str:pk>',views.update_order,name="update_order"),
    path('delete_order/<str:pk>',views.delete_order,name="delete_order"),

]