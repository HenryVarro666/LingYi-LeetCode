A = [0, 1]
B_ = [1, 0]


def _live(S):
    return 'i' in S and 'j' in S and S.get('_line', 0) >= 11


def _deps(S):
    i, j = S['i'], S['j']
    if i == 0:
        return [(0, j - 1)]
    if j == 0:
        return [(i - 1, 0)]
    return [(i - 1, j), (i, j - 1)]


def _cell(S, r, c, v):
    if not _live(S):
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if S['_line'] >= 12 and (r, c) in _deps(S) and r >= 0 and c >= 0:
        return 'blue'
    return None


def _fml(S):
    if not _live(S):
        return '`f[i][j]` = nums1 填前 i 个、nums2 填前 j 个后，两数组最大值的最小值'
    i, j = S['i'], S['j']
    if (i, j) == (0, 0):
        return '`f[0][0] = 0`：一个数都没填'
    if i == 0 or j == 0:
        return f'`f[{i}][{j}]`：只有一个数组在填，==贪心==往上推：能 +1 就 +1，奇偶不对 +2'
    return f'`f[{i}][{j}]` = 最后一个数落在 nums1（来自 `f[{i - 1}][{j}]`）或 nums2（来自 `f[{i}][{j - 1}]`）的较小者'


CONFIG = dict(
    num=3269, title='构建两个递增数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 分两个数组的前缀',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minLargest(self, nums1, nums2):

        m = len(nums1)
        n = len(nums2)

        f = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        continue
                    elif j == 1:
                        if nums2[0] == 0:
                            f[i][j] = 2
                        else:
                            f[i][j] = 1
                    elif nums2[j - 2] == nums2[j - 1]:
                        f[i][j] = f[i][j - 1] + 2
                    else:
                        f[i][j] = f[i][j - 1] + 1

                elif j == 0:
                    if i == 1:
                        if nums1[0] == 0:
                            f[i][j] = 2
                        else:
                            f[i][j] = 1
                    elif nums1[i - 2] == nums1[i - 1]:
                        f[i][j] = f[i - 1][j] + 2
                    else:
                        f[i][j] = f[i - 1][j] + 1

                else:
                    if (nums1[i - 1] + f[i - 1][j]) % 2 == 0:
                        f[i][j] = f[i - 1][j] + 2
                    else:
                        f[i][j] = f[i - 1][j] + 1

                    if (nums2[j - 1] + f[i][j - 1]) % 2 == 0:
                        f[i][j] = min(f[i][j], f[i][j - 1] + 2)
                    else:
                        f[i][j] = min(f[i][j], f[i][j - 1] + 1)

        return f[-1][-1]
''',
    call=f'Solution().minLargest({A}, {B_})',
    expect=4,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='array', var='nums1', label='nums1（0 = 要填偶数，1 = 要填奇数；绿 = 已填，黄 = 刚填的）', h=150, cell=80,
             color=lambda S, k, v: (None if 'i' not in S else 'yellow' if k == S['i'] - 1 else 'green' if k < S['i'] else None)),
        dict(type='array', var='nums2', label='nums2', h=150, cell=80,
             color=lambda S, k, v: (None if 'j' not in S else 'yellow' if k == S['j'] - 1 else 'green' if k < S['j'] else None)),
        dict(type='table', var='f', label='f[i][j]（行 = nums1 填的个数 i，列 = nums2 填的个数 j）', h=300, cell=100,
             rows=lambda S: ['i=0'] + [f'i={k + 1}' for k in range(len(A))], cols=lambda S: ['j=0'] + [f'j={k + 1}' for k in range(len(B_))],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'm = len': '`m = {m}`',
        'n = len': '`n = {n}`',
        'f = [[0]': '`f[i][j]`：nums1 填前 `i` 个、nums2 填前 `j` 个后，==最大值的最小值==',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行：nums1 填前 `{S.i}` 个' if S.get('i') is not None and S.i != B.get('i') else '整张表填完，右下角就是答案'),
        11: lambda S, B, r: f'第 `{S.i}` 行第 `{S.j}` 列：nums1 填前 {S.i} 个、nums2 填前 {S.j} 个。' + ('`i == 0`：只剩 nums2 在填' if S.i == 0 else '`i ≠ 0`，往下看 j'),
        12: lambda S, B, r: ('`j == 0`：两个数组都没填，`f[0][0] = 0`，跳过' if S.j == 0 else '`j ≠ 0`，继续判断'),
        14: lambda S, B, r: ('`j == 1`：填 nums2 的第一个数' if S.j == 1 else '`j > 1`：看前后两个数的类型'),
        15: '第一个数：`nums2[0] = {nums2[0]}`。要填偶数最小是 2，奇数最小是 1',
        16: '`f[{i}][{j}] = 2`：最小的偶数',
        18: '`f[{i}][{j}] = 1`：最小的奇数',
        19: lambda S, B, r: (f'`nums2[{S.j - 2}] = nums2[{S.j - 1}] = {S.nums2[S.j - 1]}`：同奇偶 → 中间隔了一个数，`+2`' if S.nums2[S.j - 2] == S.nums2[S.j - 1] else f'`nums2[{S.j - 2}] = {S.nums2[S.j - 2]} ≠ nums2[{S.j - 1}] = {S.nums2[S.j - 1]}`：奇偶不同 → 直接 `+1`'),
        20: '`f[{i}][{j}] = f[{i}][{j-1}] + 2` = =={f[i][j]}==',
        22: '`f[{i}][{j}] = f[{i}][{j-1}] + 1` = =={f[i][j]}==',
        24: lambda S, B, r: ('`j == 0`：只剩 nums1 在填' if S.j == 0 else '`j ≠ 0`：两个数组都在填'),
        25: lambda S, B, r: ('`i == 1`：填 nums1 的第一个数' if S.i == 1 else '`i > 1`：看前后两个数的类型'),
        26: '第一个数：`nums1[0] = {nums1[0]}`。要填偶数最小是 2，奇数最小是 1',
        27: '`f[{i}][{j}] = 2`：最小的偶数',
        29: '`f[{i}][{j}] = 1`：最小的奇数',
        30: lambda S, B, r: (f'`nums1[{S.i - 2}] = nums1[{S.i - 1}] = {S.nums1[S.i - 1]}`：同奇偶 → 隔一个数，`+2`' if S.nums1[S.i - 2] == S.nums1[S.i - 1] else f'`nums1[{S.i - 2}] ≠ nums1[{S.i - 1}]`：奇偶不同 → `+1`'),
        31: '`f[{i}][{j}] = f[{i-1}][{j}] + 2` = =={f[i][j]}==',
        33: '`f[{i}][{j}] = f[{i-1}][{j}] + 1` = =={f[i][j]}==',
        35: '两个数组都在填：最大值要么落在 nums1（接在 `f[i-1][j]` 后），要么落在 nums2（接在 `f[i][j-1]` 后），取小',
        36: lambda S, B, r: (f'来自上方：`nums1[{S.i - 1}] + f[{S.i - 1}][{S.j}] = {S.nums1[S.i - 1]} + {S.f[S.i - 1][S.j]}` 是偶数 → 需要的奇偶和当前最大值同类 → `+2`' if (S.nums1[S.i - 1] + S.f[S.i - 1][S.j]) % 2 == 0
                            else f'来自上方：`{S.nums1[S.i - 1]} + {S.f[S.i - 1][S.j]}` 是奇数 → 奇偶相反，下一个数 `+1` 就行'),
        37: '`f[{i}][{j}] = f[{i-1}][{j}] + 2` = =={f[i][j]}==',
        39: '`f[{i}][{j}] = f[{i-1}][{j}] + 1` = =={f[i][j]}==',
        41: lambda S, B, r: (f'来自左方：`nums2[{S.j - 1}] + f[{S.i}][{S.j - 1}] = {S.nums2[S.j - 1]} + {S.f[S.i][S.j - 1]}` 是偶数 → `+2`' if (S.nums2[S.j - 1] + S.f[S.i][S.j - 1]) % 2 == 0
                            else f'来自左方：`{S.nums2[S.j - 1]} + {S.f[S.i][S.j - 1]}` 是奇数 → `+1`'),
        42: '与上方比较取小：`f[{i}][{j}] = min({B.f[i][j]}, {f[i][j-1]} + 2)` = =={f[i][j]}==',
        44: '与上方比较取小：`f[{i}][{j}] = min({B.f[i][j]}, {f[i][j-1]} + 1)` = =={f[i][j]}==',
        46: '右下角 `f[m][n]`：两个数组都填完，最大值的最小值 = =={ret}==',
    },
    cards=dict(
        one_liner='贪心合并不了，那就 DP：f[i][j] = 两边各填前 i、前 j 个的最优',
        complexity='时间 `O(m·n)`，空间 `O(m·n)`',
        problem=['`nums1`、`nums2` 只含 0 和 1：0 要换成偶数，1 要换成奇数',
                 '两个数组都要严格递增，且每个数字最多用一次（两数组间不能重复）',
                 '求替换后两个数组中==最大元素的最小值==',
                 f'示例：`nums1 = {A}`，`nums2 = {B_}` → `4`'],
        quote='到了这里，感觉就没有比较直观的贪心思路了，只能转而去想能否使用动态规划。……令f[i][j]表示填充nums1的前i个数以及nums2的前j个数后，数组中最大值最小可以是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试了贪心：各自算下限再合并，遇到相同的数选谁都有反例',
              '改用 DP：`f[i][j]` 表示 nums1 填前 `i` 个、nums2 填前 `j` 个后的最大值最小',
              '最后一个数落在哪边就从哪边转移：`f[i-1][j]` 或 `f[i][j-1]`，再按奇偶 `+1` 或 `+2`，取小'],
        summary=['时间、空间都是 `O(m·n)`',
                 '易错：第 0 行、第 0 列没有「另一边」，要单独初始化（第一个数 2 或 1）',
                 '转移的 `+2` / `+1` 取决于==要填的奇偶==和当前最大值的奇偶是否一致',
                 '原文已是 Python 3 可运行的写法，仅把全空白行清成空行'],
    ),
)
