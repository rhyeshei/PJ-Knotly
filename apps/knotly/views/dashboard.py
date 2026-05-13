from django.contrib import messages
from django.db import transaction
from django.db.models import Max, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from apps.knotly.decorators import knotly_admin_required
from apps.knotly.forms import PageForm, PageSetupForm, get_block_form_class
from apps.knotly.models import Block, BlockDefinition, Category, Page
from apps.knotly.services import create_page_from_setup, get_default_content


def build_block_forms(blocks, data=None):
    block_entries = []

    for block in blocks:
        prefix = f'block-{block.pk}'
        form_class = get_block_form_class(block)
        form = form_class(data=data, block=block, prefix=prefix)
        block_entries.append(
            {
                'block': block,
                'form': form,
                'prefix': prefix,
            }
        )

    return block_entries


def build_block_palette(page):
    added_definition_ids = set(page.blocks.values_list('block_definition_id', flat=True))
    definitions = BlockDefinition.objects.filter(is_active=True).order_by('sort_order', 'label')
    return {
        'definitions': definitions,
        'added_definition_ids': added_definition_ids,
    }


@knotly_admin_required
def dashboard_home(request):
    context = {
        'published_count': Page.objects.filter(status=Page.Status.PUBLISHED).count(),
        'draft_count': Page.objects.filter(status=Page.Status.DRAFT).count(),
        'needs_update_count': Page.objects.filter(status=Page.Status.NEEDS_UPDATE).count(),
    }
    return render(request, 'knotly/dashboard/dashboard_home.html', context)


@knotly_admin_required
def page_manage(request):
    pages = Page.objects.select_related('category', 'owner_department').prefetch_related(
        'tags',
        'target_audiences',
    )

    q = request.GET.get('q', '').strip()
    page_type = request.GET.get('page_type', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        pages = pages.filter(
            Q(title__icontains=q)
            | Q(slug__icontains=q)
            | Q(summary__icontains=q)
            | Q(primary_action__icontains=q)
        )

    if page_type:
        pages = pages.filter(page_type=page_type)

    if category:
        pages = pages.filter(category_id=category)

    if status:
        pages = pages.filter(status=status)

    context = {
        'pages': pages.order_by('-updated_at', 'title'),
        'categories': Category.objects.filter(is_active=True).order_by('sort_order', 'name'),
        'page_type_choices': Page.PageType.choices,
        'status_choices': Page.Status.choices,
        'filters': {
            'q': q,
            'page_type': page_type,
            'category': category,
            'status': status,
        },
    }
    return render(request, 'knotly/dashboard/page_manage.html', context)


@knotly_admin_required
def page_create(request):
    if request.method == 'POST':
        form = PageSetupForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data.copy()
            template_choice = cleaned_data.pop('template_choice')
            tags = cleaned_data.pop('tags', None)
            target_audiences = cleaned_data.pop('target_audiences', None)
            page = create_page_from_setup(
                page_data=cleaned_data,
                template_choice=template_choice,
                tags=tags,
                target_audiences=target_audiences,
            )
            messages.success(request, 'ページを作成しました。')
            return redirect('knotly:page_edit', pk=page.pk)
    else:
        form = PageSetupForm()

    return render(
        request,
        'knotly/dashboard/page_create.html',
        {
            'form': form,
        },
    )


@knotly_admin_required
def page_edit(request, pk):
    page = get_object_or_404(Page, pk=pk)
    blocks = page.blocks.filter(is_visible=True).select_related('block_definition').order_by(
        'order',
        'id',
    )

    if request.method == 'POST':
        page_form = PageForm(request.POST, instance=page)
        block_entries = build_block_forms(blocks, data=request.POST)
        block_forms = [entry['form'] for entry in block_entries]

        if page_form.is_valid() and all(form.is_valid() for form in block_forms):
            with transaction.atomic():
                page_form.save()
                for form in block_forms:
                    form.save()
            messages.success(request, 'ページを更新しました。')
            return redirect('knotly:page_edit', pk=page.pk)
    else:
        page_form = PageForm(instance=page)
        block_entries = build_block_forms(blocks)

    return render(
        request,
        'knotly/dashboard/page_edit.html',
        {
            'page': page,
            'page_form': page_form,
            'block_entries': block_entries,
            **build_block_palette(page),
        },
    )


@knotly_admin_required
def page_preview(request, pk):
    page = get_object_or_404(Page.objects.select_related('category', 'owner_department'), pk=pk)
    blocks = page.blocks.filter(is_visible=True).select_related('block_definition').order_by(
        'order',
        'id',
    )

    return render(
        request,
        'knotly/dashboard/page_preview.html',
        {
            'page': page,
            'blocks': blocks,
        },
    )


@knotly_admin_required
def block_add(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    palette = build_block_palette(page)
    existing_definition_ids = palette['added_definition_ids']

    if request.method == 'POST':
        block_definition_id = request.POST.get('block_definition_id') or request.POST.get(
            'block_definition'
        )
        if not block_definition_id:
            messages.error(request, '追加するブロックが選択されていません。')
            return redirect('knotly:page_edit', pk=page.pk)

        try:
            block_definition_id = int(block_definition_id)
        except (TypeError, ValueError):
            messages.error(request, '不正なブロック指定です。')
            return redirect('knotly:page_edit', pk=page.pk)

        if block_definition_id in existing_definition_ids:
            messages.info(request, 'このブロックはすでに追加済みです。')
            return redirect('knotly:page_edit', pk=page.pk)

        block_definition = get_object_or_404(
            BlockDefinition.objects.filter(is_active=True),
            pk=block_definition_id,
        )
        max_order = page.blocks.aggregate(max_order=Max('order')).get('max_order') or 0
        Block.objects.create(
            page=page,
            block_definition=block_definition,
            order=max_order + 1,
            title=block_definition.label,
            content=get_default_content(block_definition.block_type),
            is_required=False,
            is_visible=True,
        )
        messages.success(request, 'ブロックを追加しました。')
        return redirect('knotly:page_edit', pk=page.pk)

    return render(
        request,
        'knotly/dashboard/block_add.html',
        {
            'page': page,
            'block_definitions': palette['definitions'],
            'added_definition_ids': palette['added_definition_ids'],
        },
    )


@knotly_admin_required
def block_delete(request, block_pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    block = get_object_or_404(Block.objects.select_related('page'), pk=block_pk)

    if block.is_required:
        messages.error(request, '必須ブロックは削除できません。')
        return redirect('knotly:page_edit', pk=block.page_id)

    block.is_visible = False
    block.save(update_fields=['is_visible', 'updated_at'])
    messages.success(request, 'ブロックを非表示にしました。')
    return redirect('knotly:page_edit', pk=block.page_id)


@knotly_admin_required
def block_move_up(request, block_pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    block = get_object_or_404(Block.objects.select_related('page'), pk=block_pk)
    previous_block = (
        Block.objects.filter(page=block.page, is_visible=True, order__lt=block.order)
        .order_by('-order', '-id')
        .first()
    )

    if previous_block is not None:
        with transaction.atomic():
            current_order = block.order
            block.order = previous_block.order
            previous_block.order = current_order
            block.save(update_fields=['order', 'updated_at'])
            previous_block.save(update_fields=['order', 'updated_at'])

    return redirect('knotly:page_edit', pk=block.page_id)


@knotly_admin_required
def block_move_down(request, block_pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    block = get_object_or_404(Block.objects.select_related('page'), pk=block_pk)
    next_block = (
        Block.objects.filter(page=block.page, is_visible=True, order__gt=block.order)
        .order_by('order', 'id')
        .first()
    )

    if next_block is not None:
        with transaction.atomic():
            current_order = block.order
            block.order = next_block.order
            next_block.order = current_order
            block.save(update_fields=['order', 'updated_at'])
            next_block.save(update_fields=['order', 'updated_at'])

    return redirect('knotly:page_edit', pk=block.page_id)
