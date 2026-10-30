CONFIG = dict(
    num=1553, title='吃掉 N 个橘子的最少天数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索 · 减 1 只为凑整除',
    tags=['灵神题单', '动态规划', '难度分 2048'],
    code='''
class Solution(object):
    def minDays(self, n):

        f = {}
        return self.dfs(n, f)

    def dfs(self, now, f):
        if now not in f:
            if now == 1:
                f[now] = 1
            elif now == 2:
                f[now] = 2
            else:
                f[now] = min(self.dfs(now // 2, f) + 1 + now % 2, self.dfs(now // 3, f) + 1 + now % 3)
        
        return f[now]
''',
    call='Solution().minDays(10)',
    expect=4,
    views=[
        dict(type='map', var='f', label='f：吃掉 i 个橘子的最少天数（记忆）', fmt=lambda k, v: f'f[{k}]={v}', font=28, h=190),
        dict(type='calls', h=300, hide=('f',)),
    ],
    watch=[('now', 'now', 'blue')],
    captions={
        'f = {}': '`f` 是备忘录：`f[i]` 表示吃掉 i 个橘子的最少天数',
        'return self.dfs(n, f)': '从 `n = {n}` 开始往下求',
        'if now not in f': lambda S, B, r: (f'`{S.now}` 还没算过，往下算' if S.now not in S.f else f'`{S.now}` 已经在 f 里了，直接用，不再重复算'),
        'if now == 1': lambda S, B, r: ('只剩 1 个：`now == 1`' if S.now == 1 else '`now` 不是 1，看下一个边界'),
        'f[now] = 1': '只剩 1 个橘子，吃 1 天：`f[1] = 1`',
        'elif now == 2': lambda S, B, r: ('只剩 2 个：`now == 2`' if S.now == 2 else '`now` 不是 2，走一般情况'),
        'f[now] = 2': '2 个橘子：吃 1 个再吃 1 个或直接除以 2 再吃 1 个，都是 2 天：`f[2] = 2`',
        'f[now] = min': '取「凑整除后除以 2」与「凑整除后除以 3」中较小的：先减 `now % 2` 或 `now % 3` 次 1，再 +1 天做除法',
        'return f[now]': '返回 `f[{now}] = {f[now]}`',
    },
    cards=dict(
        one_liner='减 1 只是为除以 2、除以 3 做铺垫',
        complexity='时间 `O(log²n)`，空间 `O(log²n)`',
        problem=['每天：吃 1 个；`n` 被 2 整除吃 `n/2` 个；被 3 整除吃 `2n/3` 个',
                 '求吃光 `n` 个橘子的最少天数',
                 '本视频：`10` → `4`'],
        quote='不会出现超过两次减1之后接上一个除以2这种情况，因为完全可以在可以除以2时就先除以2。同样地，也不会出现超过3次减一之后接上一个除以3这种情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素方程 `f[i] = min(f[i-1], f[i/2], f[i/3]) + 1` 状态太多，不可行',
              '减 1 只用来凑整除：转移改成 `f[i] = min(f[i//2] + i%2 + 1, f[i//3] + i%3 + 1)`',
              '用字典 `f` 记忆化，每个状态只算一次'],
        summary=['递归边界：`f[1] = 1`，`f[2] = 2`',
                 '`i % 2`、`i % 3` 是为凑整除而减 1 的次数',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '不记忆化会指数级重复计算'],
    ),
)
