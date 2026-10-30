def _q(S):
    return S.get('_line', 0) >= 17 and 'r' in S


CONFIG = dict(
    num=3261, title='统计满足 K 约束的子字符串数量 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑窗预处理 right[l] + 前缀和 · 每次询问 O(1)',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2659'],
    code='''
class Solution:
    def countKConstraintSubstrings(self, s: str, k: int, queries: List[List[int]]) -> List[int]:
        n = len(s)
        right = [n] * n
        pre = [0] * (n + 1)
        cnt = [0, 0]
        l = 0
        for i, c in enumerate(s):
            cnt[ord(c) & 1] += 1
            while cnt[0] > k and cnt[1] > k:
                cnt[ord(s[l]) & 1] -= 1
                right[l] = i
                l += 1
            pre[i + 1] = pre[i] + i - l + 1

        ans = []
        for l, r in queries:
            j = min(right[l], r + 1)
            ans.append(pre[r + 1] - pre[j] + (j - l + 1) * (j - l) // 2)
        return ans
''',
    call='Solution().countKConstraintSubstrings("010101", 1, [[0,5],[1,4],[2,3]])',
    expect=[15, 9, 3],
    views=[
        dict(type='string', var='s', label='s（框：滑窗 [l, i]；查询阶段为 [l, r]）', cell=90, h=210,
             pointers={'i': 'blue', 'l': 'pink'},
             window=(lambda S: S.get('l', 0), lambda S: S['r'] if _q(S) else S.get('i', 0))),
        dict(type='array', var='right', label='right[l]：窗口第一次 > l 作为左端点失效时的 i（n = 6 表示一直合法）', cell=90, h=170,
             color=lambda S, i, v: 'yellow' if _q(S) and i == S['l'] else None),
        dict(type='array', var='pre', label='pre[i+1]：以 0..i 为右端点的合法子串个数前缀和', cell=90, h=170,
             color=lambda S, i, v: 'green' if _q(S) and 'j' in S and i in (S['j'], S['r'] + 1) else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"查询 `[{S['l']}, {S['r']}]`：前半段 `[{S['l']}, j-1]` 全合法，后半段用 pre 求和" if _q(S) and 'j' in S
                           else (f"0 的个数 {S['cnt'][0]}，1 的个数 {S['cnt'][1]}，k = {S['k']}" if 'cnt' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('l', 'l', 'pink'), ('cnt', 'cnt', 'cyan'), ('j', 'j', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'right = [n] * n': '`right[l]`：左端点 `l` 在哪个右端点 `i` 时第一次失效（`left[i] > l`）；没失效就一直是 `n`',
        'pre = [0]': '`pre` 存「以 i 为右端点的合法子串个数」的前缀和',
        'cnt = [0, 0]': '`cnt[0]`、`cnt[1]` 分别统计窗口里 0 和 1 的个数',
        'cnt[ord(c) & 1] += 1': '`{c}` 进入窗口：`cnt = {cnt}`',
        'while cnt[0] > k': lambda S, B, r: (f'`cnt = {S.cnt}`，0 和 1 都 `> k = {S.k}` → ==窗口不满足 k 约束==，要缩小'
                                             if S.cnt[0] > S.k and S.cnt[1] > S.k else f'`cnt = {S.cnt}`，至少有一个 `≤ k = {S.k}` → 窗口合法'),
        'cnt[ord(s[l]) & 1] -= 1': '移出左端点 `s[{l}]`：`cnt = {cnt}`',
        'right[l] = i': '移出左端点 `s[{l}]`，`cnt = {cnt}`。左端点 `{l}` 在右端点 `{i}` 时失效 → 记 `right[{l}] = {i}`：右端点 `≥ {i}` 时，以 `{l}` 为左端点的子串不再全合法',
        'pre[i + 1]': '右端点固定为 {i}：合法左端点 `{l}..{i}` 共 `{i} - {l} + 1` = =={i - l + 1}== 个 → `pre[{i + 1}] = {pre[i + 1]}`',
        'for l, r in queries': lambda S, B, r: (f'查询 `[{S.l}, {S.r}]`：要数 `s[{S.l}..{S.r}]` 内的合法子串' if len(S.ans) < len(S.queries) else '查询全部处理完'),
        'j = min': lambda S, B, r: (f'`right[{S.l}] = {S.right[S.l]}`，`j = min({S.right[S.l]}, {S.r + 1})` = =={S.j}==：'
                                    f'右端点在 `[{S.l}, {S.j - 1}]` 的子串全合法，右端点 `≥ j` 的才要看窗口'),
        'ans.append': lambda S, B, r: (f'前半 `(j-l+1)(j-l)/2` = `{(S.j - S.l + 1) * (S.j - S.l) // 2}`（长为 j-l 的区间里所有子串）；'
                                       f'后半 `pre[{S.r + 1}] - pre[{S.j}]` = `{S.pre[S.r + 1] - S.pre[S.j]}` → ==这次答案 {S.ans[-1]}==，ans = {S.ans}'),
        'return ans': '三个查询答案：`{ans}`',
    },
    skip=['l += 1', 'ans = []', 'cnt[ord(s[l]) & 1] -= 1'],
    cards=dict(
        one_liner='一次滑窗预处理 right[l] 与前缀和，每个询问 O(1) 回答',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['二进制串 `s`，满足「0 的个数 ≤ k」或「1 的个数 ≤ k」的子串叫 k 约束子串',
                 '每个查询 `[l, r]`：数 `s[l..r]` 中 k 约束子串的个数',
                 '示例：`s="010101", k=1, queries=[[0,5],[1,4],[2,3]]` → `[15,9,3]`'],
        quote='在滑窗的过程中，如果发现窗口不满足要求，那么在移动左端点 l 之前，可以记录 right[l] = i。',
        quote_src='—— 灵茶山艾府题解 · 方法二写法二',
        idea=['右端点为 `i` 的合法子串有 `i-left[i]+1` 个，`left[i]` 单调不减 → 滑窗求出，并做前缀和 `pre`',
              '查询 `[l, r]`：以 `[l, j-1]` 为右端点的子串全合法，共 `(j-l+1)(j-l)/2` 个',
              '右端点在 `[j, r]` 时直接用 `pre[r+1] - pre[j]`；`j = min(right[l], r+1)` 不用二分'],
        summary=['时间 `O(n+q)`：滑窗 `l` 只增不减，每个询问 `O(1)`',
                 '`cnt[ord(c) & 1]`：用字符的最低位区分 "0"/"1"',
                 '`j` 要和 `r + 1` 取最小，右端点不能超出查询区间',
                 '灵神另给两种写法：方法一用 `bisect_left(left, ...)` 二分，每次询问 `O(log n)`；写法一用双指针单独预处理 `right`'],
    ),
)
