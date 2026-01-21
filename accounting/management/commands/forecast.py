from django.core.management.base import BaseCommand
from accounting.models import Asset, MonthlyFinancial, LifeGoal

class Command(BaseCommand):
    help = '包含買房、教育、旅遊的人生財富模擬'

    def handle(self, *args, **options):
        # --- 1. 設定參數 (您可以隨時回來改這裡) ---
        current_age = 35         # 現在年齡
        simulate_years = 40      # 預測未來 40 年
        avg_return_rate = 0.05   # 投資年報酬率 (假設 5%)
        inflation_rate = 0.02    # 通膨率 (假設 2%)
        
        # --- 2. 載入資料庫數據 ---
        # A. 初始資產
        current_wealth = sum(a.amount for a in Asset.objects.all())
        
        # B. 每年儲蓄 (月結餘 x 12)
        monthly_data = MonthlyFinancial.objects.first()
        if not monthly_data:
            self.stdout.write(self.style.ERROR("錯誤：請先去後台輸入「Monthly financial」資料！"))
            return
        yearly_savings = (monthly_data.total_income - monthly_data.total_expense) * 12

        # C. 人生目標
        goals = LifeGoal.objects.all()

        # --- 3. 準備列印表格 ---
        self.stdout.write(f"\n===人生財富模擬報告 (初始資產: {current_wealth:,} | 年存: {yearly_savings:,})===")
        self.stdout.write("-" * 110)
        self.stdout.write(f"{'年份':<6} {'年齡':<6} {'重大支出事件 (會扣錢)':<40} {'當年度結餘':<15} {'累積資產 (名目)':<20}")
        self.stdout.write("-" * 110)

        # --- 4. 開始逐年模擬 ---
        start_year = 2026
        
        for i in range(simulate_years):
            year = start_year + i
            age = current_age + i
            
            # A. 這一年的投資獲利 (複利)
            investment_income = current_wealth * avg_return_rate
            
            # B. 這一年的基本儲蓄
            net_change = investment_income + yearly_savings
            
            # C. 檢查這一年有沒有「人生目標」要花錢
            events_str = []
            goal_expense = 0
            
            for goal in goals:
                # 判斷今年是否在這個目標的執行期間內
                end_year = goal.start_year + goal.duration_years
                if goal.start_year <= year < end_year:
                    goal_expense += goal.cost
                    events_str.append(goal.name)
            
            # 從結餘中扣除目標花費
            net_change -= goal_expense
            current_wealth += net_change

            # D. 顯示結果
            event_display = ", ".join(events_str)
            if not event_display:
                event_display = "-"
            
            # 如果資產變負的，顯示紅色警告
            wealth_display = f"${int(current_wealth):,}"
            if current_wealth < 0:
                wealth_display = self.style.ERROR(wealth_display)
            
            self.stdout.write(f"{year:<6} {age:<6} {event_display:<40} ${int(net_change):<15,} {wealth_display:<20}")

        self.stdout.write("-" * 110)