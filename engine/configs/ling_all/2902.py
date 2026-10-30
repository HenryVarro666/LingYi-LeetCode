def _cap_fwd(S, B, ret):
    j, x, c = S.j, S.x, S.c
    return f'同余前缀和：`f[{j}] += f[{j - x}]` → `{S.f[j]}`（把间隔 `{x}` 的前面所有项都累加进来）'


def _cap_sub(S, B, ret):
    j, t = S.j, S.t
    return f'减掉多出来的：`f[{j}] -= f[{j - t}]`（间隔 `{t}` = (c+1)·x 的那一项选了 {S.c + 1} 个，超限）→ `{S.f[j]}`'


CONFIG = dict(
    num=2902, title='和带限制的子多重集合的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多重背包 · 同余前缀和优化',
    tags=['灵神题单', '动态规划', '难度分 2759'],
    code='''
class Solution:
    def countSubMultisets(self, nums: List[int], l: int, r: int) -> int:
        MOD = 10 ** 9 + 7
        total = sum(nums)
        if l > total:
            return 0

        r = min(r, total)
        cnt = Counter(nums)
        f = [cnt[0] + 1] + [0] * r
        del cnt[0]

        s = 0
        for x, c in cnt.items():
            s = min(s + x * c, r)
            for j in range(x, s + 1):
                f[j] = (f[j] + f[j - x]) % MOD  # 原地计算同余前缀和
            t = (c + 1) * x
            for j in range(s, t - 1, -1):
                f[j] = (f[j] - f[j - t]) % MOD  # 两个同余前缀和的差
        return sum(f[l:]) % MOD
''',
    call='Solution().countSubMultisets([0,2,1,1], 2, 4)',
    expect=8,
    views=[
        dict(type='map', var='cnt', label='cnt：每种数的个数', h=150, fmt=lambda k, v: f'{k}×{v}'),
        dict(type='array', var='f', label='f[j]：元素和恰好为 j 的方案数', h=250, cell=70, pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if S.get('l') is not None and S.get('_line') == 21 and i >= S['l'] else None),
        dict(type='text', fn=lambda S: (f"当前种类 `x = {S['x']}`，最多 `c = {S['c']}` 个" if 'x' in S and 'c' in S else '多重背包：同一种数选 0..c 个，不区分相同的数'), size=26, h=60),
    ],
    watch=['x', 'c', 's', 't', 'j', 'l', 'r'],
    captions={
        'total = sum': '数组总和 `{total}`，凑不出比它更大的和',
        'if l > total': '`l = {l}` > 总和 `{total}`？不成立 → 继续；否则一定凑不出，直接返回 0',
        'r = min': '和不会超过 `total`，把上界 `r` 压到 `{r}`',
        'cnt = Counter': '先数每个数出现几次：`{cnt}`',
        'f = [cnt[0]': '`f[0] = cnt[0] + 1 = {f[0]}`：0 可以放 0..cnt[0] 个，和不变，所以方案数乘进去',
        'del cnt[0]': '0 已经处理完，以后只枚举正数',
        's = min': '到目前为止最多凑出 `{s}`，循环只需到 `s`',
        'f[j] = (f[j] + f[j - x])': _cap_fwd,
        16: lambda S, B, r: f'`j` 正序 {S.x}..{S.s}：`f[j-x]` 已含新值，一路累加成同余前缀和',
        19: lambda S, B, r: (f'`j` 倒序 {S.s}..{S.t}：只有 `j ≥ t = {S.t}` 才有超限的项要减' if S.t <= S.s else f'`t = {S.t} > s = {S.s}`：没有超限的项，不用减'),
        't = (c + 1)': '`t = (c+1)·x = {t}`：选 `c+1` 个 `{x}` 是不允许的，要把这部分减掉',
        'f[j] = (f[j] - f[j - t])': _cap_sub,
        'return sum': '和在 `[{l}, {r}]` 的方案数相加 = ==`{sum(f[l:]) % MOD}`==',
    },
    cards=dict(
        one_liner='相同数字不区分 = 多重背包，用同余前缀和做到 O(1) 转移',
        complexity='时间 `O(S·min(√S, n))`，空间 `O(S)`',
        problem=['`nums` 的子多重集合：每个值 `x` 可选 `0..occ[x]` 个，无序', '求元素和在 `[l, r]` 的子多重集合个数，答案对 `10^9+7` 取模',
                 '示例：`[1,2,2,3], l=6, r=6` → `1`；视频用 `[0,2,1,1], l=2, r=4`'],
        quote='如果区分相同数字，就是 0-1 背包。如果不区分相同数字，就是多重背包。……如果求出 f[i-1] 的同余前缀和，那么 f[i][j] 就可以转换成两个同余前缀和的差了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` = 前 `i` 种数选出和为 `j` 的方案数，要枚举选 `0..c` 个', '先原地算同余前缀和 `s[p] = f[p] + s[p-x]`',
              '再减去多出来的一段：`f[j] - f[j-(c+1)x]`，两步都是 `O(1)`'],
        summary=['时间 `O(S·min(√S,n))`：不同的数至多约 `√(2S)` 种',
                 '易错：0 要单独处理，初始 `f[0] = cnt[0] + 1`；减法后要 `% MOD` 保持非负',
                 '第二个循环 `j` 必须倒序，用的是原来的同余前缀和',
                 '灵神还给了「式子变形+滚动数组」写法，本视频演示同余前缀和写法'],
    ),
)
