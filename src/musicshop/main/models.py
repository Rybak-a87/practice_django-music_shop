from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class MediaType(models.Model):
    """ Модель медиа носителя """
    name = models.CharField(max_length=100, verbose_name="Название медиа носителя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Медианоситель"
        verbose_name_plural = "Медианосители"


class Member(models.Model):
    """ Модель музыканта """
    name = models.CharField(max_length=200, verbose_name="Имя музыканта")
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Музыкант"
        verbose_name_plural = "Музыканты"


class Genre(models.Model):
    """ Модель музкального жанрова """
    name = models.CharField(max_length=50, verbose_name="Название жанра")
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Artist(models.Model):
    """ Модель исполнителя """
    name = models.CharField(max_length=200, verbose_name="Исполнитель/группа")
    genre = models.ForeignKey(Genre, verbose_name="Жанр", on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, verbose_name="Участник", related_name="artist")
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} | {self.genre.name}"

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


class Album(models.Model):
    """ Модель альбома """
    artist = models.ForeignKey(Artist, verbose_name="Исполнитель", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Название альбома")
    media_type = models.ForeignKey(MediaType, verbose_name="Медианоситель", on_delete=models.CASCADE)
    songs_list = models.TextField(verbose_name="Трек лист")
    release_date = models.DateField(verbose_name="Дата релиза")
    slug = models.SlugField()
    description = models.TextField(verbose_name="Описание", default="Описание появится позже")
    stock = models.IntegerField(verbose_name="Наличие на складе", default=1)
    price = models.DecimalField(verbose_name="Цена", max_digits=9, max_length=2)
    offer_of_the_week = models.BooleanField(verbose_name="Предложение недели", default=False)

    def __str__(self):
        return f"{self.id} | {self.artist.name} | {self.name}"

    @property
    def ct_model(self):
        return self._meta.model_name

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"


class CartProduct(models.Model):
    """ Модель продукта корзины """
    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(verbose_name="Общая цена", max_digits=9, max_length=2)

    def __str__(self):
        return f"Продукт: {self.content_object.name} (для корзины)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

        class Meta:
            verbose_name = "Продукт корзины"
            verbose_name_plural = "Продукты корзины"


class Cart(models.Model):
    """ Модель корзины """
    owner = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, verbose_name="Продукты для корзины", blank=True, null=True, related_name="related_card"
    )
    total_products = models.IntegerField(verbose_name="Общее количество товара", default=0)
    final_price = models.DecimalField(verbose_name="Общая цена", max_digits=9, max_length=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
