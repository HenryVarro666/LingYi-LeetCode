NUMS = [2, 2, 1]


def _txt(S):
    if 'sub' in S and 'p2' in S:
        sub, oa = S['sub'], S['or_all']
        k = (oa ^ sub).bit_count()
        sign = '−' if k % 2 else '+'
        return f'`S = {sub:02b}`，与 or 差 {k} 位 → ==符号 {"−" if k % 2 else "+"}==：`2^f[S] = 2^{S["f"][sub]} = {S["p2"]}`'
    if 'ans' in S and 'sub' not in S or ('s' in S and S['s'] >= S['u'] and S.get('_line') == 22 and S['i'] == S['or_all'].bit_length() - 1):
        return 'SOS DP 完成：`f[s]` = nums 中是 s 子集的元素个数'
    if 'f' in S and 'bit' in S:
        return f'SOS DP 第 {S["i"]} 位：`f[s] += f[s ^ {S["bit"]}]`，把「少这一位」的数个数并进来'
    if 'or_all' in S:
        return f'`or_all = {S["or_all"]:b}`：只在它的子集上做容斥'
    return '子序列剩余按位或 < or ⇔ 按位或≠or；用 2^n 减去「恰好等于 or」'


CONFIG = dict(
    num=3757, title='有效子序列的数量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='正难则反 + 容斥 + SOS DP',
    tags=['数学算法', '难度分 2519'],
    setup='from operator import or_',
    code='''
MOD = 1_000_000_007
MAX_N = 100_001

# 预处理 2 的幂
pow2 = [1] * MAX_N
for i in range(1, MAX_N):
    pow2[i] = (pow2[i - 1] * 2) % MOD

class Solution:
    def countEffective(self, nums: List[int]) -> int:
        # 优化：如果 nums 只有一种数字，那么非空子序列的按位或都是 or_all，只有空子序列的按位或比 or_all 小
        if all(x == nums[0] for x in nums):
            return 1

        or_all = reduce(or_, nums)
        w = or_all.bit_length()
        u = 1 << w

        f = [0] * u
        for x in nums:
            f[x] += 1
        for i in range(w):
            bit = 1 << i  # 避免在循环中反复计算 1 << i
            if or_all & bit == 0:  # 优化：or_all 中是 0 但 s 中是 1 的 f[s] 后面容斥用不到，无需计算
                continue
            s = 0
            while s < u:
                s |= bit  # 快速跳到第 i 位是 1 的 s
                f[s] += f[s ^ bit]
                s += 1
        # 计算完毕后，f[s] 表示 nums 中的是 s 的子集的元素个数

        ans = pow2[len(nums)]  # 所有子序列的个数
        # 枚举 or 的所有子集（包括空集）
        sub = or_all
        while True:
            p2 = pow2[f[sub]]
            ans -= -p2 if (or_all ^ sub).bit_count() % 2 else p2
            if sub == 0:
                break
            sub = (sub - 1) & or_all
        return ans % MOD
''',
    call=f'Solution().countEffective({NUMS})',
    expect=5,
    skip=['w = or_all.bit_length()', 'u = 1 << w', 'bit = 1 << i', 'for x in nums:'],
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90),
        dict(type='array', var='f', label='f[s]：nums 中是 s 的子集的元素个数（下标 = s）', h=250, cell=100,
             pointers={'s': 'blue', 'sub': 'pink'}),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('or_all', 'or_all', 'orange'), ('i', 'i'), ('s', 's', 'blue'), ('sub', 'sub', 'pink'), ('p2', 'p2'), ('ans', 'ans', 'green')],
    captions={
        'MOD = ': '先定义模数 `MOD = 10^9 + 7`',
        'if all(x == nums[0]': lambda S, B, r: ('全是同一个数 → 只有空子序列比 or 小' if all(x == S.nums[0] for x in S.nums)
                                                else '不是全相同，继续'),
        'return 1': '只有一种数字：非空子序列的 OR 都等于 or，只有「移除全部」有效 → `1`',
        'or_all = reduce': '`or_all` = 所有数的按位或 = `{or_all}`（二进制 `{or_all:b}`）',
        'f = [0] * u': '`f` 长 `{u}`：按位或不超过 `or_all` 的位宽',
        'f[x] += 1': '数字 `{x}` 出现一次：`f[{x}] = {f[x]}`',
        'for i in range(w)': lambda S, B, r: (f'==SOS DP 枚举第 `{S.i}` 位==' if 'i' in S and S.get('i') != B.get('i') else 'SOS DP 完成'),
        'if or_all & bit == 0': lambda S, B, r: (f'`or_all` 第 {S.i} 位是 0 → 容斥用不到，跳过' if S.or_all & S.bit == 0
                                                 else f'`or_all` 第 {S.i} 位是 1 → 要算'),
        's = 0': '`s` 从 0 开始，每次跳到第 `{i}` 位是 1 的数',
        'while s < u': '`s < {u}`，继续',
        's |= bit': '`s |= {bit}` → `s = {s}`（第 {i} 位是 1 的数）',
        'f[s] += f[s ^ bit]': '`f[{s}] += f[{s ^ bit}]` → =={f[s]}==：子集里去掉第 {i} 位的数也算进 `s` 的子集',
        's += 1': '`s` 加一，看下一个',
        'ans = pow2[len(nums)]': '先放所有子序列的个数 `2^n = {ans}`',
        'sub = or_all': '从 `or_all` 开始，枚举它的所有子集 `sub`',
        'while True': '枚举子集：容斥每一项 `±2^f[sub]`',
        'p2 = pow2[f[sub]]': '`sub = {sub:b}`：只能选是它子集的 `{f[sub]}` 个数，方案 `2^{f[sub]} = {p2}`',
        'ans -= -p2 if': lambda S, B, r: (f'`sub` 与 or 差 {(S.or_all ^ S.sub).bit_count()} 位（奇数）→ 这一项在「恰好」里是 −，`ans` 里就==加上== `{S.p2}` → `ans = {S.ans}`'
                                          if (S.or_all ^ S.sub).bit_count() % 2
                                          else f'`sub` 与 or 差 {(S.or_all ^ S.sub).bit_count()} 位（偶数）→ 这一项在「恰好」里是 +，`ans` 里就==减去== `{S.p2}` → `ans = {S.ans}`'),
        'if sub == 0': lambda S, B, r: ('空集也算过了 → 结束' if S.sub == 0 else '还没到空集，继续'),
        'sub = (sub - 1) & or_all': '`(sub-1) & or_all`：枚举下一个子集 `{sub:b}`',
        'return ans % MOD': '`2^n` 减去「OR 恰好等于 or」的个数 = 严格小于 or 的子序列数 = =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='移除后剩余的 OR 变小 ⇔ 剩余子序列的 OR < or',
        complexity='时间 `O(n + U log U)`，空间 `O(U)`',
        problem=['数组的强度 = 所有元素按位或。移除一个子序列后，剩余数组的强度==严格减少==，这个子序列就有效',
                 '返回有效子序列的个数，对 `10^9 + 7` 取模（空数组的 OR 是 0）',
                 '本视频：`nums = [2,2,1]` → `5`'],
        quote='由于剩余元素也是 nums 的一个子序列，所以问题等价于：计算 nums 的子序列 b 的个数，满足 b 的按位或严格小于 or。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等价转化：「移除的子序列」和「剩下的子序列」一一对应，数「OR 小于 or」的子序列',
              '正难则反：`2^n` 减去 OR ==恰好等于== or 的个数',
              '恰好 = 至多的容斥：`Σ (−1)^{差几位} · 2^f[S]`，`f[S]` 用 SOS DP 求'],
        summary=['时间 `O(n + U log U)`，空间 `O(U)`（不计 2 的幂预处理）',
                 '易错：所有元素相同时只有 1 个有效子序列，要先特判',
                 '易错：中途取模，减法后最后要 `ans % MOD`',
                 '`or_` 来自 `operator`，已在 setup 里 `from operator import or_`；`reduce` 同样需要导入',
                 '同类：SOS DP 题单 §9.5，容斥原理题单 §2.4，如 3670'],
    ),
)
