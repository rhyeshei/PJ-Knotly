from django.db import models

from apps.core.models import TimeStampedModel


class BlockDefinition(models.Model):
    class BlockType(models.TextChoices):
        TEXT = 'text', 'text'
        LIST = 'list', 'list'
        STEPS = 'steps', 'steps'
        FAQ = 'faq', 'faq'
        LINKS = 'links', 'links'
        CONTACT = 'contact', 'contact'

    key = models.SlugField('キー', max_length=50, unique=True)
    label = models.CharField('表示名', max_length=100)
    block_type = models.CharField('ブロック種別', max_length=20, choices=BlockType.choices)
    description = models.TextField('説明', blank=True)
    sort_order = models.PositiveIntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = 'ブロック定義'
        verbose_name_plural = 'ブロック定義'
        ordering = ('sort_order', 'label')

    def __str__(self):
        return self.label


class Block(TimeStampedModel):
    page = models.ForeignKey(
        'knotly.Page',
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name='ページ',
    )
    block_definition = models.ForeignKey(
        'knotly.BlockDefinition',
        on_delete=models.PROTECT,
        related_name='blocks',
        verbose_name='ブロック定義',
    )
    order = models.PositiveIntegerField('表示順', default=1)
    title = models.CharField('見出し', max_length=100)
    content = models.JSONField('内容', default=dict)
    is_required = models.BooleanField('必須', default=False)
    is_visible = models.BooleanField('表示', default=True)

    class Meta:
        verbose_name = 'ブロック'
        verbose_name_plural = 'ブロック'
        ordering = ('order', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=('page', 'block_definition'),
                name='unique_block_definition_per_page',
            )
        ]

    def __str__(self):
        return f'{self.page} - {self.title}'
