EQS = ["b==a", "c==b", "a!=d", "c!=a"]
K = 4  # 只画前 4 个字母 a..d（其余 22 个一直是自己的父亲）


def _fa(S):
    fa = S.get('fa')
    if fa is None or not isinstance(fa, list):
        return None
    return [f'{chr(97 + i)}→{chr(97 + fa[i])}' for i in range(K)]


def _root_color(S, i, v):
    fa = S.get('fa')
    if not isinstance(fa, list):
        return None
    r = i
    while fa[r] != r:
        r = fa[r]
    return {0: 'green', 1: 'cyan', 2: 'purple', 3: 'orange'}.get(r)


_EI = lambda S: S['equations'].index(S['equation']) if 'equation' in S and 'equations' in S else None


def _L(v):
    return chr(97 + v) if isinstance(v, int) and 0 <= v < 26 else v


def _eq(S, B, ret):
    e = S.equation
    if e[1] == '=':
        return f'`"{e}"` 是==等式== → 合并 {e[0]}、{e[3]} 所在集合'
    return f'`"{e}"` 是==不等式== → 先存进 `check_pair`，等所有等式处理完再检查'


def _find(S, B, ret):
    x = S.x
    if x != S.fa[x]:
        return f'find({_L(x)})：父亲是 {_L(S.fa[x])}，不是自己 → 继续往上找'
    return f'find({_L(x)})：{_L(x)} 就是根'


CONFIG = dict(
    num=990, title='等式方程的可满足性', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集：先合并等式，再检查不等式',
    tags=['labuladong', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def equationsPossible(self, equations):

        fa = list(range(26))
        check_pair = []
        for equation in equations:
            x = ord(equation[0]) - 97
            y = ord(equation[3]) - 97
            if equation[1] == '=':
                self.union(x, y, fa)
            else:
                check_pair.append([x, y])

        for x, y in check_pair:
            if self.find(x, fa) == self.find(y, fa):
                return False

        return True

    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)

        return fa[x]

    def union(self, x, y, fa):
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
''',
    call=f'Solution().equationsPossible({EQS})',
    expect=False,
    views=[
        dict(type='array', var=lambda S: S.get('equations'), label='equations', cell=110, h=205,
             pointers={_EI: 'blue'}, pointer_labels={_EI: 'equation'}),
        dict(type='array', var=_fa, label='fa（只画 a..d：字母 → 父亲；同色 = 同一个集合）', cell=110, h=150,
             color=_root_color, index=False),
        dict(type='array', var=lambda S: [f'{_L(a)}!={_L(b)}' for a, b in S['check_pair']] if 'check_pair' in S else None,
             label='check_pair（待检查的不等式）', cell=110, h=140, index=False),
        dict(type='calls', h=120, hide=('fa', 'equations')),
    ],
    watch=[('x', lambda S: _L(S['_inner'].get('x'))), ('y', lambda S: _L(S['_inner'].get('y'))),
           ('fa_x', lambda S: _L(S.get('fa_x'))), ('fa_y', lambda S: _L(S.get('fa_y')))],
    skip=['y = ord(equation[3])', 'check_pair = []'],
    captions={
        'fa = list(range(26))': '并查集初始化：26 个字母==各自为一个集合==，`fa[i] = i`',
        'for equation in equations': lambda S, B, r: (f'取方程 `"{S.equation}"`' if 'equation' not in B or B.equation != S.equation
                                                     else '所有方程都过了一遍'),
        'x = ord(equation[0])': '左右两个字母转成下标：`{x}`（{equation[0]}）和 `{ord(equation[3]) - 97}`（{equation[3]}）',
        "if equation[1] == '='": _eq,
        'self.union(x, y, fa)': lambda S, B, r: f'调用 `union({_L(B.x)}, {_L(B.y)})`：把两个字母所在的集合合并',
        'check_pair.append': '`check_pair` 加入 `{equation}`',
        'if x != fa[x]': _find,
        'fa[x] = self.find(fa[x], fa)': lambda S, B, r: f'递归找父亲 {_L(B.fa[B.x])} 的根，回来后 `fa[{_L(B.x)}]` ==直接指向根==（路径压缩）',
        'return fa[x]': lambda S, B, r: f'find({_L(S.x)}) 返回根 =={_L(r)}==',
        'fa_x = self.find(x, fa)': lambda S, B, r: f'`fa_x = find({_L(B.x)})`：找 {_L(B.x)} 所在集合的根',
        'fa_y = self.find(y, fa)': lambda S, B, r: f'`fa_y = find({_L(B.y)})`：找 {_L(B.y)} 所在集合的根',
        'if fa_x < fa_y': lambda S, B, r: (f'`fa_x = {_L(S.fa_x)} < fa_y = {_L(S.fa_y)}` → 让 {_L(S.fa_y)} 挂到 {_L(S.fa_x)} 下' if S.fa_x < S.fa_y
                                           else (f'根相同（都是 {_L(S.fa_x)}），已经在一个集合' if S.fa_x == S.fa_y
                                                 else f'`fa_x = {_L(S.fa_x)} > fa_y = {_L(S.fa_y)}` → 让 {_L(S.fa_x)} 挂到 {_L(S.fa_y)} 下')),
        'fa[fa_y] = fa_x': lambda S, B, r: f'`fa[{_L(S.fa_y)}] = {_L(S.fa_x)}`：两个集合合并',
        'fa[fa_x] = fa_y': lambda S, B, r: f'`fa[{_L(S.fa_x)}] = {_L(S.fa_y)}`：两个集合合并',
        'for x, y in check_pair': lambda S, B, r: ((f'等式都合并完了，再检查不等式：`{_L(S.x)} != {_L(S.y)}`' if 'fa_x' not in B and B.get('_line') != 24 and len(S.check_pair) and [S.x, S.y] == S.check_pair[0]
                                                    else f'检查下一个不等式 `{_L(S.x)} != {_L(S.y)}`')),
        'if self.find(x, fa) == self.find(y, fa)': lambda S, B, r: f'分别 find {_L(B.x)}、{_L(B.y)} 的根：根相同就说明它们==必须相等==',
        'return False': lambda S, B, r: f'{_L(S.x)}、{_L(S.y)} 的根都是 {_L(S.fa[S.x])}：它们相等，与 `{_L(S.x)} != {_L(S.y)}` ==矛盾== → 返回 `False`',
        'return True': '所有不等式两边都不在同一集合 → 返回 `True`',
    },
    max_steps=70,
    cards=dict(
        one_liner='等式能传递、不等式不能：先用并查集合并所有等式，再逐个检查不等式',
        complexity='时间 `O(n α(26))`，空间 `O(26)`',
        problem=['每个方程形如 `"a==b"` 或 `"a!=b"`（小写字母变量）',
                 '能否给变量赋整数值，让==所有方程同时成立==？',
                 '本视频：`["b==a","c==b","a!=d","c!=a"]` → `false`（c = b = a 却要 c != a）'],
        quote='等式可以传递但是不等式不行，例如我们可以通过a=b和b=c推导出a=c，但是==不能通过a!=b和b!=c推导出a!=c==。',
        quote_src='—— yiduobo 题解原文',
        idea=['利用等式的传递性，==优先处理所有等式==：并查集把相等的变量合到一个集合',
              '再遍历不等式：两侧变量在并查集中根相同 → 矛盾，返回 false',
              '合并时让编号小的根当父亲：`fa[较大根] = 较小根`'],
        summary=['时间约 `O(n)`：路径压缩后 find 近似常数；空间 `O(26)`',
                 '易错：不能边读边判不等式，==必须等所有等式合并完==再检查',
                 '`find` 里 `fa[x] = find(fa[x])` 是路径压缩',
                 '原文为 Python 2 写法，`fa = range(26)` 已改为 `fa = list(range(26))`（Python 3 的 range 不能赋值）'],
    ),
)
