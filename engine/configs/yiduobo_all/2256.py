def _f(S):
    i = S.get('index')
    if i is None or 'now' not in S:
        return '平均差 = `|左半平均 − 右半平均|`'
    n = len(S['nums'])
    if i == n - 1:
        return f"右半为空，直接取 `s // n` = {S['s'] // n}"
    return f"左 `{S['now']}//{i + 1}` = {S['now'] // (i + 1)}，右 `{S['s'] - S['now']}//{n - i - 1}` = {(S['s'] - S['now']) // (n - i - 1)}"


CONFIG = dict(
    num=2256, title='最小平均差', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀和 · 总和减前缀',
    tags=['灵神题单·动态规划', '难度分 1395'],
    code='''
class Solution(object):
    def minimumAverageDifference(self, nums):
        s = sum(nums)
        n = len(nums)

        min_diff = None
        res = None
        now = 0
        for index, num in enumerate(nums):
            now += num
            if index == n - 1:
                diff = s // n
            else:
                diff = abs(now // (index + 1) - (s - now) // (n - index - 1))
            if min_diff is None or min_diff > diff:
                min_diff = diff
                res = index

        return res
''',
    call='Solution().minimumAverageDifference([2,5,3,9,5,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 左半 0..index）', cell=84, h=190,
             pointers={'index': 'blue'}, window=(lambda S: 0, 'index'),
             color=lambda S, k, v: 'blue' if k == S.get('index') else None),
        dict(type='text', fn=_f, size=26, h=70),
    ],
    watch=[('s', 's', 'orange'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('diff', 'diff', 'pink'),
           ('min_diff', 'min_diff', 'yellow'), ('res', 'res', 'green')],
    skip=['n = len(nums)', 'res = None'],
    captions={
        's = sum': '先求总和 `s` = =={s}==：后缀和不用单独维护，`s - 前缀和` 就是',
        'min_diff = None': '`min_diff` 还没有值，用 `None` 表示',
        'now = 0': '`now` 维护当前前缀和',
        'for index, num': lambda S, B, r: (f'枚举分割下标 `index = {S.index}`，`nums[0..index]` 是左半'
                                           if S.get('index') != B.get('index') else '所有下标都枚举完'),
        'now += num': '先把 `nums[{index}] = {num}` 加进来：`now` = =={now}==',
        'if index == n - 1': lambda S, B, r: ('`index = n - 1`：右半==长度为 0==，不能再除，直接按 0 处理'
                                              if S.index == S.n - 1 else f'`index = {S.index} < n - 1`，右半非空，正常算两个平均值'),
        'diff = s // n': '右半平均视为 0，所以 `diff` = `s // n` = =={diff}==',
        'diff = abs': '左 `{now}//{index+1}` = {now//(index+1)}，右 `({s}-{now})//{n-index-1}` = {(s-now)//(n-index-1)} → `diff` = =={diff}==',
        'if min_diff is None': lambda S, B, r: ('`min_diff` 是 None，第一个直接记下' if S.min_diff is None
                                                else f'`min_diff = {S.min_diff}` {">" if S.min_diff > S.diff else "≤"} `diff = {S.diff}`：'
                                                     + ('更小，更新' if S.min_diff > S.diff else '不更小，保留之前的（下标更小）')),
        'min_diff = diff': '`min_diff` → =={min_diff}==',
        'res = index': '最优下标 `res` → =={res}==',
        'return res': '最小平均差在下标 `{ret}`',
    },
    cards=dict(
        one_liner='总和减前缀得右半，只需维护一个前缀和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找下标 `index`，使 `nums[0..index]` 的平均值与 `nums[index+1..]` 的平均值之差最小',
                 '平均值向下取整，空区间平均为 0；并列取最小下标',
                 '示例：`[2,5,3,9,5,3]` → `3`'],
        quote='这个后缀和可以通过数组总和减去前缀和得到，因此实际上需要求解的只有一个前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间长度好求：左半 `index+1`，右半 `n-index-1`',
              '先算总和 `s`，遍历时用 `now` 累加前缀，右半和 = `s - now`',
              '遍历到最后一个下标时右半为空，不能除以 0，直接置为 0 的平均'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，删去了类型说明文档字符串',
                 '易错点：`index == n - 1` 时 `diff = s // n`，因为右半平均为 0',
                 '用严格 `min_diff > diff` 更新，并列时保留更小的下标'],
    ),
)
