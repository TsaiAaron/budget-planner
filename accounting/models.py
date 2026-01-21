from django.db import models

# 1. 資產表：紀錄現在有的錢 (存款、股票、房產)
class Asset(models.Model):
    ASSET_TYPES = (
        ('CASH', '現金/存款'),
        ('STOCK', '股票/基金'),
        ('REAL_ESTATE', '房地產'),
        ('OTHER', '其他'),
    )
    name = models.CharField('資產名稱', max_length=50)
    amount = models.IntegerField('金額')
    interest_rate = models.FloatField('預估年化報酬率 (%)', default=2.0)
    type = models.CharField('類型', max_length=20, choices=ASSET_TYPES, default='CASH')

    def __str__(self):
        return f"{self.name} - ${self.amount:,}"

# 2. 每月收支表：紀錄每個月賺多少、花多少
class MonthlyFinancial(models.Model):
    year = models.IntegerField('年份', default=2026)
    month = models.IntegerField('月份', default=1)
    total_income = models.IntegerField('總收入')
    total_expense = models.IntegerField('總支出')

    def __str__(self):
        return f"{self.year}年 {self.month}月"

    # --- 關鍵修正：讓系統知道如何計算結餘 ---
    @property
    def net_balance(self):
        return self.total_income - self.total_expense

# 3. 人生目標表：紀錄買房、買車、教育基金、醫療預算
class LifeGoal(models.Model):
    GOAL_TYPES = (
        ('ONE_TIME', '單次支出 (如：買房、買車)'),
        ('RECURRING', '每年持續 (如：旅遊、孝親、醫療)'),
    )
    
    name = models.CharField('目標名稱', max_length=50) # 例如：小孩大學學費、買房頭期款
    cost = models.IntegerField('預計金額', help_text='如果是持續支出，請填每年金額')
    start_year = models.IntegerField('開始年份', default=2026)
    duration_years = models.IntegerField('持續年數', default=1, help_text='單次支出請填 1')
    
    type = models.CharField('類型', max_length=10, choices=GOAL_TYPES, default='ONE_TIME')

    def __str__(self):
        if self.duration_years > 1:
            return f"{self.name} - 每年 ${self.cost:,} (從 {self.start_year} 起共 {self.duration_years} 年)"
        return f"{self.name} - ${self.cost:,} (預計 {self.start_year} 年執行)"

# 4. 模擬參數設定 (通膨、報酬率)
class SimulationSettings(models.Model):
    inflation_rate = models.FloatField('預估通膨率 (%)', default=2.0)
    return_rate = models.FloatField('預估投資報酬率 (%)', default=5.0)
    
    def __str__(self):
        return "模擬參數設定"