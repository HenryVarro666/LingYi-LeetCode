S1, S2 = 'sea', 'eat'


def _cell(S, r, c, v):
    line = S.get('_line')
    i, j = S.get('i'), S.get('j')
    if line == 13 and i is not None and (r, c) == (i, 0):
        return 'yellow'
    if line == 15 and j is not None and (r, c) == (0, j):
        return 'yellow'
    if line not in (19, 20, 22) or i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if line == 20 and (r, c) == (i - 1, j - 1):
        return 'green'
    if line == 22 and (r, c) in ((i - 1, j), (i, j - 1)):
        return 'blue'
    return None


def _text(S, B):
    line = S.get('_line')
    if line == 22:
        i, j, f = S['i'], S['j'], S['f']
        a = f[i][j - 1] + S['nums2'][j - 1]
        b = f[i - 1][j] + S['nums1'][i - 1]
        return f"删 s2 末尾 `{f[i][j - 1]} + {S['nums2'][j - 1]} = {a}`，删 s1 末尾 `{f[i - 1][j]} + {S['nums1'][i - 1]} = {b}` → 取 =={f[i][j]}=="
    return '`f[i][j]`：s1 前 i 个与 s2 前 j 个字符==匹配的最小代价==（多一行一列表示空串）'


CONFIG = dict(
    num=712, title='两个字符串的最小ASCII删除和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='另类编辑距离 · 二维 DP',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def minimumDeleteSum(self, s1, s2):

        n = len(s1)
        m = len(s2)

        nums1 = [ord(x) for x in s1]
        nums2 = [ord(x) for x in s2]

        f = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            f[i][0] = f[i - 1][0] + nums1[i - 1]
        for j in range(1, m + 1):
            f[0][j] = f[0][j - 1] + nums2[j - 1]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if nums1[i - 1] == nums2[j - 1]:
                    f[i][j] = f[i - 1][j - 1]
                else:
                    f[i][j] = min(f[i][j - 1] + nums2[j - 1], f[i - 1][j] + nums1[i - 1])
        return f[n][m]
''',
    call=f'Solution().minimumDeleteSum({S1!r}, {S2!r})',
    expect=231,
    skip=['for i in range(1, n + 1)', 'for j in range(1, m + 1)', 'n = len(s1)', 'm = len(s2)'],
    views=[
        dict(type='array', var='nums1', label='nums1 = ord(s1)：s · e · a', h=125, cell=80, index=False,
             color=lambda S, k, v: 'blue' if S.get('_line') in (13, 19, 20, 22) and k == S.get('i', 0) - 1 else None),
        dict(type='array', var='nums2', label='nums2 = ord(s2)：e · a · t', h=125, cell=80, index=False,
             color=lambda S, k, v: 'pink' if S.get('_line') in (15, 19, 20, 22) and k == S.get('j', 0) - 1 else None),
        dict(type='text', fn=_text, size=24, h=56),
        dict(type='table', var='f', label='f（黄 = 正在算，绿/蓝 = 来源）', h=400, cell=84,
             rows=['∅'] + list(S1), cols=['∅'] + list(S2), color=_cell),
    ],
    watch=['i', 'j', ('f[i][j]', 'f[i][j]', 'yellow')],
    captions={
        'nums1 = [': '先把字符换成 ASCII 码：`nums1 = {nums1}`',
        'nums2 = [': '`nums2 = {nums2}`',
        'f = [[0] * (m + 1)': '`f[0][0] = 0`：两个串都为空，不用删',
        'f[i][0] = f[i - 1][0]': 's2 为空，s1 前 {i} 个必须全删：`f[{i}][0] = {f[i-1][0]} + {nums1[i-1]} = {f[i][0]}`',
        'f[0][j] = f[0][j - 1]': 's1 为空，s2 前 {j} 个必须全删：`f[0][{j}] = {f[0][j-1]} + {nums2[j-1]} = {f[0][j]}`',
        'if nums1[i - 1] == nums2[j - 1]': lambda S, B, r: (
            f"`s1[{S.i - 1}] = s2[{S.j - 1}] = '{S1[S.i - 1]}'`：最后一个字符能匹配，==无需删去=="
            if S.nums1[S.i - 1] == S.nums2[S.j - 1] else
            f"`'{S1[S.i - 1]}'({S.nums1[S.i - 1]}) ≠ '{S2[S.j - 1]}'({S.nums2[S.j - 1]})`：删去其中一个串的最后一个字符"),
        'f[i][j] = f[i - 1][j - 1]': '`f[{i}][{j}] = f[{i-1}][{j-1}]` = =={f[i][j]}==',
        'f[i][j] = min(': '删 s2 末尾或删 s1 末尾：`min({f[i][j-1]} + {nums2[j-1]}, {f[i-1][j]} + {nums1[i-1]})` = =={f[i][j]}==',
        'return f[n][m]': '`f[{n}][{m}]` = =={ret}==',
    },
    cards=dict(
        one_liner='只有删除的编辑距离：代价不是 1，而是字符的 ASCII 码',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['给两个字符串 `s1`、`s2`，删除一些字符使它们相等',
                 '求被删字符 ==ASCII 值之和==的最小值',
                 f'示例 / 本视频：`"{S1}"`、`"{S2}"` → `231`（115 + 116）'],
        quote='另类的编辑距离问题，不过这里只有删除操作，且==删除的代价不是1而是当前字符的ascii码==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：s1 前 i 个、s2 前 j 个字符匹配的最小代价',
              '一边为空：另一边只能全删，第 0 行 / 第 0 列是前缀 ASCII 和',
              '末尾相同继承左上；不同就删 s1 或 s2 的末尾，取代价小的'],
        summary=['时间 / 空间 `O(nm)`，也可滚动数组降到 `O(m)`',
                 '易错：`f[i][j]` 对应字符是 `s1[i − 1]`、`s2[j − 1]`',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神反过来求「最多保留」，`total − 保留 × 2`'],
    ),
)
