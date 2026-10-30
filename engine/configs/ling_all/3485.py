CONFIG = dict(
    num=3485, title='删除元素后 K 个字符串的最长公共前缀', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='排序 + 最大/次大 LCP',
    tags=['难度分 2290'],
    code='''
class Solution:
    # 计算 s 和 t 的最长公共前缀（LCP）长度
    def calc_lcp(self, s: str, t: str) -> int:
        for i, (x, y) in enumerate(zip(s, t)):
            if x != y:
                return i
        return min(len(s), len(t))

    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if k >= n:  # 移除一个字符串后，剩余字符串少于 k 个
            return [0] * n

        idx = list(range(n))
        idx.sort(key=lambda i: words[i])

        # 计算最大 LCP 长度和次大 LCP 长度，同时记录最大 LCP 来自哪里
        mx = mx2 = mx_i = -1
        for i in range(n - k + 1):
            # 排序后，[i, i+k-1] 的 LCP 等于两端点的 LCP
            lcp = self.calc_lcp(words[idx[i]], words[idx[i + k - 1]])
            if lcp > mx:
                mx, mx2, mx_i = lcp, mx, i
            elif lcp > mx2:
                mx2 = lcp

        ans = [mx] * n  # 先初始化成最大 LCP 长度
        # 移除下标在 idx[mx_i:mx_i+k] 中的字符串，会导致最大 LCP 变成次大 LCP
        for i in idx[mx_i: mx_i + k]:
            ans[i] = mx2  # 改成次大 LCP 长度
        return ans
''',
    call='Solution().longestCommonPrefix(["jump","run","run","jump","run"], 2)',
    expect=[3, 4, 4, 3, 4],
    views=[
        dict(type='array', var='words', label='words（原顺序，答案按这个顺序给）', h=150,
             color=lambda S, i, v: 'green' if 'ans' in S and 'idx' in S and 'mx_i' in S and S['mx_i'] >= 0 and i in S['idx'][S['mx_i']:S['mx_i'] + S['k']] else None),
        dict(type='array', var='idx', label='idx（按字符串排序后的下标）', h=170,
             window=(lambda S: S['i'] if 'mx_i' in S and 'ans' not in S and 'i' in S else None,
                     lambda S: S['i'] + S['k'] - 1 if 'mx_i' in S and 'ans' not in S and 'i' in S else None),
             color=lambda S, i, v: 'green' if S.get('mx_i', -1) >= 0 and S['mx_i'] <= i < S['mx_i'] + S['k'] and 'ans' in S else None),
        dict(type='text', fn=lambda S: ('按 idx 读出：' + ' · '.join(S['words'][j] for j in S['idx'])) if 'idx' in S else '', size=30, h=70),
        dict(type='array', var='ans', label='ans', h=150, color=lambda S, i, v: None),
    ],
    skip=[4, 5, 6, 7],
    watch=['k', ('mx', 'mx', 'green'), ('mx2', 'mx2', 'orange'), 'mx_i', 'lcp'],
    captions={
        'if k >= n': '`k = {k}`，`n = {n}`：删一个后还剩 `n-1` 个，不够 `k` 个才全 0 → 本例 `k >= n` 不成立',
        'idx.sort': '不能直接排 words（答案要按原下标）→ ==对下标排序==，字符串相近的会聚在一起',
        'mx = mx2 = mx_i = -1': '最大、次大 LCP 先记成 `-1`',
        'for i in range(n - k + 1)': '枚举排序后每个长为 `k` 的窗口，起点 `i = {i}`',
        21: lambda S, B, r: ('窗口 LCP = 两端点的 LCP（定理 1）：`{}` 与 `{}` → ==LCP 为 {}=='.format(S.words[S.idx[S.i]], S.words[S.idx[S.i + S.k - 1]], S.lcp) if 's' not in S['_inner'] else '算窗口 `[i, i+k-1]` 的 LCP：只比较两端点 `words[idx[i]]` 与 `words[idx[i+k-1]]`（定理 1）'),
        22: lambda S, B, r: (f'`{S.words[S.idx[S.i]]}` 与 `{S.words[S.idx[S.i + S.k - 1]]}` 的 LCP 为 =={S.lcp}==；`{S.lcp} > mx = {S.mx}` → 刷新最大' if S.lcp > S.mx else f'`{S.words[S.idx[S.i]]}` 与 `{S.words[S.idx[S.i + S.k - 1]]}` 的 LCP 为 =={S.lcp}==；`{S.lcp} > mx = {S.mx}` 不成立 → 看次大'),
        'mx, mx2, mx_i = lcp': '新最大 `mx = {mx}`，旧最大退为次大 `mx2 = {mx2}`，记下来源窗口 `mx_i = {mx_i}`',
        24: lambda S, B, r: (f'`lcp = {S.lcp} > mx2 = {S.mx2}` → 成立，更新次大' if S.lcp > S.mx2 else f'`lcp = {S.lcp} > mx2 = {S.mx2}` → 不成立，跳过'),
        'mx2 = lcp': '次大 `mx2` 更新为 `{mx2}`',
        'ans = [mx] * n': '删的字符串不在最大窗口里 → 答案仍是最大 `mx = {mx}`，先全部填 ==mx==',
        'for i in idx[mx_i': '最大窗口是 `idx[{mx_i}:{mx_i + k}]`，删其中任何一个，最大 LCP 都被破坏',
        'ans[i] = mx2': '删掉 `words[{i}]`（在最大窗口内）→ 答案退成次大 LCP =={mx2}==',
        'return ans': '答案 `{ans}`',
        'return [0]': '`k >= n`：直接返回全 0',
        'return i': '第 `{i}` 位不同 → LCP 长度为 `{i}`',
        'return min(': '一个是另一个的前缀 → 取较短长度',
    },
    cards=dict(
        one_liner='排序后窗口 LCP 看两端；删一个，答案只有最大或次大',
        complexity='时间 `O(L log n)`，空间 `O(n)`',
        problem=['给 `words` 和 `k`，对每个 `i`：删去 `words[i]` 后，任选 `k` 个字符串的最长公共前缀长度',
                 '剩下不足 `k` 个时答案为 0',
                 '示例：`["jump","run","run","jump","run"], k=2` → `[3,4,4,3,4]`'],
        quote='有序子数组的 LCP，等于子数组第一个字符串和最后一个字符串的 LCP。',
        quote_src='—— 灵茶山艾府题解（定理 1）',
        idea=['按字符串对下标排序，选 `k` 个就选连续的 `k` 个',
              '枚举所有窗口，求出最大 `mx` 与次大 `mx2`，并记住最大窗口位置',
              '删的字符串不在最大窗口 → `mx`；在里面 → `mx2`（定理 2、3）'],
        summary=['时间 `O(L log n)`（排序是瓶颈），空间 `O(n)`',
                 '不能直接排序 `words`，要排下标，答案才对得上原顺序',
                 '`mx` 和 `mx2` 要同时维护：新最大出现时，旧最大退为次大',
                 '`k >= n` 要单独返回全 0'],
    ),
)
