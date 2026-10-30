G = [[4, 2, 1, 5], [3, 3, 1, 2], [6, 1, 2, 2], [2, 5, 3, 1]]


def _col(S):
    g = S.get('grid')
    if not g:
        return ''
    if S['_line'] < 5:
        return '先把每一行升序排好：每行最大的数会被排到最右边'
    cols = [max(c) for c in zip(*g)]
    return '每列最大值：' + ' + '.join(f'`{c}`' for c in cols) + f' = =={sum(cols)}=='


def _color(S, i, j, v):
    g = S['grid']
    if S['_line'] >= 5 and v == max(r[j] for r in g):
        return 'green'
    return None


CONFIG = dict(
    num=2500, title='删除每行中的最大值', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='每行排序 · 求每列最大值',
    tags=[],
    code='''
class Solution:
    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        for row in grid:
            row.sort()
        return sum(map(max, zip(*grid)))  # 累加每列的最大值
''',
    call=f'Solution().deleteGreatestValue({G!r})',
    expect=13,
    views=[
        dict(type='grid', var='grid', label='grid（每行排序后，绿色 = 该列最大值）', color=_color, cell=100, h=400),
        dict(type='text', fn=_col, size=30, h=120),
    ],
    watch=[('row', 'row', 'blue')],
    captions={
        'for row in grid': lambda S, B, r: ('所有行都排好了，循环结束' if B.get('row') == S.row else f'取出下一行 `{S.row}`'),
        'row.sort()': '`row` 升序排序 → `{row}`：==最大值排到最右==，第 k 轮删的就是第 k 列',
        'return sum': '第 k 轮每行删掉的最大值，就是排序后倒数第 k 个数 → 逐列取最大再求和，答案 =={ret}==',
    },
    cards=dict(
        one_liner='每行排好序，每列取最大再求和',
        complexity='时间 `O(mn log n)`，空间 `O(1)`',
        problem=['矩阵每轮从每行删掉最大值，把这些被删值里的最大者加进答案',
                 '重复直到矩阵为空，求累计答案',
                 '示例：`[[1,2,4],[3,3,1]]` → `8`'],
        quote='问题等价于把每行排序之后，求每列的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每行升序排好后，第 1 轮删的是最后一列，第 2 轮删倒数第 2 列……',
              '每一轮要加的就是 ==该列的最大值==',
              '`zip(*grid)` 把矩阵转置，`map(max, ...)` 取每列最大，`sum` 累加'],
        summary=['时间 `O(mn log n)`：每行排序一次',
                 '空间 `O(1)`：直接原地排序（会改动输入）',
                 '易错点：每行各自删最大，但只有每轮的最大者进答案，不是全部相加',
                 '`zip(*grid)` 就是转置，Python 里取列的惯用写法'],
    ),
)
