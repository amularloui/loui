# catalog/serializers.py
from rest_framework import serializers
from .models import Book, BorrowTransaction
from django.contrib.auth.models import User
import datetime

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model  = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        pwd = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if pwd:
            user.set_password(pwd)
            user.save()
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available']

    def validate_copies_available(self, value):
        """
        Ensure copies_available is zero or positive.
        """
        if value < 0:
            raise serializers.ValidationError("Copies available cannot be negative.")
        return value

class BorrowTransactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title    = serializers.CharField(source='book.title',    read_only=True)

    class Meta:
        model  = BorrowTransaction
        fields = [
            'id',
            'user', 'user_username',
            'book', 'book_title',
            'borrow_date',
            'return_date',
            'status'
        ]

    def validate_borrow_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Borrow date cannot be in the future.")
        return value

    def validate_return_date(self, value):
        if value and value < datetime.date.today():
            raise serializers.ValidationError("Return date cannot be before today.")
        return value
    