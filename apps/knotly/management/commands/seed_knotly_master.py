from django.core.management.base import BaseCommand

from apps.knotly.models import BlockDefinition, Category, Department, Tag, TargetAudience


CATEGORIES = [
    {'name': 'IT・アカウント', 'slug': 'it-account'},
    {'name': '勤怠・労務', 'slug': 'attendance-labor'},
    {'name': '経費・購買', 'slug': 'expense-purchase'},
    {'name': '総務・庶務', 'slug': 'general-affairs'},
    {'name': 'セキュリティ', 'slug': 'security'},
    {'name': '入社・異動・退職', 'slug': 'lifecycle'},
]

TARGET_AUDIENCES = [
    {'name': '全社員', 'slug': 'all-employees'},
    {'name': '正社員', 'slug': 'full-time'},
    {'name': '業務委託', 'slug': 'contractor'},
    {'name': '管理職', 'slug': 'manager'},
    {'name': '新入社員', 'slug': 'new-employee'},
]

DEPARTMENTS = [
    {'name': '情報システム部', 'slug': 'information-systems'},
    {'name': '人事部', 'slug': 'human-resources'},
    {'name': '総務部', 'slug': 'general-affairs'},
    {'name': '経理部', 'slug': 'accounting'},
    {'name': '法務部', 'slug': 'legal'},
    {'name': 'コーポレート部門', 'slug': 'corporate'},
]

TAGS = [
    {'name': 'Slack', 'slug': 'slack', 'tag_type': Tag.TagType.TOOL},
    {'name': 'Google Workspace', 'slug': 'google-workspace', 'tag_type': Tag.TagType.TOOL},
    {'name': 'PC', 'slug': 'pc', 'tag_type': Tag.TagType.TOOL},
    {'name': 'アカウント', 'slug': 'account', 'tag_type': Tag.TagType.BUSINESS},
    {'name': '権限', 'slug': 'permission', 'tag_type': Tag.TagType.BUSINESS},
    {'name': '勤怠', 'slug': 'attendance', 'tag_type': Tag.TagType.BUSINESS},
    {'name': '経費', 'slug': 'expense', 'tag_type': Tag.TagType.BUSINESS},
    {'name': '備品', 'slug': 'equipment', 'tag_type': Tag.TagType.BUSINESS},
    {'name': 'セキュリティ', 'slug': 'security', 'tag_type': Tag.TagType.BUSINESS},
    {'name': '紛失', 'slug': 'lost', 'tag_type': Tag.TagType.SITUATION},
    {'name': 'ログイン不可', 'slug': 'login-issue', 'tag_type': Tag.TagType.SITUATION},
    {'name': '緊急', 'slug': 'urgent', 'tag_type': Tag.TagType.SITUATION},
    {'name': '申請', 'slug': 'application', 'tag_type': Tag.TagType.SITUATION},
    {'name': '承認', 'slug': 'approval', 'tag_type': Tag.TagType.SITUATION},
    {'name': '新入社員向け', 'slug': 'new-employee', 'tag_type': Tag.TagType.AUDIENCE},
    {'name': '管理職向け', 'slug': 'manager', 'tag_type': Tag.TagType.AUDIENCE},
]

BLOCK_DEFINITIONS = [
    {'key': 'summary', 'label': '概要', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'target', 'label': '対象者', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'steps', 'label': '手順', 'block_type': BlockDefinition.BlockType.STEPS},
    {'key': 'caution', 'label': '注意事項', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'faq', 'label': 'FAQ', 'block_type': BlockDefinition.BlockType.FAQ},
    {'key': 'contact', 'label': '問い合わせ先', 'block_type': BlockDefinition.BlockType.CONTACT},
    {'key': 'related_links', 'label': '関連リンク', 'block_type': BlockDefinition.BlockType.LINKS},
    {'key': 'update_info', 'label': '更新情報', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'extra', 'label': '補足情報', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'application_cases', 'label': '申請が必要なケース', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'required_items', 'label': '必要な情報・書類', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'application_link', 'label': '申請先・リンク', 'block_type': BlockDefinition.BlockType.LINKS},
    {'key': 'approver', 'label': '承認者・確認者', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'deadline', 'label': '締切・期限', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'symptoms', 'label': '症状・発生条件', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'first_action', 'label': 'まずやること', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'forbidden_actions', 'label': 'やってはいけないこと', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'escalation', 'label': 'エスカレーション条件', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'rule_body', 'label': 'ルール本文', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'ok_examples', 'label': 'OK例', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'ng_examples', 'label': 'NG例', 'block_type': BlockDefinition.BlockType.LIST},
    {'key': 'background', 'label': '目的・背景', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'exception', 'label': '例外対応', 'block_type': BlockDefinition.BlockType.TEXT},
    {'key': 'gray_cases', 'label': '判断に迷うケース', 'block_type': BlockDefinition.BlockType.FAQ},
]


class Command(BaseCommand):
    help = 'Seed Knotly master data.'

    def handle(self, *args, **options):
        self._seed_categories()
        self._seed_target_audiences()
        self._seed_departments()
        self._seed_tags()
        self._seed_block_definitions()
        self.stdout.write(self.style.SUCCESS('Knotly master data seeded successfully.'))

    def _seed_categories(self):
        for index, item in enumerate(CATEGORIES, start=1):
            Category.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'description': '',
                    'sort_order': index,
                    'is_active': True,
                },
            )

    def _seed_target_audiences(self):
        for item in TARGET_AUDIENCES:
            TargetAudience.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'description': '',
                    'is_active': True,
                },
            )

    def _seed_departments(self):
        for item in DEPARTMENTS:
            Department.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'description': '',
                    'is_active': True,
                },
            )

    def _seed_tags(self):
        for item in TAGS:
            Tag.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'tag_type': item['tag_type'],
                    'is_active': True,
                },
            )

    def _seed_block_definitions(self):
        for index, item in enumerate(BLOCK_DEFINITIONS, start=1):
            BlockDefinition.objects.update_or_create(
                key=item['key'],
                defaults={
                    'label': item['label'],
                    'block_type': item['block_type'],
                    'description': '',
                    'sort_order': index,
                    'is_active': True,
                },
            )
