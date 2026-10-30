CONFIG = dict(
    num=2709, title='最大公约数遍历', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='筛法 + 并查集',
    tags=['常用数据结构', '数学算法'],
    code='''
class Solution(object):
    def canTraverseAllPairs(self, nums):

        distinct_nums = []
        index_dict = {}
        mi = 10 ** 5
        ma = 0
        for v in nums:
            mi = min(mi, v)
            ma = max(ma, v)
            if v not in index_dict:
                index_dict[v] = len(distinct_nums)
                distinct_nums.append(v)

        if mi == 1:
            return len(nums) == 1

        prime = [True] * (ma + 1)
        p = 2
        fa = list(range(len(distinct_nums) + 1))

        def find(x):
            if fa[x] != x:
                return find(fa[x])
            return fa[x]

        for p in range(2, ma + 1):
            if prime[p]:
                fa_p = None
                if p in index_dict:
                    fa_p = find(index_dict[p])
                for x in range(p + p, ma + 1, p):
                    prime[x] = False
                    if x in index_dict:
                        fa_x = find(index_dict[x])
                        if fa_p is None:
                            fa_p = fa_x
                        else:
                            fa[fa_x] = fa_p

        fa_x = find(0)
        for index in range(1, len(distinct_nums)):
            if find(index) != fa_x:
                return False
        return True
''',
    call='Solution().canTraverseAllPairs([4,3,6])',
    expect=True,
    views=[
        dict(type='array', var='distinct_nums', label='distinct_nums（下标 = 并查集里的节点编号）', h=150, cell=70,
             pointers={'index': 'cyan'},
             color=lambda S, i, v: 'yellow' if 'x' in S and S.get('_line', 0) > 0 and v == S.get('x') else None),
        dict(type='array', var='fa', label='fa（并查集父亲；下标 = distinct_nums 的下标）', h=150, cell=70,
             color=lambda S, i, v: 'green' if v != i else None),
        dict(type='array', var='prime', label='prime（黄 = 当前素数 p，粉 = 正在划掉的倍数 x）', h=200, cell=60,
             pointers={'p': 'yellow', 'x if _line in (32, 33, 34, 35, 36, 37, 39) else None': 'pink'},
             pointer_labels={'x if _line in (32, 33, 34, 35, 36, 37, 39) else None': 'x'},
             dim=lambda S, i, v: i < 2 or not v),
        dict(type='text', fn=lambda S: (f"素数 `p = {S['p']}` 的倍数全部连到同一块：当前 `x = {S['x']}`" if 'x' in S and 'prime' in S and S.get('_line', 0) > 30 else '')),
    ],
    watch=[('p', 'p', 'yellow'), ('x', 'x', 'pink'), 'fa_p', 'fa_x', ('mi', 'mi', 'cyan'), ('ma', 'ma', 'green')],
    captions={
        'mi = min': '`mi = min({B.mi}, {v}) = {mi}`：顺手记下最小值，判断有没有 1',
        'ma = max': '`ma = max({B.ma}, {v}) = {ma}`：最大值决定筛到哪里',
        'index_dict[v] = len': '`{v}` 第一次出现，给它编号 `{index_dict[v]}`：并查集只管不同的数',
        'if mi == 1': lambda S, B, r: ('最小值是 1：1 和任何数的 gcd 都是 1，==1 连不上别人==' if S.mi == 1 else '没有 1，继续一般情况'),
        'return len(nums) == 1': '有 1 时只有数组仅含这一个数才为 `{ret}`',
        'prime = [True]': '`prime[x]` 标记是否还是素数，筛到最大值 `{ma}`',
        'fa = list': '并查集初始化：每个不同的数各自一块，`fa = {fa}`',
        'def find': '`find` 顺着父亲一路找到根（这里没有路径压缩）',
        'for p in range': '枚举 `p = {p}`',
        'if prime[p]': lambda S, B, r: (f'`{S.p}` 是素数 → 它的所有倍数都有公因数 `{S.p}`，要连到同一块（`fa_p` 记这一族的代表）' if S.prime[S.p] else f'`{S.p}` 已被划掉，是合数，跳过'),
        'fa_p = None': '`fa_p`：这个素数这一族的代表，暂时没有',
        'fa_p = find(index_dict[p])': '`{p}` 本身就在数组里：这一族的代表取它所在块的根',
        'for x in range(p + p': '枚举 `{p}` 的倍数 `x = {x}`',
        'prime[x] = False': '`{x}` 是 `{p}` 的倍数 → 合数',
        'if x in index_dict': lambda S, B, r: (f'`{S.x}` 在数组里（编号 {S.index_dict[S.x]}），要并入 `{S.p}` 这一族' if S.x in S.index_dict else f'`{S.x}` 不在数组里，只划掉不连'),
        'fa_x = find(index_dict[x])': '找到 `{x}`（编号 {index_dict[x]}）所在块的根 `fa_x`',
        'if fa_p is None': lambda S, B, r: ('这一族还没有代表 → 先把 `fa_x` 当代表' if S.fa_p is None else f'族代表已是 `{S.fa_p}`，要把 `{S.fa_x}` 并过来'),
        'fa_p = fa_x': '族代表 `fa_p = {fa_p}`',
        'fa[fa_x] = fa_p': '合并：`fa[{fa_x}] = {fa_p}`，现在 `fa = {fa}`',
        'fa_x = find(0)': '最后看所有数是不是同一个根，先取 0 号的根',
        'for index in range(1': '检查编号 `{index}` 的数',
        'if find(index) != fa_x': '编号 `{index}` 的数：根和 0 号的根 `{fa_x}` 相同吗？不同就连不到 0 号 → 返回 False',
        'return True': '所有数同根：任意两个下标都能走通，返回 `True`',
    },
    skip=['distinct_nums = []', 'index_dict = {}', 'mi = 10', 'ma = 0', 'distinct_nums.append', 'p = 2', 'prime[x] = False', 'fa_p = None', 'mi = min'],
    max_steps=110,
    cards=dict(
        one_liner='按素数筛：同一个素数的倍数，全部并到一起',
        complexity='时间 `O(M log log M)`（M 为最大值，再乘并查集 α），空间 `O(M)`',
        problem=['数组 `nums`，下标 `i` 和 `j` 之间能走，当且仅当 `gcd(nums[i], nums[j]) > 1`',
                 '问任意两个下标之间是否都存在路径',
                 '示例：`[4,3,6]` → `True`（4、6 有公因数 2，3、6 有公因数 3）'],
        quote='在筛法求素数的过程中，一边通过素数的倍数更新合数，一边将这些合数通过并查集连通到一起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['两两枚举是 `O(n^2)`，不行；数值范围只有 `10^5`，可以从数值入手',
              '有公因数 ⇔ 有公共素因子：每个素数 `p` 的倍数全连到一块',
              '先处理特殊情况：有 1 就连不上别人',
              '筛法结束后看所有数是不是同一个根'],
        summary=['时间约 `O(M log log M)`，空间 `O(M)`',
                 '易错点：数组里含 1，只有长度为 1 才为 True',
                 '`find` 没有路径压缩，数据大时可能偏慢；`p` 本身在数组里时要把它当族代表',
                 '原文为 Python 2 写法，`fa = range(...)` 已改为 `fa = list(range(...))`（Python 3 的 range 不能赋值）'],
    ),
)
