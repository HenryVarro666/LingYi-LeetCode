CONFIG = dict(
    num=2233, title='K 次增加后的最大乘积', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆：每次给最小的数加一',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1686'],
    code='''
class Solution:
    def maximumProduct(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        heapify(nums)
        while k:
            heapreplace(nums, nums[0] + 1)
            k -= 1

        ans = 1
        for num in nums:
            ans = ans * num % MOD
        return ans
''',
    call='Solution().maximumProduct([6, 3, 3, 2], 4)',
    expect=384,
    views=[
        dict(type='heap', var='nums', label='nums：最小堆（橙色 = 堆顶 = 当前最小）', top_color='orange', h=240),
        dict(type='text', fn=lambda S: (f"给 `x` 加一，乘积变成原来的 `(x+1)/x` 倍：`x` 越小倍数越大" if 'ans' not in S else f"逐个乘进答案，每乘一次就对 `MOD` 取模：`ans` = =={S['ans']}=="), size=26, h=70),
    ],
    watch=[('k', 'k', 'blue'), ('堆顶', lambda S: S['nums'][0] if S.get('nums') else None, 'orange'), ('ans', lambda S: S.get('ans'), 'green')],
    captions={
        'MOD = ': '答案对 `10^9 + 7` 取模；Python 没有溢出，但大数乘法慢，所以边乘边取模',
        'heapify(nums)': '原地堆化成==最小堆==：堆顶 `{nums[0]}` 是当前最小的数，`O(n)` 且不用额外空间',
        'while k': lambda S, B, r: (f'还剩 `k = {S.k}` 次操作，继续' if S.k else '`k = 0`：操作用完了'),
        'heapreplace': lambda S, B, r: (f'给最小的数 `{B.nums[0]}` 加一变成 `{B.nums[0] + 1}`：乘积涨 `{B.nums[0] + 1}/{B.nums[0]}` 倍，比给别的数加一都划算'
                                       if B.nums[0] else f'最小的数是 `0`：加一变成 `1`，乘积从 `0` 变成非零，最划算') + f'；新堆顶 =={S.nums[0]}==',
        'k -= 1': '`k` 减一 → `{k}`',
        'ans = 1': '操作完毕，把堆里的数连乘',
        'ans = ans * num % MOD': '`ans = {B.ans} × {num} % MOD` = =={ans}==',
        'return ans': '返回 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='每次给最小的数加一：加在小数上，乘积涨得最多',
        complexity='时间 `O(n + k log n)`，空间 `O(1)`（原地堆化）',
        problem=['非负整数数组 `nums`，每次可以让任意一个数加 `1`，最多 `k` 次',
                 '求操作后数组的==最大乘积==，对 `10^9 + 7` 取模',
                 '本视频：`nums = [6,3,3,2]`，`k = 4` → `384`'],
        quote='给 x 加一后，让总乘积增加了 (x+1)/x = 1+1/x 倍，那么 x 越小收益越高，所以要先加 x 最小的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['乘积涨的倍数是 `1 + 1/x`：`x` 越小涨得越多 → ==永远给最小的数加一==',
              '`x = 0` 时加一更是从 0 变成非零，同样满足「先加最小」',
              '「取最小 + 放回加一后的值」= 最小堆的 `heapreplace`，堆化还能原地做'],
        summary=['堆化 `O(n)`，`k` 次替换 `O(k log n)`；空间 `O(1)`',
                 '易错：乘的过程中就要取模，最后再取模会算出巨大的整数',
                 '为什么能中途取模：模运算对乘法封闭，见原文推荐的模运算文章',
                 '`heapreplace` 比 `heappop` + `heappush` 少一次调整'],
    ),
)
