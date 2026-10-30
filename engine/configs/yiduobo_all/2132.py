G0 = [[1, 0, 0], [1, 0, 0]]
CODE = '''
class Solution(object):
    def possibleToStamp(self, grid, stampHeight, stampWidth):

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = grid[i][j]
                    else:
                        f[i][j] = f[i][j - 1] + grid[i][j]
                elif j == 0:
                    f[i][j] = f[i - 1][j] + grid[i][j]
                else:
                    f[i][j] = f[i - 1][j] + f[i][j - 1] - f[i - 1][j - 1] + grid[i][j]
        
        g = [[0] * n for _ in range(m)]
        for i in range(stampHeight - 1, m):
            for j in range(stampWidth - 1, n):
                x = i - stampHeight + 1
                y = j - stampWidth + 1
                if x == 0:
                    if y == 0:
                        cnt = f[i][j]
                    else:
                        cnt = f[i][j] - f[i][y - 1]
                elif y == 0:
                    cnt = f[i][j] - f[x - 1][j]
                else:
                    cnt = f[i][j] - f[x - 1][j] - f[i][y - 1] + f[x - 1][y - 1]
                
                if cnt > 0:
                    g[i][j] = 0
                else:
                    g[i][j] = 1

        f = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if i == m - 1:
                    if j == n - 1:
                        f[i][j] = g[i][j]
                    else:
                        f[i][j] = f[i][j + 1] + g[i][j]
                elif j == n - 1:
                    f[i][j] = f[i + 1][j] + g[i][j]
                else:
                    f[i][j] = f[i + 1][j] + f[i][j + 1] - f[i + 1][j + 1] + g[i][j]
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    continue
                
                x = min(m - 1, i + stampHeight - 1)
                y = min(n - 1, j + stampWidth - 1)
                if x == m - 1:
                    if y == n - 1:
                        cnt = f[i][j]
                    else:
                        cnt = f[i][j] - f[i][y + 1]
                elif y == n - 1:
                    cnt = f[i][j] - f[x + 1][j]
                else:
                    cnt = f[i][j] - f[x + 1][j] - f[i][y + 1] + f[x + 1][y + 1]
                
                if cnt == 0:
                    return False

        return True
'''
_ls = CODE.split('\n')
_G = next(k for k, t in enumerate(_ls, 1) if 'g = [[0]' in t)
_F2 = [k for k, t in enumerate(_ls, 1) if 'f = [[0] * n' in t][1]
_YM = next(k for k, t in enumerate(_ls, 1) if 'y = min' in t)
_FIN = next(k for k, t in enumerate(_ls, 1) if 'for i in range(m):' in t)


def _st(S):
    ln = S.get('_line', 0)
    return 1 if ln < _G else 2 if ln < _F2 else 3 if ln < _FIN else 4


def _ok(S, k):
    return k in S


def _gcolor(S, i, j, v):
    if v == 1:
        return 'red'
    st = _st(S)
    if st == 2 and 'y' in S and 'cnt' in S or (st == 2 and 'y' in S and S['_line'] >= _G + 7):
        if S['x'] <= i <= S['i'] and S['y'] <= j <= S['j']:
            return 'yellow'
    if st == 4 and 'y' in S and S['_line'] > _YM and S['i'] <= i <= S['x'] and S['j'] <= j <= S['y']:
        return 'green' if S['_line'] > _YM + 10 and S['cnt'] > 0 else 'yellow'
    return None


def _fcolor(S, i, j, v):
    st = _st(S)
    if 'i' not in S or 'j' not in S:
        return None
    I, J = S['i'], S['j']
    if st in (1, 3):
        return 'yellow' if (i, j) == (I, J) else None
    if st == 2 and 'y' in S and S['_line'] >= _G + 5:
        x, y = S['x'], S['y']
        if (i, j) == (I, J):
            return 'yellow'
        if x > 0 and (i, j) == (x - 1, J) or y > 0 and (i, j) == (I, y - 1):
            return 'pink'
        if x > 0 and y > 0 and (i, j) == (x - 1, y - 1):
            return 'blue'
    return None


def _g2color(S, i, j, v):
    st = _st(S)
    if st == 2 and 'i' in S and (i, j) == (S['i'], S['j']) and S['_line'] >= _G + 15:
        return 'yellow'
    if st == 3 and 'i' in S and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return None


def _txt(S):
    st = _st(S)
    if st == 1:
        return '第 1 轮：`f[i][j]` = 左上角 (0,0) 到 (i,j) 的二维前缀和（要分四种情况，防止下标 −1）'
    if st == 2:
        return '第 2 轮：`g[i][j] = 1` 表示可以把邮票的==右下角==放在 (i,j)'
    if st == 3:
        return '第 3 轮：反过来算 `g` 的二维==后缀和==（右下到当前格），看某个格子能否被盖到'
    return '第 4 轮：每个空格子，看它能盖到的范围里有没有 `g = 1`'


CONFIG = dict(
    num=2132, title='用邮票贴满网格图', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和判断右下角 + 后缀和判断覆盖',
    tags=['常用数据结构', '二、差分', '难度分 2364'],
    code=CODE,
    call=f'Solution().possibleToStamp({G0}, 2, 2)',
    expect=True,
    skip=['m = len', 'n = len', 'x = i - stampHeight', 'y = j - stampWidth', 'for j in range', 'for i in range',
          'x = min', 'y = min', 'if i == 0:', 'if j == 0:', 'elif j == 0', 'if i == m - 1', 'if j == n - 1', 'elif j == n - 1',
          'if x == 0', 'if y == 0', 'elif y == 0', 'if x == m - 1', 'if y == n - 1', 'elif y == n - 1', 'continue'],
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='grid', var='grid', label='grid（红 = 被占据；黄/绿框 = 邮票能覆盖的范围）', color=_gcolor, h=190, cell=62),
        dict(type='table', var='f', label='f（前缀和 / 后缀和；黄 = 当前格，粉蓝 = 要减掉的）', color=_fcolor, h=190, cell=52),
        dict(type='table', var='g', label='g（1 = 能以此格为右下角贴邮票）', color=_g2color, h=190, cell=52),
    ],
    watch=['stampHeight', 'stampWidth', 'i', 'j', 'cnt'],
    captions={
        'f = [[0] * n': lambda S, B, r: ('`f` 记二维前缀和，先全 0' if 'g' not in S
                                         else '`f` 重新清零，这次存 `g` 的二维==后缀和==（从右下角往左上累加）'),
        'f[i][j] = grid[i][j]': '(0,0)：前缀和就是它自己，`f[0][0]` = =={f[0][0]}==',
        'f[i][j] = f[i][j - 1] + grid[i][j]': '第 0 行：只能累加左边，`f[{i}][{j}]` = =={f[i][j]}==',
        'f[i][j] = f[i - 1][j] + grid[i][j]': '第 0 列：只能累加上边，`f[{i}][{j}]` = =={f[i][j]}==',
        'f[i - 1][j] + f[i][j - 1] - f[i - 1][j - 1]': '上 + 左 − 左上 + 自己：`f[{i}][{j}]` = =={f[i][j]}==',
        'g = [[0]': '`g` 记录哪些格子能当邮票的右下角',
        'cnt = ': lambda S, B, r: (f'以 (`{S.x}`,`{S.y}`) 为左上、(`{S.i}`,`{S.j}`) 为右下的区域，元素和 `cnt` = =={S.cnt}=='
                                   if S.get('_line', 0) < _F2 else
                                   f'(`{S.i}`,`{S.j}`) 能盖到的区域 (`{S.i}`,`{S.j}`)~(`{S.x}`,`{S.y}`)，里面 `g = 1` 的个数 `cnt` = =={S.cnt}=='),
        'if cnt > 0': lambda S, B, r: (f'`cnt = {S.cnt} > 0` → 区域里有被占据的格子 → ==不能贴==' if S.cnt > 0
                                       else '`cnt = 0` → 区域全是空格 → ==能贴=='),
        'g[i][j] = 0': '`g[{i}][{j}] = 0`',
        'g[i][j] = 1': '`g[{i}][{j}] = 1`：邮票右下角可放在这里',
        'f[i][j] = g[i][j]': '右下角：后缀和就是 `g` 自己，`f[{i}][{j}]` = =={f[i][j]}==',
        'f[i][j] = f[i][j + 1] + g[i][j]': '最后一行：累加右边，`f[{i}][{j}]` = =={f[i][j]}==',
        'f[i][j] = f[i + 1][j] + g[i][j]': '最后一列：累加下边，`f[{i}][{j}]` = =={f[i][j]}==',
        'f[i + 1][j] + f[i][j + 1] - f[i + 1][j + 1]': '下 + 右 − 右下 + `g`：`f[{i}][{j}]` = =={f[i][j]}==',
        'if grid[i][j] == 1': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 1` 被占据，不用管，`continue`' if S.grid[S.i][S.j] == 1 else f'`grid[{S.i}][{S.j}] = 0` 空格子，要检查有没有邮票盖到它'),
        'if cnt == 0': lambda S, B, r: (f'空格子 (`{S.i}`,`{S.j}`)：能盖到它的 `g = 1` 有 `{S.cnt}` 个 → ==没人盖到它，返回 False=='
                                        if S.cnt == 0 else f'空格子 (`{S.i}`,`{S.j}`)：有 `{S.cnt}` 个右下角能盖到它 → 没问题'),
        'return True': '所有空格子都能被盖到，返回 `True`',
    },
    cards=dict(
        one_liner='反复用二维前缀和：先判哪里能贴，再判谁被盖到',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的 0/1 网格，0 是空格，1 是被占据',
                 '邮票 `h × w`：==不能盖 1==、不能出界、可重叠，要盖住所有空格',
                 '本视频：`[[1,0,0],[1,0,0]]`，邮票 `2×2` → `true`'],
        quote='首先，对于某个坐标为(i, j)个格子来说，能够以这个格子为右下角贴上邮票的条件为：……以(i - stampHeight +1, j - stampWidth + 1)为左上角，(i, j)为右下角的矩阵中不存在被占据的格子。',
        quote_src='—— yiduobo 题解原文',
        idea=['以 (i,j) 为右下角贴邮票：区域元素和 `== 0`，用前缀和 `f` 求',
              '`g[i][j] = 1` 记录能贴的右下角',
              '空格子 (i,j) 能被盖到 ⇔ 它右下方 `h×w` 范围内有 `g = 1`，再用 `g` 的==二维后缀和==判断'],
        summary=['时间、空间都是 `O(mn)`：前缀和一次，后缀和一次',
                 '前缀和要分 `x == 0`、`y == 0` 几种情况，避免 `f[-1]` 下标回绕',
                 '后缀和的范围右下角要用 `min(m-1, …)`、`min(n-1, …)` 夹到边界内',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：他用二维差分统计覆盖次数；这里用后缀和问“范围内有没有 1”'],
    ),
)
