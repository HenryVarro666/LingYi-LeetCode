G0 = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]


def _stage(S):
    ln = S.get('_line', 0)
    return 1 if ln <= 11 else (2 if ln <= 23 else 3)


def _rect(S):
    """stage 2: stamp rectangle in 0-index grid coords (r1, c1, r2, c2) or None"""
    if _stage(S) != 2 or S.get('_line', 0) < 18 or 'j1' not in S or 'i2' not in S:
        return None
    return (S['i1'] - 1, S['j1'] - 1, S['i2'] - 1, S['j2'] - 1)


def _gcolor(S, i, j, v):
    if v == 1:
        return 'red'
    r = _rect(S)
    if r and r[0] <= i <= r[2] and r[1] <= j <= r[3]:
        return 'green' if S['_line'] >= 19 and S['s'][S['i2']][S['j2']] - S['s'][S['i2']][S['j1'] - 1] - S['s'][S['i1'] - 1][S['j2']] + S['s'][S['i1'] - 1][S['j1'] - 1] == 0 else 'yellow'
    if _stage(S) == 3 and 'i' in S and S['_line'] >= 27 and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return None


def _scolor(S, i, j, v):
    r = _rect(S)
    if r and S['_line'] >= 18:
        i1, j1, i2, j2 = S['i1'], S['j1'], S['i2'], S['j2']
        if (i, j) == (i2, j2):
            return 'yellow'
        if (i, j) in ((i2, j1 - 1), (i1 - 1, j2)):
            return 'pink'
        if (i, j) == (i1 - 1, j1 - 1):
            return 'blue'
    if _stage(S) == 1 and 'i' in S and (i, j) == (S['i'] + 1, S['j'] + 1):
        return 'yellow'
    return None


def _dcolor(S, i, j, v):
    if _stage(S) == 3 and 'i' in S and S['_line'] >= 27:
        if (i, j) == (S['i'] + 1, S['j'] + 1):
            return 'yellow'
    if _stage(S) == 2 and S['_line'] >= 22 and 'i1' in S:
        i1, j1, i2, j2 = S['i1'], S['j1'], S['i2'], S['j2']
        if (i, j) in ((i1, j1), (i2 + 1, j2 + 1)):
            return 'green'
        if (i, j) in ((i1, j2 + 1), (i2 + 1, j1)):
            return 'pink'
    return None


def _txt(S):
    st = _stage(S)
    if st == 1:
        return '第 1 步：`s[i+1][j+1]` = 左上角 (0,0) 到 (i,j) 的元素和，用来 O(1) 判断某块有没有 1'
    if st == 2:
        if 'j1' in S and 'i2' in S and S['_line'] >= 18:
            i1, j1, i2, j2 = S['i1'], S['j1'], S['i2'], S['j2']
            sm = S['s'][i2][j2] - S['s'][i2][j1 - 1] - S['s'][i1 - 1][j2] + S['s'][i1 - 1][j1 - 1]
            return f'邮票右下角 (`{i2-1}`,`{j2-1}`)：区域元素和 =={sm}== → ' + ('能贴' if sm == 0 else '有被占据的格子，不能贴')
        return '第 2 步：枚举邮票右下角，能贴就在差分矩阵 `d` 上改 4 个角'
    return '第 3 步：对 `d` 做二维前缀和还原计数，空格子的计数不能为 0'


CONFIG = dict(
    num=2132, title='用邮票贴满网格图', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='二维前缀和 + 二维差分',
    tags=['常用数据结构', '二、差分', '难度分 2364'],
    code='''
class Solution:
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        m, n = len(grid), len(grid[0])

        # 1. 计算 grid 的二维前缀和
        s = [[0] * (n + 1) for _ in range(m + 1)]
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                s[i + 1][j + 1] = s[i + 1][j] + s[i][j + 1] - s[i][j] + v

        # 2. 计算二维差分
        # 为方便第 3 步的计算，在 d 数组的最上面和最左边各加了一行（列），所以下标要 +1
        d = [[0] * (n + 2) for _ in range(m + 2)]
        for i2 in range(stampHeight, m + 1):
            for j2 in range(stampWidth, n + 1):
                i1 = i2 - stampHeight + 1
                j1 = j2 - stampWidth + 1
                if s[i2][j2] - s[i2][j1 - 1] - s[i1 - 1][j2] + s[i1 - 1][j1 - 1] == 0:
                    d[i1][j1] += 1
                    d[i1][j2 + 1] -= 1
                    d[i2 + 1][j1] -= 1
                    d[i2 + 1][j2 + 1] += 1

        # 3. 还原二维差分矩阵对应的计数矩阵（原地计算）
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                d[i + 1][j + 1] += d[i + 1][j] + d[i][j + 1] - d[i][j]
                if v == 0 and d[i + 1][j + 1] == 0:
                    return False
        return True
''',
    call=f'Solution().possibleToStamp({G0}, 2, 2)',
    expect=True,
    skip=['i1 = ', 'j1 = ', 'for i, row in enumerate', 'for j, v in enumerate', 'for i2 in', 'for j2 in', 'm, n = len'],
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='grid', var='grid', label='grid（红 = 被占据；黄/绿框 = 当前邮票位置）', color=_gcolor, h=250, cell=70),
        dict(type='table', var='s', label='s 二维前缀和（黄 = 右下角，粉/蓝 = 要减掉的）', color=_scolor, h=280, cell=56),
        dict(type='table', var='d', label='d 二维差分（绿 = +1，粉 = −1）', color=_dcolor, h=330, cell=50),
    ],
    watch=['stampHeight', 'stampWidth', 'i2', 'j2', 'i', 'j'],
    captions={
        's = [[0]': '前缀和数组 `s` 比 grid 多一行一列，`s[i+1][j+1]` 是左上角 (0,0) 到 (i,j) 的元素和',
        's[i + 1][j + 1] =': '`s[{i+1}][{j+1}]` = 上 + 左 − 左上（重复加了一次）+ `grid[{i}][{j}]` = =={s[i+1][j+1]}==',
        'd = [[0]': '差分矩阵 `d`：多一圈，放邮票只改 4 个角，最后前缀和还原计数',
        'if s[i2][j2]': lambda S, B, r: (f'邮票右下角 (`{S.i2-1}`,`{S.j2-1}`)、左上角 (`{S.i1-1}`,`{S.j1-1}`)：'
            f'矩形和 `{S.s[S.i2][S.j2] - S.s[S.i2][S.j1-1] - S.s[S.i1-1][S.j2] + S.s[S.i1-1][S.j1-1]}`'
            + (' == 0 → ==没有被占据的格子，能贴==' if S.s[S.i2][S.j2] - S.s[S.i2][S.j1-1] - S.s[S.i1-1][S.j2] + S.s[S.i1-1][S.j1-1] == 0
               else ' ≠ 0 → 里面有 1，不能贴')),
        'd[i1][j1] += 1': '左上角 +1：从这里开始，右下方整块都多一张邮票',
        'd[i1][j2 + 1] -= 1': '右边界外一列 −1：把右侧多出来的影响抵消',
        'd[i2 + 1][j1] -= 1': '下边界外一行 −1：把下方多出来的影响抵消',
        'd[i2 + 1][j2 + 1] += 1': '右下角外 +1：上面两次减重复了，加回来',
        'd[i + 1][j + 1] +=': '`d[{i+1}][{j+1}]` 做二维前缀和，还原成这个格子被盖的次数 = =={d[i+1][j+1]}==',
        'if v == 0 and': lambda S, B, r: (f'`grid[{S.i}][{S.j}]` 是被占据的格子，不用被盖' if S.v == 1
            else f'空格子 (`{S.i}`,`{S.j}`) 被盖了 `{S.d[S.i+1][S.j+1]}` 次 → ' + ('==没人盖，返回 False==' if S.d[S.i+1][S.j+1] == 0 else '至少一张，没问题')),
        'return True': '所有空格子都被盖住，返回 `True`',
    },
    cards=dict(
        one_liner='能贴就贴：前缀和判断能不能贴，差分统计谁被盖到',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的 0/1 矩阵，0 是空格，1 是被占据',
                 '用 `h × w` 的邮票盖住所有空格，==不能盖 1==、不能出界，可以重叠',
                 '本视频：`3×3` 网格，邮票 `2×2` → `true`'],
        quote='由于邮票可以互相重叠，贪心地想，能放邮票就放邮票。……怎么快速判断一个矩形区域可以放邮票？求出 grid 的二维前缀和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：每个合法位置都放一张，重叠不影响答案',
              '二维前缀和：矩形元素和 `== 0` 就说明里面没有被占据的格子',
              '二维差分：放一张邮票 = `d` 的 4 个角各改一次，最后前缀和还原计数'],
        summary=['时间、空间都是 `O(mn)`，不用 `O(mnhw)` 暴力放邮票',
                 '差分矩阵 `d` 比 grid 多一圈（`m+2`、`n+2`），下标整体 +1，`j2+1`、`i2+1` 才不越界',
                 '易错：矩形和公式 `s[i2][j2] - s[i2][j1-1] - s[i1-1][j2] + s[i1-1][j1-1]` 的符号',
                 '易错：只检查 `v == 0` 的格子是否计数为 0，被占据的格子不用盖'],
    ),
)
