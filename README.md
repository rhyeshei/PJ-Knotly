# Knotly

Knotly は、コーポレート部門が社内手続き・社内ルール・トラブル対応ページを、**ブロック構造**で作成・管理・公開できる Django SSR ベースの社内ナレッジ管理ツールです。

自由にページを作れる柔軟さを持ちながら、ページタイプとブロック定義によって情報の見やすさや構造を崩しにくいことを重視しています。

> 現在このプロジェクトは **制作途中の MVP 開発段階** です。基本導線と主要画面は実装済みですが、UI 調整や今後の機能拡張を継続しています。

## 概要

社内向け情報は、自由度を高くしすぎると書き方がばらつき、読みづらくなります。  
一方で、固定テンプレートだけにすると、現場で必要な情報を載せにくくなります。

Knotly はその中間を狙ったプロダクトです。

- ページタイプごとに推奨ブロックを持つ
- 管理者は必要に応じてブロックを追加・削除・並び替えできる
- 社員は検索・フィルタで必要な情報にたどり着ける

MVP では、社内情報のうち次の 3 領域に絞っています。

- 申請方法
- トラブル対応
- 社内ルール

## 解決する課題

Knotly は、次のような課題の解決を目的としています。

- 社内手続きのページが人によって書き方にばらつき、必要な情報を探しづらい
- トラブル対応時に「まず何をすべきか」がページによって分かりづらい
- 社内ルールが散在し、検索しても意図した情報にたどり着きにくい
- 一般的な wiki だと自由すぎて構造が崩れやすい
- 固定テンプレート型ツールだと柔軟性が足りない

## 主な機能

- ページタイプ別のページ作成
- ページタイプに応じた初期ブロック自動生成
- ブロック単位での本文編集
- ブロック追加
- ブロックの非表示化による削除
- ブロックの上へ / 下へ並び替え
- 下書き / 公開 / 非公開 / 要更新 の状態管理
- 管理者向けプレビュー
- 公開ページの一覧・検索・フィルタ

## MVPでできること

### 社員向け

- トップ画面の閲覧
- 公開ページ一覧の閲覧
- キーワード検索
- ページタイプ / カテゴリ / 対象者 / タグでのフィルタ
- ページ詳細の閲覧

### 管理者向け

- 独自ダッシュボードからのページ作成
- ページ基本情報の編集
- 初期ブロックの自動生成
- ブロック本文の編集
- 任意ブロックの追加
- 任意ブロックの非表示化
- ブロック順の調整
- プレビュー表示

### Django Admin

- マスタデータ管理
- データ確認
- 緊急時の補助的な修正

## 技術スタック

- Python 3
- Django 4.2
- SQLite
- Django Templates
- Custom CSS

フロントエンドは Django SSR 前提で、Bootstrap や Tailwind には依存していません。

## セットアップ手順

プロジェクトルートで以下を実行してください。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_knotly_master
python manage.py createsuperuser
python manage.py runserver
```

## 初期データ投入手順

Knotly では fixture ではなく management command で初期マスタデータを投入します。

```bash
source .venv/bin/activate
python manage.py seed_knotly_master
```

投入対象:

- Category
- TargetAudience
- Department
- Tag
- BlockDefinition

このコマンドは `update_or_create` ベースで実装しているため、再実行しても重複しません。

## 起動方法

```bash
source .venv/bin/activate
python manage.py runserver
```

起動後、ブラウザで `http://127.0.0.1:8000/` にアクセスしてください。

## 主なURL

### 社員向け

- `/` : トップ画面
- `/pages/` : ページ一覧 / 検索
- `/pages/<slug>/` : ページ詳細

### 管理者向け

- `/dashboard/` : 管理ダッシュボード
- `/dashboard/pages/` : ページ管理一覧
- `/dashboard/pages/new/` : ページ新規作成
- `/dashboard/pages/<id>/edit/` : ページ編集
- `/dashboard/pages/<id>/preview/` : ページプレビュー
- `/dashboard/pages/<id>/blocks/add/` : ブロック追加

### Django Admin

- `/admin/`

## ディレクトリ構成

```text
Project-Knotly/
├── AGENTS.md
├── DESIGN_GUIDE.md
├── Tasks.md
├── README.md
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/
│   │   ├── apps.py
│   │   └── models.py
│   └── knotly/
│       ├── admin.py
│       ├── apps.py
│       ├── urls.py
│       ├── forms/
│       │   ├── block.py
│       │   └── page.py
│       ├── management/
│       │   └── commands/
│       │       └── seed_knotly_master.py
│       ├── models/
│       │   ├── block.py
│       │   ├── master.py
│       │   └── page.py
│       ├── services/
│       │   ├── block_templates.py
│       │   └── page_factory.py
│       ├── templates/
│       │   └── knotly/
│       │       ├── components/
│       │       ├── dashboard/
│       │       └── public/
│       └── views/
│           ├── dashboard.py
│           └── public.py
├── templates/
│   └── base.html
└── static/
    └── css/
        └── knotly.css
```

## 開発方針

Knotly では、次の方針を重視しています。

- **構造化されたページ作成体験を優先する**
- **通常のページ運用は Django admin ではなく独自 dashboard で行う**
- **本文は Page に直接持たせすぎず、Block として管理する**
- **Block.content は JSONField だが、UI では JSON を直接見せない**
- **MVP では機能を広げすぎず、ページ作成から公開までの基本導線を磨く**
- **UI は静かで整理された SaaS 感を重視する**
- **制作途中であることを前提に、小さく確認しながら段階的に改善する**

## 今後追加予定の機能

MVP 後の拡張候補として、以下を想定しています。

- AI による文章補助
- AI 検索
- RAG
- Slack 連携
- Notion 連携
- 承認ワークフロー
- コメント機能
- 閲覧ログ / 集計
- 更新期限通知
- 履歴管理 / 版管理
- ファイル添付
- リッチテキスト対応

## 補足

Knotly は、単なる社内 wiki ではなく、**柔軟に作れるが、構造は崩れない** ことを重視した社内ナレッジツールです。  
ポートフォリオとして見る場合も、Django による SSR 構成、業務要件に沿った情報設計、管理画面と公開画面の責務分離を意識したプロジェクトとして確認できます。
