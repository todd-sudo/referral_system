from rest_framework import serializers

from .models import ReferralUser, SMSCode


class ActivateInviteCodeSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(max_length=6)

    class Meta:
        model = ReferralUser
        fields = [
            "invite_code"
        ]


class ParentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralUser
        fields = ("phone",)


class ChildUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralUser
        fields = ["phone"]


class ReferralUserProfileSerializer(serializers.ModelSerializer):
    parent = ParentUserSerializer(read_only=True)
    childs = serializers.SerializerMethodField()

    def get_childs(self, obj):
        return ChildUserSerializer(
            instance=ReferralUser.objects.filter(parent=obj),
            many=True,
            read_only=True
        ).data

    class Meta:
        model = ReferralUser
        fields = (
            "phone",
            "parent",
            "invite_code",
            "childs",
        )


class ReferralUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralUser
        fields = [
            "phone",
            "invite_code"
        ]


class SendSMSCodeSerializer(serializers.ModelSerializer):
    """ Отправка СМС кода
    """
    class Meta:
        model = ReferralUser
        fields = ["phone"]


class AuthUserSerializer(serializers.ModelSerializer):
    """ Авторизация пользователя(подтверждение СМС кода)
    """
    class Meta:
        model = SMSCode
        fields = ["code"]

