G = [[1, 1], [1, 0]]


def _I(S):
    return S.get('_inner') or S


def _agrid(S):
    return [list(r) for r in S['a']] if 'a' in S else None


def _fml(S):
    I = _I(S)
    if 'border' in I and 'j' in I and 'pre_top' in I:
        i, j = I['i'], I['j']
        if I['left'] < 0:
            return f'第 {i} 行到第 {j} 列还没有 1 → 面积 = ==上面的结果=='
        if I['pre_top'] < 0:
            return f'这行有 1、上面全是 0 → 面积 = ==右 {I["right"]} − 左 {I["left"]} + 1=='
        return '上下都有 1 → 面积 = ==(右 − 左 + 1) × (下 − 上 + 1)=='
    if 'lt' in S:
        return '已算好：' + '  '.join(f'{k} = {S[k]}' for k in ('lt', 'lb') if k in S)
    return '`f[i+1][j+1]` = 左上角 (0,0)、右下角 (i,j) 的子矩形里，包住所有 1 的最小矩形面积'


def _fml2(S):
    return '  '.join(f'{k} = {S[k]}' for k in ('rb', 'rt') if k in S)


def _fc(S, r, c, v):
    I = _I(S)
    if 'pre_top' in I and 'j' in I and (r, c) == (I['i'] + 1, I['j'] + 1):
        return 'yellow'
    return None


def _gc(S, r, c, v):
    I = _I(S)
    if 'pre_top' in I and 'j' in I and (r, c) == (I['i'], I['j']):
        return 'yellow'
    return None


CONFIG = dict(
    num=3197, title='包含所有 1 的最小矩形面积 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='六种划分 + 四角前缀最小矩形 DP',
    tags=['动态规划', '常用数据结构', '难度分 2541'],
    code='''
def rotate(a: List[List[int]]) -> List[List[int]]:
    return list(zip(*reversed(a)))

class Solution:
    def minimumSum(self, grid: List[List[int]]) -> int:
        return min(self.solve(grid), self.solve(rotate(grid)))

    def solve(self, a: List[List[int]]) -> int:
        m, n = len(a), len(a[0])

        def minimumArea(a: List[List[int]]) -> List[List[int]]:
            m, n = len(a), len(a[0])
            # f[i+1][j+1] 表示包含【左上角为 (0,0) 右下角为 (i,j) 的子矩形】中的所有 1 的最小矩形面积
            f = [[0] * (n + 1) for _ in range(m + 1)]
            border = [(-1, 0, 0)] * n
            for i, row in enumerate(a):
                left, right = -1, 0
                for j, x in enumerate(row):
                    if x:
                        if left < 0:
                            left = j
                        right = j
                    pre_top, pre_left, pre_right = border[j]
                    if left < 0:  # 这一排目前全是 0
                        f[i + 1][j + 1] = f[i][j + 1]  # 等于上面的结果
                    elif pre_top < 0:  # 这一排有 1，上面全是 0
                        f[i + 1][j + 1] = right - left + 1
                        border[j] = (i, left, right)
                    else:  # 这一排有 1，上面也有 1
                        l = min(pre_left, left)
                        r = max(pre_right, right)
                        f[i + 1][j + 1] = (r - l + 1) * (i - pre_top + 1)
                        border[j] = (pre_top, l, r)
            return f

        # 预处理每一行最左最右 1 的列号，用于中间区域最小矩形面积的计算
        lr = [None] * m
        for i in range(m):
            l, r = -1, 0
            for j in range(n):
                if a[i][j]:
                    if l < 0:
                        l = j
                    r = j
            lr[i] = (l, r)

        # lt[i+1][j+1] = 包含【左上角为 (0,0) 右下角为 (i,j) 的子矩形】中的所有 1 的最小矩形面积
        lt = minimumArea(a)
        a = rotate(a)
        # lb[i][j+1] = 包含【左下角为 (m-1,0) 右上角为 (i,j) 的子矩形】中的所有 1 的最小矩形面积
        lb = rotate(rotate(rotate(minimumArea(a))))
        a = rotate(a)
        # rb[i][j] = 包含【右下角为 (m-1,n-1) 左上角为 (i,j) 的子矩形】中的所有 1 的最小矩形面积
        rb = rotate(rotate(minimumArea(a)))
        a = rotate(a)
        # rt[i+1][j] = 包含【右上角为 (0,n-1) 左下角为 (i,j) 的子矩形】中的所有 1 的最小矩形面积
        rt = rotate(minimumArea(a))

        ans = inf
        if m >= 3:
            for i in range(1, m):
                left, right, top, bottom = n, -1, m, -1
                for j in range(i + 1, m):
                    l, r = lr[j - 1]
                    if l >= 0:
                        left = min(left, l)
                        right = max(right, r)
                        top = min(top, j - 1)
                        bottom = j - 1
                    # 图片上左
                    ans = min(ans, lt[i][n] + (right - left + 1) * (bottom - top + 1) + lb[j][n])

        if m >= 2 and n >= 2:
            for i in range(1, m):
                for j in range(1, n):
                    # 图片上中
                    ans = min(ans, lt[i][n] + lb[i][j] + rb[i][j])
                    # 图片上右
                    ans = min(ans, lt[i][j] + rt[i][j] + lb[i][n])
        return ans
''',
    call=f'Solution().minimumSum({G})',
    expect=3,
    skip=[2, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 29, 30, 31, 33, 34,
          9, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 49, 52, 55, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 73, 74, 75],
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='text', fn=_fml2, size=24, h=50),
        dict(type='grid', var=_agrid, label='a（当前方向的网格；黄 = 正在处理的格子）', cell=84, h=200, color=_gc),
        dict(type='table', var='f', label='f[i][j]：包住左上角子矩形里所有 1 的最小面积', cell=84, h=240, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('left', 'left', 'cyan'), ('right', 'right', 'orange'), ('ans', 'ans', 'green')],
    captions={
        6: lambda S, B, r: ('先按原方向求最小总面积；再旋转 90 度求一遍' if r is None
                            else f'两个方向取较小：答案 = =={r}=='),
        25: '这行到第 `{j}` 列还没有 1 → 面积同上一行：`f[{i+1}][{j+1}] = {f[i+1][j+1]}`',
        27: '这行有 1、上面全是 0 → 面积 = 最右 − 最左 + 1 = `{right} − {left} + 1` = =={f[i+1][j+1]}==',
        32: '上下都有 1 → 边界合并：宽 `{r} − {l} + 1` × 高 `{i} − {pre_top} + 1` = =={f[i+1][j+1]}==',
        48: '`lt`：以左上角 (0,0) 为角的所有子矩形，各自包住其中全部 1 的最小面积',
        51: '网格转 90 度再算，转回来 → `lb`（左下角）',
        54: '再转一次 → `rb`（右下角为角）',
        57: '再转一次 → `rt`（右上角为角）。四个角的预处理完成',
        77: lambda S, B, r: f'上中：上半 `lt[{S.i}][{S.n}]` = {S.lt[S.i][S.n]} + 左下 `lb[{S.i}][{S.j}]` = {S.lb[S.i][S.j]} + 右下 `rb[{S.i}][{S.j}]` = {S.rb[S.i][S.j]} → `ans` = =={S.ans}=='
                            ,
        79: lambda S, B, r: f'上右：左上 `lt[{S.i}][{S.j}]` = {S.lt[S.i][S.j]} + 右上 `rt[{S.i}][{S.j}]` = {S.rt[S.i][S.j]} + 下半 `lb[{S.i}][{S.n}]` = {S.lb[S.i][S.n]} → `ans` = =={S.ans}==',
        80: '这个方向的最小总面积 = =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='三个矩形只有六种切法，其中四种每块都含一个角：四角前缀 DP',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['二进制网格里选 ==3 个互不重叠==的矩形，盖住所有 1，求面积和最小',
                 '矩形可以相接；示例 `[[1,0,1],[1,1,1]]` → `5`',
                 '本视频：`[[1,1],[1,0]]` → `3`（三个 1 各用一个 1×1）'],
        quote='在六种划分方案中，右边四种每个区域都包含 grid 的一个角。尝试 DP。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三块不重叠矩形 = 先横/竖切一刀，再把其中一块切一刀 → 共六种',
              '右边四种每块都带一个角：`f[i+1][j+1]` 记左上角子矩形里包住所有 1 的最小面积',
              '用 `border` 滚动记上、左、右边界；转 90 度复用同一函数得到另外三个角',
              '左边两种的中间块：预处理每行最左最右的 1，枚举两条分割线时增量维护'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：`left < 0` 表示该行目前没有 1，三种情况必须分开',
                 '易错：旋转后 `lb`、`rb`、`rt` 还要转回来才对得上下标',
                 '易错：`m >= 3` / `m >= 2 and n >= 2` 保证每块非空',
                 '题解的方法一是暴力枚举，同一个格子被反复遍历；这里用 DP 消除重复',
                 '思考题：改成 4 个矩形怎么办'],
    ),
)
