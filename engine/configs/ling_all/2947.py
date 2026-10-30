def _col(S, i, v):
    return 'purple' if v in 'aeiou' else None


CONFIG = dict(
    num=2947, title='统计美丽子字符串 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表 · 质因数化简平方',
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
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s（紫 = 元音 +1，白 = 辅音 −1）', pointers={'i': 'blue'}, color=_col, h=170),
        dict(type='map', var='cnt', label='cnt：(i % k, 前缀和) → 出现次数', fmt=lambda k, v: f"{k}: {v}", h=230, font=30),
        dict(type='text', fn=lambda S: (f"`k'` = =={S['k']}==：子串长度必须是 {S['k']} 的倍数，且元音 − 辅音 = 0；`ans` = =={S['ans']}==" if 'ans' in S and 'cnt' in S else ''), h=80),
    ],
    watch=['k', 'i', 'pre_sum', 'p', ('ans', 'ans', 'green')],
    captions={
        'k = self.sqrt(k * 4)': '`L²` 要被 `4k` 整除 ⇔ `L` 是 `sqrt(4k)`（质因子幂次向上取半）的倍数：新 `k` = =={k}==',
        'cnt = Counter': '哈希表 key 是 `(下标 % k, 前缀和)`；先放 `({k} - 1, 0)`，因为 `k-1` 和 `-1` 同余，代表空前缀',
        'ans = pre_sum = 0': '`pre_sum` 元音记 +1、辅音记 −1；子数组和为 0 ⇔ 元音辅音一样多',
        'pre_sum += 1': lambda S, B, r: (f"`'{S.c}'` 是元音 → `pre_sum` + 1 = =={S.pre_sum}==" if S.c in 'aeiou' else f"`'{S.c}'` 是辅音 → `pre_sum` − 1 = =={S.pre_sum}=="),
        'p = (i % k, pre_sum)': '当前前缀的 key：`(i % k, pre_sum)` = ==`{p}`==',
        'ans += cnt[p]': '之前有 `{cnt[p]}` 个前缀和它 key 相同 → 各自对应一个美丽子串：`ans` = `{B.ans} + {cnt[p]}` = =={ans}==',
        'cnt[p] += 1': '把当前前缀记入哈希表：`cnt[{p}]` = {cnt[p]}',
        'return ans': '美丽子字符串共 ==`{ans}`== 个',
        'res *= i': '质因子 `{i}` 的幂次取一半向上：`res` = {res}',
        'return res': '`sqrt` 结果 ==`{res}`==',
    },
    cards=dict(
        one_liner='平方整除化成倍数，再用前缀和 + 哈希表计数',
        complexity='时间 `O(n + √k)`，空间 `O(n)`',
        problem=['元音数 == 辅音数，且两者乘积能被 `k` 整除的非空子串叫美丽子串，求个数',
                 '示例：`"baeyh"`，`k = 2` → `2`', '本视频：同上，`k` 先化成 `k\'`'],
        quote='把元音视作 1，辅音视作 -1。「元音字母和辅音字母的数量相等」就等价于：找到一个和为 0 的连续子数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度 `L`，两种字母各 `L/2`，乘积条件即 `L² % 4k == 0`',
              '对 `4k` 质因数分解，每个 `p^e` 要求 `L` 含 `p^⌈e/2⌉`，得到 `L` 必须是 `k\'` 的倍数',
              '子数组和为 0 且 `(i−j) % k\' == 0` ⇔ `(i % k\', 前缀和)` 相同，用哈希表计数'],
        summary=['时间 `O(n + √k)`，空间 `O(n)`',
                 '易错：初始放入的是 `(k\'-1, 0)`，对应下标 -1 的空前缀',
                 '`sqrt` 不是开平方，而是「最小的 m 使 n | m²」',
                 '同类：560、974、525 等前缀和 + 哈希表'],
    ),
)
