from django import forms
from .models import LifeGoal, Asset, MonthlyFinancial, SimulationSettings

# 1. 人生目標表單
class LifeGoalForm(forms.ModelForm):
    class Meta:
        model = LifeGoal
        fields = ['name', 'cost', 'start_year', 'duration_years', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

# 2. 資產表單
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'amount', 'interest_rate', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

# 3. 月度收支表單 (原本缺少的)
class MonthlyFinancialForm(forms.ModelForm):
    class Meta:
        model = MonthlyFinancial
        fields = ['year', 'month', 'total_income', 'total_expense']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_expense': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# 4. 參數設定表單 (新增的)
class SimulationSettingsForm(forms.ModelForm):
    class Meta:
        model = SimulationSettings
        fields = ['inflation_rate', 'return_rate']
        widgets = {
            'inflation_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'return_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }