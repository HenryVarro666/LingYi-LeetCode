def _color(S, r, c, v):
    i, j, ln = S.get('i'), S.get('j'), S.get('_line')
    if i is None or j is None or ln not in (12, 14, 16, 18):
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if ln == 18 and (r, c) == (i - 1, j - 1):
        return 'green'
    if ln in (14, 18) and (r, c) == (i, j - 1):
        return 'blue'
    if ln in (16, 18) and (r, c) == (i - 1, j):
        return 'blue'
    return None


def _formula(S):
    i, j, ln = S.get('i'), S.get('j'), S.get('_line')
    if i is None or j is None or ln not in (12, 14, 16, 18):
        return '`f[i][j]`：两数组前缀的最大点积（非空）'
    a, b, f = S['nums1'][i], S['nums2'][j], S['f']
    if ln == 12:
        return f'第一个格子只能选 `{a}×{b}` = =={a * b}=='
    if ln == 14:
        return f'`max(f[0][{j - 1}], {a}×{b})` = `max({f[i][j - 1]}, {a * b})`'
    if ln == 16:
        return f'`max(f[{i - 1}][0], {a}×{b})` = `max({f[i - 1][j]}, {a * b})`'
    return (f'选：`max(f[{i - 1}][{j - 1}], 0) + {a}×{b}` = {max(f[i - 1][j - 1], 0) + a * b}　'
            f'丢 a：{f[i - 1][j]}　丢 b：{f[i][j - 1]}')


CONFIG = dict(
    num=1458, title='两个子序列的最大点积', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 分边界四种情况',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1824'],
    code='''
class Solution(object):
    def maxDotProduct(self, nums1, nums2):

        m = len(nums1)
        n = len(nums2)

        f = [[None] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = nums1[i] * nums2[j]
                    else:
                        f[i][j] = max(f[i][j - 1], nums1[i] * nums2[j])
                elif j == 0:
                    f[i][j] = max(f[i - 1][j], nums1[i] * nums2[j])
                else:
                    f[i][j] = max(max(f[i - 1][j - 1], 0) + nums1[i] * nums2[j], f[i][j - 1], f[i - 1][j])
                    
        return f[-1][-1]
''',
    call='Solution().maxDotProduct([2, 1, -2], [3, 0, -6])',
    expect=18,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿/蓝 = 它依赖的格子）', h=380, cell=110,
             rows=lambda S: [f'{v}' for v in S['nums1']], cols=lambda S: [f'{v}' for v in S['nums2']],
             color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('nums1[i]', 'nums1[i]', 'blue'), ('nums2[j]', 'nums2[j]', 'pink')],
    captions={
        'm = len': '`m = {m}`：`nums1` 的长度',
        'n = len': '`n = {n}`：`nums2` 的长度',
        'f = [[None]': '`f[i][j]`：`nums1[:i+1]` 与 `nums2[:j+1]` 的最大点积；先全部留空',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行：`nums1[{S.i}] = {S.nums1[S.i]}`' if S.i != B.get('i') else '所有格子都算完了'),
        'if i == 0': lambda S, B, r: (f'`i = {S.i}`：是 `nums1` 的第一个数' if S.i == 0 else f'`i = {S.i} ≠ 0`：看 `j` 是否为 0'),
        11: lambda S, B, r: ('`j = 0`：两个数组都只有第一个元素，==必须选它们==（非空）' if S.j == 0 else '`j > 0`：可以选 `nums2[j]`，也可以沿用左边'),
        15: lambda S, B, r: ('`j = 0`：第一列，只能用 `nums2[0]`' if S.j == 0 else '`j > 0`：左边、上边、左上角都存在，走一般转移'),
        'f[i][j] = nums1[i] * nums2[j]': '`f[0][0] = {nums1[i]} × {nums2[j]}` = =={f[i][j]}==',
        'f[i][j] = max(f[i][j - 1]': '`i = 0` 只能用 `nums1[0]`：选 `nums2[{j}]` = {nums1[i] * nums2[j]}，或沿用左边 `{f[i][j - 1]}` → =={f[i][j]}==',
        'f[i][j] = max(f[i - 1][j], ': '`j = 0` 只能用 `nums2[0]`：选 `nums1[{i}]` = {nums1[i] * nums2[j]}，或沿用上边 `{f[i - 1][j]}` → =={f[i][j]}==',
        'max(max(f[i - 1][j - 1], 0)': '配对：`max({f[i - 1][j - 1]}, 0) + {nums1[i]}×{nums2[j]}` = {max(f[i - 1][j - 1], 0) + nums1[i] * nums2[j]}；放弃一个：`{f[i][j - 1]}`、`{f[i - 1][j]}` → 取大 =={f[i][j]}==',
        'return f[-1][-1]': '右下角 `f[{m - 1}][{n - 1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='左上角为负就不要了：max(左上, 0) + 当前乘积',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['两数组各选一个==长度相同的非空子序列==，求点积的最大值',
                 '示例：`[2,1,-2,5]` 与 `[3,0,-6]` → `18`',
                 '本视频：`[2,1,-2]` 与 `[3,0,-6]` → `18`'],
        quote='由于题目要求的子序列必须非空，因此这里必须选择nums1[0]以及nums2[0]……若这个值小于0，那么就没必要保留下来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：`nums1` 前 `i` 个与 `nums2` 前 `j` 个的最大点积',
              '第一行、第一列要单独写：只有一个元素时必须选它，不能用 0 当空',
              '一般格子：配对 `max(f[i-1][j-1], 0) + a·b`，或丢掉 `a` / 丢掉 `b`',
              '答案在右下角 `f[-1][-1]`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：边界不能初始化成 0，否则会变成选空序列；这里用分类讨论回避',
                 '易错：左上角为负时要和 0 取最大',
                 '对比灵神：灵神用 `-inf` 边界统一了四种情况，再压成一维',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
