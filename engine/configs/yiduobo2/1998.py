NUMS = [6, 5, 3, 10]
PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _root(fa, v):
    while fa[v] != v:
        v = fa[v]
    return v


def _active():
    out = set(NUMS)
    for v in NUMS:
        p = 2
        while p * p <= v:
            while v % p == 0:
                out.add(p)
                v //= p
            p += 1
        if v > 1:
            out.add(v)
    return out


ACTIVE = _active()


def _fa_color(S, i, v):
    fa = S.get('fa')
    if fa is None or i not in ACTIVE:
        return None
    roots = sorted({_root(fa, a) for a in ACTIVE})
    return PAL[roots.index(_root(fa, i)) % len(PAL)]


def _groups(S):
    fa = S.get('fa')
    if fa is None or not isinstance(fa, list):
        return ''
    g = {}
    for a in sorted(ACTIVE):
        g.setdefault(_root(fa, a), []).append(a)
    parts = ['{' + ','.join(map(str, v)) + '}' for v in g.values()]
    return '连通块：' + '  '.join(f'`{p}`' for p in parts)


def _cap_union_call(S, B, ret):
    num, now, p = B.num, B.now, B.prime[B.now]
    return f'`{now}` 的最小质因子是 `{p}` → 把数 `{num}` 和质数 `{p}` ==合并到一个集合=='


def _cap_ne(S, B, ret):
    if S.fa_x != S.fa_y:
        return f'`find({S.x}) = {S.fa_x}`，`find({S.y}) = {S.fa_y}`：不在一个集合 → 合并'
    return f'`find({S.x}) = find({S.y}) = {S.fa_x}`：已经连通，不用合并'


def _cap_check(S, B, ret):
    i, num, nums, fa = B.index, B.num, B.nums, B.fa
    if num == nums[i]:
        return f'排序后第 `{i}` 位是 `{num}`，原数组这里也是 `{num}` → 不用动'
    same = _root(fa, num) == _root(fa, nums[i])
    if same:
        return f'第 `{i}` 位要从 `{nums[i]}` 变成 `{num}`：两者==在同一个连通分量==里 → 可以换过来'
    return f'第 `{i}` 位要从 `{nums[i]}` 变成 `{num}`，但它们不连通 → 返回 False'


CONFIG = dict(
    num=1998, title='数组的最大公因数排序', difficulty='Hard', category='图论',
    author='yiduobo', technique='质因数分解 + 并查集',
    tags=['字节30天'],
    code='''
class Solution(object):
    def gcdSort(self, nums):

        max_num = max(nums)
        prime = list(range(max_num + 1))

        x = 2
        while x * x <= max_num:
            now = x + x
            while now <= max_num:
                if prime[now] == now:
                    prime[now] = x
                now += x
            x += 1

        fa = list(range(max_num + 1))
        for num in nums:
            now = num
            while now > 1:
                self.union(num, prime[now], fa)
                now //= prime[now]

        for index, num in enumerate(sorted(nums)):
            if num != nums[index] and self.find(num, fa) != self.find(nums[index], fa):
                return False

        return True

    def union(self, x, y, fa):
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x != fa_y:
            if fa_x < fa_y:
                fa[fa_x] = fa_y
            else:
                fa[fa_y] = fa_x

    def find(self, x, fa):
        if fa[x] != x:
            fa[x] = self.find(fa[x], fa)

        return fa[x]
''',
    call=f'Solution().gcdSort({NUMS})',
    expect=True,
    skip=[9, 10, 11, 12, 13, 18, 21, 30, 31, 39, 40, 42],
    views=[
        dict(type='array', var='nums', label=f'nums（黄 = 当前处理的数；排序后应为 {sorted(NUMS)}）', h=190, cell=76,
             pointers={'index if _line >= 23 else None': 'pink'}, pointer_labels={'index if _line >= 23 else None': 'index'},
             color=lambda S, i, v: 'yellow' if v == S.get('num') and S.get('_line', 0) in (17, 19, 20, 32, 33, 34, 36) else None),
        dict(type='array', var='prime', label='prime[v]：v 的最小质因子（橙 = 合数，被筛过）', h=180, cell=70,
             pointers={'x if _line <= 14 else None': 'blue'}, pointer_labels={'x if _line <= 14 else None': 'x'},
             color=lambda S, i, v: 'orange' if i >= 2 and v != i else None),
        dict(type='array', var=lambda S: S['fa'] if isinstance(S.get('fa'), list) else None,
             label='fa（并查集；同色 = 同一个集合，只给用到的数上色）', h=150, cell=70,
             color=_fa_color),
        dict(type='text', fn=_groups, size=26, h=60),
    ],
    watch=[('num', 'num', 'yellow'), ('now', 'now'), ('fa_x', 'fa_x', 'blue'), ('fa_y', 'fa_y', 'pink')],
    captions={
        'max_num = max(nums)': '`max_num = {max_num}`',
        'prime = list(range': '先用筛法求每个数的==最小质因子==：初始 `prime[v] = v`',
        'x = 2': '从 `x = 2` 开始筛',
        'while x * x <= max_num': lambda S, B, r: (f'`{B.x} × {B.x} = {B.x * B.x} ≤ {S.max_num}`：用 `{B.x}` 去筛它的倍数' if B.x * B.x <= S.max_num
                                                   else f'`{B.x} × {B.x} > {S.max_num}`：筛完了'),
        'x += 1': '`{x - 1}` 的倍数中还没被标记的，最小质因子记为 `{x - 1}`',
        'fa = list(range': '并查集：每个数和每个质数都是一个节点，`fa[v] = v`',
        'for num in nums': lambda S, B, r: (f'分解 `{S.num}` 的质因数' if S.get('num') != B.get('num') or 'num' not in B
                                            else '所有数都处理完：==有公共质因子的数都连在了一起=='),
        'while now > 1': lambda S, B, r: (f'`now = {B.now}` > 1：还有质因子 `prime[{B.now}] = {B.prime[B.now]}`' if B.now > 1
                                          else f'`{B.num}` 分解完毕'),
        'self.union(num, prime[now], fa)': _cap_union_call,
        'if fa_x != fa_y': _cap_ne,
        'if fa_x < fa_y': lambda S, B, r: (f'`{S.fa_x} < {S.fa_y}` → 小的挂到大的下面' if S.fa_x < S.fa_y else f'`{S.fa_x} > {S.fa_y}` → 小的挂到大的下面'),
        'fa[fa_x] = fa_y': '`fa[{fa_x}] = {fa_y}`',
        'fa[fa_y] = fa_x': '`fa[{fa_y}] = {fa_x}`',
        'for index, num in enumerate(sorted': lambda S, B, r: (f'和排序后的数组逐位比较：第 `{S.index}` 位应为 `{S.num}`'
                                                               if S.get('index') != B.get('index') or 'index' not in B else '每一位都能换到位'),
        'if num != nums[index]': _cap_check,
        'return False': '有一位换不过来 → 返回 False',
        'return True': '每一位要的数都和原来的数连通 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='有公共质因子的数连边，同一连通分量里可以任意排列',
        complexity='时间 `O(U log log U + n log U · α)`，空间 `O(U)`',
        problem=['若 `gcd(nums[i], nums[j]) > 1`，可以交换 `nums[i]` 和 `nums[j]`，次数不限',
                 '问能否把 `nums` 排成==非递减顺序==',
                 '示例：`[7,21,3]` → `true`；`[5,2,6,2]` → `false`（5 不能和任何数交换）',
                 f'本视频：`{NUMS}` → `true`（6 和 10 通过质因子 2 相连，6 和 3 通过 3 相连）'],
        quote='把数值不互质的位置之间连上边，就可以得到若干个连通分量。==对于同一个连通分量中的位置，是可以任意排布顺序的==。',
        quote_src='—— yiduobo 题解原文',
        idea=['判断连通：对每个数==分解质因数==，用并查集把数和它的质因子合并',
              '分解质因数：先用筛法求每个数的最小质因子，再迭代除下去',
              '最后和排序后的数组逐位比：不同的位置，两个数必须在同一个集合'],
        summary=['筛法预处理最小质因子，分解每个数只要 `O(log U)` 次除法',
                 '数和==质数==合并（而不是两两求 gcd），避免 `O(n^2)`',
                 '原文为 Python 2 写法：`range(...)` 当列表用 → 改为 `list(range(...))`；`now /= ...` → `now //= ...`',
                 '同时删去了类型说明文档字符串；find 带路径压缩，union 时小的挂到大的下面'],
    ),
)
