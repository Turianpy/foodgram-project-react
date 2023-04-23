from django.db import models


class BlacklistedToken(models.Model):
    """
    Модель для хранения токенов, которые были отозваны через logout эндпоинт.
    """
    token = models.CharField(max_length=255, verbose_name='Токен авторизации')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='blacklisted_tokens',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Blacklisted token'
        verbose_name_plural = 'Blacklisted tokens'
        unique_together = ('token', 'user')
