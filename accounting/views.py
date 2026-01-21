from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, MonthlyFinancial, LifeGoal, SimulationSettings
from .forms import LifeGoalForm, AssetForm, MonthlyFinancialForm, SimulationSettingsForm

# --- 1. 儀表板 (核心預測功能) ---
def dashboard(request):
    # A. 抓取設定參數 (如果資料庫沒有，就用預設值)
    settings = SimulationSettings.objects.first()
    if not settings:
        # 如果還沒設定過，建立一個預設的
        settings = SimulationSettings.objects.create(inflation_rate=2.0, return_rate=5.0)
    
    # 將百分比轉為小數 (例如 5% -> 0.05)
    avg_return_rate = settings.return_rate / 100
    inflation_rate_decimal = settings.inflation_rate / 100

    current_age = 35
    simulate_years = 40
    
    # B. 抓取資料
    assets = Asset.objects.all()
    current_wealth = sum(a.amount for a in assets)
    
    monthly_data = MonthlyFinancial.objects.first()
    yearly_savings = 0
    if monthly_data:
        yearly_savings = (monthly_data.total_income - monthly_data.total_expense) * 12
        
    goals = LifeGoal.objects.all()

    # C. 開始模擬
    report_data = []
    start_year = 2026
    
    for i in range(simulate_years):
        year = start_year + i
        age = current_age + i
        
        # 1. 投資複利 (使用設定的報酬率)
        investment_income = current_wealth * avg_return_rate
        
        # 2. 加上本金儲蓄 (這裡也可以考慮加入通膨對薪資的影響，目前先維持簡單)
        net_change = investment_income + yearly_savings
        
        # 3. 扣掉人生目標
        goal_names = []
        goal_expense = 0
        for goal in goals:
            end_year = goal.start_year + goal.duration_years
            if goal.start_year <= year < end_year:
                # 簡單計算：目標金額是否要考慮通膨？
                # 如果是現在輸入的金額，到未來可能會變貴。
                # 這裡我們先用名目金額計算，進階版可以再乘上 (1 + inflation)^i
                goal_expense += goal.cost
                goal_names.append(goal.name)
        
        net_change -= goal_expense
        current_wealth += net_change
        
        report_data.append({
            'year': year,
            'age': age,
            'events': ", ".join(goal_names) if goal_names else "-",
            'savings': int(net_change),
            'wealth': int(current_wealth),
            'is_negative': current_wealth < 0
        })

    # D. 打包資料
    chart_years = [row['year'] for row in report_data]
    chart_wealth = [row['wealth'] for row in report_data]

    context = {
        'report_data': report_data,
        'initial_wealth': sum(a.amount for a in assets),
        'yearly_savings': yearly_savings,
        'chart_years': chart_years,
        'chart_wealth': chart_wealth,
        'settings': settings, # 把設定也傳給網頁顯示
    }
    return render(request, 'accounting/dashboard.html', context)


# --- 2. 參數設定 (修改通膨/報酬率) ---
def settings_edit(request):
    # 永遠只抓第一筆設定
    settings = SimulationSettings.objects.first()
    if not settings:
        settings = SimulationSettings.objects.create()

    if request.method == 'POST':
        form = SimulationSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # 修改完直接回儀表板看結果
    else:
        form = SimulationSettingsForm(instance=settings)
    
    return render(request, 'accounting/form.html', {'form': form, 'title': '修改模擬參數'})


# --- 3. 資產管理 (Assets) ---
def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'accounting/asset_list.html', {'assets': assets})

def asset_edit(request, pk=None):
    if pk:
        asset = get_object_or_404(Asset, pk=pk)
        title = "修改資產"
    else:
        asset = None
        title = "新增資產"
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'accounting/form.html', {'form': form, 'title': title})

def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'accounting/confirm_delete.html', {'object': asset})


# --- 4. 收支管理 (Income) ---
def income_list(request):
    records = MonthlyFinancial.objects.all().order_by('-year', '-month')
    return render(request, 'accounting/income_list.html', {'records': records})

def income_edit(request, pk=None):
    if pk:
        record = get_object_or_404(MonthlyFinancial, pk=pk)
        title = "修改收支"
    else:
        record = None
        title = "新增收支"
    
    if request.method == 'POST':
        form = MonthlyFinancialForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = MonthlyFinancialForm(instance=record)
    return render(request, 'accounting/form.html', {'form': form, 'title': title})

def income_delete(request, pk):
    record = get_object_or_404(MonthlyFinancial, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('income_list')
    return render(request, 'accounting/confirm_delete.html', {'object': record})


# --- 5. 人生目標 (Goals) ---
def goal_list(request):
    goals = LifeGoal.objects.all().order_by('start_year')
    return render(request, 'accounting/goal_list.html', {'goals': goals})

def goal_edit(request, pk=None):
    if pk:
        goal = get_object_or_404(LifeGoal, pk=pk)
        title = "修改人生目標"
    else:
        goal = None
        title = "新增人生目標"

    if request.method == 'POST':
        form = LifeGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = LifeGoalForm(instance=goal)
    return render(request, 'accounting/form.html', {'form': form, 'title': title})

def goal_delete(request, pk):
    goal = get_object_or_404(LifeGoal, pk=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'accounting/confirm_delete.html', {'object': goal})