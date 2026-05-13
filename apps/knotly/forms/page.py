from django import forms
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from apps.knotly.models import Category, Department, Page, Tag, TargetAudience


class PageSetupForm(forms.Form):
    TEMPLATE_CHOICES = [
        ('application', '申請方法テンプレート'),
        ('trouble', 'トラブル対応テンプレート'),
        ('rule', '社内ルールテンプレート'),
        ('blank', 'まっさらから作成'),
    ]

    template_choice = forms.ChoiceField(
        label='作成方式',
        choices=TEMPLATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='テンプレートから始めるか、まっさらな状態から構成するかを選びます。',
    )
    title = forms.CharField(
        label='タイトル',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    category = forms.ModelChoiceField(
        label='カテゴリ',
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    target_audiences = forms.ModelMultipleChoiceField(
        label='対象者',
        queryset=TargetAudience.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    tags = forms.ModelMultipleChoiceField(
        label='タグ',
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    owner_department = forms.ModelChoiceField(
        label='担当部署',
        queryset=Department.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    urgency = forms.ChoiceField(
        label='緊急度',
        choices=Page.Urgency.choices,
        initial=Page.Urgency.NORMAL,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by(
            'sort_order',
            'name',
        )
        self.fields['target_audiences'].queryset = TargetAudience.objects.filter(
            is_active=True
        ).order_by('name')
        self.fields['tags'].queryset = Tag.objects.filter(is_active=True).order_by('name')
        self.fields['owner_department'].queryset = Department.objects.filter(
            is_active=True
        ).order_by('name')


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
