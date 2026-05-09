from django.db import transaction

from apps.knotly.models import Block, BlockDefinition, Page
from apps.knotly.services.block_templates import get_default_block_template


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


@transaction.atomic
def create_page_with_default_blocks(page_data, tags=None, target_audiences=None):
    page = Page.objects.create(**page_data)

    if tags is not None:
        page.tags.set(tags)

    if target_audiences is not None:
        page.target_audiences.set(target_audiences)

    create_default_blocks_for_page(page)
    return page


def create_default_blocks_for_page(page):
    template = get_default_block_template(page.page_type)
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
