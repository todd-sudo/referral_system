from django.db import models


class ReferralUser(models.Model):
    """ Кастомный пользователь для реферальной системы
    """
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    invite_code = models.CharField(
        "Инвайт код", max_length=6, null=True, blank=True
    )
    phone = models.CharField("Телефон", max_length=11, unique=True)

    def __str__(self):
        return f"{self.phone} - {self.invite_code}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class SMSCode(models.Model):
    """ [Имитация] Модель для СМС кодов подтверждения
    """
    code = models.PositiveIntegerField("Код подтверждения")

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = verbose_name_plural = "Код подтверждения"
