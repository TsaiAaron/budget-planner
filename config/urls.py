from django.contrib import admin
from django.urls import path
from accounting.views import (
    dashboard, 
    settings_edit, # 新增這個
    goal_list, goal_edit, goal_delete,
    asset_list, asset_edit, asset_delete,
    income_list, income_edit, income_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 首頁
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard),

    # 1. 參數設定 (通膨/報酬率)
    path('settings/', settings_edit, name='settings_edit'),

    # 2. 資產管理
    path('assets/', asset_list, name='asset_list'),
    path('assets/add/', asset_edit, name='asset_add'),
    path('assets/edit/<int:pk>/', asset_edit, name='asset_edit'),
    path('assets/delete/<int:pk>/', asset_delete, name='asset_delete'),

    # 3. 收支管理
    path('income/', income_list, name='income_list'),
    path('income/add/', income_edit, name='income_add'),
    path('income/edit/<int:pk>/', income_edit, name='income_edit'),
    path('income/delete/<int:pk>/', income_delete, name='income_delete'),

    # 4. 人生目標
    path('goals/', goal_list, name='goal_list'),
    path('goals/add/', goal_edit, name='goal_add'),
    path('goals/edit/<int:pk>/', goal_edit, name='goal_edit'),
    path('goals/delete/<int:pk>/', goal_delete, name='goal_delete'),
]