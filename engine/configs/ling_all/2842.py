def _freq(S):
    f = {}
    for ch in S['s']:
        f[ch] = f.get(ch, 0) + 1
    return '各字母出现次数：' + '　'.join(f'`{ch}`×{v}' for ch, v in sorted(f.items()))


def _col(S, i, v):
    f = S['s'].count(v)
    return {1: 'blue', 2: 'green', 3: 'orange'}.get(f, 'purple')


def _txt(S):
    if 'ans' not in S:
        return '按「次数」分组：次数相同的字母互相等价'
    k = S['k']
    return f"还要选 `k = {k}` 种字母　当前方案数 `ans` = =={S['ans']}=="


CONFIG = dict(
    num=2842, title='统计一个字符串的 k 子序列美丽值最大的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='贪心 · 组合计数',
    tags=['灵神题单', '数学算法', '难度分 2092'],
    code='''
class Solution:
    def countKSubsequencesWithMaxBeauty(self, s: str, k: int) -> int:
        MOD = 10 ** 9 + 7
        ans = 1
        cnt = Counter(Counter(s).values())
        for c, num in sorted(cnt.items(), reverse=True):
            if num >= k:
                return ans * pow(c, k, MOD) * comb(num, k) % MOD
            ans *= pow(c, num, MOD)
            k -= num
        return 0  # k 太大，无法选 k 个不一样的字符
''',
    call='Solution().countKSubsequencesWithMaxBeauty("abbcccdd", 3)',
    expect=12,
    views=[
        dict(type='string', var='s', label='s（蓝 = 出现 1 次，绿 = 2 次，橙 = 3 次）', cell=90, h=170, color=_col),
        dict(type='text', h=80, size=28, fn=_freq),
        dict(type='map', var='cnt', label='cnt：出现次数 → 有几种字母', fmt=lambda k, v: f'出现 {k} 次: {v} 种', h=150, font=30),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('k', 'k', 'blue'), ('c', 'c', 'orange'), ('num', 'num', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '乘法原理：各步方案数相乘，`ans` 从 1 开始',
        'cnt = Counter(Counter(s).values())': lambda S, B, r: '先数每个字母出现几次，再数「出现次数」的个数：`cnt = {}`（次数 → 有几种字母）'.format(dict(S.cnt)),
        'for c, num in sorted': lambda S, B, r: (f'从出现次数最多的开始贪心：次数 `c = {S.c}` 的字母有 `num = {S.num}` 种，还要选 `k = {S.k}` 种'
                                                if 'c' in S and not (B.get('c') == S.c and B.get('_line') == 10) else '没有更小的次数了'),
        'if num >= k': lambda S, B, r: (f'`num = {S.num} >= k = {S.k}`：这 {S.num} 种字母里挑 {S.k} 种就够了，次数最多的先挑完' if S.num >= S.k
                                       else f'`num = {S.num} < k = {S.k}`：这 {S.num} 种字母必须==全选=='),
        'return ans * pow': '每种选中的字母有 `{c}` 个位置可选 → `{c}^{k}`；从 `{num}` 种里选 `{k}` 种 → `C({num}, {k})`。返回 =={ret}==',
        'ans *= pow': '全选：每种字母有 `{c}` 种选法，共 `{num}` 种 → 乘 `{c}^{num}`，`ans = {ans}`',
        'k -= num': '已选了 `{num}` 种，还差 `k = {k}` 种',
        'return 0': '次数全用完还凑不够 `k` 种 → 没有合法子序列，返回 0',
    },
    max_steps=60,
    cards=dict(
        one_liner='次数大的字母先选；次数相同的字母，统一用组合数',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['`k` 子序列：长为 `k`、字符互不相同的子序列；美丽值 = 每个字符在 `s` 中的出现次数之和',
                 '求美丽值最大的 `k` 子序列有多少个（对 `10^9+7` 取模），下标不同就算不同',
                 '示例：`s = "bcca", k = 2` → `4`'],
        quote='统计每个字符出现次数的个数，然后从大到小遍历次数 c 及其个数 num。如果 num<k，那么这 c 种字符每种选一个，方案数为 c^num；如果 num≥k，方案数为 c^k · C(num, k)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['要美丽值最大，就==优先选出现次数大的字母==',
              '次数相同的字母地位相同：不够 k 种就全选，够了就从中挑 k 种',
              '每个选中的字母有 `c` 个位置可选 → 乘 `c`',
              '本视频：`abbcccdd`, `k=3`：`c` 全选 ×3，`b、d` 里选 2 种 `C(2,2)×2^2` → `12`'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '`k` 太大（种类不够）要返回 0，别漏掉最后的 `return 0`',
                 '`comb` 需要 Python 3.8+；LeetCode 上 `pow(c, k, MOD)` 即快速幂',
                 '注意 `ans *= pow(...)` 这一行没有取模，最终返回时才取模（Python 大整数不会溢出）'],
    ),
)
