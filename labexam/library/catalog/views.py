# catalog/views.py

import datetime
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book, BorrowTransaction
from .serializers import (
    UserSerializer,
    BookSerializer,
    BorrowTransactionSerializer
)

# --- User Management ---

@api_view(['GET', 'POST'])
def user_list_create(request):
    """
    GET: List all users
    POST: Create a new user
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def user_update_delete(request, pk):
    """
    PUT: Update an existing user
    DELETE: Delete a user
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# --- Book Management ---

@api_view(['GET', 'POST'])
def book_list_create(request):
    """
    GET: List all books
    POST: Create a new book
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def book_update_delete(request, pk):
    """
    PUT: Update book details
    DELETE: Delete a book if no active borrows
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if BorrowTransaction.objects.filter(book=book, status='BORROWED').exists():
        return Response(
            {'error': 'Cannot delete: active borrow exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# --- Transaction List (GET only) ---

@api_view(['GET'])
def transaction_list(request):
    """
    GET: List all borrow transactions
    """
    txns = BorrowTransaction.objects.select_related('book', 'user').all()
    serializer = BorrowTransactionSerializer(txns, many=True)
    return Response(serializer.data)


# --- Borrow Book (POST only) ---

@api_view(['POST'])
def borrow_book(request):
    """
    POST: Create a new borrow transaction (updates copies_available)
    """
    serializer = BorrowTransactionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    book = Book.objects.get(pk=serializer.validated_data['book'].id)
    if book.copies_available < 1:
        return Response({'error': 'No copies available'},
                        status=status.HTTP_400_BAD_REQUEST)

    # decrement available copies
    book.copies_available -= 1
    book.save()

    # save the transaction (status defaults to 'BORROWED')
    txn = serializer.save()
    return Response(BorrowTransactionSerializer(txn).data,
                    status=status.HTTP_201_CREATED)


# --- Return Book (POST only) ---

@api_view(['POST'])
def return_book(request, txn_id):
    """
    POST: Mark a borrow as returned (updates return_date and copies_available)
    """
    try:
        txn = BorrowTransaction.objects.get(pk=txn_id, status='BORROWED')
    except BorrowTransaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return_date = request.data.get('return_date')
    payload = {
        'user': txn.user.id,
        'book': txn.book.id if txn.book else None,
        'borrow_date': txn.borrow_date,
        'return_date': return_date,
        'status': 'RETURNED'
    }
    serializer = BorrowTransactionSerializer(txn, data=payload, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # restore available copies
    if txn.book:
        txn.book.copies_available += 1
        txn.book.save()

    txn = serializer.save()
    return Response(BorrowTransactionSerializer(txn).data)
