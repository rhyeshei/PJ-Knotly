from django.db import models


class Department(models.Model):
    name = models.CharField('部署名', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = '部署'
        verbose_name_plural = '部署'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    sort_order = models.PositiveIntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ('sort_order', 'name')

    def __str__(self):
        return self.name


class Tag(models.Model):
    class TagType(models.TextChoices):
        TOOL = 'tool', 'tool'
        SITUATION = 'situation', 'situation'
        BUSINESS = 'business', 'business'
        AUDIENCE = 'audience', 'audience'

    name = models.CharField('タグ名', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    tag_type = models.CharField('タグ種別', max_length=20, choices=TagType.choices)
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TargetAudience(models.Model):
    name = models.CharField('対象者名', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = '対象者'
        verbose_name_plural = '対象者'
        ordering = ('name',)

    def __str__(self):
        return self.name
