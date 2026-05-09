from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.knotly.models import Category, Page, Tag, TargetAudience


def home(request):
    published_pages = Page.objects.filter(status=Page.Status.PUBLISHED)
    context = {
        'categories': Category.objects.filter(is_active=True).order_by('sort_order', 'name'),
        'recent_pages': published_pages.select_related('category', 'owner_department')
        .prefetch_related('tags', 'target_audiences')
        .order_by('-published_at', '-updated_at')[:6],
        'intent_links': [
            {'label': '申請したい', 'page_type': Page.PageType.APPLICATION},
            {'label': '困っている', 'page_type': Page.PageType.TROUBLE},
            {'label': 'ルールを確認したい', 'page_type': Page.PageType.RULE},
        ],
    }
    return render(request, 'knotly/public/home.html', context)


def page_list(request):
    pages = Page.objects.filter(status=Page.Status.PUBLISHED).select_related(
        'category',
        'owner_department',
    ).prefetch_related(
        'tags',
        'target_audiences',
    )

    q = request.GET.get('q', '').strip()
    page_type = request.GET.get('page_type', '').strip()
    category = request.GET.get('category', '').strip()
    target = request.GET.get('target', '').strip()
    tag = request.GET.get('tag', '').strip()

    if q:
        pages = pages.filter(
            Q(title__icontains=q)
            | Q(summary__icontains=q)
            | Q(slug__icontains=q)
            | Q(blocks__content__icontains=q)
            | Q(tags__name__icontains=q)
        )

    if page_type:
        pages = pages.filter(page_type=page_type)

    if category:
        pages = pages.filter(category_id=category)

    if target:
        pages = pages.filter(target_audiences__id=target)

    if tag:
        pages = pages.filter(tags__id=tag)

    context = {
        'pages': pages.distinct().order_by('-published_at', '-updated_at', 'title'),
        'categories': Category.objects.filter(is_active=True).order_by('sort_order', 'name'),
        'tags': Tag.objects.filter(is_active=True).order_by('name'),
        'target_audiences': TargetAudience.objects.filter(is_active=True).order_by('name'),
        'page_type_choices': Page.PageType.choices,
        'filters': {
            'q': q,
            'page_type': page_type,
            'category': category,
            'target': target,
            'tag': tag,
        },
    }
    return render(request, 'knotly/public/page_list.html', context)


def page_detail(request, slug):
    page = get_object_or_404(
        Page.objects.filter(status=Page.Status.PUBLISHED)
        .select_related('category', 'owner_department')
        .prefetch_related('tags', 'target_audiences'),
        slug=slug,
    )
    blocks = page.blocks.filter(is_visible=True).select_related('block_definition').order_by(
        'order',
        'id',
    )

    return render(
        request,
        'knotly/public/page_detail.html',
        {
            'page': page,
            'blocks': blocks,
        },
    )
