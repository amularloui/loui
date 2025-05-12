# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # User management
    path('users/', views.user_list_create),
    path('users/<int:pk>/', views.user_update_delete),

    # Book management
    path('books/', views.book_list_create),
    path('books/<int:pk>/', views.book_update_delete),

    # Borrow/list transactions
    path('transactions/', views.transaction_list),      # GET only
    path('borrow/', views.borrow_book),                # POST only

    # Return
    path('return/<int:txn_id>/', views.return_book),   # POST only
]

