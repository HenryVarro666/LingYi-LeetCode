def _k(S):
    """当前处理的下标：由前缀和反推（示例前缀和互不相同）"""
    if 'num' not in S or 'now' not in S:
        return None
    nums, now = S['nums'], S['now']
    after = S['_line'] >= _AFTER
    tot = 0
    for k, x in enumerate(nums):
        if (not after and tot == now) or (after and tot + x == now):
            return k
        tot += x
    return None


_AFTER = 7

CONFIG = dict(
    num=1413, title='逐步求和得到正数的最小值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='前缀和 · 找最小前缀和',
    code='''
class Solution(object):
    def minStartValue(self, nums):

        res = 1
        now = 0
        for num in nums:
            now += num
            if now < 0:
                res = max(res, -now + 1)
        
        return res
''',
    call='Solution().minStartValue([-3,2,-3,2,4])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前元素，灰 = 已处理）', cell=90, h=230,
             color=lambda S, i, v: 'blue' if _k(S) == i else None,
             dim=lambda S, i, v: _k(S) is not None and i < _k(S)),
        dict(type='text', fn=lambda S: (f"当前 `res = {S['res']}`：前缀和 `now = {S['now']}`，加上起始值 = =={S['now'] + S['res']}==（要 ≥ 1）" if 'now' in S and 'res' in S else ''), size=30, h=100),
        dict(type='text', fn=lambda S: '要求：每一步 `起始值 + now ≥ 1`，所以前缀和最低到 `m` 时，起始值至少是 `1 − m`', size=26, h=80),
    ],
    watch=[('num', 'num', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 1': '`res` 是答案：起始值至少为 1',
        'now = 0': '`now` 是前缀和',
        'for num in nums': '取下一个数 `num = {num}`',
        'now += num': '前缀和 `now` = `{B.now} + ({num})` = =={now}==',
        'if now < 0': lambda S, B, r: (f'`now = {S.now} < 0`：前缀和为负，起始值必须补够 → ==需要更新答案==' if S.now < 0
                                       else f'`now = {S.now} ≥ 0`：起始值 1 就够了，不用动'),
        'res = max': '起始值至少 `-now + 1 = {-now + 1}` 才能让这一步 ≥ 1 → `res = max({B.res}, {-now + 1})` = =={res}==',
        'return res': '前缀和最低点对应的起始值就是答案：`{res}`',
    },
    cards=dict(
        one_liner='起始值取决于前缀和的最低点：最低点为 m，答案就是 1 − m',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个整数数组 `nums`，选一个正数起始值 `startValue`，从左到右逐步累加',
                 '要求每一步的累加和都 ==≥ 1==，求最小的 `startValue`',
                 '示例：`[-3,2,-3,2,4]` → `5`'],
        quote='直接一趟扫描计算前缀和，在计算的过程中找出前缀和中的最小值。若这个最小值为负数，那么这个最小值的倒数加上1就是最终答案，否则答案为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['起始值 `s` 加上每个前缀和都要 ≥ 1，只需最小的前缀和满足即可',
              '最小前缀和为负数 `m`：`s + m ≥ 1` → `s ≥ 1 − m`；否则 `s = 1`',
              '代码里边扫边把 `res` 抬到 `-now + 1` 的最大值，等价于取最低点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`res` 初值是 1（不是 0），因为起始值必须是正数',
                 '易错：前缀和为负数才更新，`-now + 1` 里的 `+1` 不能漏',
                 '原文题解里的“倒数”实为“相反数”：`-m + 1`',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
