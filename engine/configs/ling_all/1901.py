MAT = [[1, 4, 3, 2, 6], [5, 6, 5, 3, 7], [7, 9, 12, 4, 8], [2, 3, 10, 1, 0]]


def _cell(S, i, j, v):
    if 'left' not in S:
        return None
    mid = S.get('i')
    if mid is not None and i == mid:
        if 'mx' in S and v == S['mx']:
            return 'green'
        return 'blue'
    return None


def _dim(S, i, j, v):
    if 'left' not in S:
        return False
    return not (S['left'] <= i <= S['right'] + 1)


def _info(S):
    if 'left' not in S:
        return '二分「峰顶所在的行号」，每次只看一整行的最大值'
    l, r = S['left'], S['right']
    if l > r:
        return f'区间空了：`left = {l}`，峰顶行就是第 =={l}== 行'
    return f'候选行 `[{l}, {r}]`（最后一行 {len(S["mat"]) - 1} 不在范围内，它是兜底答案）'


CONFIG = dict(
    num=1901, title='寻找峰值 II', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分行号 · 取行最大值',
    tags=['灵神题单'],
    code='''
class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:
        left, right = 0, len(mat) - 2
        while left <= right:
            i = (left + right) // 2
            mx = max(mat[i])
            if mx > mat[i + 1][mat[i].index(mx)]:
                right = i - 1  # 峰顶行号 <= i
            else:
                left = i + 1  # 峰顶行号 > i
        return [left, mat[left].index(max(mat[left]))]
''',
    call=f'Solution().findPeakGrid({MAT})',
    expect=[2, 2],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='grid', var='mat', cell=96, h=420, color=_cell, dim=_dim),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('i', 'i', 'yellow'), ('mx', 'mx', 'green')],
    captions={
        'left, right = 0': '二分行号：区间 `[0, m-2]` = `[{left}, {right}]`。==最后一行不放进去==，避免 `i+1` 越界',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`，还有候选行' if S.left <= S.right
                                                else f'`left = {S.left} > right = {S.right}`，区间空了 → 结束'),
        'i = (left + right)': '取中间行 `i = {i}`',
        'mx = max': '第 {i} 行最大值 `mx = {mx}`，在第 {mat[i].index(mx)} 列。它比同行其他数都大，只需再和上下比',
        'if mx >': lambda S, B, r: (f'`mx = {S.mx}` > 正下方 `{S.mat[S.i + 1][S.mat[S.i].index(S.mx)]}` → ==上半部分（含第 {S.i} 行）必有峰顶=='
                                    if S.mx > S.mat[S.i + 1][S.mat[S.i].index(S.mx)]
                                    else f'`mx = {S.mx}` < 正下方 `{S.mat[S.i + 1][S.mat[S.i].index(S.mx)]}` → 往下走更高，==峰顶在更下面的行=='),
        'right = i - 1': '峰顶行号 <= {i} → `right = {right}`，扔掉下半部分',
        'left = i + 1': '峰顶行号 > {i} → `left = {left}`，扔掉上半部分',
        'return [left': '峰顶行 `{left}`，该行最大值所在列就是答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='二分行号：行最大值若比下面小，峰顶一定在下面',
        complexity='时间 `O(n log m)`，空间 `O(1)`',
        problem=['矩阵里严格大于上下左右的数是「峰值」，相邻数互不相等，周围一圈当作 `-1`',
                 '找任意一个峰值的位置，要求 `O(m log n)` 或 `O(n log m)`',
                 '本视频：4×5 矩阵 → `[2, 2]`（值 12）'],
        quote='如果 mat[i] 的最大值比它下面的相邻数字小，则存在一个峰顶，其行号大于 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想「人往高处走」：能找到峰顶，但蛇形路径最坏 `O(mn)`',
              '改成二分行号：取一整行的最大值，它必然比左右大，只需和==下方==比',
              '初始区间 `[0, m-2]`：全部往下走时，最后一行必含峰顶，也不用判越界'],
        summary=['时间 `O(n log m)`：二分 `log m` 次，每次扫一行求最大值',
                 '易错：区间右端点是 `m-2` 而不是 `m-1`，否则 `mat[i+1]` 越界',
                 '题解还给了左闭右开、开区间两种写法，原理相同，本视频用闭区间',
                 '同类题：162. 寻找峰值（一维版，同样在 `[0, n-2]` 二分）'],
    ),
)
