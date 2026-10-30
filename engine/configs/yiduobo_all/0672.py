CONFIG = dict(
    num=672, title='灯泡开关 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='状态闭环 · 分类讨论',
    code='''
class Solution(object):
    def flipLights(self, n, m):

        if n == 0:
            return 1

        if m == 0:
            return 1

        if n == 1:
            return 2

        if n == 2:
            if m == 1:
                return 3
            else:
                return 4

        if m == 1:
            return 4
        elif m == 2:
            return 7
        else:
            return 8
''',
    call='[Solution().flipLights(1, 1), Solution().flipLights(2, 1), Solution().flipLights(3, 1), Solution().flipLights(3, 2), Solution().flipLights(5, 5)]',
    expect=[2, 3, 4, 7, 8],
    views=[
        dict(type='text', size=34, fn=lambda S: (f"当前询问：灯泡数 `n = {S['n']}`，操作次数 `m = {S['m']}`" if 'n' in S else '')),
        dict(type='text', size=30, fn=lambda S: '操作：1 翻转全部；2 翻转偶数位；3 翻转奇数位；4 翻转 3k+1 位'),
        dict(type='text', size=30, fn=lambda S: '同一操作做两次无效；操作 1 = 操作 2 + 操作 3'),
        dict(type='text', size=30, fn=lambda S: '8 个状态闭环：`m=0` → 1，`m=1` → 4，`m=2` → 7，`m≥3` → 8'),
    ],
    watch=[('n', 'n', 'blue'), ('m', 'm', 'pink')],
    captions={
        'if n == 0': lambda S, B, r: ('`n = 0`：没有灯泡，只有一种状态 → 返回 1' if S.n == 0 else f'`n = {S.n}` 不是 0 → 往下判断'),
        'if m == 0': lambda S, B, r: ('`m = 0`：不操作，灯泡全亮，只有 1 种 → 返回 1' if S.m == 0 else f'`m = {S.m}` > 0 → 往下判断'),
        'if n == 1': lambda S, B, r: ('`n = 1`：四种操作对一个灯泡都等于翻转它，只有开/关 2 种 → 返回 2' if S.n == 1 else '`n ≥ 2` → 往下判断'),
        'if n == 2': lambda S, B, r: ('`n = 2`：操作 3、4 都只动灯泡 1，有效操作只有 3 种 → 分情况' if S.n == 2 else '`n ≥ 3`：四种操作互不重合 → 按 m 分情况'),
        'if m == 1:': lambda S, B, r: (f'`m = {S.m}`' + (' → 做一次操作' if S.m == 1 else ' → 不止一次，状态更多')),
        'elif m == 2': lambda S, B, r: f'`m = {S.m}`' + (' → 两次操作可得 7 种（s0 也能回到）' if S.m == 2 else ' → 三次及以上'),
        'return 3': '`n = 2, m = 1`：一次操作得 s1、s2、s3 → ==3 种==',
        'return 4': lambda S, B, r: ('`n = 2, m ≥ 2`：s0~s3 全能到 → ==4 种==' if S.n == 2 else '`n ≥ 3, m = 1`：一次操作得 s1~s4 → ==4 种=='),
        'return 7': '`n ≥ 3, m = 2`：第二轮得 s0、s1、s2、s3、s5、s6、s7 → ==7 种==',
        'return 8': '`m ≥ 3`：第三轮起 s0~s7 全部可达 → ==8 种==',
        'return 1': '只有初始状态 → 1 种',
        'return 2': '只有开/关两种 → 2 种',
    },
    cards=dict(
        one_liner='先推出 8 个状态的闭环，再按灯泡数、操作数分类',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 盏灯，四种操作：全部翻转 / 翻转偶数位 / 翻转奇数位 / 翻转第 `3k+1` 位',
                 '恰好做 `m` 次操作，问最终有多少种不同的灯光状态',
                 '示例：`n=1, m=1` → `2`；`n=3, m=2` → `7`',
                 '本视频连续问 5 组 `(n, m)`'],
        quote='执行的顺序是无关紧要的……执行两次相同的操作将无事发生。最后，操作2和操作3各执行一次相当于执行了一次操作1。',
        quote_src='—— yiduobo 题解原文',
        idea=['顺序无关、同一操作两次抵消，操作 1 = 操作 2 + 操作 3',
              '设 s0 全亮，推出 s0~s7 共 8 个状态互相转移，形成闭环',
              '第一轮得 4 个，第二轮得 7 个，第三轮起全部 8 个',
              '灯泡不够时操作会重合：`n=1` 只有 2 种，`n=2` 最多 4 种'],
        summary=['时间、空间都是 `O(1)`：直接查结论',
                 '易错：`m = 0` 时只有 1 种；`m = 2` 是 7 而不是 8',
                 '易错：`n = 1`、`n = 2` 时操作重合，要单独讨论',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
