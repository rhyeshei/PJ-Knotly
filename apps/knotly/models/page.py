from django.db import models

from apps.core.models import TimeStampedModel


class Page(TimeStampedModel):
    class PageType(models.TextChoices):
        APPLICATION = 'application', '申請方法'
        TROUBLE = 'trouble', 'トラブル対応'
        RULE = 'rule', '社内ルール'
        CUSTOM = 'custom', '自由作成'

    class Status(models.TextChoices):
        DRAFT = 'draft', '下書き'
        PUBLISHED = 'published', '公開中'
        PRIVATE = 'private', '非公開'
        NEEDS_UPDATE = 'needs_update', '要更新'

    class Urgency(models.TextChoices):
        NORMAL = 'normal', '通常'
        HIGH = 'high', '急ぎ'
        URGENT = 'urgent', '緊急'

    title = models.CharField('タイトル', max_length=200)
    slug = models.SlugField('slug', max_length=200, unique=True)
    page_type = models.CharField('ページタイプ', max_length=20, choices=PageType.choices)
    status = models.CharField(
        '公開状態',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    urgency = models.CharField(
        '緊急度',
        max_length=20,
        choices=Urgency.choices,
        default=Urgency.NORMAL,
    )
    summary = models.TextField('概要', blank=True)
    primary_action = models.TextField('まずやること', blank=True)
    category = models.ForeignKey(
        'knotly.Category',
        on_delete=models.PROTECT,
        related_name='pages',
        verbose_name='カテゴリ',
    )
    owner_department = models.ForeignKey(
        'knotly.Department',
        on_delete=models.PROTECT,
        related_name='owned_pages',
        verbose_name='担当部署',
    )
    tags = models.ManyToManyField(
        'knotly.Tag',
        blank=True,
        related_name='pages',
        verbose_name='タグ',
    )
    target_audiences = models.ManyToManyField(
        'knotly.TargetAudience',
        blank=True,
        related_name='pages',
        verbose_name='対象者',
    )
    published_at = models.DateTimeField('公開日時', blank=True, null=True)

    class Meta:
        verbose_name = 'ページ'
        verbose_name_plural = 'ページ'
        ordering = ('-updated_at', 'title')

    def __str__(self):
        return self.title
