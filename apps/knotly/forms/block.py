from django import forms

from apps.knotly.models import Block, BlockDefinition


class BaseBlockForm(forms.Form):
    title = forms.CharField(
        label='見出し',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        self.block = block
        super().__init__(*args, **kwargs)
        self.fields['title'].initial = block.title

    def save(self):
        self.block.title = self.cleaned_data.get('title', '')
        self.block.content = self.get_content()
        self.block.save(update_fields=['title', 'content', 'updated_at'])
        return self.block

    def get_content(self):
        raise NotImplementedError


class TextBlockForm(BaseBlockForm):
    text = forms.CharField(
        label='本文',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        self.fields['text'].initial = block.content.get('text', '')

    def get_content(self):
        return {'text': self.cleaned_data.get('text', '')}


class ListBlockForm(BaseBlockForm):
    items = forms.CharField(
        label='項目',
        required=False,
        help_text='1行につき1項目として入力してください。',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        self.fields['items'].initial = '\n'.join(block.content.get('items', []))

    def get_content(self):
        raw_items = self.cleaned_data.get('items', '')
        items = [line.strip() for line in raw_items.splitlines() if line.strip()]
        return {'items': items}


class StepsBlockForm(BaseBlockForm):
    steps = forms.CharField(
        label='手順',
        required=False,
        help_text='1行につき1手順として入力してください。',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        self.fields['steps'].initial = '\n'.join(block.content.get('steps', []))

    def get_content(self):
        raw_steps = self.cleaned_data.get('steps', '')
        steps = [line.strip() for line in raw_steps.splitlines() if line.strip()]
        return {'steps': steps}


class FaqBlockForm(BaseBlockForm):
    items = forms.CharField(
        label='FAQ',
        required=False,
        help_text='1行につき「質問｜回答」の形式で入力してください。',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        lines = []
        for item in block.content.get('items', []):
            lines.append(f"{item.get('question', '')}｜{item.get('answer', '')}")
        self.fields['items'].initial = '\n'.join(lines)

    def get_content(self):
        raw_items = self.cleaned_data.get('items', '')
        items = []

        for line in raw_items.splitlines():
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if '｜' in stripped_line:
                question, answer = stripped_line.split('｜', 1)
            elif '|' in stripped_line:
                question, answer = stripped_line.split('|', 1)
            else:
                question, answer = stripped_line, ''

            items.append(
                {
                    'question': question.strip(),
                    'answer': answer.strip(),
                }
            )

        return {'items': items}


class LinksBlockForm(BaseBlockForm):
    links = forms.CharField(
        label='リンク',
        required=False,
        help_text='1行につき「ラベル｜URL」の形式で入力してください。',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        lines = []
        for link in block.content.get('links', []):
            lines.append(f"{link.get('label', '')}｜{link.get('url', '')}")
        self.fields['links'].initial = '\n'.join(lines)

    def get_content(self):
        raw_links = self.cleaned_data.get('links', '')
        links = []

        for line in raw_links.splitlines():
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if '｜' in stripped_line:
                label, url = stripped_line.split('｜', 1)
            elif '|' in stripped_line:
                label, url = stripped_line.split('|', 1)
            else:
                label, url = stripped_line, ''

            links.append(
                {
                    'label': label.strip(),
                    'url': url.strip(),
                }
            )

        return {'links': links}


class ContactBlockForm(BaseBlockForm):
    department = forms.CharField(
        label='担当部署',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    method = forms.CharField(
        label='連絡方法',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    note = forms.CharField(
        label='補足',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    def __init__(self, *args, block: Block, **kwargs):
        super().__init__(*args, block=block, **kwargs)
        self.fields['department'].initial = block.content.get('department', '')
        self.fields['method'].initial = block.content.get('method', '')
        self.fields['note'].initial = block.content.get('note', '')

    def get_content(self):
        return {
            'department': self.cleaned_data.get('department', ''),
            'method': self.cleaned_data.get('method', ''),
            'note': self.cleaned_data.get('note', ''),
        }


def get_block_form_class(block: Block):
    block_type = block.block_definition.block_type

    if block_type == BlockDefinition.BlockType.TEXT:
        return TextBlockForm
    if block_type == BlockDefinition.BlockType.LIST:
        return ListBlockForm
    if block_type == BlockDefinition.BlockType.STEPS:
        return StepsBlockForm
    if block_type == BlockDefinition.BlockType.FAQ:
        return FaqBlockForm
    if block_type == BlockDefinition.BlockType.LINKS:
        return LinksBlockForm
    if block_type == BlockDefinition.BlockType.CONTACT:
        return ContactBlockForm

    return TextBlockForm
