import random
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from chat.tasks import send_verification_email
User = get_user_model()


class UserRegistrationApiView(APIView):
    def post(self, request):
        user_email = request.data.get('email')

        if not user_email:
            return Response({"error": "Email kiriting!"}, status=400)

        # Har bir so‘rov uchun yangi kod yaratish
        verification_code = random.randint(100000, 999999)


        # saqlash
        cache.set(user_email, verification_code, timeout=300)

        # Kodni saqlash (misol: Redis, DB, yoki vaqtinchalik dict) — bu qadam yetishmayapti

        send_verification_email(user_email, verification_code)

        return Response({"message": "Kod yuborildi!"}, status=200)


class VerifyCodeTokenAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        saved_code = cache.get(email)

        if not saved_code or str(saved_code) != str(code):
            return Response({"error": "Wrong Code.!"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })



