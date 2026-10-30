def _uf(S, key):
    u = S.get('u')
    return getattr(u, key, None) if u is not None else None


CONFIG = dict(
    num=3551, title='数位和排序需要的最小交换次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='下标连边 · 并查集数环',
    tags=['难度分 1507'],
    code='''
# 完整的并查集模板，见我的数据结构题单
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己，大小为 1
        self._fa = list(range(n))  # 代表元
        self.cc = n  # 连通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        # 如果 fa[x] == x，则表示 x 是代表元
        if self._fa[x] != x:
            self._fa[x] = self.find(self._fa[x])  # fa 改成代表元
        return self._fa[x]

    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, from_: int, to: int) -> None:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了
        self.cc -= 1  # 成功合并，连通块个数减一

class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        a = sorted((sum(map(int, str(x))), x, i) for i, x in enumerate(nums))
        n = len(a)
        u = UnionFind(n)
        for i, t in enumerate(a):
            u.merge(i, t[2])
        return n - u.cc
''',
    call='Solution().minSwaps([18, 43, 34, 16])',
    expect=2,
    views=[
        dict(type='array', var=lambda S: [t[1] for t in S['a']] if 'a' in S else [], label='排序后的数（数位和升序，同和按值）；原数组 [18,43,34,16]',
             cell=100, h=190, pointers={'i': 'blue'}),
        dict(type='array', var=lambda S: [t[2] for t in S['a']] if 'a' in S else [], label='t[2]：每个数排序前的下标（排序后位置 i → t[2] 连边）',
             cell=100, h=190, pointers={'i': 'blue'}),
        dict(type='array', var=lambda S: _uf(S, '_fa'), label='并查集 fa（代表元）', cell=100, h=190,
             color=lambda S, i, v: 'green' if v == i else None),
        dict(type='text', h=70, size=28, fn=lambda S: (f"连通块个数 `cc = {_uf(S, 'cc')}`，答案 = n − cc" if _uf(S, 'cc') is not None else '')),
    ],
    watch=['i', ('n', 'n', 'green'), ('cc', "_uf(S, 'cc')", 'yellow')],
    captions={
        'self._fa = list(range(n))': '一开始每个点自成一个集合：`fa = {self._fa}`',
        'self.cc = n': '连通块个数先记为 `n`',
        'a = sorted(': '按（数位和，数值，原下标）排序：`{a}`',
        'n = len(a)': '`n = {n}`',
        'u = UnionFind(n)': '建并查集：`n` 个点，每个点是排序前的一个下标',
        'for i, t in enumerate(a)': '第 `{i}` 个位置：排序后这里该放原下标 `{t[2]}` 的数（`{t[1]}`）',
        'u.merge(i, t[2])': '在「排序后位置 `{i}`」与「排序前下标 `{t[2]}`」之间连边',
        'x, y = self.find': '分别找 `from_ = {from_}` 和 `to = {to}` 所在集合的代表元',
        'if x == y': '`x = {x}`，`y = {y}`：{"同一个集合 → 又成环，这条边不合并" if x == y else "不同集合 → 要合并"}',
        'self._fa[x] = y': '合并：`fa[{x}] = {y}`',
        'self.cc -= 1': '成功合并，连通块个数减一 → `cc = {self.cc}`',
        'return n - u.cc': '每个大小为 k 的环需要 k−1 次交换，合计 `n − cc = {n} − {u.cc}` = =={ret}==',
    },
    skip=['return self._fa[x]'],
    max_steps=90,
    cards=dict(
        one_liner='排序前后下标连边成环，每个环要 k−1 次交换',
        complexity='时间 `O(n log U + n log n)`，空间 `O(n)`',
        problem=['互不相同的正整数数组 `nums`，按数位和升序排，和相同则数值小的在前',
                 '每次交换任意两个位置的值，求排成该顺序的最少交换次数',
                 '示例：`[18,43,34,16]`，数位和 `[9,7,7,7]`，排序后 `[16,34,43,18]`，答案 `2`',
                 '本视频：`nums = [18,43,34,16]` → `2`'],
        quote='在「排序前的元素下标」与「排序后的元素下标」之间连边，得到一个图。图中每个大小为 k 连通块（有 k 个点和 k 条边，是个环），需要 k-1 次交换操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右，把元素交换到它排序后的位置：一个大小为 k 的环要换 k−1 次',
              '所以答案 = n − 连通块个数（每个连通块少操作一次）',
              '数连通块用并查集：对每个排序后位置 `i` 与原下标 `t[2]` 做 `merge`，最后看 `cc`'],
        summary=['时间 `O(n log U + n log n)`，空间 `O(n)`',
                 '易错点：连边连的是下标，不是元素值，下标范围小，可以直接用数组',
                 '`merge` 成功才让 `cc` 减一，同集合时不能重复减',
                 '`find` 做路径压缩，保证接近 `O(1)`',
                 '写法二：不用并查集，直接把访问过的位置标 −1，沿环走一圈，数环的个数 `cc`，答案同样是 `n − cc`'],
    ),
)
