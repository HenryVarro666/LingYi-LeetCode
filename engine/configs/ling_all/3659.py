NUMS, K = [1, 2, 2, 3, 2, 4], 3

CONFIG = dict(
    num=3659, title='数组元素分组', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='出现次数上限 · 数组计数 + 提前返回',
    tags=['灵神题单', '难度分 1440'],
    code='''
class Solution:
    def partitionArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        if n % k:
            return False
        cnt = [0] * (max(nums) + 1)
        n //= k  # 避免在循环中反复做除法
        for x in nums:
            cnt[x] += 1
            if cnt[x] > n:
                return False
        return True
''',
    call=f'Solution().partitionArray({NUMS}, {K})',
    expect=False,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'blue' if S.get('x') == v and 'cnt' in S and S['cnt'][v] > S.get('n', 99) else None),
        dict(type='array', var='cnt', label='cnt[x]（x 出现的次数，下标 = 元素值）', pointers={'x': 'blue'}, h=190,
             color=lambda S, i, v: 'red' if 'n' in S and v > S['n'] else None),
        dict(type='text', size=30, h=90,
             fn=lambda S: f"一共 `{S['k']}` 个一组，组数 `n/k = {S['n']}`：每个数最多出现 {S['n']} 次" if S['n'] < len(S['nums']) else ''),
    ],
    watch=['n', 'k', 'x'],
    captions={
        'if n % k': '`{n} % {k}` = `{n % k}`：' + '总数必须是 `k` 的倍数，否则一定剩下元素',
        'cnt = [0]': '`cnt` 按元素值计数，下标 `0 ~ {max(nums)}`',
        'n //= k': '`n // k` = `{n}` 就是==组数==：同一个数每组最多用一次，所以出现次数不能超过 `{n}`',
        'for x in nums': '取下一个元素 `x = {x}`',
        'cnt[x] += 1': '`{x}` 出现了 `{cnt[x]}` 次',
        'if cnt[x] > n': lambda S, B, r: f'`cnt[{S.x}] = {S.cnt[S.x]}` > 组数 `{S.n}` → ' + ('==放不下，必有一组含重复，返回 False==' if S.cnt[S.x] > S.n else '没超过，继续'),
        'return True': '没有谁超过组数 → 可以分组',
    },
    cards=dict(
        one_liner='每个数的出现次数，不能超过组数 n/k',
        complexity='时间 `O(n+U)`，空间 `O(U)`（U 为最大值）',
        problem=['把 `nums` 分成若干组，每组恰好 `k` 个==互不相同==的元素，所有元素都要用上',
                 '判断能否做到',
                 f'示例：`nums={NUMS}`，`k={K}`，`n=6` 分 2 组，但 `2` 出现 3 次'],
        quote='每次把 m 减少 1，其余元素的个数就要减少 k-1，所以其余元素的个数必须至少为 m·(k-1)，即 m·k ≤ n。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先要 `n % k == 0`，否则分不完',
              '出现最多的数出现 `m` 次，每次分组至多带走它一个 → 其余元素至少要有 `m·(k-1)` 个',
              '化简得 `m·k ≤ n`；遍历计数时一旦某个数超过 `n/k` 就提前返回'],
        summary=['时间 `O(n+U)`，空间 `O(U)`',
                 '易错：别忘了先判 `n % k`',
                 '原文还有哈希表写法 `max(Counter(nums).values()) * k <= n`，数组写法的优化版即本视频',
                 '同类题：§1.8 相邻不同（装满杯子 2335 是 k=2 的特例）'],
    ),
)
