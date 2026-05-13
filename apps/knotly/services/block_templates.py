from apps.knotly.models import Page


BLANK_TEMPLATE_CHOICE = 'blank'

DEFAULT_BLOCK_TEMPLATES = {
    Page.PageType.APPLICATION: [
        {'order': 1, 'key': 'summary', 'is_required': True},
        {'order': 2, 'key': 'target', 'is_required': True},
        {'order': 3, 'key': 'application_cases', 'is_required': True},
        {'order': 4, 'key': 'steps', 'is_required': True},
        {'order': 5, 'key': 'required_items', 'is_required': True},
        {'order': 6, 'key': 'application_link', 'is_required': True},
        {'order': 7, 'key': 'contact', 'is_required': True},
        {'order': 8, 'key': 'update_info', 'is_required': True},
    ],
    Page.PageType.TROUBLE: [
        {'order': 1, 'key': 'summary', 'is_required': True},
        {'order': 2, 'key': 'target', 'is_required': True},
        {'order': 3, 'key': 'symptoms', 'is_required': True},
        {'order': 4, 'key': 'first_action', 'is_required': True},
        {'order': 5, 'key': 'forbidden_actions', 'is_required': True},
        {'order': 6, 'key': 'steps', 'is_required': True},
        {'order': 7, 'key': 'contact', 'is_required': True},
        {'order': 8, 'key': 'update_info', 'is_required': True},
    ],
    Page.PageType.RULE: [
        {'order': 1, 'key': 'summary', 'is_required': True},
        {'order': 2, 'key': 'target', 'is_required': True},
        {'order': 3, 'key': 'rule_body', 'is_required': True},
        {'order': 4, 'key': 'ok_examples', 'is_required': False},
        {'order': 5, 'key': 'ng_examples', 'is_required': False},
        {'order': 6, 'key': 'exception', 'is_required': False},
        {'order': 7, 'key': 'contact', 'is_required': True},
        {'order': 8, 'key': 'update_info', 'is_required': True},
    ],
    BLANK_TEMPLATE_CHOICE: [],
}


def get_default_block_template(template_choice):
    return DEFAULT_BLOCK_TEMPLATES.get(template_choice, [])
