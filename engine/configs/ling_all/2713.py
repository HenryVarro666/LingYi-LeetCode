MAT = [[3, 1, 6], [3, 5, 7]]


def _grid_color(S, i, j, v):
    pos = S.get('pos')
    if pos is None or '_' not in S:
        return None
    if (i, j) in pos:
        return 'yellow'
    if v < S['_']:
        return 'green'
    return None


def _rm_color(S, i, v):
    pos = S.get('pos') or []
    return 'yellow' if any(p[0] == i for p in pos) else None


def _cm_color(S, j, v):
    pos = S.get('pos') or []
    return 'yellow' if any(p[1] == j for p in pos) else None


def _text(S):
    if 'pos' not in S or '_' not in S:
        return '`f[i][j]` = 到达 `(i,j)` 最多访问几格；`row_max / col_max` 记录每行、每列已算出的最大 f'
    fs = S.get('fs')
    head = f"当前处理值 ==x {S['_']}== 的格子（黄色）；绿色 = 更小的、已经算好的"
    if fs is not None:
        head += f"；`fs = {fs}`"
    return head


CONFIG = dict(
    num=2713, title='矩阵中严格递增的单元格数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按值从小到大 + 行最大/列最大',
    tags=['灵神题单', '动态规划', '难度分 2387'],
    code='''
class Solution:
    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        g = defaultdict(list)
        for i, row in enumerate(mat):
            for j, x in enumerate(row):
                g[x].append((i, j))  # 相同元素放在同一组，统计位置

        row_max = [0] * len(mat)
        col_max = [0] * len(mat[0])
        for _, pos in sorted(g.items(), key=lambda p: p[0]):
            # 先把所有 f 值都算出来，再更新 row_max 和 col_max
            fs = [max(row_max[i], col_max[j]) + 1 for i, j in pos]
            for (i, j), f in zip(pos, fs):
                row_max[i] = max(row_max[i], f)  # 更新第 i 行的最大 f 值
                col_max[j] = max(col_max[j], f)  # 更新第 j 列的最大 f 值
        return max(row_max)
''',
    call=f'Solution().maxIncreasingCells({MAT})',
    expect=4,
    skip=['g = defaultdict', 'for i, row in enumerate', 'for j, x in enumerate', 'g[x].append'],
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='grid', var='mat', color=_grid_color, h=230, cell=96),
        dict(type='array', var='row_max', label='row_max（每行已算出的最大 f，黄 = 本组涉及的行）', color=_rm_color, h=150),
        dict(type='array', var='col_max', label='col_max（每列已算出的最大 f，黄 = 本组涉及的列）', color=_cm_color, h=150),
    ],
    watch=[('x', "_", 'blue'), ('pos', 'pos', 'yellow'), ('fs', 'fs', 'green')],
    captions={
        'row_max = [0]': '`row_max[i]`：第 `i` 行已算出的最大 f，没算过就是 0',
        'col_max = [0]': '`col_max[j]`：第 `j` 列已算出的最大 f',
        'for _, pos in sorted': lambda S, B, r: (f"按值从小到大：处理值 `{S['_']}` 的所有格子 `{S['pos']}`" if B.get('pos') != S.get('pos') else '所有分组都处理完了'),
        'fs = [': '这一组每个格子：`f = max(行最大, 列最大) + 1` → `fs = {fs}`。==先全算出来再更新==，同值格子才不会互相影响',
        'for (i, j), f in zip': lambda S, B, r: ('这一组的格子都更新完了' if (B.get('f') == S['f'] and (B.get('i'), B.get('j')) == (S['i'], S['j'])) else f"取出格子 `({S['i']}, {S['j']})` 和它的 `f = {S['f']}`"),
        'row_max[i] = max': '第 `{i}` 行最大 f 更新为 `{row_max[i]}`',
        'col_max[j] = max': '第 `{j}` 列最大 f 更新为 `{col_max[j]}`',
        'return max(row_max)': '答案是 `row_max` 的最大值 `{max(row_max)}`',
    },
    cards=dict(
        one_liner='按值从小到大算，只需知道每行每列当前最大的 f',
        complexity='时间 `O(mn log mn)`，空间 `O(mn)`',
        problem=['可从一格走到同行或同列中值更大的格子，任选起点',
                 '求最多能访问多少个格子',
                 '本视频：`[[3,1,6],[3,5,7]]` → `4`'],
        quote='我们不需要知道具体从哪个单元格转移过来，只需要知道所有转移来源的最大值是多少。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按值从小到大算：同行同列里比它小的 `f` 都已算好，更大的还是 0',
              '所以 `f[i][j] = max(row_max[i], col_max[j]) + 1`，`f` 数组可省',
              '相同的值分成一组：先算完整组的 `f`，再统一更新行列最大值'],
        summary=['时间 `O(mn log mn)`（排序），空间 `O(mn)`',
                 '易错：同值格子立刻更新 `row_max`，会让它们互相接龙，答案偏大',
                 '答案取 `row_max` 的最大值，`col_max` 的最大值与之相等',
                 '字典按值分组再 `sorted`，也可以直接对所有格子排序后按值分批'],
    ),
)
