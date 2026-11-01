def _fa(S):
    u = S.get('u')
    if u is None:
        return None
    return list(u.fa)


def _fa_color(S, k, v):
    n = len(S['a'])
    if k < n:
        return 'blue'
    return 'orange' if v != k else None


def _groups(S):
    g = S.get('groups')
    if g is None:
        return None
    return {p: f'{x[0]}@{x[1]}' for p, x in enumerate(g) if x[0]}


def _txt(S):
    a = S.get('a')
    n = S.get('n')
    if a is None or n is None:
        return '预处理：每个数的质因子 `pf[v]`；下标 i 与质数 p+n 放进同一个并查集'
    ln = S.get('_line', 0)
    if 'v' in S and 'i' in S and ln <= 20:
        return f"`a[{S['i']}] = {S['v']}`，质因子 `pf[{S['v']}] = {PF[S['v']]}`：下标 {S['i']} 并到质数结点 `p + n`（橙色，下标 ≥ {n}）"
    return '同一个集合里的数可以随便换位置 → 每组内部排序后按原下标填回去'


PF = {}
for _v in range(2, 9):
    PF[_v] = [p for p in range(2, _v + 1) if _v % p == 0 and all(p % q for q in range(2, p))]


CONFIG = dict(
    num=1998, title='数组的最大公因数排序', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='质因数分解 + 中介并查集（Go 原文转写）',
    tags=['常用数据结构', '难度分 2429'],
    setup='''
mx = 8
pf = [[] for _ in range(mx + 1)]
for i in range(2, mx + 1):
    if not pf[i]:
        for j in range(i, mx + 1, i):
            pf[j].append(i)
''',
    code='''
class UnionFind:
    def __init__(self, n):
        self.fa = list(range(n))

    def find(self, x):
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def merge(self, from_, to):
        self.fa[self.find(from_)] = self.find(to)


class Solution:
    def gcdSort(self, a: List[int]) -> bool:
        n = len(a)
        u = UnionFind(n + mx)
        for i, v in enumerate(a):
            for p in pf[v]:
                u.merge(i, p + n)  # 用并查集将下标 i 和质数 p 合并，为了区分下标集合和质数集合，将 p 加上 n

        # 整理处于同一集合的元素及其下标
        groups = [[[], []] for _ in range(mx)]  # groups[p] = [vs, is]
        for i, v in enumerate(a):
            p = u.find(i) - n
            groups[p][0].append(v)
            groups[p][1].append(i)

        # 每一组内的元素可以直接或间接交换，因此对每组元素直接排序，然后按照在原数组中的顺序填回去
        for g in groups:
            g[0].sort()
            for j, v in enumerate(g[0]):
                a[g[1][j]] = v
        return all(a[i - 1] <= a[i] for i in range(1, n))  # 判断数组是否有序
''',
    call='Solution().gcdSort([4, 2, 5, 7])',
    expect=True,
    skip=['n = len(a)', 'p = u.find(i) - n', 'for j, v in enumerate', 'def ', 'for g in groups', 'if self.fa[x] != x', 'return self.fa[x]', 'self.fa[x] = self.find(self.fa[x])'],
    max_steps=80,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='a', label='a', cell=90, h=150, pointers={'i': 'blue'},
             color=lambda S, k, v: 'green' if S.get('_line', 0) >= 28 and S.get('g') and k in S['g'][1] and S['g'][0] else None),
        dict(type='array', var=_fa, label='并查集 fa（0..n-1 = 下标，n.. = 质数 p+n）', cell=64, h=160, color=_fa_color),
        dict(type='map', var=_groups, label='groups[质数] = 值列表@原下标列表', fmt=lambda k, v: f'质数 {k}：{v}', h=170, font=22),
    ],
    watch=[('n', 'n', 'blue'), ('i', 'i', 'blue'), ('v', 'v', 'pink'), ('p', 'p', 'yellow')],
    captions={
        'u = UnionFind': '并查集开 `n + mx` 个结点：前 n 个是下标，后面是质数（p + n）',
        'for i, v in enumerate': lambda S, B, r: ('所有数都处理完了' if B.get('i') == S.get('i') and B.get('v') == S.get('v') else f'看 `a[{S.i}] = {S.v}`'),
        'for p in pf[v]': lambda S, B, r: (f'`{S.v}` 的质因子是 `{S.pf[S.v] if "pf" in S else PF[S.v]}`，逐个处理' if 'p' not in B or B.get('p') == S.get('p') else f'质因子 `p = {S.p}`'),
        'u.merge(i, p + n)': '`merge(下标 {i}, 质数结点 {p + n})`：有同一质因子的数，通过这个质数结点连成一个集合',
        'groups = [': '准备 `groups[p]`：按集合代表元把值和原下标分组',
        'for i, v in enumerate(a):\n': '',
        'groups[p][0].append(v)': '`a[{i}] = {v}` 属于代表元 `{u.find(i) - n}` 这一组：记下值',
        'groups[p][1].append(i)': '同时记下它的原下标 `{i}`',
        'g[0].sort()': lambda S, B, r: (f'这一组（代表元的值和下标）：`{S.g[0]}`、`{S.g[1]}`，==组内排序==：同组的数可任意换位 → `{S.g[0]}`' if S.g[0] else '这一组是空的（没有数用到这个质数），跳过'),
        'a[g[1][j]] = v': '把排好序的第 {j} 个值 `{v}` 填回这组的第 {j} 个原位置 `a[{g[1][j]}]`',
        'return all': lambda S, B, r: f'整个数组 `{S.a}` {"是非递减的 → True" if r else "不是非递减的 → False"}',
    },
    cards=dict(
        one_liner='共享质因子就能换位：下标和质数连进同一个并查集',
        complexity='时间 `O(n log C)`，空间 `O(n + C)`（C 为值域上界）',
        problem=['`gcd(nums[i], nums[j]) > 1` 才能交换这两个数，操作任意次',
                 '问能否把数组排成非递减',
                 '示例：`[10,5,9,3,15]` → `true`；本视频演示 `[4,2,5,7]`（质数表上限缩小为 8）'],
        quote='用并查集将下标 i 和质数 p 合并，为了区分下标集合和质数集合，将 p 加上 n。每一组内的元素可以直接或间接交换，因此对每组元素直接排序，然后按照在原数组中的顺序填回去。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['有公共质因子就能换 → 把「下标 i」与它的每个质因子 p 连到同一个集合，==质数当中介==',
              '同集合内的数可以任意重排（连通 = 可换位）',
              '每组排好序填回原位置，最后检查整个数组是否有序'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；质因子表 `pf` 的预处理（原文 `init`）放在 setup，且视频里把 `mx` 从 `1e5` 缩小为 8 方便演示',
                 '`struct{vs, is}` 用 `[vs, is]` 的二元列表表示，`sort.IntsAreSorted` 用逐项比较代替',
                 '时间 `O(n log C)`（质因子个数 ≤ log C），空间 `O(n + C)`',
                 '易错点：质数结点要 `+ n` 与下标区分；每个 `a[i] ≥ 2` 至少有一个质因子，所以代表元一定是质数结点'],
    ),
)
