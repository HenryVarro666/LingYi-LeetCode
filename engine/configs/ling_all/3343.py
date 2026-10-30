def _top(S):
    if 'left1' not in S:
        n = S.get('n')
        if 'cnt' in S and 'total' in S:
            return f"数字出现次数 `cnt`，数字和 `total = {S['total']}`；目标：分成两个多重集，和都是 `total/2`"
        return '把 `num` 的数字分成两组：第一组 `n1 = n//2` 个，两组数字和相等'
    return (f"`dfs({S['i']}, {S['left1']}, {S['left_s']})`：数字 `0..{S['i']}` 还要分，"
            f"第一组还差 ==`{S['left1']}`== 个数、==和还差 `{S['left_s']}`==")


CONFIG = dict(
    num=3343, title='统计平衡排列的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多重集排列 + 记忆化搜索',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2615'],
    code='''
MOD = 1_000_000_007
MX = 41

fac = [0] * MX  # f[i] = i!
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_f = [0] * MX  # inv_f[i] = i!^-1
inv_f[-1] = pow(fac[-1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_f[i - 1] = inv_f[i] * i % MOD

class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        cnt = [0] * 10
        total = 0
        for c in map(int, num):
            cnt[c] += 1
            total += c

        if total % 2:
            return 0

        pre = list(accumulate(cnt))

        @cache
        def dfs(i: int, left1: int, left_s: int) -> int:
            if i < 0:
                return 1 if left_s == 0 else 0
            res = 0
            c = cnt[i]
            left2 = pre[i] - left1
            for k in range(max(c - left2, 0), min(c, left1) + 1):
                if k * i > left_s:
                    break
                r = dfs(i - 1, left1 - k, left_s - k * i)
                res += r * inv_f[k] * inv_f[c - k]
            return res % MOD

        n = len(num)
        n1 = n // 2
        return fac[n1] * fac[n - n1] * dfs(9, n1, total // 2) % MOD
''',
    call='Solution().countBalancedPermutations("112")',
    expect=1,
    skip=['if i < 0', 'if k * i > left_s', 'for c in map', 'cnt[c] += 1', 'total += c', 'res = 0', 'left2 = ', 'c = cnt[i]'],
    max_steps=52,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='cnt', label='cnt[d]：数字 d 的出现次数（蓝 = 正在分配的数字）', cell=70, h=190,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'blue' if k == S.get('i') and 'left1' in S else None),
        dict(type='calls', h=230),
    ],
    watch=[('i', 'i', 'blue'), ('left1', 'left1', 'cyan'), ('left_s', 'left_s', 'orange'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt = [0] * 10': '`cnt[d]` 统计每个数字出现几次',
        'if total % 2': lambda S, B, r: (f'数字和 `{S.total}` 是奇数，分不成两个和相等的集合 → 返回 0' if S.total % 2
                                          else f'数字和 `{S.total}` 是偶数，每组的和都要是 `{S.total // 2}`'),
        'pre = list(accumulate(cnt))': '`pre[i]` = 数字 `0..i` 一共有几个，用来算第二组还剩几个 `left2`',
        'return 1 if left_s': lambda S, B, r: (f'数字 `0..9` 都分完，`left_s = {S.left_s}`：==恰好为 0 才合法== → 返回 {1 if S.left_s == 0 else 0}'),
        'for k in range': lambda S, B, r: f'数字 `{S.i}` 有 `{S.c}` 个：分 `k` 个给第一组，`k ∈ [{max(S.c - S.left2, 0)}, {min(S.c, S.left1)}]`',
        'r = dfs': '放好后处理更小的数字：进入 `dfs({i}, {left1}, {left_s})`',
        'res += r': '乘 `1/(k!(c−k)!)` 累加 → `res = {res}`',
        'return res % MOD': '`dfs({i}, {left1}, {left_s})` = =={ret}==',
        'n1 = n // 2': '第一组 `n1 = n // 2 = {n1}` 个，第二组 `n - n1` 个',
        'return fac[n1]': lambda S, B, r: (f'`n1! × (n-n1)! × dfs` = =={r}==' if r is not None else f'答案 = `n1! × (n-n1)! × dfs(9, {S.n1}, {S.total // 2})`：先算 dfs，从数字 9 开始分'),
    },
    cards=dict(
        one_liner='先把数字分成两个等和的多重集，再乘上两边的排列数',
        complexity='时间 `O(n^2 S)`，空间 `O(D n S)`（`D = 10`）',
        problem=['奇数下标数字之和 = 偶数下标数字之和 的字符串叫==平衡==的',
                 '求 `num` 的所有不同排列中，平衡的有几个（模 `10^9+7`）',
                 '本视频：`"112"` → `1`（只有 `"121"` 平衡）'],
        quote='可以把 num 分成两个多重集，大小分别为 ⌊n/2⌋ 和 ⌈n/2⌉，每个多重集的元素和均为 total/2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设数字 `i` 有 `k_i` 个分给第一组，两组排列数相乘，提出分子后只剩 `∏ 1/(k_i!(cnt_i−k_i)!)`',
              '`dfs(i, left1, left_s)` 从大到小枚举数字：第一组还差几个、和还差多少',
              '`left2 = pre[i] - left1` 约束第二组的容量，所以 `k` 的范围是 `[max(c-left2,0), min(c,left1)]`'],
        before=[dict(heading='预处理：阶乘与逆元', lines=['`fac[i] = i!`，`inv_f[i] = (i!)^-1 mod p`', '除法在取模下要用逆元：`pow(x, -1, MOD)`', '这一段在类外，视频里跳过'])],
        summary=['时间 `O(n^2 S)`：状态 `i` 与枚举 `k` 合起来才 `O(n)`',
                 '易错：==先判断 total 的奇偶==；奇数直接返回 0',
                 '`k` 的下界 `max(c-left2, 0)`：第二组放不下的必须给第一组',
                 '题解还给了写法二（空间更省的写法）和 1:1 翻译的递推，本视频只演示写法一',
                 '同类题：3539. 魔法序列的数组乘积之和'],
    ),
)
