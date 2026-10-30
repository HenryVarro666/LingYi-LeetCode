def _cell(S, i, j, v):
    if v == 'O':
        return 'green'
    if v == 'W':
        return 'pink'
    if v == 'E':
        return 'blue'
    return None


_ARR = ['右 →', '下 ↓', '左 ←', '上 ↑']


def _info(S):
    inner = S['_inner']
    if 'd' not in inner:
        return '弹珠盘：`O` 洞（绿）、`W` 逆时针转向器（粉）、`E` 顺时针转向器（蓝）、`.` 空地'
    return f"当前方向 ==`{_ARR[inner['d']]}`==，剩余步数 `left = {inner['left']}`，位置 `({inner['x']},{inner['y']})`"


CONFIG = dict(
    num='LCP 63', title='弹珠游戏', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='枚举入口 · 直接模拟（路径唯一，不需要 DFS）',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))  # 右下左上（顺时针）

class Solution:
    def ballGame(self, num: int, plate: List[str]) -> List[List[int]]:
        m, n = len(plate), len(plate[0])

        def check(x: int, y: int, d: int) -> bool:
            left = num
            while plate[x][y] != 'O':
                if left == 0: return False  # 无剩余步数
                if plate[x][y] == 'W':   d = (d + 3) % 4  # 逆时针
                elif plate[x][y] == 'E': d = (d + 1) % 4  # 顺时针
                x += DIRS[d][0]
                y += DIRS[d][1]
                if not (0 <= x < m and 0 <= y < n): return False  # 出界
                left -= 1
            return True

        ans = []
        for j in range(1, n - 1):
            if plate[0][j] == '.' and check(0, j, 1): ans.append([0, j])  # 上边
            if plate[-1][j] == '.' and check(m - 1, j, 3): ans.append([m - 1, j])  # 下边
        for i in range(1, m - 1):
            if plate[i][0] == '.' and check(i, 0, 0): ans.append([i, 0])  # 左边
            if plate[i][-1] == '.' and check(i, n - 1, 2): ans.append([i, n - 1])  # 右边
        return ans
''',
    call='Solution().ballGame(4, ["..E.", ".EOW", "..W."])',
    expect=[[2, 1]],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='grid', var='plate', label='plate（黄 = 弹珠位置）', cell=110, h=380,
             color=_cell, cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'yellow')]),
        dict(type='stack', var='ans', label='ans（能入洞的打入位置）', h=110),
    ],
    watch=[('left', lambda S: S['_inner'].get('left'), 'cyan'), ('d', lambda S: S['_inner'].get('d'), 'yellow')],
    skip=['m, n = len', 'ans = []'],
    max_steps=70,
    captions={
        'left = num': '这颗弹珠最多走 `num = {num}` 步，`left` 记剩余步数',
        'while plate[x][y]': lambda S, B, r: (f'`plate[{S.x}][{S.y}] = {S.plate[S.x][S.y]!r}`'
                                              + (' 是洞 → ==入洞=='
                                                 if S.plate[S.x][S.y] == 'O' else ' 不是洞，继续滚')),
        'if left == 0': lambda S, B, r: ('`left = 0`：步数用完还没入洞 → ==返回 False==' if S.left == 0
                                         else f'`left = {S.left}`，还有步数'),
        "plate[x][y] == 'W'": lambda S, B, r: (f'`plate[{S.x}][{S.y}] = W`：逆时针转 90 度，`d = (d + 3) % 4` → =={_ARR[S.d]}=='
                                               if S.plate[S.x][S.y] == 'W' else f'不是 `W`，看下一个'),
        "plate[x][y] == 'E'": lambda S, B, r: (f'`plate[{S.x}][{S.y}] = E`：顺时针转 90 度，`d = (d + 1) % 4` → =={_ARR[S.d]}=='
                                               if S.plate[S.x][S.y] == 'E' else '是空地 `.`，方向不变'),
        'x += DIRS': lambda S, B, r: f'沿方向 =={_ARR[S.d]}== 前进：行 `x = {B.x} → {S.x}`',
        'y += DIRS': lambda S, B, r: f'列 `y = {B.y} → {S.y}`，弹珠来到 `({S.x},{S.y})`',
        'if not (0 <= x < m': lambda S, B, r: (f'`({S.x},{S.y})` 出界 → 弹珠飞出盘面，==返回 False==' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
                                               else f'`({S.x},{S.y})` 还在盘内'),
        'left -= 1': '走了一步，`left` → {left}',
        'return True': '`plate[x][y] == O`：弹珠落入洞中 → ==返回 True==',
        "plate[0][j] == '.'": lambda S, B, r: (f'上边入口 `(0,{S.j})`：是空地才能打入，方向朝下 `d = 1`' if S.plate[0][S.j] == '.'
                                               else f'上边入口 `(0,{S.j})` 是 `{S.plate[0][S.j]}`，不是空地，不能打入'),
        "plate[-1][j] == '.'": lambda S, B, r: (f'下边入口 `({S.m - 1},{S.j})`：是空地才能打入，方向朝上 `d = 3`' if S.plate[-1][S.j] == '.'
                                                else f'下边入口 `({S.m - 1},{S.j})` 是 `{S.plate[-1][S.j]}`，不是空地，不能打入'),
        "plate[i][0] == '.'": lambda S, B, r: (f'左边入口 `({S.i},0)`：是空地才能打入，方向朝右 `d = 0`' if S.plate[S.i][0] == '.'
                                               else f'左边入口 `({S.i},0)` 是 `{S.plate[S.i][0]}`，不是空地，不能打入'),
        "plate[i][-1] == '.'": lambda S, B, r: (f'右边入口 `({S.i},{S.n - 1})`：是空地才能打入，方向朝左 `d = 2`' if S.plate[S.i][-1] == '.'
                                                else f'右边入口 `({S.i},{S.n - 1})` 是 `{S.plate[S.i][-1]}`，不是空地，不能打入'),
        'return ans': '枚举完所有入口，能入洞的打入位置：`{ans}`',
    },
    cards=dict(
        one_liner='路径唯一：枚举每个入口，直接模拟弹珠滚动',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['弹珠盘 `plate`：`O` 洞、`W` 逆时针转向器、`E` 顺时针转向器、`.` 空地',
                 '只能在边缘的空地（不含四角）、沿垂直于边缘的方向打入，最多前进 `num` 步',
                 '返回所有能让弹珠入洞的打入位置',
                 '本视频：`num = 4`，`plate = ["..E.",".EOW","..W."]` → `[[2,1]]`'],
        quote='由于路径是唯一的，一个入口只会对应一个唯一的出口……枚举所有入口，模拟即可。==不需要 DFS，写个循环就行==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['入口确定后，弹珠遇到转向器怎么转都是确定的，所以路径唯一',
              '不同入口的路径互不重叠、也没有环，每个状态至多访问一次',
              '方向数组按右下左上（顺时针）排，顺时针 `+1`，逆时针 `+3`（等价 `-1`）'],
        summary=['时间 `O(mn)`：状态（位置，方向）共 `4mn` 个，每个至多访问一次；空间 `O(1)`',
                 '逆时针写 `(d + 3) % 4`，避免负数取模',
                 '步数 `left` 在入洞前才扣；`left == 0` 时还没入洞就失败',
                 '四个角不能打入，所以边的枚举范围是 `1 ~ n-2` / `1 ~ m-2`',
                 '入口必须是 `.`，且方向与边缘垂直'],
    ),
)
