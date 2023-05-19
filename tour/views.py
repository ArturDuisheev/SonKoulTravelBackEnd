import re

import requests
from django.db.migrations import serializer
from rest_framework import viewsets, status, permissions
from rest_framework import viewsets, status, permissions, mixins, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import telegram
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    TourAddSerializer,
    TourProgramSerializer,
    PriceSerializer,
    TipsSerializer,
    PhotoSerializer,
    BookingPrivateTourSerializer,
    BookingGroupTourSerializer,
    TourDatesSerializer, PriceDetailsCreateSerializer, PriceDetailsSerializer
)
from .models import (
    TourAdd,
    TourProgram,
    Price,
    Tips,
    Photo,
    TourDates,
    BookingGroupTour,
    BookingPrivateTour, PriceDetails, TourDate,
)
from .filters import TourAddFilter


@ratelimit(rate='5/h', block=True)
class TelegramSendMessage(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get("name")
            contacts = request.data.get("email_or_whatsapp")
            if not name:
                raise serializers.ValidationError("Данное поле не может быть пустым")
            if not contacts:
                raise serializers.ValidationError("Данное поле не может быть пустым")
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', contacts) and not re.match(r'^\+[0-9]+$', contacts):
                raise serializers.ValidationError\
                    ("Поле email_or_whatsapp должно быть в формате email или номера WhatsApp")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # Отправка данных в телеграмм
            bot_token = 'BOT TOKEN'
            chat_id = 'CHAT ID'
            message = f'Name: {serializer.data["name"]}\nEmail: {serializer.data["email_or_whatsapp"]}\nDate: {str(serializer.data["date"])}'
            # Отправка данных в телеграм
            bot_token = '5964377497:AAEXxcJ745bQpNUpB2neHIjMMkf0IBF5mn4'
            chat_id = '860389338'
            message = f'Name: {serializer.data["name"]}\n' \
                      f'Contacts: {serializer.data["email_or_whatsapp"]}\n' \
                      f'Date: {str(serializer.data["date_str"])}'
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
            requests.post(url)

            headers = self.get_success_headers(serializer.data)

            response_data = {
                "message": "Your request has been successfully submitted! A manager will contact you soon.",
            }

            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            response_data = {
                "message": str(e),
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response_data = {
                "message": "Your request has not been successfully submitted! Please try again later.",
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class TourAddViewSet(viewsets.ModelViewSet):
    queryset = TourAdd.objects.all()
    serializer_class = TourAddSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourAddFilter

    def create(self, request):
        serializer = TourAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responce_201 = {
                "message": "Tour added successfully",
            }
            return Response(responce_201, status=status.HTTP_201_CREATED)
        response_400 = {
            "message": "Tour not added",
        }
        return Response(response_400, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            tour = TourAdd.objects.get(pk=pk)
            serializer = TourAddSerializer(tour, data=request.data)
            if serializer.is_valid():
                serializer.save()
                responce_200 = {
                    "message": "Tour updated successfully",
                }
                return Response(responce_200, status=status.HTTP_200_OK)
            response_400 = {
                "message": "Tour not updated",
            }
            return Response(response_400, status=status.HTTP_400_BAD_REQUEST)
        except TourAdd.DoesNotExist:
            responce_404 = {
                "message": "Tour not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            tour = TourAdd.objects.get(pk=pk)
            tour.delete()
            responce_204 = {
                "message": "Tour deleted successfully",
            }
            return Response(responce_204, status=status.HTTP_204_NO_CONTENT)
        except TourAdd.DoesNotExist:
            responce_404 = {
                "message": "Tour not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)


class TourProgramViewSet(viewsets.ModelViewSet):
    queryset = TourProgram.objects.all()
    serializer_class = TourProgramSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = TourProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responce_201 = {
                "message": "Program added successfully",
            }
            return Response(responce_201, status=status.HTTP_201_CREATED)
        response_400 = {
            "message": "Program not added",
        }
        return Response(response_400, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            program = TourProgram.objects.get(pk=pk)
            serializer = TourProgramSerializer(program, data=request.data)
            if serializer.is_valid():
                serializer.save()
                responce_200 = {
                    "message": "Program updated successfully",
                }
                return Response(responce_200, status=status.HTTP_200_OK)
            response_400 = {
                "message": "Program not updated",
            }
            return Response(response_400, status=status.HTTP_400_BAD_REQUEST)
        except TourProgram.DoesNotExist:
            responce_404 = {
                "message": "Program not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            program = TourProgram.objects.get(pk=pk)
            program.delete()
            responce_204 = {
                "message": "Program deleted successfully",
            }
            return Response(responce_204, status=status.HTTP_204_NO_CONTENT)
        except TourProgram.DoesNotExist:
            responce_404 = {
                "message": "Program not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responce_201 = {
                "message": "Price added successfully",
            }
            return Response(responce_201, status=status.HTTP_201_CREATED)
        response_400 = {
            "message": "Price not added",
        }
        return Response(response_400, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            price = Price.objects.get(pk=pk)
            serializer = PriceSerializer(price, data=request.data)
            if serializer.is_valid():
                serializer.save()
                responce_200 = {
                    "message": "Price updated successfully",
                }
                return Response(responce_200, status=status.HTTP_200_OK)
            response_400 = {
                "message": "Price not updated",
            }
            return Response(response_400, status=status.HTTP_400_BAD_REQUEST)
        except Price.DoesNotExist:
            responce_404 = {
                "message": "Price not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            price = Price.objects.get(pk=pk)
            price.delete()
            responce_204 = {
                "message": "Price deleted successfully",
            }
            return Response(responce_204, status=status.HTTP_204_NO_CONTENT)
        except Price.DoesNotExist:
            responce_404 = {
                "message": "Price not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)


class PriceDetailsCreateViewSet(viewsets.ViewSet):
    serializer_class = PriceDetailsCreateSerializer
    permission_classes = (permissions.AllowAny, )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        person = serializer.validated_data['person']
        per_person = serializer.validated_data['per_person']

        in_com = per_person * person
        serializer.validated_data['in_com'] = in_com

        PriceDetails = serializer.save()

        return Response({
            'id': PriceDetails.id,
            'person': person,
            'in_com': in_com,
            'per_person': per_person
        }, status=status.HTTP_201_CREATED)


class PriceDetailsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PriceDetails.objects.all()
    serializer_class = PriceDetailsSerializer
    permission_classes = (permissions.AllowAny, )


class TipsViewSet(viewsets.ModelViewSet):
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = TipsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responce_201 = {
                "message": "Tips added successfully",
            }
            return Response(responce_201, status=status.HTTP_201_CREATED)
        response_400 = {
            "message": "Tips not added",
        }
        return Response(response_400, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            tips = Tips.objects.get(pk=pk)
            serializer = TipsSerializer(tips, data=request.data)
            if serializer.is_valid():
                serializer.save()
                responce_200 = {
                    "message": "Tips updated successfully",
                }
                return Response(responce_200, status=status.HTTP_200_OK)
            response_400 = {
                "message": "Tips not updated",
            }
            return Response(response_400, status=status.HTTP_400_BAD_REQUEST)
        except Tips.DoesNotExist:
            responce_404 = {
                "message": "Tips not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            tips = Tips.objects.get(pk=pk)
            tips.delete()
            responce_204 = {
                "message": "Tips deleted successfully",
            }
            return Response(responce_204, status=status.HTTP_204_NO_CONTENT)
        except Tips.DoesNotExist:
            responce_404 = {
                "message": "Tips not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responce_201 = {
                "message": "Photo added successfully",
            }
            return Response(responce_201, status=status.HTTP_201_CREATED)
        response_400 = {
            "message": "Photo not added",
        }
        return Response(response_400, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            serializer = PhotoSerializer(photo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                responce_200 = {
                    "message": "Photo updated successfully",
                }
                return Response(responce_200, status=status.HTTP_200_OK)
            response_400 = {
                "message": "Photo not updated",
            }
            return Response(response_400, status=status.HTTP_400_BAD_REQUEST)
        except Photo.DoesNotExist:
            responce_404 = {
                "message": "Photo not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            photo.delete()
            responce_204 = {
                "message": "Photo deleted successfully",
            }
            return Response(responce_204, status=status.HTTP_204_NO_CONTENT)
        except Photo.DoesNotExist:
            responce_404 = {
                "message": "Photo not found",
            }
            return Response(responce_404, status=status.HTTP_404_NOT_FOUND)


class TourDateViewSet(viewsets.ModelViewSet):
    queryset = TourDates.objects.all()
    serializer_class = TourDatesSerializer
    permission_classes = [IsSuperuser | permissions.IsAuthenticatedOrReadOnly]


# -*- coding: utf-8 -*-
class BookingPrivateTourViewSet(viewsets.ModelViewSet):
    queryset = BookingPrivateTour.objects.all()
    serializer_class = BookingPrivateTourSerializer


class BookingGroupTourViewSet(viewsets.ModelViewSet):
    queryset = BookingGroupTour.objects.all()
    serializer_class = BookingGroupTourSerializer


class TourDatesCreateViewSet(viewsets.ModelViewSet):
    queryset = TourDate.objects.all()
    serializer_class = TourDatesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





