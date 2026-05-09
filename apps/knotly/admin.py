from django.contrib import admin

from apps.knotly.models import (
    Block,
    BlockDefinition,
    Category,
    Department,
    Page,
    Tag,
    TargetAudience,
)


class BlockInline(admin.TabularInline):
    model = Block
    extra = 0
    fields = (
        'order',
        'block_definition',
        'title',
        'is_required',
        'is_visible',
        'content',
    )
    ordering = ('order', 'id')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('is_active',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sort_order', 'is_active')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('is_active',)
    ordering = ('sort_order', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tag_type', 'is_active')
    search_fields = ('name', 'slug')
    list_filter = ('tag_type', 'is_active')
    ordering = ('name',)


@admin.register(TargetAudience)
class TargetAudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('is_active',)
    ordering = ('name',)


@admin.register(BlockDefinition)
class BlockDefinitionAdmin(admin.ModelAdmin):
    list_display = ('label', 'key', 'block_type', 'sort_order', 'is_active')
    search_fields = ('label', 'key', 'description')
    list_filter = ('block_type', 'is_active')
    ordering = ('sort_order', 'label')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'page_type',
        'status',
        'urgency',
        'category',
        'owner_department',
        'published_at',
        'updated_at',
    )
    search_fields = ('title', 'slug', 'summary', 'primary_action')
    list_filter = ('page_type', 'status', 'urgency', 'category', 'owner_department')
    ordering = ('-updated_at', 'title')
    filter_horizontal = ('tags', 'target_audiences')
    inlines = (BlockInline,)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'page',
        'block_definition',
        'order',
        'is_required',
        'is_visible',
        'updated_at',
    )
    search_fields = ('title', 'page__title', 'block_definition__label', 'block_definition__key')
    list_filter = ('is_required', 'is_visible', 'block_definition__block_type')
    ordering = ('page', 'order', 'id')
