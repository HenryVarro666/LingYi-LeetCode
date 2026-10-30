G = [[4, 2, 4, 1], [2, 4, 4, 2], [3, 2, 2, 4]]


def _mat(S):
    a = S.get('a')
    if a is None:
        a = S.get('grid')
    return [list(r) for r in a] if a is not None else None


def _in(S, i, j, v):
    a, s = S.get('a'), S.get('s')
    if a is None or not s:
        return None
    acc = 0
    for k, r in enumerate(a):
        acc += sum(r)
        if i == k:
            return 'green' if acc <= s else None
    return None


def _txt(S):
    if 'a' not in S:
        return f"整个矩阵元素和 `total = {S['total']}`" if 'total' in S else ''
    kind = '水平分割（按行）' if S['a'] is S['grid'] else '垂直分割（转置后按行）'
    s, t = S['s'], S['total']
    return f"{kind}：`s = {s}`，`2s = {2 * s}`，`total = {t}` → " + ('==相等==' if 2 * s == t else ('2s 还小' if 2 * s < t else '2s 已超过'))


CONFIG = dict(
    num=3546, title='等和矩阵分割 I', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='前缀和 · 转置复用',
    code='''
class Solution:
    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        total = sum(sum(row) for row in grid)

        # 能否水平分割
        def check(a: List[List[int]]) -> bool:
            s = 0
            for row in a[:-1]:  # 最后一行无需遍历
                s += sum(row)
                if s * 2 == total:
                    return True
            return False

        # 水平分割 or 垂直分割
        return check(grid) or check(list(zip(*grid)))
''',
    call=f'Solution().canPartitionGrid({G})',
    expect=True,
    views=[
        dict(type='grid', var=_mat, label='当前被检查的矩阵 a（绿 = 已划进第一部分的行）', cell=84, h=360, color=_in),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=['total', 's', 'row'],
    captions={
        'total = sum': '先求全矩阵元素和 `total = {total}`；要分成相等两半，每半都得是 `total / 2`',
        'def check': '`check(a)`：只考虑一条水平线，逐行累加第一部分的和',
        's = 0': '第一部分的元素和 `s` 从 0 开始',
        'for row in a[:-1]': lambda S, B, r: (f'这一行 `{list(S.row)}` 并入第一部分' if 'row' in S and not ('row' in B and S.row == B.row) else '这个方向的分割线都试过了'),
        's += sum(row)': '第一部分加上这一行：`s = {s}`',
        'if s * 2 == total': lambda S, B, r: (f'`2 × {S.s} = {2 * S.s}` ' + ('==等于== ' if 2 * S.s == S.total else '不等于 ') + f'`total = {S.total}`'
                                             + ('，这条线分出两个等和部分' if 2 * S.s == S.total else '，线再往下移')),
        'return True': '找到了：这条分割线两边和相等 → 返回 `True`',
        'return False': lambda S, B, r: ('水平方向没有合适的分割线 → 接着转置，检查垂直方向' if S.a is S.grid else '垂直方向也没有 → 返回 `False`'),
        'return check(grid) or': lambda S, B, r: ('先试水平分割：`check(grid)`' if r is None else '水平不行，转置 `zip(*grid)` 后垂直分割成功 → 返回 `True`'),
    },
    cards=dict(
        one_liner='两半相等就是 `2s = total`，竖着切就转置再用同一段代码',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 正整数矩阵，能否用一条水平或垂直线分成两个非空部分',
                 '两部分元素和要相等',
                 '示例：`[[1,4],[2,3]]` → 水平切开两边都是 5，`true`；本视频用 3×4 矩阵，需要竖着切'],
        quote='设第一部分的元素和为 s，那么第二部分的元素和为 total−s，题目要求 s = total−s，即 2s=total。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先算 `total`，水平分割时一行一行累加第一部分的和 `s`',
              '每加完一行就判断 `s * 2 == total`',
              '垂直分割：把矩阵旋转（转置）90 度，复用同一个 `check`'],
        summary=['时间 `O(mn)`，转置 `zip(*grid)` 需要 `O(mn)` 额外空间',
                 '易错：只遍历 `a[:-1]`，第二部分不能为空',
                 '元素都是正数，`s` 单调增，所以最多命中一次',
                 '`zip(*grid)` 得到的是元组列表，`sum(row)` 照样能用'],
    ),
)
