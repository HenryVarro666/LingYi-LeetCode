CONFIG = dict(
    num=1913, title='两个数对之间的最大乘积差', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描 · 最大两数与最小两数',
    code='''
class Solution(object):
    def maxProductDifference(self, nums):

        ma1 = ma2 = 0
        mi1 = mi2 = 10001
        for num in nums:
            if num > ma1:
                ma1, ma2 = num, ma1
            elif num > ma2:
                ma2 = num

            if num < mi1:
                mi1, mi2 = num, mi1
            elif num < mi2:
                mi2 = num
        
        return ma1 * ma2 - mi1 * mi2
''',
    call='Solution().maxProductDifference([5,6,2,7,4])',
    expect=34,
    views=[
        dict(type='text', fn=lambda S: (f"最大两个：`{S['ma1']}`、`{S['ma2']}`　最小两个：`{S['mi1']}`、`{S['mi2']}`" if 'ma1' in S and 'mi2' in S else ''), size=30),
        dict(type='array', var='nums', h=300, label='nums',
             color=lambda S, i, v: ('green' if v in (S.get('ma1'), S.get('ma2')) else 'pink' if v in (S.get('mi1'), S.get('mi2')) else None) if 'num' in S else None,
             dim=lambda S, i, v: False),
        dict(type='text', fn=lambda S: (f"当前 `num = {S['num']}`" if 'num' in S else ''), size=30),
    ],
    watch=['num', ('ma1', 'ma1', 'green'), ('ma2', 'ma2', 'green'), ('mi1', 'mi1', 'pink'), ('mi2', 'mi2', 'pink')],
    captions={
        'ma1 = ma2 = 0': '最大、次大从 `0` 开始（数都是正数）',
        'mi1 = mi2 = 10001': '最小、次小从 `10001` 开始（比上限 10^4 大）',
        'for num in nums': lambda S, B, r: ('数组扫完，四个数都找到了' if 'num' in B and B.num == S.num and S.nums[-1] == S.num else f'一趟扫描，同时维护最大两个和最小两个：当前 `num = {S.num}`'),
        'if num > ma1': lambda S, B, r: f'`{S.num} > ma1 = {S.ma1}`？' + ('成立 → 新的最大值' if S.num > S.ma1 else '不成立'),
        'ma1, ma2 = num, ma1': '新最大 `ma1 = {ma1}`，旧最大退位成次大 `ma2 = {ma2}`',
        'elif num > ma2': lambda S, B, r: f'没超过最大，但 `{S.num} > ma2 = {S.ma2}`？' + ('成立 → 新的次大值' if S.num > S.ma2 else '不成立'),
        'ma2 = num': '次大值更新：`ma2 = {ma2}`',
        'if num < mi1': lambda S, B, r: f'`{S.num} < mi1 = {S.mi1}`？' + ('成立 → 新的最小值' if S.num < S.mi1 else '不成立'),
        'mi1, mi2 = num, mi1': '新最小 `mi1 = {mi1}`，旧最小退位成次小 `mi2 = {mi2}`',
        'elif num < mi2': lambda S, B, r: f'没低于最小，但 `{S.num} < mi2 = {S.mi2}`？' + ('成立 → 新的次小值' if S.num < S.mi2 else '不成立'),
        'mi2 = num': '次小值更新：`mi2 = {mi2}`',
        'return': '最大积 `{ma1} × {ma2}` 减最小积 `{mi1} × {mi2}` = =={ret}==',
    },
    cards=dict(
        one_liner='数都是正数：最大积 = 最大两数相乘，最小积 = 最小两数相乘',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数对 `(a,b)` 与 `(c,d)` 的乘积差为 `a*b - c*d`',
                 '从 `nums` 选四个不同下标，使乘积差最大，返回这个最大值',
                 '示例：`[5,6,2,7,4]` → `34`（`6*7 - 2*4`）'],
        quote='由于题目给出的数都是正数，那么最大的乘积显然是数组中最大的两个数相乘得到的，而最小的乘积则是数组中最小的两个数相乘得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积差要最大：被减的积尽量小，减的积尽量大',
              '正数下，大积用最大两数，小积用最小两数',
              '不用排序：一趟扫描维护 `ma1/ma2/mi1/mi2` 四个变量'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '更新次大前，要先判断是否超过最大：超过时旧最大退位成次大',
                 '初始值：最大从 `0`，最小从 `10001`，由数据范围决定',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串，其余原样'],
    ),
)
