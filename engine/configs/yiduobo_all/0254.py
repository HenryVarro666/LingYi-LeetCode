CONFIG = dict(
    num=254, title='因子的组合', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='记忆化搜索 · 因子递减去重',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def getFactors(self, n):

        f = {}
        f[1] = []

        def dfs(now,):
            if now not in f:
                f[now] = [[now]]
                x = 2
                while x * x <= now:
                    if now % x == 0:
                        for combo in dfs(now // x):
                            if combo[-1] >= x:
                                f[now].append(combo[:])
                                f[now][-1].append(x)
                    x += 1

            return f[now]

        return dfs(n)[1:]
''',
    call='Solution().getFactors(12)',
    expect=[[6, 2], [3, 2, 2], [4, 3]],
    views=[
        dict(type='map', var='f', label='f：now → 乘积为 now 的因子组合（含 [now] 本身）', h=300,
             fmt=lambda k, v: str(v)),
        dict(type='calls', h=200),
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"`now = {S['_inner']['now']}`，试除 `x = {S['_inner']['x']}`" if 'x' in S['_inner'] else '')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('x', lambda S: S['_inner'].get('x'), 'orange'),
           ('combo', lambda S: S['_inner'].get('combo'), 'pink')],
    skip=['f = {}', 'f[1] = []'],
    captions={
        'if now not in f': lambda S, B, ret: (f"`{S['_inner']['now']}` 还没算过 → 开始计算" if S['_inner']['now'] not in B['f']
                                              else f"`{S['_inner']['now']}` ==已在 f 里==，直接用记忆的结果"),
        'f[now] = [[now]]': '先放入 `[{now}]`：==自身不拆==也算一组，最后返回时要去掉',
        'x = 2': '从因子 `2` 开始枚举，`x * x <= now` 即可',
        'while x * x': lambda S, B, ret: (f"`{S['_inner']['x']}×{S['_inner']['x']} <= {S['_inner']['now']}`，继续枚举" if S['_inner']['x'] ** 2 <= S['_inner']['now']
                                          else f"`{S['_inner']['x']}×{S['_inner']['x']} > {S['_inner']['now']}`，枚举结束"),
        'if now % x == 0': '`{now} % {x} == 0`？→ {"整除，x 是因子" if now % x == 0 else "不是因子"}',
        'for combo in dfs': '取 `dfs({now} // {x}) = dfs({now // x})` 的组合，逐个尝试追加 `{x}`',
        'if combo[-1] >= x': lambda S, B, ret: (f"`combo[-1] = {S['_inner']['combo'][-1]} >= x = {S['_inner']['x']}`：保持==单调不增==，可以追加 `{S['_inner']['x']}`"
                                                if S['_inner']['combo'][-1] >= S['_inner']['x']
                                                else f"`combo[-1] = {S['_inner']['combo'][-1]} < x = {S['_inner']['x']}`：追加后会变成递增，和已有组合重复 → 跳过"),
        'f[now].append(combo[:])': '复制 `combo` 放进 `f[{now}]`（必须复制，否则会改到别处的记忆结果）',
        'f[now][-1].append(x)': '末尾追加 `{x}` → `{f[now][-1]}`',
        'x += 1': '`x` → {x}',
        'return f[now]': '`f[{now}]` = `{f[now]}`',
        'return dfs(n)[1:]': lambda S, B, ret: (f'`[1:]` 去掉第一个 `[{S.n}]`（自身）→ `{ret}`' if ret is not None else f'调用 `dfs({S.n})`，求 `{S.n}` 的全部因子组合'),
    },
    max_steps=120,
    cards=dict(
        one_liner='枚举最小因子 x，递归拆 n/x，只接受不增的组合',
        complexity='时间约 `O(n·√n)` 量级（因子组合数很少），空间 `O(n)`',
        problem=['把整数 `n` 写成 ==大于 1 且小于 n== 的因子的乘积，列出所有不同的组合（顺序不同算同一种）',
                 '示例：`n = 12` → `[[2,6],[2,2,3],[3,4]]`（顺序不限）（顺序不限）',
                 '本视频：`n = 12`，代码输出 `[[6,2],[3,2,2],[4,3]]`'],
        quote='对于合并的因子组合以及x，若这个因子组合中最小的因子大于等于x，才执行合并操作，这样一来就可以保证得到的所有因子组合都是单调不增的。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举 `n` 的因子 `x`，递归求 `n/x` 的全部因子组合，再追加 `x`',
              '同一个数会被多次递归，用字典 `f` 做==记忆化==',
              '`[2,4]` 和 `[4,2]` 重复：要求组合末尾 `>= x`，保证单调不增'],
        result='得到 3 组，去掉自身 `[12]` 后返回',
        summary=['`f[now]` 里先放了 `[now]` 自身，所以最后要 `[1:]` 去掉',
                 '追加前必须 `combo[:]` 复制，否则会污染记忆里的列表',
                 '`combo[-1] >= x` 是去重的关键',
                 '原文为 Python 2 写法，整数除法 `now / x` 已改为 `now // x`'],
    ),
)
