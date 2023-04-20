from django.db import models


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='blacklisted_tokens')

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Blacklisted token'
        verbose_name_plural = 'Blacklisted tokens'
        unique_together = ('token', 'user')