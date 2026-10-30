def _bits(x, n):
    return format(x, f'0{n}b')[::-1]   # 低位在左：第 j 位 = 第 j 列


def _cols(S):
    if 'subset' not in S:
        return set()
    return {j for j in range(len(S['mat'][0])) if S['subset'] >> j & 1}


def _txt(S):
    if 'subset' not in S or 'u' not in S:
        return '每一行压成二进制 `mask`，第 j 位 = 第 j 列是不是 1'
    n = len(S['mat'][0])
    if S['subset'] >= S['u']:
        return f"`subset = {S['subset']}` ≥ `u = {S['u']}`：所有大小为 {S['numSelect']} 的列集合都枚举完了"
    cols = sorted(_cols(S))
    return f"当前选的列 `subset = {_bits(S['subset'], n)}`（低位在左）→ 列 {cols}"


CONFIG = dict(
    num=2397, title='被列覆盖的最多行数', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique="Gosper's Hack 枚举固定大小子集",
    tags=['灵神题单·链表树与回溯', '难度分 1719'],
    code='''
class Solution:
    def maximumRows(self, mat: List[List[int]], numSelect: int) -> int:
        mask = [sum(x << j for j, x in enumerate(row)) for i, row in enumerate(mat)]
        ans = 0
        u = 1 << len(mat[0])
        subset = (1 << numSelect) - 1
        while subset < u:
            covered_rows = sum(row & subset == row for row in mask)
            ans = max(ans, covered_rows)
            lb = subset & -subset
            x = subset + lb
            subset = ((subset ^ x) // lb >> 2) | x
        return ans
''',
    call='Solution().maximumRows([[0,0,0],[1,0,1],[0,1,1],[0,0,1]], 2)',
    expect=3,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 选中列的 1，红 = 未选中列的 1）', h=300, cell=80,
             color=lambda S, i, j, v: ('yellow' if v == 1 and j in _cols(S) else 'red' if v == 1 else None)
             if 'subset' in S else None),
        dict(type='array', var='mask', label='mask（每行 1 的列集合，十进制）', h=150, cell=90),
        dict(type='text', h=90, size=30, fn=_txt),
    ],
    watch=['subset', 'covered_rows', ('ans', 'ans', 'green'), 'u'],
    captions={
        'mask = [': '每行压成整数：第 j 位为 1 表示第 j 列有 1 → `mask = {mask}`',
        'u = 1 <<': '一共 `{len(mat[0])}` 列，集合范围是 `[0, u)`，`u = {u}`',
        'subset = (1 << numSelect) - 1': '最小的大小为 `{numSelect}` 的集合：低 `{numSelect}` 位全 1，`subset = {subset}`',
        'while subset < u': lambda S, B, r: (f"`subset = {S.subset} < u = {S.u}`，还有集合没枚举" if S.subset < S.u
                                             else f"`subset = {S.subset} ≥ u = {S.u}`：枚举完毕"),
        'covered_rows = sum': '`row & subset == row` 说明这行的 1 都被选中 → 覆盖 =={covered_rows}== 行',
        'ans = max': '`ans = max({B.ans}, {covered_rows}) = {ans}`',
        'lb = subset': '`lb` = lowbit，`subset` 最低位的 1：`{lb}`',
        'x = subset + lb': '加上 lowbit，最低的一段连续 1 进位：`x = {x}`',
        'subset = ((': 'Gosper：把进位丢掉的 1 挪回最低位 → 下一个同样大小的集合 `subset = {subset}`',
        'return ans': '最多能覆盖 `{ans}` 行',
    },
    cards=dict(
        one_liner='只枚举大小恰好为 numSelect 的列集合，O(1) 跳到下一个',
        complexity='时间 `O(m·C(n, numSelect))`，空间 `O(m)`',
        problem=['矩阵 `mat` 只含 0/1，必须选 `numSelect` 个不同的列',
                 '一行的所有 1 都落在选中的列里，这行就被覆盖（全 0 行自动覆盖）',
                 '示例：`[[0,0,0],[1,0,1],[0,1,1],[0,0,1]]`，选 2 列 → `3`'],
        quote='通过使用 Gosper\'s Hack，我们可以在 O(1) 的时间内找到下一个大小为 numSelect 的集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把每行压成一个二进制数 `mask`，列集合用 `subset` 表示',
              '行被覆盖 ⟺ `mask` 是 `subset` 的子集 ⟺ `row & subset == row`',
              '方法一枚举全部 `2^n` 个数再过滤 `bit_count`；方法二用 Gosper 直接跳'],
        summary=['时间 `O(m·C(n, numSelect))`，空间 `O(m)`',
                 '`mask` 里第 j 位对应第 j 列，别把行列弄反',
                 '`lb = subset & -subset` 是 lowbit；Gosper 的除法必须是整除 `//`',
                 '方法一：枚举 `range(1 << n)` 再用 `bit_count() == numSelect` 过滤，多了无效枚举'],
    ),
)
