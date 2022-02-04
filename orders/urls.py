from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_page", views.login_page, name="login_page"),
    path("register_page", views.register_page, name="register_page"),
    path("addUser", views.addUser, name="addUser"),
    path("login_view", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout"),
    path("order/<step_name>", views.order, name="order"),
    path("disOpt", views.disOpt, name="disOpt"),
    path("completeOrder", views.completeOrder, name="completeOrder"),
    path("placePizzaOrder", views.placePizzaOrder, name="placePizzaOrder"),
    path("delOrder", views.delOrder, name="delOrder"),
    path("track", views.track, name="track"),
    path("addCredit", views.addCredit, name="addCredit"),
    path("updateCredit", views.updateCredit, name="updateCredit"),
    path("checkOut", views.checkOut, name="checkOut"),
    path("trackFood", views.trackFood, name="trackFood"), 
    path("returnBalance", views.returnBalance, name="returnBalance"),
    path("showStatus", views.showStatus, name="showStatus"),
    path("updateStatus", views.updateStatus, name="updateStatus")
]
