G = [[6, 2, 1, 3], [4, 2, 1, 5], [9, 2, 8, 7], [4, 1, 2, 9]]
DX = [0, -1, -1, -1, 1, 1, 1]
DY = [0, -1, 0, 1, -1, 0, 1]


def _color(S, i, j, v):
    c = S.get('_inner', {})
    if 'i' in c and 'j' in c:
        ci, cj = c['i'], c['j']
        if (i, j) == (ci, cj):
            return 'yellow'
        k = c.get('index')
        done = set()
        if k is not None and 'now' in c:
            done = {(ci + DX[t], cj + DY[t]) for t in range(k + (1 if S.get('_line', 0) >= 0 else 0))}
        if (i, j) in {(ci + DX[t], cj + DY[t]) for t in range(7)}:
            return 'blue'
    return None


CONFIG = dict(
    num=2428, title='沙漏的最大总和', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举连接处 + 方向数组',
    tags=[],
    code='''
class Solution(object):
    def maxSum(self, grid):

        res = 0
        m = len(grid)
        n = len(grid[0])

        dx = [0, -1, -1, -1, 1, 1, 1]
        dy = [0, -1, 0, 1, -1, 0, 1]

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                now = 0
                for index in range(7):
                    now += grid[i + dx[index]][j + dy[index]]
                res = max(res, now)

        return res
''',
    call=f'Solution().maxSum({G})',
    expect=30,
    skip=['m = len', 'n = len', 'now = 0', 'dx = [', 'dy = [', 'for index in range'],
    views=[
        dict(type='grid', var='grid', color=_color, h=420),
        dict(type='text', size=28, fn=lambda S: (lambda c: f"连接处 `({c['i']},{c['j']})`，已累加 `{c.get('now', 0)}`，当前 `res` = =={c.get('res', S.get('res', 0))}==" if 'i' in c and 'j' in c else '')(S.get('_inner', {}))),
    ],
    watch=['i', 'j', 'index', 'now', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录目前见过的最大沙漏和（元素都 ≥ 0，初值 0 够用）',
        'for i in range': '沙漏是 3×3，中心 `i` 只能取 `1 ~ m-2`，边上的行当不了连接处',
        'for j in range': '同理列 `j` 取 `1 ~ n-2`',
        'now += grid': '偏移 `({dx[index]},{dy[index]})` → 加上 `grid[{i + dx[index]}][{j + dy[index]}] = {grid[i + dx[index]][j + dy[index]]}`，`now` = =={now}==',
        'res = max': '七格加完：`res = max({B.res}, {now})` = =={res}==',
        'return res': '所有连接处都试过，最大沙漏和 = =={res}==',
    },
    cards=dict(
        one_liner='沙漏是固定的工字形，枚举连接处，七个偏移相加',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['矩阵中的沙漏：上 3 格、中 1 格、下 3 格，不能旋转', '返回所有沙漏元素和的最大值',
                 '示例：`[[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]` → `30`'],
        quote='沙漏严格定义为工字形块，且这个块的大小也不会放大，那么就可以直接枚举工字形的连接处。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举连接处 `(x, y)`：左上、上、右上、左下、下、右下，再加自己',
              '把七个偏移写进 `dx`、`dy` 两个数组，用内层循环累加',
              '每个中心算完一个和，取最大'],
        summary=['时间 `O(mn)`（七格是常数），空间 `O(1)`',
                 '`i`、`j` 从 1 到 `m-2`、`n-2`，保证沙漏不出界',
                 '`dx[0]=dy[0]=0` 就是中心格自己',
                 '对比灵神：灵神把七格直接写成一个表达式，这里用方向数组循环'],
    ),
)
