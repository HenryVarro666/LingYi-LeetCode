MAT = [[3, 1, 6], [3, 5, 7]]


def _grp(S):
    nl, l, r = S.get('num_list'), S.get('left'), S.get('right')
    if nl is None or l is None or l >= len(nl):
        return None
    if r is None or r <= l:
        r = l + 1
    return [(x, y) for _, x, y in nl[l:r]]


def _cur(S):
    nl, l = S.get('num_list'), S.get('left')
    if nl is None or l is None or l >= len(nl) or S.get('right') is None:
        return None
    return -nl[l][0]


def _grid_color(S, i, j, v):
    g, c = _grp(S), _cur(S)
    if g is None or c is None:
        return None
    if (i, j) in g:
        return 'yellow'
    if v > c:
        return 'green'
    return None


def _rm_color(S, i, v):
    g = _grp(S) or []
    return 'yellow' if S.get('right') is not None and any(p[0] == i for p in g) else None


def _cm_color(S, j, v):
    g = _grp(S) or []
    return 'yellow' if S.get('right') is not None and any(p[1] == j for p in g) else None


def _text(S):
    c = _cur(S)
    if c is None:
        return '`row[i]` / `col[j]`：第 `i` 行、第 `j` 列已算出的最大 f；==从最大的值开始往小算=='
    return f"当前这一批：值 ==x {c}== 的格子（黄色）；绿色 = 更大的、已经算好的；`step = {S.get('step')}`"


CONFIG = dict(
    num=2713, title='矩阵中严格递增的单元格数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='值从大到小 + row/col 最大值（同值分批）',
    tags=['灵神题单', '动态规划', '难度分 2387'],
    code='''
class Solution(object):
    def maxIncreasingCells(self, mat):

        m = len(mat)
        n = len(mat[0])

        row = [0] * m
        col = [0] * n

        num_list = []
        for i in range(m):
            for j in range(n):
                num_list.append([-mat[i][j], i, j])
        
        num_list.sort()
        left = 0
        res = 0
        while left < len(num_list):
            right = left + 1
            while right < len(num_list) and num_list[left][0] == num_list[right][0]:
                right += 1

            step = []
            for v, x, y in num_list[left: right]:
                step.append(max(row[x], col[y]) + 1)
                res = max(res, step[-1])
            
            for index in range(len(step)):
                v, x, y = num_list[left + index]
                row[x] = max(row[x], step[index])
                col[y] = max(col[y], step[index])
            
            left = right
        
        return res
''',
    call=f'Solution().maxIncreasingCells({MAT})',
    expect=4,
    skip=['m = len', 'n = len', 'for i in range(m)', 'for j in range(n)', 'num_list.append', 'num_list = []',
          'v, x, y = num_list[left + index]', 'for index in range', 'for v, x, y'],
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='grid', var='mat', color=_grid_color, h=230, cell=96),
        dict(type='array', var='row', label='row（每行已算出的最大 f，黄 = 本批涉及的行）', color=_rm_color, h=150),
        dict(type='array', var='col', label='col（每列已算出的最大 f，黄 = 本批涉及的列）', color=_cm_color, h=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('step', 'step', 'yellow'), ('res', 'res', 'green')],
    captions={
        'row = [0]': '`row[i]`：第 `i` 行目前算出的最大 f',
        'col = [0]': '`col[j]`：第 `j` 列目前算出的最大 f',
        'num_list.sort()': '存成 `[-值, i, j]` 再排序 → ==值从大到小==。算某格时，比它大的格子 f 都已算好',
        'left = 0': '`left` 是当前批次的起点',
        'res = 0': '`res` 记录最大的 f',
        'while left < len': lambda S, B, r: (f"`left = {S.left}`，还有格子没处理，继续" if S.left < len(S.num_list) else f"`left = {S.left}` 已到末尾，所有格子都算完"),
        'right = left + 1': '先假设这一批只有 `num_list[left]` 一个',
        'while right < len': lambda S, B, r: ((f"`num_list[{S.right}]` 的值和 `num_list[{S.left}]` 相同 → 同一批" if S.right < len(S.num_list) and S.num_list[S.left][0] == S.num_list[S.right][0] else f"`right = {S.right}`：到头或值不同了，这一批是 `[{S.left}, {S.right})`")),
        'right += 1': '同值格子并入这一批，`right` → {right}',
        'step = []': '`step` 暂存这批每个格子的 f：==先算完，再统一更新 row/col==',
        'step.append': '`f = max(row[{x}], col[{y}]) + 1` = =={step[-1]}==（格子 `({x}, {y})`）',
        'res = max(res, step[-1])': '`res` 更新为 {res}',
        'row[x] = max': '第 `{x}` 行的最大值更新为 `{row[x]}`',
        'col[y] = max': '第 `{y}` 列的最大值更新为 `{col[y]}`',
        'left = right': '这一批处理完，`left` 跳到 {right}',
        'return res': '最多访问 `{res}` 个格子',
    },
    cards=dict(
        one_liner='先把格子按值排序，行列各记一个最大值，同值的分批算',
        complexity='时间 `O(mn log mn)`，空间 `O(mn)`',
        problem=['可从一格走到同行或同列中值更大的格子，任选起点',
                 '求最多能访问多少个格子',
                 '本视频：`[[3,1,6],[3,5,7]]` → `4`'],
        quote='将所有单元格从大到小进行排序，然后逐个计算其对应的f值，此时计算f[i][j]时，所有已经计算好f值的单元格的数值必然都大于(i, j)的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP：`f[i][j]` 是从 `(i,j)` 出发最多走几格，要枚举整行整列，`O((mn)^2)`',
              '值从大到小算：同行同列已算好的格子都比它大，取 `max(row[i], col[j]) + 1`',
              '值相同的格子在一个批次里分别算，再统一更新 `row` 和 `col`'],
        summary=['时间 `O(mn log mn)`，空间 `O(mn)`',
                 '易错：同值格子必须同批计算，否则同行同列的相等值会互相接龙',
                 '`num_list` 存 `-值` 才能用默认排序得到从大到小',
                 '对比灵神：灵神按值从小到大算「到达」，yiduobo 从大到小算「出发」，答案相同'],
    ),
)
