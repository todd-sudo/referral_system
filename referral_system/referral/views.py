import datetime
import random
import string
import uuid

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework import status, permissions, parsers

from .serializers import (
    ActivateInviteCodeSerializer,
    ReferralUserDetailSerializer,
    ReferralUserProfileSerializer,
    SendSMSCodeSerializer,
    AuthUserSerializer,
)
from .models import ReferralUser
from .utils import create_task_message_send, local_tz


class ActivateInviteCodeView(CreateAPIView):
    """ Активация инвайт кода

    create:

        invite_code: Инвайт код
    """
    serializer_class = ActivateInviteCodeSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        invite_code = dict(serializer.data).get("invite_code")
        try:
            # me = ReferralUser.objects.get(phone=request.META.get('HTTP_PHONE'))
            me = ReferralUser.objects.get(phone=request.session["phone"])
        except ReferralUser.DoesNotExist:
            return Response(
                {"detail": "Unauthorized", "error": "Проверьте данные"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if me.parent is not None:
            return Response(
                {"detail": "У вас уже есть активированный invite code"},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )
        try:
            parent = ReferralUser.objects.get(invite_code=invite_code)
        except ReferralUser.DoesNotExist:
            return Response(
                {"detail": "Пользователя с таким invite code нет"},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )
        me.parent = parent
        me.save()

        return Response(
            ReferralUserDetailSerializer(me).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ProfileView(RetrieveAPIView):
    """ Профиль пользователя

    retrieve:

        id: ID пользователя
    """
    queryset = ReferralUser.objects.select_related("parent")
    serializer_class = ReferralUserProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # current_user_phone = request.META.get('HTTP_PHONE')
        current_user_phone = request.session["phone"]
        if current_user_phone == instance.phone:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )


class SendCodeSMSView(CreateAPIView):
    """ Авторизация пользователя
    """
    serializer_class = SendSMSCodeSerializer
    queryset = ReferralUser.objects.all()
    parser_classes = (parsers.MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        phone = dict(serializer.data).get("phone")
        code = random.randint(1000, 9999)
        request.session["phone"] = phone
        request.session["code"] = code

        # имитация задержки сервера
        delay = datetime.timedelta(seconds=3)
        now = datetime.datetime.now(tz=local_tz)
        date_start = now + delay

        # создает задачу для отправки СМС
        create_task_message_send(
            name_task=f"task_{uuid.uuid4().hex}",
            phone=phone,
            code=code,
            # время отправки СМС(имитация задержки сервера)
            start_time=date_start,
        )
        # в тестовых целях
        data = dict(serializer.data)
        data["sms_code"] = code
        print(data)
        return Response(
            data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class ActivateSMSCode(CreateAPIView):
    """ Активация SMS кода, авторизация и добавление пользователя в БД
    """
    serializer_class = AuthUserSerializer
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        # current_user_phone = request.META.get('HTTP_PHONE')
        current_user_phone = request.session["phone"]
        input_sms_code = dict(serializer.data).get("code")
        sms_code = request.session["code"]

        if input_sms_code == sms_code:
            try:
                user = ReferralUser.objects.get(phone=current_user_phone)
                _serializer = ReferralUserProfileSerializer(user)
                return Response(
                    _serializer.data,
                    status=status.HTTP_200_OK,
                    headers=headers
                )
            except ReferralUser.DoesNotExist:
                invite_code = "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=6)
                )
                user = ReferralUser.objects.create(
                    phone=current_user_phone,
                    invite_code=invite_code
                )
                _serializer = ReferralUserProfileSerializer(user)
                return Response(
                    _serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )

        return Response(
            {"detail": "Incorrect SMS code"},
            status=status.HTTP_400_BAD_REQUEST,
            headers=headers
        )
