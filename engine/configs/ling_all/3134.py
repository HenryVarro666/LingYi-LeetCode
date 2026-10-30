CONFIG = dict(
    num=3134, title='找出唯一性数组的中位数', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='二分答案 + 滑窗数子数组',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·二分算法', '难度分 2451'],
    code='''
class Solution:
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        n = len(nums)
        k = (n * (n + 1) // 2 + 1) // 2

        def check(upper: int) -> bool:
            cnt = l = 0
            freq = defaultdict(int)
            for r, in_ in enumerate(nums):
                freq[in_] += 1  # 移入右端点
                while len(freq) > upper:  # 窗口内元素过多
                    out = nums[l]
                    freq[out] -= 1  # 移出左端点
                    if freq[out] == 0:
                        del freq[out]
                    l += 1
                cnt += r - l + 1  # 右端点固定为 r 时，有 r-l+1 个合法左端点
                if cnt >= k:
                    return True
            return False

        return bisect_left(range(len(set(nums))), True, 1, key=check)
''',
    call='Solution().medianOfUniquenessArray([4,3,5,4])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [l, r]，窗口内不同元素 ≤ upper）', pointers={'l': 'blue', 'r': 'pink'},
             window=('l', 'r'), cell=100, h=230,
             dim=lambda S, i, v: 'r' in S and 'l' in S and not (S['l'] <= i <= S['r'])),
        dict(type='map', var='freq', label='freq（窗口内每个数的次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=34),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"二分的中位数 `upper` = =={S['upper']}==；累计 `cnt` = {S['cnt']}，目标 `k` = {S['k']}"
                           if 'upper' in S and 'cnt' in S else
                           (f"共 `m` = {S['n']*(S['n']+1)//2} 个子数组，中位数是第 `k` = =={S['k']}== 小" if 'k' in S else ''))),
    ],
    watch=[('k', 'k', 'yellow'), ('upper', 'upper', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`：子数组共有 `n(n+1)/2` = {n*(n+1)//2} 个，每个对应一个 distinct 值',
        'k = (n *': '中位数是这些值里第 `k = (m+1)//2` = =={k}== 小的（偶数个取较小的）',
        'def check': '`check(upper)`：`cnt` 统计 distinct ≤ upper 的子数组个数，`l` 是窗口左端点。distinct 值 `≤ upper` 的子数组够不够 `k` 个？`upper` 越大越容易够，有==单调性==，可二分',
        'freq = defaultdict': '`freq` 记录窗口里每个数的出现次数，`len(freq)` 就是窗口的 distinct 值',
        'freq[in_] += 1': '右端点 `r = {r}`：`nums[{r}] = {in_}` 进入窗口，窗口有 `{len(freq)}` 种数',
        'while len(freq) > upper': lambda S, B, r: (f'`len(freq) = {len(S.freq)} > upper = {S.upper}` → ==窗口内元素过多==，要缩小'
                                                    if len(S.freq) > S.upper else f'`len(freq) = {len(S.freq)} ≤ upper = {S.upper}` → 窗口合法'),
        'if freq[out] == 0': lambda S, B, r: (f'移出左端点 `nums[{S.l - 1 if False else S.l}]`：`{S.out}` 次数减一后为 0 → 窗口里已没有它，要从 freq 删掉，distinct 值才会减小'
                                              if S.freq[S.out] == 0 else f'移出左端点 `nums[{S.l}]`：`{S.out}` 还剩 {S.freq[S.out]} 个 → 保留，distinct 值不变'),
        'del freq[out]': '从 `freq` 删掉 `{out}`，窗口只剩 `{len(freq)}` 种数；`l` 随后右移',
        'cnt += r - l': '右端点固定为 {r} 时，左端点 `{l}..{r}` 都合法，共 `{r} - {l} + 1` = =={r - l + 1}== 个 → `cnt = {cnt}`',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}` → 已经够 k 个，`upper = {S.upper}` ==满足要求==，可提前返回'
                                         if S.cnt >= S.k else f'`cnt = {S.cnt} < k = {S.k}` → 还不够，继续看下一个右端点'),
        'return True': '`upper = {upper}` 够了，返回 True（二分往小的方向收缩）',
        'return False': '扫完所有右端点仍不到 k 个 → `upper = {upper}` ==太小==，返回 False',
        'return bisect_left': '`bisect_left` 在 `upper ∈ [1, {len(set(nums))})` 上二分：找第一个 `check(upper)` 为 True 的值。`check` 用滑窗数 distinct ≤ upper 的子数组，够 k 个就是 True',
    },
    skip=['out = nums[l]', 'freq[out] -= 1', 'l += 1', 'freq = defaultdict', 'for r, in_', 'cnt = l = 0'],
    cards=dict(
        one_liner='二分猜中位数 upper，再用滑窗数出 distinct ≤ upper 的子数组有几个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对 `nums` 所有非空子数组，取各自的不同元素个数，排序得到「唯一性数组」，求它的中位数（偶数个取较小的）',
                 '示例：`[4,3,5,4]` → 唯一性数组 `[1,1,1,1,2,2,2,3,3,3]` → `2`'],
        quote='考虑这 m 个数中，小于等于某个定值 upper 的数有多少个。由于 upper 越大，小于等于 upper 的数越多，有单调性，故可以二分中位数为 upper。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组共 `m = n(n+1)/2` 个，中位数是第 `k = (m+1)//2` 小：==二分答案==',
              '`check(upper)`：distinct ≤ upper 的子数组 ≥ k 个吗？子数组越长 distinct 不会变小 → ==滑动窗口==',
              '窗口 distinct 超过 upper 就移出左端点；右端点固定时合法左端点有 `r-l+1` 个'],
        summary=['时间 `O(n log n)`：二分 `log n` 次，每次滑窗 `O(n)`',
                 '二分区间 `(0, 不同元素个数)` 开区间：0 一定不满足，`len(set(nums))` 一定满足',
                 '`freq[out] == 0` 时必须 `del`，否则 `len(freq)` 不会减小',
                 '`bisect_left(..., key=check)` 需要 Python 3.10+，本视频的 Mac 环境满足',
                 '答案一定是某个子数组的 distinct 值：否则 `d-1` 也满足，与最小性矛盾'],
    ),
)
