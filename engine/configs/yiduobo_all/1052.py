def _wl(S):
    if 'index' not in S:
        return None
    return max(0, S['index'] - S['X'] + 1)


def _ccol(S, i, v):
    if 'index' not in S or i > S['index']:
        return None
    if S['grumpy'][i] == 0:
        return 'green'
    return 'pink' if _wl(S) <= i else None


def _cdim(S, i, v):
    if 'index' not in S or i > S['index']:
        return False
    return S['grumpy'][i] == 1 and i < _wl(S)


def _txt(S):
    if 'origin' not in S:
        return ''
    return (f"`origin = {S['origin']}`（不生气，必然满意）　`now = {S['now']}`　"
            f"`change = {S['change']}`")


CONFIG = dict(
    num=1052, title='爱生气的书店老板', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='origin + 长为 X 的滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1418'],
    code='''
class Solution(object):
    def maxSatisfied(self, customers, grumpy, X):

        origin = 0
        now = 0
        change = 0
        for index in range(X):
            if grumpy[index] == 0:
                origin += customers[index]
            else:
                now += customers[index]

        change = now
        for index in range(X, len(customers)):
            if grumpy[index] == 0:
                origin += customers[index]
            else:
                now += customers[index]

            if grumpy[index - X] == 1:
                now -= customers[index - X]

            change = max(change, now)

        return change + origin
''',
    call='Solution().maxSatisfied([1,0,1,2,1,1,7,5], [0,1,0,1,0,1,0,1], 3)',
    expect=16,
    views=[
        dict(type='array', var='customers', label='customers（绿 = 计入 origin，粉 = 窗口内计入 now）', h=240, cell=96,
             pointers={'index': 'blue'}, window=(_wl, 'index'), color=_ccol, dim=_cdim),
        dict(type='array', var='grumpy', label='grumpy', h=150, cell=96,
             color=lambda S, i, v: 'pink' if v else None),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('origin', 'origin', 'green'), ('now', 'now', 'pink'),
           ('change', 'change', 'orange')],
    captions={
        'origin = 0': '`origin`：grumpy 为 0 的顾客总数，==无论如何都满意==',
        'now = 0': '`now`：当前窗口内 grumpy 为 1 的顾客数',
        'change = 0': '`change`：`now` 的最大值，也就是技巧最多能多挽回几人',
        'for index in range(X)': lambda S, B, ret: (f'初始化窗口 `0..{S.X - 1}`：看第 `{S.index}` 分钟'
                                                   if 'index' not in B or S.index != B.index else '初始窗口统计完了'),
        'for index in range(X, len': lambda S, B, ret: (f'右边界移到 `{S.index}`，左边 `{S.index - S.X}` 将离开'
                                                        if B.get('index') != S.index else '窗口滑到底了'),
        'if grumpy[index] == 0': lambda S, B, ret: (f'`grumpy[{S.index}] = 0`：老板不生气，顾客本来就满意'
                                                    if S.grumpy[S.index] == 0 else f'`grumpy[{S.index}] = 1`：生气，要靠技巧挽回'),
        'origin += customers[index]': '`origin += {customers[index]}` → `{origin}`',
        'now += customers[index]': '新加入窗口的是生气时的顾客：`now += {customers[index]}` → `{now}`',
        'change = now': '第一个窗口能挽回 `now = {now}` 人，作为 `change` 初值',
        'if grumpy[index - X] == 1': lambda S, B, ret: (f'离开窗口的第 `{S.index - S.X}` 分钟老板生气 → 要从 now 里减掉'
                                                        if S.grumpy[S.index - S.X] == 1 else
                                                        f'离开窗口的第 `{S.index - S.X}` 分钟老板不生气 → 它在 origin 里，now 不变'),
        'now -= customers[index - X]': '`now -= {customers[index - X]}` → `{now}`',
        'change = max': lambda S, B, ret: (f'`now = {S.now} > {B.change}` → 窗口放这里更好，`change = {S.change}`'
                                           if S.change > B.change else f'`now = {S.now} ≤ {B.change}`，`change` 不变'),
        'return change + origin': '`change + origin = {change} + {origin}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='先把不生气的顾客全收下，再找挽回最多生气顾客的窗口',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`customers[i]` 是第 i 分钟的顾客数；`grumpy[i] = 1` 时老板生气，顾客不满意',
                 '老板能让自己==连续 X 分钟==不生气（只能用一次），求最多满意顾客数',
                 '示例：`[1,0,1,2,1,1,7,5]`，`[0,1,0,1,0,1,0,1]`，`X = 3` → `16`'],
        quote='所有grumpy等于0时的顾客都必然是满意的，设这些顾客的总数为origin，那么我们的目标就是找到一个区间，使得这个区间内==grumpy等于1时对应的顾客总数最多==。',
        quote_src='—— yiduobo 题解原文',
        idea=['技能固定连续 X 分钟 → 区间长度固定为 X → 滑动窗口',
              '右边界进来的若 grumpy 为 1，`now` 加上；左边界出去的若为 1，`now` 减掉',
              '答案 = 滑动过程中最大的 `now` + `origin`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先单独初始化 `0..X−1` 的窗口，再从 X 开始每次右移一格',
                 '易错：离开窗口时只有 ==grumpy 为 1== 的才从 now 里减',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神用 `s[g] += c` 一个循环同时算两部分'],
    ),
)
