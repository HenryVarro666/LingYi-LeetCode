FF = [[0, 0, 1], [1, 0, 1], [1, 1, 1]]


def _stage(S):
    ln = S.get('_line', 0)
    return 1 if ln <= 15 else 2 if ln <= 29 else 3


def _txt(S):
    st = _stage(S)
    ln = S.get('_line', 0)
    if st == 1 and 'side' in S and ln <= 10:
        i, j, s = S['i'], S['j'], S['side']
        return f'力场 (`{i}`,`{j}`) 边长 `{s}`：坐标 ×2 后 x∈[`{2*i-s}`,`{2*i+s}`]，y∈[`{2*j-s}`,`{2*j+s}`]'
    if st == 1:
        return '第 1、2 步：收集所有矩形边界坐标（×2 去掉 0.5），排序离散化'
    if st == 2:
        if 'r1' in S and ln >= 20:
            return f'第 3 步：离散化后矩形 行 `{S["r1"]}`~`{S["r2"]}`，列 `{S["c1"]}`~`{S["c2"]}`，在 diff 里只改 4 个角（下标 +1）'
        return '第 3 步：每个矩形在二维差分上改 4 个角'
    return '第 4 步：二维前缀和还原每个点的力场强度，取最大值'


def _dcolor(S, i, j, v):
    st = _stage(S)
    ln = S.get('_line', 0)
    if st == 2 and 'r1' in S and ln >= 26:
        r1, r2, c1, c2 = S['r1'], S['r2'], S['c1'], S['c2']
        if (i, j) in ((r1 + 1, c1 + 1), (r2 + 2, c2 + 2)):
            return 'green'
        if (i, j) in ((r1 + 1, c2 + 2), (r2 + 2, c1 + 1)):
            return 'pink'
        return None
    if st == 3 and ln >= 35 and 'j' in S and (i, j) == (S['i'], S['j']):
        return 'yellow' if S['diff'][i][j] < S['ans'] or ln == 35 else 'green'
    return None


CONFIG = dict(
    num='LCP 74', title='最强祝福力场', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='离散化 + 二维差分',
    tags=['常用数据结构', '二、差分'],
    code='''
class Solution:
    def fieldOfGreatestBlessing(self, forceField: List[List[int]]) -> int:
        # 1. 统计所有左下和右上坐标
        x_set = set()
        y_set = set()
        for i, j, side in forceField:
            x_set.add(2 * i - side)
            x_set.add(2 * i + side)
            y_set.add(2 * j - side)
            y_set.add(2 * j + side)

        # 2. 离散化
        xs = sorted(x_set)
        ys = sorted(y_set)
        n, m = len(xs), len(ys)

        # 3. 二维差分：快速地把一个矩形范围内的数都 +1
        diff = [[0] * (m + 2) for _ in range(n + 2)]
        for i, j, side in forceField:
            r1 = bisect_left(xs, 2 * i - side)
            r2 = bisect_left(xs, 2 * i + side)
            c1 = bisect_left(ys, 2 * j - side)
            c2 = bisect_left(ys, 2 * j + side)
            # 将区域 r1<=r<=r2 && c1<=c<=c2 上的数都加上 x
            # 多 +1 是为了方便求后面用二维前缀和复原
            diff[r1 + 1][c1 + 1] += 1
            diff[r1 + 1][c2 + 2] -= 1
            diff[r2 + 2][c1 + 1] -= 1
            diff[r2 + 2][c2 + 2] += 1

        # 4. 直接在 diff 上复原（二维前缀和），计算最大值
        ans = 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                diff[i][j] += diff[i][j - 1] + diff[i - 1][j] - diff[i - 1][j - 1]
                ans = max(ans, diff[i][j])
        return ans
''',
    call=f'Solution().fieldOfGreatestBlessing({FF})',
    expect=3,
    skip=['r1 = ', 'r2 = ', 'c1 = ', 'c2 = ', 'n, m = len', 'for j in range'],
    max_steps=100,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var=lambda S: sorted(S['x_set']) if 'x_set' in S and 'xs' not in S else S.get('xs'),
             label='xs（所有矩形的 x 边界，×2 后离散化）', h=160, cell=70),
        dict(type='array', var=lambda S: sorted(S['y_set']) if 'y_set' in S and 'ys' not in S else S.get('ys'),
             label='ys（所有矩形的 y 边界，×2 后离散化）', h=160, cell=70),
        dict(type='table', var='diff', label='diff（二维差分，行 = xs 下标 + 1，列 = ys 下标 + 1；绿 = +1，粉 = −1）',
             color=_dcolor, h=380, cell=60),
    ],
    watch=['i', 'j', 'side', ('ans', 'ans', 'green')],
    captions={
        'x_set = set()': '力场是正方形：只关心每个正方形的==左下、右上==坐标，先准备两个集合',
        'for i, j, side in forceField:': lambda S, B, r: ('力场遍历完了' if 'i' in B and (S.i, S.j, S.side) == (B.i, B.j, B.side)
                                                          else ('取一片力场：中心 (`{}`,`{}`)，边长 `{}`'.format(S.i, S.j, S.side)
                                                                + ('' if S.get('_line') <= 10 else '，在 diff 上 +1'))),
        'y_set = set()': '`y_set` 同理存 y 方向的边界',
        'x_set.add(2 * i - side)': '左边界 `2i − side` = `{2*i-side}`：==坐标 ×2==，这样 0.5 变成整数 1',
        'x_set.add(2 * i + side)': '右边界 `2i + side` = `{2*i+side}`',
        'y_set.add(2 * j - side)': '下边界 `2j − side` = `{2*j-side}`',
        'y_set.add(2 * j + side)': '上边界 `2j + side` = `{2*j+side}`',
        'xs = sorted': '排序去重得到 `xs`：只有这几个 x 坐标可能是强度变化的位置，==离散化==后坐标只剩 {len(xs)} 个',
        'ys = sorted': '同理 `ys` 有 {len(ys)} 个，后面的二维数组只要 `{len(xs)} × {len(ys)}`',
        'diff = [[0]': '`diff` 多一圈（`+2`），第 4 步复原时不用判断边界',
        'diff[r1 + 1][c1 + 1] += 1': lambda S, B, r: (f'这片力场在离散化后覆盖 行 `{S.r1}`~`{S.r2}`、列 `{S.c1}`~`{S.c2}`（`bisect_left` 找下标）；'
                                                      f'左上角 `diff[{S.r1+1}][{S.c1+1}]` +1'),
        'diff[r1 + 1][c2 + 2] -= 1': '右边界外一列 −1，抵消向右的传播',
        'diff[r2 + 2][c1 + 1] -= 1': '下边界外一行 −1，抵消向下的传播',
        'diff[r2 + 2][c2 + 2] += 1': '右下角外 +1：前两次减重复了，补回来',
        'ans = 0': '`ans` 记录最大力场强度',
        'diff[i][j] +=': '`diff[{i}][{j}]` 加上 上 + 左 − 左上，复原成该点的力场强度 = =={diff[i][j]}==',
        'ans = max': '`ans = max({B.ans}, {diff[i][j]})` = =={ans}==',
        'return ans': '最大力场强度是 =={ret}==',
    },
    cards=dict(
        one_liner='坐标 ×2 去掉小数，离散化后做二维差分',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`，`n` 是力场个数',
        problem=['`forceField[i] = [x, y, side]`：以 `(x, y)` 为中心、边长 `side` 的正方形力场（边缘也算）',
                 '某点的强度 = 覆盖它的力场个数，求最大强度',
                 '本视频：`[[0,0,1],[1,0,1],[1,1,1]]` → `3`'],
        quote='统计所有左下和右上坐标，由于会出现 0.5，可以将坐标乘 2。离散化横纵坐标。二维差分，具体见视频讲解。用二维前缀和复原，计算最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['坐标最大 `10^9`，但最多 100 片力场，只有 ==边界坐标== 才会让强度变化',
              '边界排序去重 → 离散化成小下标，二维数组只有 `O(n^2)` 大',
              '每片力场 = 矩形 +1，用二维差分 4 个角；最后二维前缀和还原再取 max'],
        summary=['时间 `O(n^2)`：离散化后 xs、ys 各最多 `2n` 个',
                 '易错：中心可能在 `.5`，所以全部坐标 ×2，边界是 `2i ± side`',
                 '易错：边缘也算覆盖，所以用 `bisect_left` 把两端都取闭区间',
                 'diff 多 +1、+2 偏移是为了前缀和还原时不用判断下标越界',
                 '同类题：2132. 用邮票贴满网格图（二维差分）'],
    ),
)
