G = [[6, 2, 1, 3], [4, 2, 1, 5], [9, 2, 8, 7], [4, 1, 2, 9]]


def _hg(i, j):
    return {(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)}


def _sums(g):
    return {(i, j): sum(g[a][b] for a, b in _hg(i, j)) for i in range(1, len(g) - 1) for j in range(1, len(g[0]) - 1)}


def _best(g):
    d = _sums(g)
    return max(d, key=lambda k: d[k])


def _color(S, i, j, v):
    g = S.get('grid')
    if g is None:
        return None
    bc = _best(g)
    if (i, j) == bc:
        return 'yellow'
    return 'blue' if (i, j) in _hg(*bc) else None


def _list(S):
    d = _sums(S['grid'])
    return '各中心七格之和：' + '  '.join(f'`({i},{j})`={v}' for (i, j), v in d.items())


CONFIG = dict(
    num=2428, title='沙漏的最大总和', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='枚举沙漏中心',
    tags=[],
    code='''
class Solution:
    def maxSum(self, grid: List[List[int]]) -> int:
        return max(grid[i - 1][j - 1] + grid[i - 1][j] + grid[i - 1][j + 1] + grid[i][j] +
                   grid[i + 1][j - 1] + grid[i + 1][j] + grid[i + 1][j + 1]
                   for i in range(1, len(grid) - 1) for j in range(1, len(grid[i]) - 1))
''',
    call=f'Solution().maxSum({G})',
    expect=30,
    views=[
        dict(type='grid', var='grid', color=_color, h=420),
        dict(type='text', size=28, fn=lambda S: _list(S) if 'grid' in S else ''),
        dict(type='text', size=30, fn=lambda S: (lambda bc: f"最大的沙漏：中心 `{bc}`（黄 = 中心，蓝 = 其余六格）= =={_sums(S['grid'])[bc]}==")(_best(S['grid'])) if 'grid' in S else ''),
    ],
    watch=[],
    captions={
        'return max': lambda S, B, r: ('生成器按行列枚举每个沙漏中心 `(i, j)`（`i`、`j` 都从 1 到 len-2，保证不出界），每个中心把七格相加，交给 `max`' if r is None
                                       else f'`max` 在所有中心的和里取最大 → =={r}=='),
        'for i in range': '枚举完毕：4 个中心的和已经比较过，最大的就是答案',
    },
    cards=dict(
        one_liner='沙漏不能旋转，枚举中心，七格相加取最大',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['在 `m×n` 矩阵里找「工字形」沙漏：上排 3 格、中间 1 格、下排 3 格', '返回所有沙漏中元素和的最大值',
                 '示例：`[[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]` → `30`'],
        quote='按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['沙漏固定 3×3，不能旋转，由中心 `(i,j)` 唯一确定',
              '中心必须在 `1 ≤ i ≤ m-2`、`1 ≤ j ≤ n-2`，才不会出界',
              '一个生成器表达式把七格直接写出来，交给 `max`'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '枚举范围是 `range(1, len(grid) - 1)`，沙漏要整个落在矩阵内',
                 '中间行只取中心一格，不是整行三格',
                 '本视频 4×4 示例共 4 个中心，最大的是 (1,1)，和为 30'],
    ),
)
