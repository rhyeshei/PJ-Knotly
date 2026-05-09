from django import forms
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from apps.knotly.models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title',
            'slug',
            'page_type',
            'status',
            'urgency',
            'summary',
            'primary_action',
            'category',
            'owner_department',
            'tags',
            'target_audiences',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'page_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'primary_action': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'owner_department': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'target_audiences': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'slug': 'URLに使う文字列です。未入力の場合は自動生成されます。',
            'primary_action': 'トラブル対応ページなどで、最初に取るべき行動を入力します。',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')

        if slug:
            return slug

        base_slug = slugify(title or '')
        if not base_slug:
            base_slug = f"page-{get_random_string(8).lower()}"

        return base_slug
