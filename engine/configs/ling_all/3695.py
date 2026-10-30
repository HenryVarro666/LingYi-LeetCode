NUMS = [5, 2, 4, 1, 3]
SWAPS = [[0, 1], [1, 2], [3, 4]]
PAL = ['blue', 'pink', 'purple', 'cyan', 'orange']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _fa(S):
    uf = S.get('uf')
    return list(uf._fa) if uf is not None else None


def _gcol(S, i, v):
    uf = S.get('uf')
    if uf is None:
        return None
    fa = uf._fa
    r = _root(fa, i)
    if sum(1 for k in range(len(fa)) if _root(fa, k) == r) == 1:
        return None
    return PAL[r % len(PAL)]


def _txt(S):
    uf = S.get('uf')
    if uf is None:
        return ''
    odd = '　'.join(f'集合 `{r}` 奇数下标 =={uf.odd[r]}== 个' for r in range(len(uf._fa)) if _root(uf._fa, r) == r)
    return odd


CONFIG = dict(
    num=3695, title='交换元素后的最大交替和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='并查集 · 同组排序后小的取负',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
# 模板来源 https://leetcode.cn/circle/discuss/mOr1u6/
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己
        self._fa = list(range(n))  # 代表元
        self.odd = [i % 2 for i in range(n)]  # 集合中的奇数个数
        self.cc = n  # 连通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        # 如果 fa[x] == x，则表示 x 是代表元
        fa = self._fa
        if fa[x] != x:
            fa[x] = self.find(fa[x])  # fa 改成代表元
        return fa[x]

    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, from_: int, to: int) -> None:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return
        self._fa[x] = y  # 合并集合
        self.odd[y] += self.odd[x]  # 更新集合中的奇数个数

class Solution:
    def maxAlternatingSum(self, nums: List[int], swaps: List[List[int]]) -> int:
        uf = UnionFind(len(nums))
        for p, q in swaps:
            uf.merge(p, q)

        g = defaultdict(list)
        for i, x in enumerate(nums):
            g[uf.find(i)].append(x)  # 相同集合的元素分到同一组

        ans = 0
        for i, a in g.items():
            a.sort()
            odd = uf.odd[i]
            # 小的取负号，大的取正号
            ans += sum(a[odd:]) - sum(a[:odd])
        return ans
''',
    call=f'Solution().maxAlternatingSum({NUMS!r}, {SWAPS!r})',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums（同色 = 同一连通块，可任意交换）', h=170, color=_gcol, cell=90),
        dict(type='array', var=_fa, label='fa（并查集代表元）', h=170, cell=90),
        dict(type='text', fn=_txt, h=70, size=26),
        dict(type='map', var='g', label='g（代表元 → 同组元素）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('i', 'i', 'yellow'), ('odd', 'odd', 'orange'), ('ans', 'ans', 'green')],
    skip=['self._fa = list', 'self.odd = [', 'self.cc = n', 'fa = self._fa', 'x, y = self.find', 'return fa[x]'],
    captions={
        'uf = UnionFind': '一开始每个下标自成一个集合；`odd[i]` 记录集合中奇数下标个数',
        'for p, q in swaps': lambda S, B, ret: (f'能交换 `{S.p}` 和 `{S.q}` → 把它们所在集合合并' if 'p' not in B or (S.p, S.q) != (B.p, B.q) else '所有交换对都合并完了'),
        'uf.merge(p, q)': '合并 `{p}` 与 `{q}`',
        'if fa[x] != x': lambda S, B, ret: (f'`find({S.x})`：`fa[{S.x}] = {S.fa[S.x]}` ≠ `{S.x}`，不是代表元 → 往上找' if S.fa[S.x] != S.x
                                            else f'`find({S.x})`：`fa[{S.x}] = {S.x}`，自己就是代表元'),
        'fa[x] = self.find': '先递归找上一层的代表元，回来后把 `fa[x]` 直接改成代表元（路径压缩）',
        'if x == y': lambda S, B, ret: ('已在同一集合，不用合并' if S.x == S.y else f'代表元 `{S.x}` ≠ `{S.y}`：两个集合要合并'),
        'self._fa[x] = y': '把 `{x}` 的集合并到 `{y}` 下面',
        'self.odd[y] += self.odd[x]': '奇数下标个数相加 → 集合 `{y}` 有 `{self.odd[y]}` 个奇数下标',
        'g = defaultdict': '按集合分组：同一连通块里的值放在一起',
        'for i, x in enumerate(nums)': lambda S, B, ret: (f'下标 `{S.i}`，值 `{S.x}`' if 'i' not in B or S.i != B.i else '分组完成'),
        'g[uf.find(i)].append(x)': '这个值放进它所在集合（代表元）的组 → `{dict(g)}`',
        'for i, a in g.items()': lambda S, B, ret: (f'处理集合 `{S.i}`，组内值 `{S.a}`' if 'a' not in B or S.i != B.i else '所有组都算完了'),
        'a.sort()': '组内排序：`{a}`',
        'odd = uf.odd[i]': '这个集合有 `{odd}` 个奇数下标 → 需要 `{odd}` 个负号',
        'ans += sum': lambda S, B, ret: f'小的前 `{S.odd}` 个取负：`−{sum(S.a[:S.odd])}`，其余取正：`+{sum(S.a[S.odd:])}` → ans `{S.ans}`',
        'return ans': '最大交替和 `{ans}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='同一连通块里的数能随意排：小的放奇数位，大的放偶数位',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 的交替和 = 偶数下标之和 − 奇数下标之和，要最大化',
                 '`swaps` 里的下标对可以交换任意次、任意顺序',
                 '本视频：`nums = [5,2,4,1,3]`，`swaps = [[0,1],[1,2],[3,4]]` → `9`'],
        quote='用并查集把 p_i 和 q_i 合并。合并后，同一集合（连通块）中的元素可以随意交换。……对于同一组，设奇数下标个数为 odd。把元素从小到大排序后，前 odd 个元素取负号，其余元素取正号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合并 `(p, q)`：连通块里的元素可以任意排列',
              '负号位置 = 奇数下标，个数就是并查集额外维护的 `odd`',
              '同组从小到大排序：前 `odd` 个最小的取负，其余取正'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '并查集除了找代表元，还要在 `merge` 里累加 `odd`',
                 '题解还给了建图 + DFS + 快速选择的 `O(n)` 做法',
                 '易错：`odd` 要用集合代表元 `i` 去取，不是 `nums` 下标',
                 '同类题：1202 交换字符串中的元素、1722 最小汉明距离'],
    ),
)
