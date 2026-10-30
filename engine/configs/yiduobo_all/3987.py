CONFIG = dict(
    num=3987, title='处理所有元素的成本', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='整体看待 · 求和后算次数',
    tags=['灵神题单', '贪心与思维', '难度分 1550'],
    code='''
class Solution(object):
    def minimumCost(self, nums, k):
        
        s = sum(nums)
        if s <= k:
            return 0
        
        need = s - k
        mod = 10 ** 9 + 7
        t = (need - 1) // k + 1
        return (1 + t) * t // 2 % mod
''',
    call='Solution().minimumCost([1,2,7,13], 4)',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums（资源不会虚空消耗，当成一个整体）', cell=100),
        dict(type='text', size=28, fn=lambda S: (
            f"总需求 `s = {S['s']}`，初始资源 `k = {S['k']}`" + (f"，还缺 `need = {S['need']}`" if 'need' in S else '')
            if 's' in S else '')),
        dict(type='text', size=28, fn=lambda S: (f"补 `t = {S['t']}` 次：成本 `1+2+…+{S['t']}` = =={(1+S['t'])*S['t']//2}==" if 't' in S else '')),
    ],
    watch=[('s', 's', 'blue'), ('k', 'k', 'pink'), 'need', ('t', 't', 'green')],
    captions={
        's = sum': '把 nums 看成一个整体：总共要消耗 `s = {s}`',
        'if s <= k': lambda S, B, r: (f'`s = {S.s} ≤ k = {S.k}`：初始资源就够，成本 0' if S.s <= S.k
                                      else f'`s = {S.s} > k = {S.k}`：初始资源不够，需要补充'),
        'need = ': '上一次补充的资源还能留到后面用 → 只需补够 `need = {s} - {k}` = =={need}==',
        'mod = ': '答案要对 `10^9 + 7` 取模',
        't = ': '每次补 `k = {k}`，次数 `t = ({need} - 1) // {k} + 1` = =={t}==',
        'return (1': '补 `t` 次，成本 `1 + 2 + … + {t}` = `(1+{t})×{t}//2` = ==15==',
    },
    cards=dict(
        one_liner='资源不会虚空消耗：只看总和，一次算出补几次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['按顺序处理 `nums`，资源不够就补 `k` 单位，第 j 次补充成本为 j',
                 '求处理完所有元素的最小总成本（对 `10^9+7` 取模）',
                 '本视频：`nums=[1,2,7,13]`，`k=4` → `15`'],
        quote='由于这里的资源是不会虚空消耗的，也就是说上一次补充的资源使用之后，还可以累加到之后使用，因此在这里完全可以将nums视为一个整体。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文先推逐步模拟：每次 `need = nums[i]-now`，补 `(need-1)//k+1` 次',
              '再进一步：整体看，先求和 `s`，把初始 `k` 补到 `≥ s`',
              '次数 `t` 确定后，成本就是 `1 + 2 + … + t`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`s <= k` 要先特判返回 0，否则 `need - 1` 会变成负数',
                 '原文为 Python 2 风格，只多了空行，代码未改',
                 '对比灵神：灵神先逐个模拟再给出等价的整体写法；yiduobo 直接用整体求和'],
    ),
)
