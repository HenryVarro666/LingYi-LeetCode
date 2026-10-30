MAT = [[1, 4, 3, 2, 6], [5, 6, 5, 3, 7], [7, 9, 12, 4, 8], [2, 3, 10, 1, 0]]


def _cell(S, i, j, v):
    if 'l' not in S or 'mid' not in S:
        return None
    mid = S['mid']
    if i == mid and 9 <= S.get('_line', 0) <= 21:
        return 'blue'
    if i == mid + 1 and 9 <= S.get('_line', 0) <= 21:
        return 'pink'
    return None


def _info(S):
    if 'l' not in S or 'r' not in S:
        return '按行二分：比较「中线两行」的最大值，留下较大的那一半'
    if 'top_max' in S and 'bottom_max' in S and 'mid' in S and S.get('_line', 0) >= 14:
        return f'第 {S["mid"]} 行最大 `{S["top_max"]}`（蓝） vs 第 {S["mid"] + 1} 行最大 `{S["bottom_max"]}`（粉）'
    return f'候选行 `[{S["l"]}, {S["r"]}]`'


CONFIG = dict(
    num=1901, title='寻找峰值 II', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='按行分治 · 比较相邻两行最大值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findPeakGrid(self, mat):

        m = len(mat)
        n = len(mat[0])
        l = 0
        r = m - 1
        while l < r:
            mid = (l + r) >> 1
            top_max = 0
            for num in mat[mid]:
                top_max = max(top_max, num)
            
            bottom_max = 0
            for num in mat[mid + 1]:
                bottom_max = max(bottom_max, num)
            
            if top_max > bottom_max:
                r = mid
            else:
                l = mid + 1
        
        ma = mat[l][0];
        res_y = 0
        for index in range(1, n):
            if mat[l][index] > ma:
                ma = mat[l][index];
                res_y = index
        
        return [l, res_y]
''',
    call=f'Solution().findPeakGrid({MAT})',
    expect=[2, 2],
    skip=['m = len', 'n = len', 'l = 0', 'r = m - 1', 'top_max = 0', 'bottom_max = 0',
          'for num in', 'top_max = max', 'bottom_max = max'],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='grid', var='mat', cell=96, h=420, color=_cell),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'),
           ('top_max', 'top_max', 'blue'), ('bottom_max', 'bottom_max', 'pink')],
    captions={
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，候选行还没缩成一行' if S.l < S.r
                                        else f'`l = {S.l} == r = {S.r}`：只剩第 =={S.l}== 行 → 峰值在这一行'),
        'mid = (l + r)': '取中间的两行：第 `{mid}` 行和第 `{mid + 1}` 行，它们之间的「接壤线」要比大小',
        'if top_max > bottom_max': lambda S, B, r: (
            f'上行最大 `{S.top_max}` > 下行最大 `{S.bottom_max}`：上行最大值比下边、左右都大 → ==上半（含第 {S.mid} 行）必有极大值=='
            if S.top_max > S.bottom_max else
            f'上行最大 `{S.top_max}` < 下行最大 `{S.bottom_max}`：下行的最大值更大，==峰值在下半（第 {S.mid + 1} 行起）=='),
        'r = mid': '舍弃下半：`r = {r}`',
        'l = mid + 1': '舍弃上半：`l = {l}`',
        'ma = mat[l][0]': '只剩第 `{l}` 行了，扫一遍找这一行的最大值，从第 0 列开始',
        'if mat[l][index] > ma': '`mat[{l}][{index}] = {mat[l][index]}` vs 当前最大 `{ma}` → ' + '{"更大，记下列号" if mat[l][index] > ma else "不更大"}',
        'ma = mat[l][index]': '更新最大值 `ma = {ma}`，列号 `{index}`',
        'res_y = index': '`res_y = {res_y}`',
        'return [l, res_y]': '峰值位置 ==`{ret}`==',
    },
    cards=dict(
        one_liner='把接壤的中线「堵死」：取两行最大值，留较大的一半',
        complexity='时间 `O(n log m)`，空间 `O(1)`',
        problem=['矩阵里严格大于上下左右的数叫峰值，相邻数互不相同，周围当作 `-1`',
                 '返回任意一个峰值的位置，要求 `O(m log n)` 或 `O(n log m)`',
                 '本视频：4×5 矩阵 → `[2, 2]`'],
        quote='对于这两个最大值中较大的那一个……由于其是中线的最大值，因此x必然大于上下两侧的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想一维：`a[mid] < a[mid+1]` 则右边必有极大值',
              '二维不能只看一个数：单调路径可能从别处绕过接壤线 → 取==中线最大值==堵死',
              '我选分成上下两半：比较第 `mid` 行和第 `mid+1` 行的最大值，留较大那边'],
        summary=['时间 `O(n log m)`：二分 `log m` 次，每次扫两行',
                 '`l < r` 收缩到一行后，再扫这一行求最大值的列号',
                 '易错：`top_max` 初值 0 依赖 `mat[i][j] >= 1`（题目保证）',
                 '对比灵神：灵神只和「最大值正下方」一个数比，yiduobo 比两行的最大值'],
    ),
)
