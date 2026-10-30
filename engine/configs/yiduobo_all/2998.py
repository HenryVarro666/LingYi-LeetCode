CONFIG = dict(
    num=2998, title='使 X 和 Y 相等的最少操作次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='暴力 BFS（x−y 轮上界）',
    tags=['图论算法', '难度分 1795'],
    code='''
class Solution(object):
    def minimumOperationsToMakeEqual(self, x, y):

        if x < y:
            return y - x
        
        vis = set([x])
        q = [x]
        head, tail = 0, 1
        for rnd in range(x - y):
            for x in q[head : tail]:
                if x % 5 == 0 and x // 5 not in vis:
                    q.append(x // 5)
                    vis.add(q[-1])
                if x % 11 == 0 and x // 11 not in vis:
                    q.append(x // 11)
                    vis.add(q[-1])
                if x + 1 not in vis:
                    q.append(x + 1)
                    vis.add(q[-1])
                if x - 1 not in vis:
                    q.append(x - 1)
                    vis.add(q[-1])
                
                if y in vis:
                    return rnd + 1
            
            head, tail = tail, len(q)
        
        return x - y
''',
    call='Solution().minimumOperationsToMakeEqual(26, 1)',
    expect=3,
    views=[
        dict(type='text', h=70, fn=lambda S: f"BFS 第 `{S['rnd'] + 1}` 轮（`rnd` = =={S['rnd']}==）；目标 `y = {S['y']}`" if 'rnd' in S else ''),
        dict(type='array', var='q', label='q（BFS 队列；蓝框 = 本轮处理的窗口 [head, tail)）', cell=56, h=190,
             pointers={'head': 'blue', 'tail': 'pink'}, window=('head', lambda S: S['tail'] - 1)),
        dict(type='set', var='vis', label='vis（已入队的数字）', h=190, font=24),
    ],
    watch=[('rnd', 'rnd', 'blue'), 'x', 'y', ('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    captions={
        'if x < y': lambda S, B, r: (f'`x = {S.x} < y = {S.y}`：只有 +1 能让 x 变大 → 答案就是 `y - x`' if S.x < S.y
                                     else f'`x = {S.x} >= y = {S.y}`：要往下走，开始 BFS'),
        'vis = set': '`vis` 记录出现过的数字，避免重复入队',
        'q = [x]': '队列初始只有起点 `{x}`',
        'head, tail = 0, 1': '`[head, tail)` 是本轮要处理的区间',
        'for rnd in range': lambda S, B, r: ('轮次上界是 `x - y`：全用 -1 也要 25 步，BFS 不会更久；这里一轮 = 一层' if S.rnd == 0 else f'进入第 `{S.rnd + 1}` 轮'),
        'for x in q': lambda S, B, r: f'本轮处理的数字 `x = {S.x}`（这里复用了变量名 x）',
        'x % 5 == 0 and': lambda S, B, r: (f'`{S.x}` 是 5 的倍数且 `{S.x // 5}` 没见过 → 除以 5 入队' if S.x % 5 == 0 and S.x // 5 not in B.vis
                                          else (f'`{S.x}` 不是 5 的倍数 → 不能除 5' if S.x % 5 else f'`{S.x // 5}` 已见过 → 跳过')),
        'x % 11 == 0 and': lambda S, B, r: (f'`{S.x}` 是 11 的倍数且 `{S.x // 11}` 没见过 → 除以 11 入队' if S.x % 11 == 0 and S.x // 11 not in B.vis
                                           else (f'`{S.x}` 不是 11 的倍数 → 不能除 11' if S.x % 11 else f'`{S.x // 11}` 已见过 → 跳过')),
        'x + 1 not in vis': lambda S, B, r: (f'`{S.x + 1}` 没见过 → `+1` 入队' if S.x + 1 not in B.vis else f'`{S.x + 1}` 见过了 → 跳过'),
        'x - 1 not in vis': lambda S, B, r: (f'`{S.x - 1}` 没见过 → `-1` 入队' if S.x - 1 not in B.vis else f'`{S.x - 1}` 见过了 → 跳过'),
        'vis.add(q[-1])': '刚入队的 `{q[-1]}` 立刻记进 `vis`',
        'if y in vis': lambda S, B, r: (f'`y = {S.y}` 已经被走到了 → 第 `{S.rnd + 1}` 轮就是最少操作数' if S.y in S.vis
                                        else f'`y = {S.y}` 还没出现在 `vis` 里，继续'),
        'return rnd + 1': '返回 `rnd + 1` = =={ret}==',
        'head, tail = tail': '本轮结束，下一轮区间 `[{head}, {tail})`',
        'return x - y': '（兜底）',
    },
    skip=['q.append', 'vis = set'],
    max_steps=80,
    cards=dict(
        one_liner='x、y 不大，直接暴力 BFS，轮数上界是 x−y',
        complexity='时间 `O(x)` 量级，空间 `O(x)`',
        problem=['正整数 `x`、`y`；每次可：5 的倍数除以 5、11 的倍数除以 11、`x±1`',
                 '求让 `x` 变成 `y` 的最少操作数',
                 '示例：`x=26, y=1` → `3`'],
        quote='四种操作只有加1操作可以使得x变大，因此当x小于y时，答案就是y - x。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x < y`：只能 +1，直接 `y - x`',
              '否则从 `x` 开始 BFS，每个数尝试四种操作，新数字入队',
              '轮数不会超过 `x - y`（全用 -1），所以不用针对 5 和 11 做特殊优化'],
        summary=['数字范围 ≤ 10⁴，用 `set` 去重的暴力 BFS 足够',
                 '`for x in q[head : tail]` 里复用了变量名 `x`，所以兜底的 `return x - y` 不是原始 x',
                 '`y in vis` 一出现就返回当前轮数 `rnd + 1`',
                 '原文为 Python 2 写法，其中的 `/` 已改为 `//`（整数除法）'],
    ),
)
