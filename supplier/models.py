from django.db import models


CURRENCY_CHOICES = [
    ('BYN', 'BYN'),
    ('RUB', 'RUB'),
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('CNY', 'CNY'),
]


class Country(models.Model):
    """
    Страны для привязки брендов и поставщиков.
    """
    name = models.CharField(
        'Название',
        max_length=30,
        unique=True,
        db_index=True,
        help_text='Название страны'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name',)


class EquipmentLine(models.Model):
    """
    Линейки оборудования производителей.

    Различные категории оборудования: частотные преобразователи,
    контроллеры, серво и т.д.
    """
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Название линейки оборудования'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Линейка оборудования'
        verbose_name_plural = 'Линейки оборудования'
        ordering = ('name',)


class Supplier(models.Model):
    """
    Компании-поставщики оборудования с контактной информацией и валютой торговли.
    """
    name = models.CharField(
        'Наименование',
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Название компании-поставщика'
    )
    site = models.CharField('Сайт', max_length=100, help_text='Веб-сайт поставщика')
    country = models.ForeignKey(
        Country,
        verbose_name='Страна',
        on_delete=models.PROTECT,
        related_name='suppliers',
        help_text='Страна регистрации поставщика'
    )
    currency = models.CharField(
        'Валюта',
        max_length=3,
        choices=CURRENCY_CHOICES,
        db_index=True,
        help_text='Валюта, в которой поставщик указывает цены'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ('name',)


class Brand(models.Model):
    """
    Бренды производителей оборудования.

    Компании-производители с их специализацией и связями с поставщиками.
    """
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
        db_index=True,
        help_text='Название бренда'
    )
    site = models.CharField('Сайт', max_length=150, help_text='Официальный сайт производителя')
    country = models.ForeignKey(
        Country,
        verbose_name='Страна',
        on_delete=models.PROTECT,
        related_name='brands',
        help_text='Страна производителя'
    )
    equipment_lines = models.ManyToManyField(
        EquipmentLine,
        verbose_name='Линейки оборудования',
        related_name='brands',
        help_text='Виды оборудования, которые производит компания'
    )
    description = models.TextField('Описание', blank=True, help_text='Описание компании и её продукции')
    suppliers = models.ManyToManyField(
        Supplier,
        verbose_name='Поставщики',
        related_name='brands',
        help_text='Поставщики, которые работают с этим брендом'
    )
    logo = models.ImageField(
        'Логотип',
        upload_to='logos/',
        blank=True,
        null=True,
        help_text='Логотип компании'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('name',)
