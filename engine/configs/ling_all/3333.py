def _f_col(S, i, v):
    j = S.get('j')
    c = S.get('c')
    if j is None:
        return None
    if S['_line'] in (36, 37) and c is not None:
        pass
    return 'blue' if i == j else ('yellow' if c is not None and i == j - c - 1 else None)


CONFIG = dict(
    num=3333, title='找到初始输入字符串 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='分组 + 多重背包 + 前缀和优化',
    tags=['动态规划', '数学算法', '难度分 2629'],
    code='''
class Solution:
    def possibleStringCount(self, word: str, k: int) -> int:
        n = len(word)
        if n < k:  # 无法满足要求
            return 0

        MOD = 1_000_000_007
        cnts = []
        ans = 1
        cnt = 0
        for i in range(n):
            cnt += 1
            if i == n - 1 or word[i] != word[i + 1]:
                # 如果 cnt = 1，这组字符串必选，无需参与计算
                if cnt > 1:
                    if k > 0:  # 保证空间复杂度为 O(k)
                        cnts.append(cnt - 1)
                    ans = ans * cnt % MOD
                k -= 1  # 注意这里把 k 减小了
                cnt = 0

        if k <= 0:
            return ans

        f = [1] * k
        for c in cnts:
            # 原地计算 f 的前缀和
            for j in range(1, k):
                f[j] = (f[j] + f[j - 1]) % MOD
            # 计算子数组和
            for j in range(k - 1, c, -1):
                f[j] -= f[j - c - 1]
        return (ans - f[-1]) % MOD
''',
    call="Solution().possibleStringCount('aabbcc', 6)",
    expect=1,
    max_steps=90,
    skip=['MOD = 1_000', 'cnts = []', 'ans = 1', 'cnt = 0', 'n = len', 'cnt += 1', 'for i in range', 'for j in range(1, k)', 'for j in range(k - 1'],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符 i）', h=150, pointers={'i': 'blue'}, cell=60),
        dict(type='array', var='cnts', label='cnts：每组「长度 − 1」= 可额外多选的个数', h=150, cell=60),
        dict(type='array', var='f', label='f[j]：至多额外选 j 个字符的方案数（蓝 = j，黄 = 要减去的 j-c-1）', h=190, cell=70, color=_f_col),
        dict(type='text', fn=lambda S: (f"不考虑 k 的原串个数 `ans` = =={S['ans']}==；还需 `k` = =={S['k']}== 个额外字符之内的方案要减掉" if 'ans' in S and 'k' in S else ''), size=26),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'pink'), ('ans', 'ans', 'green'), ('c', 'c', 'orange'), ('j', 'j', 'cyan')],
    captions={
        'if n < k': lambda S, B, r: (f'`n = {S.n} < k = {S.k}`：长度凑不够 → 返回 0' if S.n < S.k else f'`n = {S.n} ≥ k = {S.k}`，有解，继续'),
        'if i == n - 1 or word[i] != word[i + 1]': lambda S, B, r: f'`i = {S.i}`：' + ('到了 ==这一组的末尾==，开始结算这一组' if (S.i == S.n - 1 or S.word[S.i] != S.word[S.i + 1]) else '后面还是同一个字符，继续数'),
        'if cnt > 1': lambda S, B, r: f'这一组长度 `cnt = {S.cnt}`：' + ('可能多按了，要参与计算' if S.cnt > 1 else '只有 1 个，必选，无需参与计算'),
        'if k > 0': lambda S, B, r: ('`k > 0`：还需要 DP，记下 `cnt - 1`' if S.k > 0 else '`k <= 0`：后面用不到 DP，不用再记'),
        'cnts.append': '`cnts` 加入 `cnt - 1 = {cnt - 1}`：这一组最多额外多选这么多个',
        'ans = ans * cnt': '乘法原理：这组有 `{cnt}` 种可能 → `ans` = =={ans}==',
        'k -= 1': '每组必选 1 个，所以 `k` 少 1 → `k = {k}`（还差几个额外字符才够 k）',
        'if k <= 0': lambda S, B, r: (f'`k = {S.k} <= 0`：每组必选的字符就已经够长 → 直接返回 `ans`' if S.k <= 0 else f'`k = {S.k} > 0`：还要减去「长度 < k」的原串，需要 DP'),
        'f = [1] * k': '`f[j]`：从前 0 组至多选 `j` 个额外字符 = 1（什么也不选）',
        'for c in cnts': '依次加入每一组（多重背包的一种物品，最多选 `c` 个）',
        'f[j] = (f[j] + f[j - 1])': '原地算前缀和：`f[{j}]` = ==至多选 {j} 个==的方案数 = {f[j]}',
        'f[j] -= f[j - c - 1]': lambda S, B, r: f'这组最多选 `c = {S.c}` 个：减去选了超过 c 个的情况 `f[{S.j - S.c - 1}]` → `f[{S.j}]` = =={S.f[S.j]}==（倒序，用的是旧前缀和）',
        'return (ans - f[-1])': lambda S, B, r: f'答案 = 总数 `{S.ans}` − 长度 < k 的原串 `{S.f[-1]}` = =={r}==',
    },
    cards=dict(
        one_liner='正难则反：总数减去长度小于 k 的，后者是多重背包',
        complexity='时间 `O(n + k^2)`，空间 `O(k)`',
        problem=['Alice 打字时某个键可能按太久，同一个字符被输入多次；给你最终的 `word` 和 `k`',
                 '求原串（长度至少 `k`）有多少种可能，对 `10^9+7` 取模',
                 '示例：`"aabbccdd", k=7` → `5`',
                 '本视频：`"aabbcc", k=6` → `1`'],
        quote='考虑长度小于 k 的原串。1. 计算不考虑 k 的情况下，有多少个原串。2. 计算长度小于 k 的原串个数。3. 二者相减，即为长度大于等于 k 的原串个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分成连续相同的几组，每组长度为 `c`，原串里这一组有 `c` 种可能，乘起来是总数',
              '每组先必选 1 个，长度小于 k 就是「额外选的字符」总数不超过 `k-1-m`：这是==多重背包方案数==',
              '`f[i][j] = s[j+1] - s[max(j-c,0)]`，用前缀和把转移变成 `O(1)`；去掉第一维后倒序更新'],
        summary=['时间 `O(n + k^2)`，空间 `O(k)`（`k > 0` 才记录 `cnts`）',
                 '`k -= 1` 在每组结算时执行：它同时是「每组必选 1 个」的扣除',
                 '`k <= 0` 时每组必选的字符已达标，直接返回 `ans`',
                 '倒序更新 + 原地前缀和，别忘了 `% MOD`；本题题解还给了二维版本（非原地），这里演示空间优化版',
                 '相似题：2902 和带限制的子多重集合的数目'],
    ),
)
