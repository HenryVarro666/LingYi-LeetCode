CONFIG = dict(
    num=2303, title='计算应缴税款总额', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='分段累计，浮点放最后（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def calculateTax(self, brackets: List[List[int]], income: int) -> float:
        ans, pre = 0, 0
        for b in brackets:
            up, p = b[0], b[1]
            if income <= up:
                ans += (income - pre) * p
                break
            ans += (up - pre) * p
            pre = up
        return ans / 100
''',
    call='Solution().calculateTax([[3,50],[7,10],[12,25]], 10)',
    expect=2.65,
    views=[
        dict(type='grid', var='brackets', rows=None, cols=['上限', '税率%'], h=230,
             color=lambda S, i, j, v: 'blue' if S.get('b') is not None and S['brackets'][i] is S['b'] else None),
        dict(type='text', fn=lambda S: (f"已累计 `ans = {S['ans']}`（单位：元×百分点），上一档上限 `pre = {S['pre']}`" if 'pre' in S else ''), h=70),
    ],
    watch=['income', 'pre', 'up', 'p', ('ans', 'ans', 'green')],
    captions={
        'ans, pre = 0': '`ans` 累计「金额 × 税率(整数百分点)」，先不除 100，避免浮点误差；`pre` 是上一档上限',
        'for b in': '看下一个税级 `{b}`',
        'up, p =': '这一档：上限 `up = {up}`，税率 `p = {p}%`',
        'if income <= up': '`income = {income}` {"≤" if income <= up else ">"} `up = {up}`：{"收入在这一档里结束，只算到 income 为止" if income <= up else "收入超过本档，整档都要交税"}',
        'ans += (income - pre)': '最后一段：`({income} − {pre}) × {p}` = {(income - pre) * p} → `ans = {ans}`',
        'break': '收入已经算完，不用再看更高的税级 → 跳出',
        'ans += (up - pre)': '整档：`({up} − {pre}) × {p}` = {(up - pre) * p} → `ans = {ans}`',
        'pre = up': '这一档的上限成为下一档的起点：`pre = {pre}`',
        'return ans / 100': '最后一步才除以 100：`{ans} / 100` = =={ret}==',
    },
    cards=dict(
        one_liner='整数累加到最后，再统一除以 100',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`brackets[i] = [上限, 税率%]`，按上限从低到高',
                 '每档只对「本档上限 − 上一档上限」这一段收税',
                 '示例：`[[3,50],[7,10],[12,25]]`，`income = 10` → `2.65`'],
        quote='把浮点运算放在最后做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一档的收入段是 `up - pre`，税 = 段长 × `p / 100`',
              '先累加 `段长 × p`（全是整数），最后一次除以 100',
              '收入不超过上限时，只算到 `income` 并 `break`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：最后一档要用 `income - pre`，不是 `up - pre`',
                 '`income = 0` 时第一档就 break，结果为 0'],
    ),
)
