def _top(S):
    ln = S.get('_line') or 0
    if 'B' not in S:
        return '先把 `(l, r, k)` 相同的询问合并：`v` 相乘'
    B = S['B']
    if 'diff' in S and ln >= 38:
        return f'`k = {S.get("k")}` 这一组：把下标 `start, start+k, …` 抽成一条链，用==商分数组==做前缀积'
    return f'阈值 `B = {B}`：`k < {B}` 的询问分组做商分，`k ≥ {B}` 的直接暴力'


CONFIG = dict(
    num=3655, title='区间乘法查询后的异或 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='根号分治 · 商分数组',
    tags=['常用数据结构', '难度分 2454'],
    code='''
class Solution:
    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        MOD = 1_000_000_007
        prod = defaultdict(lambda: 1)
        for l, r, k, v in queries:
            t = (l, r, k)
            prod[t] = prod[t] * v % MOD

        n = len(nums)
        B = isqrt(len(prod))
        groups = [[] for _ in range(B)]

        for (l, r, k), v in prod.items():
            if k < B:
                groups[k].append((l, r, v))
            else:
                for i in range(l, r + 1, k):
                    nums[i] = nums[i] * v % MOD

        for k, g in enumerate(groups):
            if not g:
                continue

            buckets = [[] for _ in range(k)]
            for t in g:
                buckets[t[0] % k].append(t)

            for start, bucket in enumerate(buckets):
                if not bucket:
                    continue
                if len(bucket) == 1:
                    # 只有一个询问，直接暴力
                    l, r, v = bucket[0]
                    for i in range(l, r + 1, k):
                        nums[i] = nums[i] * v % MOD
                    continue

                m = (n - start - 1) // k + 1
                diff = [1] * (m + 1)
                for l, r, v in bucket:
                    diff[l // k] = diff[l // k] * v % MOD
                    r = (r - start) // k + 1
                    diff[r] = diff[r] * pow(v, -1, MOD) % MOD

                mul_d = 1
                for i in range(m):
                    mul_d = mul_d * diff[i] % MOD
                    j = start + i * k
                    nums[j] = nums[j] * mul_d % MOD

        return reduce(xor, nums)
''',
    call='Solution().xorAfterQueries([1,2,3,4,5,6], [[1,4,1,3],[2,5,3,2],[0,2,1,2],[0,2,1,5],[3,5,2,4],[1,3,1,7]])',
    expect=1069,
    views=[
        dict(type='text', fn=_top, size=23, h=80),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, label='nums（模 10^9+7）',
             window=None, cell=100, h=190),
        dict(type='array', var='diff', pointers={'i': 'blue'}, label='diff（商分数组：初值全是 1，乘 v / 乘逆元）', cell=100, h=190),
        dict(type='map', var='prod', fmt=lambda k, v: f'{k} → {v}', h=170),
    ],
    watch=[('B', 'B', 'orange'), ('k', 'k', 'yellow'), ('start', 'start', 'cyan'), ('mul_d', 'mul_d', 'green')],
    captions={
        't = (l, r, k)': '询问 `[{l},{r},{k},{v}]`：前三项 `{t}` 相同的可以合并',
        'prod[t] = prod[t]': '询问 `[{l},{r},{k},{v}]`：前三项 `{t}` 相同的合并，`v` 乘起来 → `prod[{t}] = {prod[t]}`',
        'B = isqrt': lambda S, B, r: f'阈值 `B = isqrt({len(S.prod)}) = {S.B}`：`k` 小用商分，`k` 大暴力，两边都约 `n√q`',
        'groups = [[]': '`groups[k]` 收集 `k < B` 的询问',
        'for (l, r, k), v in prod.items()': '取一条合并后的询问 `({l},{r},{k})`，乘数 `{v}`',
        'if k < B': lambda S, B, r: (f'`k = {S.k} < B = {S.B}`：步长小，暴力会很慢 → 留给商分' if S.k < S.B else f'`k = {S.k} ≥ B = {S.B}`：步长大，至多 `n/k` 个下标 → 直接暴力'),
        'groups[k].append': '放进 `groups[{k}]`：`({l}, {r}, {v})`',
        'nums[i] = nums[i] * v % MOD': '暴力：`nums[{i}]` 乘 `{v}` → =={nums[i]}==',
        'for k, g in enumerate(groups)': '处理 `k = {k}` 的询问组',
        'if not g': lambda S, B, r: ('这个 `k` 没有询问，跳过（不建商分数组）' if not S.g else '这个 `k` 有询问，继续'),
        'buckets = [[]': '按 `l % k` 分桶：同一桶的询问作用在同一条下标链上',
        'buckets[t[0] % k]': '`l = {t[0]}`，`{t[0]} % {k} = {t[0]%k}` → 放进桶 {t[0]%k}',
        'for start, bucket': '桶 `start = {start}`：下标链 `{start}, {start}+{k}, …`',
        'if not bucket': lambda S, B, r: ('空桶，跳过' if not S.bucket else '这个桶有询问'),
        'if len(bucket) == 1': lambda S, B, r: (f'桶里只有 {len(S.bucket)} 个询问 → 直接暴力' if len(S.bucket) == 1 else f'桶里有 {len(S.bucket)} 个询问 → 值得用商分合并'),
        'm = (n - start': '这条链上共有 `m = {m}` 个下标',
        'diff = [1] * (m + 1)': '商分数组 `diff` 长度 `m + 1`，初始全是 ==1==（乘法的单位元）',
        'diff[l // k] = ': '链上起点 `l // k = {l//k}`：`diff[{l//k}]` 乘 `{v}` → =={diff[l//k]}==',
        'diff[r] = diff[r]': '链上终点的下一格是 `(r − start)//k + 1 = {r}`，乘 `{v}` 的==逆元==（`pow(v, -1, MOD)`）撤销影响：`diff[{r}] = {diff[r]}`',
        'mul_d = 1': '`mul_d` 是 `diff` 的前缀积',
        'mul_d = mul_d * diff[i]': '前缀积：`mul_d = {mul_d}`（链上第 `{i}` 个位置要乘的总倍数）',
                'nums[j] = nums[j] * mul_d': '链上第 `{i}` 个位置 = 下标 `j = {start}+{i}×{k} = {j}`：`nums[{j}]` 乘 `mul_d` → =={nums[j]}==',
        'return reduce': '最后把所有数异或：`{ret}`',
    },
    skip=['MOD = 1_000_000_007', 'j = start', 'for t in g', 'n = len(nums)', 'for l, r, k, v in queries', 't = (l, r, k)', 'groups = [[]', 'if not g', 'if not bucket', 'continue', 'for i in range(m)', 'for l, r, v in bucket', 'mul_d = 1', 'm = (n - start', 'r = (r - start', 'for start, bucket'],
    max_steps=110,
    cards=dict(
        one_liner='步长小用商分，步长大暴力，阈值取 √q',
        complexity='时间 `O(n√q + q log M)`，空间 `O(n + q)`',
        problem=['`queries[i] = [l, r, k, v]`：对下标 `l, l+k, l+2k, … ≤ r` 的数都乘 `v`（模 `10^9+7`）',
                 '处理完所有询问，返回 `nums` 所有元素的==异或==',
                 '本视频：`n=6`，6 个询问（合并后 5 个）'],
        quote='对于 k≥B 的询问，使用算法一，即暴力计算。对于 k<B 的询问，使用算法二，即用商分数组记录询问。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：每个询问 `O(n/k)`，`k` 大时很快；差分：`k` 小时能把询问摊成 `k` 条链上的商分',
              '商分数组 = 差分的乘法版：起点乘 `v`，终点后一格乘==逆元==，前缀积就是每个位置的总倍数',
              '按 `(k, l mod k)` 分桶，每桶一条链；只有一个询问的桶直接暴力；`(l,r,k)` 相同先合并'],
        summary=['时间 `O(n√q + q log M)`（逆元用 `pow(v, -1, MOD)`），空间 `O(n + q)`',
                 '易错点：链上终点是 `(r − start)//k + 1`，不要直接用 `r`；乘法要全程取模',
                 '懒创建：没有询问的 `k` 和空桶都不遍历',
                 '灵神还给了更简单的写法一：`diff[k]` 按 `k` 建整条商分数组，空间 `O(n√q)`',
                 '`isqrt`、`reduce`、`xor`、`defaultdict` 均为 LeetCode 预置'],
    ),
)
