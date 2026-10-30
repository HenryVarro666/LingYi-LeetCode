def _x(S):
    if 'total' in S and 's' in S:
        return f"s = ==%d==，total = %d → 需要删的数 x = 2s − total = ==%d==" % (S['s'], S['total'], 2 * S['s'] - S['total'])
    return ''


CONFIG = dict(
    num=3548, title='等和矩阵分割 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右维护左 · 哈希集合', tags=['贪心与思维', '难度分 2245'],
    code='''
class Solution:
    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        total = sum(sum(row) for row in grid)

        # 能否水平分割
        def check(a: List[List[int]]) -> bool:
            m, n = len(a), len(a[0])

            # 删除上半部分中的一个数，能否满足要求
            def f(a: List[List[int]]) -> bool:
                st = {0}  # 0 对应不删除数字
                s = 0
                for i, row in enumerate(a[:-1]):
                    for j, x in enumerate(row):
                        s += x
                        # 第一行，不能删除中间元素
                        if i > 0 or j == 0 or j == n - 1:
                            st.add(x)
                    # 特殊处理只有一列的情况，此时只能删除第一个数或者分割线上那个数
                    if n == 1:
                        if s * 2 == total or s * 2 - total == a[0][0] or s * 2 - total == row[0]:
                            return True
                        continue
                    if s * 2 - total in st:
                        return True
                    # 如果分割到更下面，那么可以删第一行的元素
                    if i == 0:
                        st.update(row)
                return False

            # 删除上半部分中的数 or 删除下半部分中的数
            return f(a) or f(a[::-1])

        # 水平分割 or 垂直分割
        return check(grid) or check(list(zip(*grid)))
''',
    call='Solution().canPartitionGrid([[1,2,4],[2,3,5]])',
    expect=False,
    views=[
        dict(type='grid', var='a', h=200,
             cursors=[('i', 'j', 'yellow', '')],
             color=lambda S, i, j, v: ('blue' if 'i' in S and i < S['i'] else None)),
        dict(type='set', var='st', h=110, label='st：可删的数', fmt=lambda x: str(x)),
        dict(type='text', fn=_x, h=60),
    ],
    watch=['total', 's', ('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'n'],
    captions={
        'total = sum': '先求整张表总和 `total` = =={total}==，后面都拿它和上半部分和 `s` 比',
        'm, n = len': '`a` 是 `{m}` 行 `{n}` 列（垂直分割时会转置成另一张表再来一遍）',
        'st = {0}': '集合 `st` 记录“可以删除的数”，预先放 `0` 代表不删，把两种情况合成一种',
        's = 0': '`s` = 上半部分元素和，一行一行往下加',
        's += x': '`s += {x}` → =={s}==：上半部分又多了一个数',
        'if i > 0 or j == 0': lambda S, B, r: (f'`i={S.i}, j={S.j}`：' + ('第一行的中间元素：删了会把这一行断成两截 → ==不能删==' if not (S.i > 0 or S.j == 0 or S.j == S.n - 1) else ('不在第一行：下面的行把它连住了 → ==能删==' if S.i > 0 else '第一行的两端：删了仍连通 → ==能删=='))),
        'st.add(x)': '`{x}` 放进 `st`（它是一个可以删的数）',
        'if n == 1': lambda S, B, r: ('只有一列：只能删第一个数或分割线上的数，走特殊判断' if S.n == 1 else f'`n = {S.n}`，不是单列 → 走通用判断'),
        'if s * 2 - total in st': lambda S, B, r: f'要删的数 `x = 2×{S.s} − {S.total} = {S.s*2-S.total}`，在 `st` 里吗？→ ' + ('==在，返回 True==' if S.s*2-S.total in S.st else '不在，这条分割线不行'),
        'if i == 0': lambda S, B, r: ('分割线在第一行下面：再往下移时，第一行有第二行连着，中间元素也能删了' if S.i == 0 else '`i > 0`，第一行早已补进集合'),
        'st.update(row)': '把第一行所有数补进 `st`',
        'return f(a) or f(a[::-1])': '先试“删上半部分”`f(a)`；不行再把表上下翻转，等价于“删下半部分”',
        'return False': '这一轮没有可行的分割 → `False`',
        'return check(grid)': '先查水平分割 `check(grid)`；不行再把表转置（`zip(*grid)`）查垂直分割',
    },
    cards=dict(
        one_liner='设上半部分和为 s，删 x 后相等 ⇔ 2s − total = x',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['在 `m×n` 的正整数矩阵上切一刀（横或竖），两部分非空',
                 '两部分和相等，或从其中一部分删掉 ==一个格子== 后相等，且删后该部分仍连通',
                 '示例：`[[1,2,4],[2,3,5]]` → `false`（删 `3` 会让下半部分断开）'],
        quote='删第一部分中的元素 x：s − x = total − s，即 ==2s − total = x==。每一行遍历结束后，判断 x = 2s − total 是否在哈希集合中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一边累加上半部分和 `s`，一边把遍历过的数放进集合，这就是“枚举右、维护左”',
              '预先放入 `0`，“不删”和“删”合并成一种判断',
              '连通性分类：单行时只能删两端，单列时只能删首个或分割线上的数，其余随便删',
              '删下半部分 = 把表上下翻转；垂直分割 = 把表转置'],
        summary=['时间 `O(mn)`：每个格子进集合一次；空间 `O(mn)`',
                 '易错：第一行的中间元素，要等分割线下移到第二行后才能删',
                 '易错：`n == 1` 时只能删第一个数或分割线上的数，要单独判断',
                 '上下翻转、转置复用同一段代码，不用写四遍'],
    ),
)
