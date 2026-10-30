SRC = 'abba'
PAT = 'aba'
TGT = [1, 2]
E = "j if _line in (21, 22, 23, 24) else None"


def _info(S):
    i = S.get('i')
    if i is None:
        return '`f[j]`：source 的前 i 个字符里能选出 pattern 前 j 个字符时，最多删几个；`None` = 做不到'
    line = S.get('_line')
    if line in (22, 23, 24) and S.get('j') is not None:
        j = S['j']
        if j == 0:
            return '`j = 0`：没有 `pattern[j-1]` 可匹配，只能靠上面的「删除」'
        a, b = S['source'][i - 1], S['pattern'][j - 1]
        return f"`source[{i-1}] = {a}`，`pattern[{j-1}] = {b}` → " + ('==相等：可尝试匹配==' if a == b else '不相等：不能匹配')
    return f"处理 `source` 的第 {i} 个字符 `source[{i-1}] = {S['source'][i-1]}`"


CONFIG = dict(
    num=3316, title='从原字符串里进行删除操作的最多次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维 DP 压成一维（j 倒序）+ None 表示不可行',
    tags=['灵神题单', 'LCS 进阶', '难度分 2062'],
    code='''
class Solution(object):
    def maxRemovals(self, source, pattern, targetIndices):

        n = len(source)
        m = len(pattern)

        f = [None] * (m + 1)
        p = 0
        f[0] = 0
        for i in range(1, n + 1):
            while p < len(targetIndices) and targetIndices[p] < i - 1:
                p += 1
            
            if p < len(targetIndices) and targetIndices[p] == i - 1:
                delta = 1
            else:
                delta = 0

            for j in range(m, -1, -1):
                if f[j] is not None:
                    f[j] = f[j] + delta
                if j > 0 and source[i - 1] == pattern[j - 1] and f[j - 1] is not None:
                    if f[j] is None or f[j] < f[j - 1]:
                        f[j] = f[j - 1]

        return f[m]
''',
    call=f'Solution().maxRemovals({SRC!r}, {PAT!r}, {TGT!r})',
    expect=1,
    skip=['while p', 'p += 1', 'delta = 1', 'if f[j] is not None', 'n = len', 'm = len', 'p = 0', 'f[0] = 0', 'for j in range', 'else:', 'delta = 0', 'if f[j] is None or'],
    max_steps=80,
    views=[
        dict(type='string', var='source', label='source（蓝 = 当前字符；橙 = 在 targetIndices 里）', h=130, cell=70,
             color=lambda S, k, v: 'blue' if k == S.get('i', 0) - 1 else ('orange' if k in S['targetIndices'] else None)),
        dict(type='string', var='pattern', label='pattern（粉 = 尝试匹配的 pattern[j-1]）', h=160, cell=70,
             pointers={"j - 1 if _line in (22, 23, 24) and j > 0 else None": 'pink'},
             pointer_labels={"j - 1 if _line in (22, 23, 24) and j > 0 else None": 'j-1'},
             color=lambda S, k, v: 'pink' if S.get('_line') in (22, 23, 24) and S.get('j') and k == S['j'] - 1 else None),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='array', var='f', label='f[j]：前 i 个字符里选出 pattern[:j] 时最多删几个（None = 做不到）', h=210, cell=100,
             pointers={E: 'pink'}, pointer_labels={E: 'j'}, index=True,
             color=lambda S, k, v: 'yellow' if S.get('j') is not None and S.get('_line') in (21, 22, 23, 24) and k == S['j'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'orange'), ('delta', 'delta', 'orange'), ('j', 'j', 'pink'), ('f[m]', 'f[-1]', 'green')],
    captions={
        'f = [None]': '`f[j]` 先全是 `None`（暂时没有可行方案）；`f[0] = 0`：空串匹配空序列，删 0 个',
        'for i in range(1': '处理 `source` 的前 `{i}` 个字符：新来的是 `source[{i-1}]`',
        'while p < len': '`targetIndices` 有序：指针 `p` 跳过已经小于 `i-1` 的下标 → `p = {p}`',
        'if p < len(targetIndices) and targetIndices[p] == i - 1': '`targetIndices` 有序，指针 `p` 只往右走：`source[{i-1}]` {"在" if p < len(targetIndices) and targetIndices[p] == i - 1 else "不在"}里 → `delta = {1 if p < len(targetIndices) and targetIndices[p] == i - 1 else 0}`（能删才 +1）',
        'f[j] = f[j] + delta': '情况一：删掉 `source[{i-1}]`（它不参与匹配）：`f[{j}] = f[{j}] + {delta}` = {f[j]}',
        'if j > 0 and source': lambda S, B, r: (f'`j = 0`：没有 `pattern` 字符可匹配，跳过' if S.j == 0 else
                                                 (f'`source[{S.i-1}] = {S.source[S.i-1]}` 等于 `pattern[{S.j-1}]`，且 `f[{S.j-1}] = {S.f[S.j-1]}` 可行 → 可以匹配'
                                                  if S.source[S.i-1] == S.pattern[S.j-1] and S.f[S.j-1] is not None
                                                  else f'`source[{S.i-1}]` 与 `pattern[{S.j-1}]` 不能匹配（字符不同或 `f[{S.j-1}]` 不可行）')),
        'f[j] = f[j - 1]': '情况二：匹配更优（`f[{j}]` 原来不可行或更小）→ `f[{j}] = f[{j-1}]` = =={f[j]}==',
        'return f[m]': '`f[{m}]` = pattern 整体保留时最多删的个数 = =={ret}==',
    },
    cards=dict(
        one_liner='每个字符：删掉(能删就+1) 或 拿去匹配 pattern，取最优',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['`pattern` 是 `source` 的子序列，`targetIndices` 是有序的可删下标',
                 '删一个下标在 `targetIndices` 里的字符，删后 `pattern` 仍是子序列；删除不改变下标',
                 '求最多删几次；示例：`"abbaa", "aba", [0,1,2]` → `1`；视频里用 `"abba", "aba", [1,2]`'],
        quote='令f[i][j]表示source的前i个字符，在满足可以从中选出子序列构成pattern的前j个字符的前提下最多可以删除的字符数量。',
        quote_src='—— yiduobo 题解',
        idea=['没想到好的贪心，数据规模适合 `O(n^2)` → 往动态规划靠',
              '无论 `j` 是多少，都可以删掉 `source` 的第 i 个字符：`f[i-1][j] + delta`，`delta` 看下标是否在 `targetIndices` 里',
              '`source[i-1] == pattern[j-1]` 时还可以匹配，用 `f[i-1][j-1]` 更新',
              '`f` 每轮只依赖上一轮，倒序遍历 `j` 省掉 `i` 这一维；不可行用 `None` 表示'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：不可行状态是 `None` 不是 0，更新前要判空',
                 '易错：`j` 倒序，否则 `f[j-1]` 已经是新值',
                 '`targetIndices` 有序，所以用指针 `p` 代替集合'],
    ),
)
