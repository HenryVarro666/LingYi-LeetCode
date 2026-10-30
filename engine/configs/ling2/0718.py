A = [1, 2, 3, 2, 1]
B_ = [3, 2, 1, 4, 7]


def _cell(S, r, c, v):
    if 'i' not in S or 'j' not in S or S['_line'] not in (7, 8):
        if S['_line'] == 9 and v == 3:
            return 'green'
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i + 1, j + 1):
        return 'yellow'
    if A[i] == B_[j] and (r, c) == (i, j):
        return 'blue'
    return None


def _formula(S):
    if 'i' in S and 'j' in S and S['_line'] in (7, 8):
        i, j, x, y = S['i'], S['j'], S['x'], S['y']
        if x != y:
            return f'`nums1[{i}] = {x}` ≠ `nums2[{j}] = {y}` → 以它们结尾的公共子数组为空，`f[{i + 1}][{j + 1}]` 保持 0'
        return f'`{x} == {y}`：接在 `f[{i}][{j}]` 后面 → `f[{i + 1}][{j + 1}] = {S["f"][i][j]} + 1 =` =={S["f"][i + 1][j + 1]}=='
    return '`f[i+1][j+1]`：以 `nums1[i]`、`nums2[j]` ==结尾==的最长公共子数组长度'


def _if(S, B, ret):
    i, j, x, y = S.i, S.j, S.x, S.y
    if x == y:
        return f'`nums1[{i}] = nums2[{j}] = {x}` → 可以在左上角的公共子数组后面==接上=='
    return f'`{x}` ≠ `{y}` → 保持 0'


CONFIG = dict(
    num=718, title='最长重复子数组', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='动态规划（仿照 1143 最长公共子序列）',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        n, m = len(nums1), len(nums2)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i, x in enumerate(nums1):
            for j, y in enumerate(nums2):
                if x == y:
                    f[i + 1][j + 1] = f[i][j] + 1
        return max(map(max, f))  # 所有 f[i][j] 的最大值
''',
    call=f'Solution().findLength({A}, {B_})',
    expect=3,
    skip=['n, m = len', 'for j, y in'],
    views=[
        dict(type='text', fn=_formula, size=26),
        dict(type='table', var='f', label='f：行头 = nums1 [1,2,3,2,1]，列头 = nums2 [3,2,1,4,7]（黄 = 正在算，蓝 = 左上角）', h=560, cell=84,
             color=_cell, rows=lambda S: ['空'] + [str(x) for x in A], cols=lambda S: ['空'] + [str(y) for y in B_],
             cursors=[('i + 1', 'j + 1', 'yellow', '')]),
    ],
    watch=[('i', 'i', 'pink'), ('x', 'x', 'pink'), ('j', 'j', 'cyan'), ('y', 'y', 'cyan')],
    captions={
        'f = [[0]': '多开一行一列：`f[0][j] = f[i][0] = 0` 表示==空子数组==，免去特判',
        'for i, x in enumerate(nums1)': lambda S, B, ret: (f'`i = {S.i}`：以 `nums1[{S.i}] = {S.x}` 结尾，扫一遍 `nums2`'
                                                           if B.get('i') != S.i else '填表结束'),
        'if x == y': _if,
        'f[i + 1][j + 1] = f[i][j] + 1': '`f[{i + 1}][{j + 1}] = f[{i}][{j}] + 1 = {f[i + 1][j + 1]}`：左上角的长度 + 1',
        'return max(map(max, f))': '答案是==所有== `f[i][j]` 的最大值：=={ret}==（`[3,2,1]`）',
    },
    cards=dict(
        one_liner='仿照 1143：以 nums1[i]、nums2[j] 结尾，相等就接在左上角后面',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['给两个整数数组 `nums1`、`nums2`，返回两个数组中==公共的、长度最长的子数组==的长度',
                 '子数组必须==连续==（对比 1143 的子序列）',
                 '示例：`[1,2,3,2,1]`、`[3,2,1,4,7]` → `3`（`[3,2,1]`）'],
        quote='仿照 1143，定义 f[i+1][j+1] 表示==以 nums1[i] 结尾的子数组和以 nums2[j] 结尾的子数组==的最长公共子数组的长度。这里 +1 是为了兼容空子数组的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums1[i] ≠ nums2[j]`：以它俩结尾不可能公共 → `f[i+1][j+1] = 0`',
              '相等：在以 `nums1[i-1]`、`nums2[j-1]` 结尾的公共子数组后面添加 → `f[i][j] + 1`',
              '答案不一定在右下角：取所有 `f[i][j]` 的最大值'],
        result='最长公共子数组 `[3,2,1]`，长度 `3` ✓',
        summary=['时间 `O(nm)`，空间 `O(nm)`（可优化成 `O(m)`，同 1143）',
                 '和 1143 的区别：不相等时是 ==0==，不是 `max(f[i][j+1], f[i+1][j])`',
                 '`+1` 偏移：第 0 行/列表示空子数组，不用特判 `i = 0` 或 `j = 0`',
                 '附：后缀数组可做到 `O(n + m)`'],
    ),
)
