from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью (картинка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью (картинка)', **NULLABLE)
    link_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'
    PAYMENT_CHOICES = [
        (CASH, 'cash'),
        (TRANSFER, 'transfer')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=20, default=CASH,
                                      verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.payment_date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
