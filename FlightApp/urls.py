from django.urls import path

from FlightApp import views

urlpatterns = [
    path('',views.log_fun,name='log'),
    path('reg',views.reg_fun,name='reg'),

    # admin urls
    path('adminhome',views.adminhome_fun,name='adminhome'),
    path('addflights',views.addflights_fun,name='addflights'),
    path('displayflight',views.displayflight_fun,name='displayflight'),
    path('reservation',views.reservation_fun,name='reservation'),
    path('status/<int:id>',views.status_fun,name='status'),
    path('logout',views.logoutadmin_fun,name='logout'),
    
    
    # user urls
    path('findflights',views.findflights_fun,name='findflights'),
    path('bookflight/<int:id>',views.bookflight_fun,name='bookflight'),
    path('displayreservation',views.displayreservation_fun,name='displayreservation'),
    path('userlogout',views.userlogout_fun,name='userlogout')
]