def _eq(S):
    if 'v' in S and 'a' in S and 'cnt' in S:
        return f"当前方程 `val[{S['a']}] = val[{S['b']}] × {S['v']}`"
    return ''


def _rel(S):
    if 'fa_a' in S and 'fa_b' in S and S.get('_line') is not None:
        return f"`fa_a = {S['fa_a']}`，`fa_b = {S['fa_b']}`" if S['fa_a'] == S['fa_b'] else ''
    return ''


CONFIG = dict(
    num=2307, title='检查方程中的矛盾之处', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='带权并查集 · 倍数关系',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def checkContradictions(self, equations, values):

        fa = {}
        weight = {}
        eps = 10 ** -5

        def find(x):
            if x not in fa:
                fa[x] = x
                weight[x] = 1.0
            elif fa[x] != x:
                tmp = find(fa[x])
                weight[x] *= weight[fa[x]]
                fa[x] = tmp
                
            
            return fa[x]

        mapping = {}
        cnt = 0
        for (a, b), v in zip(equations, values):
            if a not in mapping:
                mapping[a] = cnt
                cnt += 1
            
            if b not in mapping:
                mapping[b] = cnt
                cnt += 1
            
            a = mapping[a]
            b = mapping[b]

            fa_a = find(a)
            fa_b = find(b)

            

            if fa_a == fa_b:
                if abs(weight[a] - weight[b] * v) > eps:
                    return True
            else:
                fa[fa_b] = fa_a
                weight[fa_b] = weight[a] / weight[b] / v

        return False
''',
    call="Solution().checkContradictions([['a','b'],['b','c'],['a','c']], [3, 0.5, 5])",
    expect=True,
    views=[
        dict(type='text', h=70, size=30, fn=_eq),
        dict(type='map', var='mapping', label='mapping（变量名 → 编号）', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var='fa', label='fa（父节点）', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var='weight', label='weight（到父节点的倍数）', fmt=lambda k, v: f'{k}: {v:.3g}', h=130, font=28),
        dict(type='calls', h=170),
    ],
    watch=['a', 'b', 'v', 'fa_a', 'fa_b'],
    captions={
        'fa = {}': '`fa` 保存父节点，用字典，节点第一次出现时再建',
        'weight = {}': '`weight[x]` 满足 `weight[x] * val[x] = val[fa[x]]`，即 x 到父亲的倍数',
        'eps = ': '浮点数比较用误差 `eps`，不直接用 `==`',
        'if x not in fa': lambda S, B, r: (f'`{S.x}` 第一次出现：自成一块' if S.x not in B.fa
                                           else f'`{S.x}` 已经在并查集里了'),
        'fa[x] = x': '`fa[{x}] = {x}`，自己是根',
        'weight[x] = 1.0': '`weight[{x}] = 1.0`：到自己的倍数为 1',
        'elif fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}`，不是根 → 要往上找根并压缩路径' if S.fa[S.x] != S.x
                                            else f'`fa[{S.x}] = {S.x}`：{S.x} 就是根，直接返回'),
        'tmp = find': '递归找父亲的根 `tmp = {tmp}`，递归过程中父亲的 `weight` 已更新为到根的倍数',
        'weight[x] *= ': 'x→父亲→根：倍数相乘，`weight[{x}]` → =={weight[x]:.3g}==',
        'fa[x] = tmp': '`fa[{x}]` 直接指向根 `{tmp}`',
        'return fa[x]': '返回 `{x}` 的根 `{ret}`',
        'mapping[a] = cnt': '变量名映射成数字编号：`{a}` → `{cnt}`',
        'mapping[b] = cnt': '变量名映射成数字编号：`{b}` → `{cnt}`',
        'cnt += 1': '编号加一',
        'a = mapping[a]': '`a` 换成编号 `{a}`',
        'b = mapping[b]': '`b` 换成编号 `{b}`',
        'fa_a = find': '`find(a)`：找 a 的根，并让 `weight[a]` 变成 a 到根的倍数',
        'fa_b = find': '`find(b)`：找 b 的根，并让 `weight[b]` 变成 b 到根的倍数',
        'if fa_a == fa_b': lambda S, B, r: (f'根相同 `{S.fa_a}`：a、b 已在同一块，`val[a]/val[b]` 已确定，要验证是否等于 v' if S.fa_a == S.fa_b
                                            else f'根不同 `{S.fa_a} != {S.fa_b}`：之前没有关系，合并两块，不会矛盾'),
        'if abs(weight[a]': '已有结论 `val[a]/val[b] = {weight[a]/weight[b]:.3g}`，题目给 `v = {v}`，差 `{abs(weight[a] - weight[b] * v):.3g}` > `eps`，不一致',
        'return True': '`val[a] / val[b]` 与已有结论不一致 → 发现==矛盾==，返回 True',
        'fa[fa_b] = fa_a': '`fa_b` 的根挂到 `fa_a` 下：`fa[{fa_b}] = {fa_a}`',
        'weight[fa_b] = ': '`weight[fa_b] = weight[a] / weight[b] / v` = =={weight[fa_b]:.3g}==（由 `val[b]/val[a] = 1/v` 推出）',
        'return False': '所有方程都没有冲突，返回 False',
    },
    skip=['return fa[x]'],
    max_steps=110,
    cards=dict(
        one_liner='用带权并查集记录倍数，同一块里再出现的方程只需校验',
        complexity='时间 `O(n α(n))`，空间 `O(n)`',
        problem=['给出方程 `A / B = v`（即 `val[A] = val[B] × v`），判断这些方程是否==互相矛盾==',
                 '两个值的比相差不超过 `1e-5` 视为相等',
                 '本视频：`a=3b`、`b=0.5c`、`a=5c` → 由前两式 `a=1.5c`，与第三式矛盾 → `True`'],
        quote='除了常规并查集维护每个节点的父节点fa之外，还需要维护使用另一个数组weight维护当前节点与父节点的放缩关系。简单来说，就是weight[x] * val[x] = val[fa[x]]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`weight[x]` 记录 x 到父亲的倍数；`find` 压缩路径时倍数相乘',
              '新方程两端同根：`weight[a]` 与 `weight[b] * v` 必须相等，否则矛盾',
              '不同根：`fa[fa_b] = fa_a`，`weight[fa_b] = weight[a] / weight[b] / v`（由 `val[b]/val[a] = 1/v` 推得）'],
        summary=['时间近似 `O(n)`，空间 `O(n)`',
                 '先用 `mapping` 把字符串变量映射成整数编号',
                 '浮点比较要用 `eps`，不能直接判等',
                 '`find` 里先递归再乘 `weight[fa[x]]`，顺序不能反',
                 '题面库里没有，题意按 LeetCode 2307 和 yiduobo 原文整理；原文代码无需改动即可在 Python 3 运行'],
    ),
)
