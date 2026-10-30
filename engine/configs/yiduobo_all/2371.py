GRID = [[3, 2, 4], [1, 5, 2], [4, 1, 3]]


def _cur(S):
    if 'i' not in S or 'j' not in S or 'res' not in S or 'row' not in S:
        return '把每个数按大小排序，小的先定值'
    i, j = S['i'], S['j']
    v = S['res'][i][j]
    if v == 0:
        return f"轮到 `grid[{i}][{j}] = {GRID[i][j]}`：要比第 {i} 行、第 {j} 列已用的最大值都大"
    return f"`grid[{i}][{j}] = {GRID[i][j]}` 被映射为 =={v}=="


def _gcolor(S, i, j, v):
    if 'i' in S and 'j' in S and 'res' in S and (i, j) == (S['i'], S['j']):
        return 'yellow'
    if 'res' in S and 'i' in S and S['res'][i][j] != 0:
        return 'dim'
    return None


def _rcolor(S, i, j, v):
    if 'i' in S and 'j' in S and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return 'green' if v else None


CONFIG = dict(
    num=2371, title='最小化网络中的最大值', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='排序 + 行列当前最大值',
    tags=['灵神题单', '拓扑排序'],
    code='''
class Solution(object):
    def minScore(self, grid):

        m = len(grid)
        n = len(grid[0])
        num_list = []
        for i in range(m):
            for j in range(n):
                num_list.append([grid[i][j], i, j])
        
        row = [0] * m
        col = [0] * n
        res = [[0] * n for _ in range(m)]
        for _, i, j in sorted(num_list):
            res[i][j] = max(row[i], col[j]) + 1
            row[i] = res[i][j]
            col[j] = res[i][j]
        
        return res
''',
    call=f'Solution().minScore({GRID})',
    expect=[[3, 2, 4], [1, 3, 2], [4, 1, 3]],
    result_fn=None,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前处理的格子，灰 = 已定值）', cell=56, h=190,
             color=_gcolor),
        dict(type='grid', var='res', label='res（重新编号后的结果）', cell=56, h=190, color=_rcolor),
        dict(type='array', var='row', label='row[i]：第 i 行目前用到的最大值', cell=60, h=150, pointers={'i': 'blue'}),
        dict(type='array', var='col', label='col[j]：第 j 列目前用到的最大值', cell=60, h=150, pointers={'j': 'pink'}),
        dict(type='text', h=70, size=28, fn=_cur),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    skip=['m = len', 'n = len', 'num_list = []', 'num_list.append', 'for i in range(m)', 'for j in range(n)'],
    captions={
        'row = [0] * m': '`row`、`col` 记录每行每列已分配的最大值，起点 0',
        'res = [[0]': '`res` 先全填 0，按数值从小到大逐个填',
        'for _, i, j in sorted': lambda S, B, r: ('所有数都处理完了' if S.res[S.i][S.j] != 0 else f'取下一个最小的数：`grid[{S.i}][{S.j}] = {S._}`，位置 `({S.i}, {S.j})`'),
        'res[i][j] = max': '同行最大 `{row[i]}`、同列最大 `{col[j]}` → 至少比两者都大：`res[{i}][{j}]` 取 =={res[i][j]}==',
        'row[i] = res': '第 {i} 行的最大值更新为 `{row[i]}`',
        'col[j] = res': '第 {j} 列的最大值更新为 `{col[j]}`',
        'return res': '全部填完，返回 `res`',
    },
    cards=dict(
        one_liner='数值从小到大排序，每个格子取行列已用最大值 +1',
        complexity='时间 `O(mn·log(mn))`，空间 `O(mn)`',
        problem=['给 m×n 矩阵，把每个元素重新赋值成正整数',
                 '要求同一行、同一列内的相对大小不变，且新矩阵的最大值尽量小',
                 '示例：`[[3,2,4],[1,5,2],[4,1,3]]` → `[[3,2,4],[1,3,2],[4,1,3]]`'],
        quote='可以使用两个数组row以及col记录每一行和每一列当前的最大值，这样一来对于位置(i, j)，就可以通过row[i]以及col[j]来确定(i, j)可以填充的最小整数。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小值一定映射为 1，它只会影响自己所在的行和列',
              '于是把所有格子按数值排序，从小到大处理',
              '每个格子只受已处理的同行同列约束 → 取 `max(row[i], col[j]) + 1`'],
        summary=['时间 `O(mn·log(mn))`（排序），空间 `O(mn)`',
                 '排序元组 `[值, i, j]` 相同值时按 i、j 排，不影响结果',
                 '相同数值在不同行列互不约束，所以可以映射成同一个数',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '本质是按拓扑序（值从小到大）给格子分层'],
    ),
)
