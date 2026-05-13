from django.db import transaction
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from apps.knotly.models import Block, BlockDefinition, Page
from apps.knotly.services.block_templates import (
    BLANK_TEMPLATE_CHOICE,
    get_default_block_template,
)


TEMPLATE_TO_PAGE_TYPE = {
    Page.PageType.APPLICATION: Page.PageType.APPLICATION,
    Page.PageType.TROUBLE: Page.PageType.TROUBLE,
    Page.PageType.RULE: Page.PageType.RULE,
    BLANK_TEMPLATE_CHOICE: Page.PageType.CUSTOM,
}


def get_default_content(block_type):
    defaults = {
        BlockDefinition.BlockType.TEXT: {'text': ''},
        BlockDefinition.BlockType.LIST: {'items': []},
        BlockDefinition.BlockType.STEPS: {'steps': []},
        BlockDefinition.BlockType.FAQ: {'items': []},
        BlockDefinition.BlockType.LINKS: {'links': []},
        BlockDefinition.BlockType.CONTACT: {
            'department': '',
            'method': '',
            'note': '',
        },
    }
    return defaults.get(block_type, {'text': ''})


def generate_slug(title, slug=''):
    if slug:
        return slug

    base_slug = slugify(title or '')
    if not base_slug:
        base_slug = f"page-{get_random_string(8).lower()}"

    candidate = base_slug
    while Page.objects.filter(slug=candidate).exists():
        candidate = f"{base_slug}-{get_random_string(4).lower()}"

    return candidate


@transaction.atomic
def create_page_with_default_blocks(page_data, tags=None, target_audiences=None):
    page = Page.objects.create(**page_data)

    if tags is not None:
        page.tags.set(tags)

    if target_audiences is not None:
        page.target_audiences.set(target_audiences)

    create_default_blocks_for_page(page)
    return page


@transaction.atomic
def create_page_from_setup(page_data, template_choice, tags=None, target_audiences=None):
    page_type = TEMPLATE_TO_PAGE_TYPE.get(template_choice, Page.PageType.CUSTOM)
    page_payload = {
        **page_data,
        'page_type': page_type,
        'status': Page.Status.DRAFT,
        'summary': page_data.get('summary', ''),
        'primary_action': page_data.get('primary_action', ''),
    }
    page_payload['slug'] = generate_slug(
        title=page_payload.get('title', ''),
        slug=page_payload.get('slug', ''),
    )

    page = Page.objects.create(**page_payload)

    if tags is not None:
        page.tags.set(tags)

    if target_audiences is not None:
        page.target_audiences.set(target_audiences)

    if template_choice != BLANK_TEMPLATE_CHOICE:
        create_default_blocks_for_page(page, template_choice=template_choice)

    return page


def create_default_blocks_for_page(page, template_choice=None):
    template_key = template_choice or page.page_type
    template = get_default_block_template(template_key)
    definition_map = {
        definition.key: definition
        for definition in BlockDefinition.objects.filter(
            key__in=[item['key'] for item in template],
            is_active=True,
        )
    }

    blocks = []
    for item in template:
        definition = definition_map.get(item['key'])
        if definition is None:
            continue

        blocks.append(
            Block(
                page=page,
                block_definition=definition,
                order=item['order'],
                title=definition.label,
                content=get_default_content(definition.block_type),
                is_required=item['is_required'],
                is_visible=True,
            )
        )

    if blocks:
        Block.objects.bulk_create(blocks)

    return blocks
