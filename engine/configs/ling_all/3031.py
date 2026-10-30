def _top(S):
    if 'z' not in S or 'i' not in S:
        return '`z[i]` = 后缀 `s[i:]` 与 `s` 的最长公共前缀（LCP）长度'
    s, k, n, i = S['s'], S['k'], S['n'], S['i']
    zi = S['z'][i]
    if i % k == 0:
        ok = zi >= n - i
        return f"`i = {i}` 是 k 的倍数：后缀 `{s[i:]}` 的 LCP = {zi}，需要 ≥ {n - i} → {'==满足==' if ok else '不满足'}"
    return f"`i = {i}`：后缀 `{s[i:]}` 与 `{s}` 的 LCP 已算出 `z[{i}] = {zi}`（不是 k 的倍数，不用判断）"


def _box(S, B, ret):
    l, r = S.l, S.r
    return f'已知 z-box：`s[{l}..{r}]` 等于 `s` 的前缀 `s[0..{r - l}]`'


CONFIG = dict(
    num=3031, title='将单词恢复初始状态所需的最短时间 II', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='Z 函数（扩展 KMP）',
    tags=['灵神题单', '字符串', '难度分 2278'],
    code='''
class Solution:
    def minimumTimeToInitialState(self, s: str, k: int) -> int:
        n = len(s)
        z = [0] * n
        l = r = 0
        for i in range(1, n):
            if i <= r:
                z[i] = min(z[i - l], r - i + 1)
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
            if i % k == 0 and z[i] >= n - i:
                return i // k
        return (n - 1) // k + 1
''',
    call='Solution().minimumTimeToInitialState("abababab", 3)',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', label='s（蓝框 = z-box，指针 i = 当前后缀起点）', pointers={'i': 'blue'}, window=('l', 'r'), h=210,
             color=lambda S, idx, v: ('green' if (S.get('i') is not None and S['i'] <= idx < S['i'] + S['z'][S['i']]) else None) if 'z' in S and 'i' in S else None),
        dict(type='array', var='z', label='z 数组', pointers={'i': 'blue'}, h=200,
             color=lambda S, idx, v: 'green' if S.get('i') == idx and 'i' in S else None),
    ],
    watch=[('i', 'i', 'blue'), ('l', 'l', 'cyan'), ('r', 'r', 'cyan'), ('k', 'k'), ('n - i', 'n - i', 'orange')],
    captions={
        'z = [0] * n': '`z[i]`：后缀 `s[i:]` 与 `s` 的最长公共前缀长度；`z[0]` 不用算，先全填 0',
        'l = r = 0': '`[l, r]` 是目前向右==扩得最远==的 z-box：`s[l..r]` 等于 `s` 的前缀',
        'for i in range': '算下一个后缀 `s[{i}:]` 的 `z[{i}]`',
        'if i <= r': lambda S, B, ret: (f'`i = {S.i} ≤ r = {S.r}`：`i` 落在 z-box 里 → ==可以借用以前的结果==' if S.i <= S.r
                                        else f'`i = {S.i} > r = {S.r}`：在 z-box 外面，没有现成信息，只能从 0 开始暴力比'),
        'z[i] = min': '`s[i..r]` 等于 `s[i-l..r-l]`，所以 `z[i]` 至少是 `min(z[i-l], r-i+1)` = =={z[i]}==（不能超过 z-box 右端）',
        'while i + z[i] < n': lambda S, B, ret: (f"比 `s[{S.z[S.i]}] = '{S.s[S.z[S.i]]}'` 和 `s[{S.i + S.z[S.i]}] = '{S.s[S.i + S.z[S.i]]}'` → ==相等==，继续往右扩"
                                                 if S.i + S.z[S.i] < S.n and S.s[S.z[S.i]] == S.s[S.i + S.z[S.i]]
                                                 else (f'`i + z[i] = {S.i + S.z[S.i]}` 到头了，不再扩' if S.i + S.z[S.i] >= S.n
                                                       else f"比 `s[{S.z[S.i]}] = '{S.s[S.z[S.i]]}'` 和 `s[{S.i + S.z[S.i]}] = '{S.s[S.i + S.z[S.i]]}'` → ==不等==，停止，`z[{S.i}] = {S.z[S.i]}`")),
        'l, r = i, i + z[i]': '匹配到了更靠右的位置 → 更新 z-box：`l = {l}`，`r = {r}`',
        'z[i] += 1': '多匹配一个字符，`z[{i}]` = =={z[i]}==',
        'if i % k == 0': lambda S, B, ret: (f'`i = {S.i}` 是 k 的倍数，操作 {S.i // S.k} 次后剩下的是 `s[{S.i}:]`；它是 `s` 的前缀 ⇔ `z[{S.i}] = {S.z[S.i]} ≥ n - i = {S.n - S.i}` → '
                                            + ('==成立=='  if S.z[S.i] >= S.n - S.i else '不成立')
                                            if S.i % S.k == 0 else f'`i = {S.i}` 不是 k 的倍数，每秒只删 k 个，不可能停在这里 → 跳过'),
        'return i // k': '后缀能接成 `s` 的前缀，末尾补任意字符即可还原 → 答案 `i // k` = =={ret}==',
        'return (n - 1) // k + 1': '所有 `s[xk:]` 都不是前缀 → 全部删光重建，需要 `ceil(n / k)` = =={ret}== 次',
    },
    cards=dict(
        one_liner='操作 x 次后剩下后缀 s[xk:]，它是 s 的前缀就能还原',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每秒删掉 `word` 的前 `k` 个字符，再在末尾补任意 `k` 个字符',
                 '求最少几秒（> 0）能让 `word` 变回初始状态',
                 '示例：`word = "abacaba"`，`k = 3` → `2`；本视频用 `"abababab"`，`k = 3` → `2`'],
        quote='只要 s[k:] 是 s 的前缀，就能让 s 恢复成其初始值。……我们通过计算 s 后缀与 s 的 LCP 长度，即 Z 函数（扩展 KMP）来判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['末尾能补任意字符：剩下的后缀只要是 `s` 的前缀，后面照原样补回去就行',
              '依次检查 `s[k:]`、`s[2k:]`、…：`z[i] ≥ n - i` 就说明后缀是前缀',
              '都不行就删光重来：`ceil(n/k)` 次；Z 函数借用 z-box 做到线性'],
        result='`i = 6`：后缀 `ab` 就是前缀 → 6 // 3 = 2 秒 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；`n` 最大 10^6，不能每个 i 暴力比较',
                 '易错：只在 `i % k == 0` 时判断，但 z 必须每个 `i` 都算',
                 '易错：兜底答案是 `(n - 1) // k + 1`，即向上取整，不是 `n // k`',
                 '同类题：2223 构造字符串的总得分和（Z 函数）'],
    ),
)
