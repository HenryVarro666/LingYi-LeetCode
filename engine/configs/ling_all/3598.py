def _lcp(a, b):
    c = 0
    for x, y in zip(a, b):
        if x != y:
            break
        c += 1
    return c


CONFIG = dict(
    num=3598, title='相邻字符串之间的最长公共前缀', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='维护前二大 LCP',
    tags=['灵神题单', '动态规划', '难度分 1655'],
    code='''
@cache  # 不加就是 O(1) 空间，但测试发现，加这个更快（可能有些测试数据有很多重复的字符串）
def lcp(s: str, t: str) -> int:
    cnt = 0
    for x, y in zip(s, t):
        if x != y:
            break
        cnt += 1
    return cnt

class Solution:
    def longestCommonPrefix(self, words: List[str]) -> List[int]:
        n = len(words)
        mx1 = mx2 = i1 = -2
        for i in range(n - 1):
            l = lcp(words[i], words[i + 1])
            if l > mx1:
                mx2 = mx1
                mx1, i1 = l, i
            elif l > mx2:
                mx2 = l

        ans = [0] * n
        for i in range(n):
            l = lcp(words[i - 1], words[i + 1]) if 0 < i < n - 1 else 0
            if i != i1 and i != i1 + 1:  # 最大 LCP 没被破坏
                ans[i] = max(mx1, l)
            else:
                ans[i] = max(mx2, l)
        return ans
''',
    call="Solution().longestCommonPrefix(['jump','run','run','jump','run'])",
    expect=[3, 0, 0, 3, 3],
    skip=['cnt = 0', 'for x, y in zip', 'if x != y', 'break', 'cnt += 1', 'n = len(words)', 'ans = [0] * n'],
    views=[
        dict(type='array', var='words', pointers={'i': 'blue'}, h=215, cell=120, label='words（相邻两个之间的 LCP）',
             color=lambda S, k, v: ('yellow' if 'i1' in S and S['i1'] >= 0 and k in (S['i1'], S['i1'] + 1) else None)),
        dict(type='array', var='ans', h=170, cell=120, label='ans[i]：删掉 words[i] 后的答案'),
        dict(type='text', h=100, fn=lambda S: (f"最大 LCP `mx1 = {S['mx1']}`（words[{S['i1']}] 与 words[{S['i1']+1}]，黄色），次大 `mx2 = {S['mx2']}`" if 'mx1' in S and S['mx1'] >= 0 else ('正在统计相邻对的最大和次大 LCP' if 'mx1' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('l', 'l', 'cyan'), ('mx1', 'mx1', 'green'), ('mx2', 'mx2', 'orange'), ('i1', 'i1', 'yellow')],
    captions={
        'return cnt': '`lcp` 返回公共前缀长度 `{cnt}`',
        'mx1 = mx2 = i1': '`mx1` 最大 LCP、`mx2` 次大 LCP、`i1` 是最大 LCP 的左端下标，先都设成 -2',
        'for i in range(n - 1)': lambda S, B, r: f'看相邻对 `(words[{S.i}], words[{S.i+1}])`',
        'l = lcp(words[i], words[i + 1])': lambda S, B, r: f"`{S.words[S.i]}` 和 `{S.words[S.i+1]}` 的公共前缀长度 `l` = =={_lcp(S.words[S.i], S.words[S.i+1])}==",
        'if l > mx1': lambda S, B, r: (f"`l = {S.l} > mx1 = {S.mx1}`：成为新的最大，原来的最大降为次大" if S.l > S.mx1 else f"`l = {S.l}` 没超过最大 `mx1 = {S.mx1}`，再看能不能当次大"),
        'mx2 = mx1': '次大 `mx2` ← 原来的最大 `{mx2}`',
        'mx1, i1 = l, i': '最大 `mx1` = {mx1}，记下位置 `i1 = {i1}`',
        'elif l > mx2': lambda S, B, r: (f"`l = {S.l} > mx2 = {S.mx2}`：成为新的次大" if S.l > S.mx2 else f"`l = {S.l}` 也不超过次大 `mx2 = {S.mx2}`，忽略"),
        'mx2 = l': '次大 `mx2` = {mx2}',
        'for i in range(n):': '枚举要删除的 `words[{i}]`',
        'l = lcp(words[i - 1], words[i + 1])': lambda S, B, r: (f"删掉 `words[{S.i}]` 后，`{S.words[S.i-1]}` 和 `{S.words[S.i+1]}` 变成相邻，新增 LCP `l` = =={_lcp(S.words[S.i-1], S.words[S.i+1])}==" if 0 < S.i < len(S.words) - 1 else "两端的元素删掉后没有新的相邻对，`l = 0`"),
        'if i != i1 and i != i1 + 1': lambda S, B, r: (f"`i = {S.i}` 不在最大 LCP 的两个字符串里 → 最大 LCP 没被破坏" if S.i != S.i1 and S.i != S.i1 + 1 else f"`i = {S.i}` 正是构成最大 LCP 的字符串 → 最大 LCP 被破坏，只能用次大"),
        'ans[i] = max(mx1, l)': '`ans[{i}] = max(mx1, l) = max({mx1}, {l})` = =={ans[i]}==',
        'ans[i] = max(mx2, l)': '`ans[{i}] = max(mx2, l) = max({mx2}, {l})` = =={ans[i]}==',
        'return ans': '全部算完：`{ans}`',
    },
    cards=dict(
        one_liner='删掉一个字符串，只影响它相邻的两对：只需维护最大和次大 LCP',
        complexity='时间 `O(L)`，空间 `O(1)`（不计返回值和缓存）',
        problem=['依次删除 `words[i]`，求删除后所有相邻字符串对的最长公共前缀（LCP）的最大值',
                 '没有相邻对或没有公共前缀时为 `0`',
                 '本视频：`["jump","run","run","jump","run"]` → `[3,0,0,3,3]`'],
        quote='实际上，我们不需要维护第三大 LCP。……所以 i2 也无需维护。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['先遍历所有相邻对，维护最大 `mx1`（及其下标 `i1`）和次大 `mx2`',
              '删 `i` 时：新增 `words[i-1]` 与 `words[i+1]` 的 LCP `l`',
              '最大 LCP 没被破坏取 `max(mx1, l)`；被破坏则取 `max(mx2, l)`',
              '次大一定够用：被破坏时 `l >= mx2`，第三大不会超过它'],
        summary=['时间 `O(L)`，`L` 为字符总长；空间 `O(1)`，`@cache` 只是常数优化',
                 '`i1` 记录的是相邻对的左端，所以被破坏的是 `i1` 和 `i1+1`',
                 '`i = 0` 或 `n-1` 时没有新相邻对，`l` 取 0（Python 的 `words[-1]` 不会真被用到）',
                 '另有方法一：前后缀分解，`pre_max` / `suf_max` 两趟；方法二：维护前三大'],
    ),
)
