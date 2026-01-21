from django.contrib import admin
from .models import Asset, MonthlyFinancial, LifeGoal

# 1. 資產後台設定
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'amount', 'interest_rate')
    list_filter = ('type',)

# 2. 月度收支後台設定
@admin.register(MonthlyFinancial)
class MonthlyFinancialAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'total_income', 'total_expense', 'net_balance')
    
    def net_balance(self, obj):
        return obj.total_income - obj.total_expense
    net_balance.short_description = '本月結餘'

# 3. 人生目標後台設定
@admin.register(LifeGoal)
class LifeGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'cost', 'start_year', 'duration_years')
    list_filter = ('type',)