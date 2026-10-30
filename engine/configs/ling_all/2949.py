def _cnt_fmt(k, v):
    return f'(下标%k′={k[0]}, 前缀和={k[1]}) → {v} 次'


def _txt(S):
    if 'pre_sum' not in S:
        return ''
    if 'k' in S and S['_line'] <= 5:
        return f"`4k = 4×{S['K0']} = {S['K0']*4}` → 长度 L 必须是 ==`{S['k']}`== 的倍数"
    return f"元音 +1、辅音 −1，前缀和 `pre_sum = {S['pre_sum']}`；长度是 `{S['k']}` 的倍数 ⇔ 下标模 `{S['k']}` 相同"


CONFIG = dict(
    num=2949, title='统计美丽子字符串 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表 · 平方化为倍数',
    tags=['灵神题单', '常用数据结构', '难度分 2445'],
    setup='K0 = 2',
    code='''
class Solution:
    def beautifulSubstrings(self, s: str, k: int) -> int:
        k = self.sqrt(k * 4)
        cnt = Counter([(k - 1, 0)])  # k-1 和 -1 同余
        ans = pre_sum = 0
        for i, c in enumerate(s):
            pre_sum += 1 if c in "aeiou" else -1
            p = (i % k, pre_sum)
            ans += cnt[p]
            cnt[p] += 1
        return ans

    def sqrt(self, n: int) -> int:
        res = 1
        i = 2
        while i * i <= n:
            i2 = i * i
            while n % i2 == 0:
                res *= i
                n //= i2
            if n % i == 0:
                res *= i
                n //= i
            i += 1
        if n > 1:
            res *= n
        return res
''',
    call='Solution().beautifulSubstrings("baeyh", 2)',
    expect=2,
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=170, label='s（元音 +1，辅音 −1）',
             color=lambda S, i, v: ('green' if v in 'aeiou' else 'pink') if 'pre_sum' in S and i <= S.get('i', -1) else None),
        dict(type='map', var='cnt', fmt=_cnt_fmt, h=300, font=26, label='cnt：(i % k′, 前缀和) 出现次数'),
        dict(type='text', size=26, h=90, fn=_txt),
    ],
    watch=[('k′', 'k', 'cyan'), ('i', 'i', 'blue'), ('pre_sum', 'pre_sum', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'k = self.sqrt': '`4k = {K0*4}`：要 `L² % 4k = 0`，先找 L 必须是谁的倍数 → `k′ = {ret}`（这里 k 已改写为 {k}）',
        'cnt = Counter': '哈希表 key = (`i % k′`, `前缀和`)；先放 `(k′−1, 0)`：空前缀 s[-1]=0，下标 -1 与 k′-1 同余',
        'ans = pre_sum = 0': '`ans` 是美丽子串个数，`pre_sum` 是前缀和',
        'pre_sum +=': lambda S, B, r: f'`{S.c}` 是{"元音 → +1" if S.c in "aeiou" else "辅音 → −1"}，`pre_sum` = {S.pre_sum}',
        'p = (i % k, pre_sum)': 'key `p = ({i % k}, {pre_sum})`：下标模 k′ 相同 ∧ 前缀和相同 ⇒ 中间那段长度是 k′ 的倍数且和为 0',
        'ans += cnt[p]': lambda S, B, r: (f'`cnt[p]` = {S.cnt[S.p] if S.p in S.cnt else 0}：之前有这么多个起点和现在配对 → `ans` = =={S.ans}==' ),
        'cnt[p] += 1': '把当前位置也记入 `cnt[{p}]` = {cnt[p]}，留给后面的右端点',
        'return ans': '美丽子串共 `{ans}` 个',
        'res = 1': '`res` 累乘需要的质因子；`n` 是还没分解的部分',
        'while i * i <= n': lambda S, B, r: (f'`i = {S.i}`：{S.i}² ≤ {S.n} → 继续试除' if S.i * S.i <= S.n else f'`{S.i}² > {S.n}` → 试除结束'),
        'i2 = i * i': '`i² = {i2}`',
        'while n % i2 == 0': lambda S, B, r: (f'`n % {S.i2} == 0`：`{S.i}^2` 能整除 → 一对平方只需 L 含一个 {S.i}' if S.n % S.i2 == 0 else f'`{S.n} % {S.i2} ≠ 0`：没有更多平方因子'),
        'res *= i': '`res *= {i}` → {res}：这一个 {i} 必须在 L 里',
        'n //= i2': '`n //= {i2}` → {n}',
        'if n % i == 0': lambda S, B, r: (f'`{S.n} % {S.i} == 0`：还剩一个 {S.i}（奇数次幂）→ L 也要含 {S.i}（向上取整 ⌈e/2⌉）' if S.n % S.i == 0 else f'`{S.n} % {S.i} ≠ 0`：没有剩余的 {S.i}'),
        'n //= i\n': '`n //= {i}` → {n}',
        'i += 1': '`i` → {i}',
        'if n > 1': lambda S, B, r: (f'`n = {S.n} > 1`：剩下一个大质数，L 必须含它' if S.n > 1 else f'`n = {S.n}`：没有剩余'),
        'res *= n': '`res *= {n}` → {res}',
        'return res': 'L 必须是 `{res}` 的倍数',
    },
    skip=['i2 = i * i'],
    cards=dict(
        one_liner='把「L² 被 4k 整除」化为「L 是 k′ 的倍数」，再用前缀和 + 哈希表计数',
        complexity='时间 `O(n + sqrt(k))`，空间 `O(n)`',
        problem=['字符串 `s` 和正整数 `k`，子串里元音数 = 辅音数，且两者乘积能被 `k` 整除，就是==美丽子串==',
                 '求美丽子串的个数',
                 '示例：`s="baeyh", k=2` → `2`'],
        quote='把元音视作 1，辅音视作 −1。「元音字母和辅音字母的数量相等」就等价于：找到一个和为 0 的连续子数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度 L 偶数，元音辅音各 L/2，乘积条件 ⇔ `L² % (4k) = 0`',
              '对每个质因子 `p^e` 取 `p^⌈e/2⌉`，乘起来得 `k′`：L 必须是 `k′` 的倍数',
              '「和为 0」+「长度是 k′ 的倍数」⇔ 前缀和相等 ∧ 下标模 k′ 相等，用哈希表计数'],
        summary=['时间 `O(n + sqrt(k))`，空间 `O(n)`',
                 '初始放 `(k′−1, 0)` 代表空前缀，下标 −1 与 k′−1 同余',
                 '`sqrt` 函数：偶数次幂取一半，奇数次幂向上取整',
                 '相似思路：974、523、525、1915 等「前缀和 + 哈希表」题'],
    ),
)
