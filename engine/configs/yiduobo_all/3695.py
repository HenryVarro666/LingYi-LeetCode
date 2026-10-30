NUMS = [5, 2, 4, 1, 3]
SWAPS = [[0, 1], [1, 2], [3, 4]]
PAL = ['blue', 'pink', 'purple', 'cyan', 'orange']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _gcol(S, i, v):
    fa = S.get('fa')
    if fa is None:
        return None
    r = _root(fa, i)
    if sum(1 for k in range(len(fa)) if _root(fa, k) == r) == 1:
        return None
    return PAL[r % len(PAL)]


def _txt(S):
    g = S.get('group')
    if not g:
        return '先用并查集连通下标，再按连通块分组'
    return '　'.join(f'块 `{k}`：下标 {v}' for k, v in g.items())


CONFIG = dict(
    num=3695, title='交换元素后的最大交替和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='并查集 · 同块降序 · 前 even 个取正',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maxAlternatingSum(self, nums, swaps):
        
        n = len(nums)
        fa = [index for index in range(n)]

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y in swaps:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
        
        group = {}
        for index in range(n):
            fa_index = find(fa, index)
            if fa_index not in group:
                group[fa_index] = []
            group[fa_index].append(index)

        res = 0
        for index_list in group.values():
            num_list = [nums[index] for index in index_list]
            even = sum([index % 2 == 0 for index in index_list])
            num_list.sort(reverse=True)
            res += sum(num_list[:even])
            res -= sum(num_list[even:])
        
        return res
''',
    call=f'Solution().maxAlternatingSum({NUMS!r}, {SWAPS!r})',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums（同色 = 同一连通块）', h=170, color=_gcol, cell=90),
        dict(type='array', var='fa', label='fa（并查集）', h=170, cell=90),
        dict(type='text', fn=_txt, h=70, size=26),
        dict(type='array', var='num_list', label='num_list（本块的值，降序）', h=160, cell=90),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('even', 'even', 'orange'), ('res', 'res', 'green')],
    skip=['n = len', 'fa = [index', 'def find', 'return fa[x]', 'group = {}', 'fa_x = find', 'fa_y = find', 'for index in range(n)', 'if fa_index not in group', 'group[fa_index] = []'],
    captions={
        'for x, y in swaps': lambda S, B, ret: (f'可以交换 `{S.x}` 和 `{S.y}` → 下标连一条边' if 'x' not in B or (S.x, S.y) != (B.x, B.y) else '所有边都连完了'),
        'if fa[x] != x': lambda S, B, ret: (f'`find({S.x})`：`fa[{S.x}] = {S.fa[S.x]}` ≠ `{S.x}`，不是代表元 → 往上找' if S.fa[S.x] != S.x
                                            else f'`find({S.x})`：`fa[{S.x}] = {S.x}`，自己就是代表元'),
        'fa[x] = find(fa, fa[x])': '递归去找上一层的代表元，回来后顺手把 `fa[x]` 改成代表元（路径压缩）',
        'fa_index = find(fa, index)': '给下标 `{index}` 找所在块的代表元',
        'if fa_x != fa_y': lambda S, B, ret: (f'代表元 `{S.fa_x}` ≠ `{S.fa_y}`：不同连通块' if S.fa_x != S.fa_y else f'代表元都是 `{S.fa_x}`：早已连通'),
        'fa[fa_x] = fa_y': '把 `{fa_x}` 并到 `{fa_y}` 下面 → `fa = {fa}`',
        'group[fa_index].append(index)': '下标 `{index}` 归入块 `{fa_index}` → `{group}`',
        'for index_list in group.values()': lambda S, B, ret: (f'处理一个连通块，下标 `{S.index_list}`' if 'index_list' not in B or S.index_list != B.index_list else '所有块处理完了'),
        'num_list = [': '取出这些下标上的值：`{num_list}`',
        'even = sum': '块里偶数下标有 `{even}` 个 → 要放 `{even}` 个大数',
        'num_list.sort': '降序排：`{num_list}`',
        'res += sum': '前 `{even}` 个最大的放偶数位，加上 `{sum(num_list[:even])}` → res `{res}`',
        'res -= sum': '其余的放奇数位，减去 `{sum(num_list[even:])}` → res `{res}`',
        'return res': '最大交替和 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='连通块里随便排：大的放偶数位，小的放奇数位',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 的交替和 = 偶数下标之和 − 奇数下标之和，要最大化',
                 '`swaps` 给出可交换的下标对，可交换任意次、任意顺序',
                 '本视频：`nums = [5,2,4,1,3]`，`swaps = [[0,1],[1,2],[3,4]]` → `9`'],
        quote='如果将数组下标视为图中的点，那么一组swaps中的下标对就相当于在图中对应的点间连上了一条边。……图中同一连通块中的点可以随意排列。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标是点，swaps 是边：同一连通块里的数可以随意排列',
              '块内偶数下标有 `even` 个 → 放最大的 `even` 个，其余放奇数位',
              '用并查集连通，再用字典把下标按块分组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`even` 是块内偶数下标的个数，不是值的个数',
                 '`sort(reverse=True)` 后前 `even` 个加，后面的减',
                 '原文代码在 Python 3 下无需改动',
                 '对比灵神：灵神在并查集里维护奇数个数、升序排；这里分组后统计偶数个数、降序排'],
    ),
)
