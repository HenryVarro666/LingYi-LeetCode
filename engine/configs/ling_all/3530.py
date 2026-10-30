def _txt(S):
    if 's' not in S or 'f' not in S:
        return '`pre[j]`：课程 j 的先修课集合（二进制，第 x 位 = 1 表示课 x 是先修课）'
    n = len(S['pre'])
    s = S['s']
    got = [k for k in range(n) if s >> k & 1]
    return f'已学 `S = {s:0{n}b}`（课程 {got}），`i = |S|+1 = {S.get("i", bin(s).count("1") + 1)}`，`f[S] = {S["f"][s]}`'


CONFIG = dict(
    num=3530, title='有向无环图中合法拓扑排序的最大利润', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP · 刷表法（先修课）',
    tags=['灵神题单', '动态规划', '难度分 2353'],
    code='''
class Solution:
    def maxProfit(self, n: int, edges: List[List[int]], score: List[int]) -> int:
        if not edges:
            score.sort()
            return sum(s * i for i, s in enumerate(score, 1))

        # 记录每个节点的先修课（直接前驱）
        pre = [0] * n
        for x, y in edges:
            pre[y] |= 1 << x

        f = [-1] * (1 << n)
        f[0] = 0
        for s, fs in enumerate(f):
            if fs < 0:  # 不合法状态，比如已经学完后面的课程，但前面的课程还没学
                continue
            i = s.bit_count() + 1  # 已学课程数加一
            # 枚举还没学过的课程 j，且 j 的所有先修课都学完了
            for j, p in enumerate(pre):
                if (s >> j & 1) == 0 and (s | p) == s:
                    new_s = s | 1 << j
                    r = f[s] + score[j] * i
                    if r > f[new_s]:  # 手写 max
                        f[new_s] = r
        return f[-1]
''',
    call='Solution().maxProfit(3, [[0, 1], [0, 2]], [1, 6, 3])',
    expect=25,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='score', label='score（蓝 = 正在考虑的课 j）', cell=70, h=170, pointers={'j': 'blue'}),
        dict(type='array', var='f', label='f[S]（-1 = 不合法；黄 = 当前 S，绿 = 刚更新的 S∪{j}）', cell=76, h=210,
             pointers={'s': 'yellow', 'new_s': 'green'},
             color=lambda S, i, v: 'green' if v >= 0 else None,
             dim=lambda S, i, v: v < 0),
        dict(type='array', var='pre', label='pre[j]：j 的先修课集合（二进制数）', cell=70, h=170, pointers={'j': 'blue'}),
    ],
    watch=['s', 'fs', 'i', 'j', 'p', 'new_s', 'r'],
    skip=['enumerate(f)', 'for x, y in edges', 'for j, p in enumerate', 'pre = [0]'],
    captions={
        'if not edges': '`edges` 非空 → 不能直接排序，要考虑先修关系（没有边时按分数从小到大选最优，排序不等式）',
        'pre[y] |= 1 << x': lambda S, B, r: f'边 `{S.x} → {S.y}`：课 {S.x} 是课 {S.y} 的先修课，`pre[{S.y}] = {S.pre[S.y]:0{S.n}b}`',
        'f = [-1]': '`f[S]`：已学集合为 `S` 时已获得的最大利润；`-1` = 还没到达（不合法）',
        'f[0] = 0': '一门课都没学，利润 0',
        'if fs < 0': lambda S, B, r: (f'`f[{B.s}] = {B.fs} < 0`：==没被更新过==，说明这个状态不合法（先修课没学完就学了后面的课）→ 跳过'
                                      if B.fs < 0 else f'`f[{B.s}] = {B.fs}`：合法状态，往后转移'),
        'i = s.bit_count()': '已学 `{i-1}` 门，下一门是==第 `{i}` 个==学的 → 得分乘 `{i}`',
        'if (s >> j & 1) == 0': lambda S, B, r: (
            f'课 {B.j} 已学过 → 跳过' if B.s >> B.j & 1 else
            (f'课 {B.j} 没学过，先修课 `{B.p:0{B.n}b}` ⊆ `S = {B.s:0{B.n}b}` → ==可以学==' if B.s | B.p == B.s
             else f'课 {B.j} 没学过，但先修课 `{B.p:0{B.n}b}` 还没学完 → 不能学')),
        'new_s = s | 1 << j': '学完课 `{j}`：`S` 变成 `new_s = {new_s:0{n}b}`',
        'r = f[s] + score[j] * i': '利润 `r = f[{s}] + score[{j}] × {i} = {f[s]} + {score[j]*i}` = =={r}==',
        'if r > f[new_s]': '`r = {B.r}` 对比 `f[{B.new_s}] = {B.f[B.new_s]}`：{"更大 → 更新" if B.r > B.f[B.new_s] else "不更大 → 不变"}',
        'f[new_s] = r': '`f[{new_s}]` 更新为 =={r}==（学课顺序不同可能到达同一个集合，取最大）',
        'return f[-1]': '全部学完 `f[-1]` = =={ret}==：最优顺序是 `0 → 2 → 1`',
    },
    max_steps=60,
    cards=dict(
        one_liner='把拓扑序看成选课：先修课全学完才能学下一门',
        complexity='时间 `O(m + n·2^n)`，空间 `O(2^n)`',
        problem=['`n` 个节点的有向无环图，`edges[i] = [u, v]` 表示 `u` 在 `v` 之前',
                 '合法拓扑序里第 `p` 个处理的节点，利润 = `score × p`，总利润取和',
                 '求最大总利润；示例：`n=3, edges=[[0,1],[0,2]], score=[1,6,3]` → `25`'],
        quote='把拓扑序理解为先修课关系，在学习课程 j 之前，j 的所有先修课（直接前驱）必须全部学完。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用二进制集合 `S` 表示已学课程，`pre[j]` 表示 j 的先修课集合',
              '枚举下一门 `j`：`j ∉ S` 且 `pre[j] ⊆ S`（即 `s | p == s`），得分 `score[j] × (|S|+1)`',
              '写法三是刷表法：从 `f[S]` 去更新 `f[S∪{j}]`，没被更新过的状态不合法，直接跳过'],
        summary=['时间 `O(m + n·2^n)`，空间 `O(2^n)`',
                 '`pre[y] |= 1 << x`：边 `x→y` 表示 x 是 y 的先修课；`(s | p) == s` 判断先修课全学完',
                 '没有边时按分数从小到大排序即最优（排序不等式），可直接返回',
                 '另两种写法：写法一记忆化搜索，写法二倒序递推（会超时），写法三刷表法最快',
                 '`bit_count` 为 Python 3.10+，Mac 的 3.10 上可用'],
    ),
)
