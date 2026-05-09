from django.urls import path

from apps.knotly.views import dashboard, public

app_name = 'knotly'

urlpatterns = [
    path('', public.home, name='home'),
    path('pages/', public.page_list, name='page_list'),
    path('pages/<slug:slug>/', public.page_detail, name='page_detail'),
    path('dashboard/', dashboard.dashboard_home, name='dashboard_home'),
    path('dashboard/pages/', dashboard.page_manage, name='page_manage'),
    path('dashboard/pages/new/', dashboard.page_create, name='page_create'),
    path('dashboard/pages/<int:pk>/edit/', dashboard.page_edit, name='page_edit'),
    path('dashboard/pages/<int:pk>/preview/', dashboard.page_preview, name='page_preview'),
    path(
        'dashboard/pages/<int:page_pk>/blocks/add/',
        dashboard.block_add,
        name='block_add',
    ),
    path(
        'dashboard/blocks/<int:block_pk>/delete/',
        dashboard.block_delete,
        name='block_delete',
    ),
    path(
        'dashboard/blocks/<int:block_pk>/move-up/',
        dashboard.block_move_up,
        name='block_move_up',
    ),
    path(
        'dashboard/blocks/<int:block_pk>/move-down/',
        dashboard.block_move_down,
        name='block_move_down',
    ),
]
