CONFIG = dict(
    num=891, title='子序列宽度之和', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 贡献法（最大值加、最小值减）',
    tags=['灵神题单·贪心与思维', '难度分 2000'],
    code='''
class Solution:
    def sumSubseqWidths(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        nums.sort()
        n = len(nums)
        pow2 = [0] * n
        pow2[0] = 1
        for i in range(1, n):
            pow2[i] = pow2[i - 1] * 2 % MOD  # 预处理 2 的幂次
        return sum((pow2[i] - pow2[-1 - i]) * x
                   for i, x in enumerate(nums)) % MOD
''',
    call='Solution().sumSubseqWidths([2, 1, 3, 5])',
    expect=30,
    views=[
        dict(type='text', size=28, fn=lambda S: '排序后，`nums[i]` 当最大值有 `2^i` 次（加），当最小值有 `2^(n-1-i)` 次（减）'),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=220, label='nums（排序后）'),
        dict(type='array', var='pow2', pointers={'i': 'pink'}, h=220, label='pow2[i] = 2^i'),
    ],
    watch=[('n', 'n', 'blue'), ('i', 'i', 'pink')],
    skip=['for i, x in enumerate'],
    captions={
        'nums.sort()': '先排序：子序列只看最大、最小值，和顺序无关 → `{nums}`',
        'n = len(nums)': '`n = {n}`',
        'pow2 = [0] * n': '`pow2[i]` 存 `2^i`（取模后），先占位',
        'pow2[0] = 1': '`2^0 = 1`',
        'for i in range(1': '预处理 2 的幂次：`i = {i}`',
        'pow2[i] = ': '`pow2[{i}] = pow2[{i-1}] × 2` = =={pow2[i]}==：每多一个元素，选法翻倍',
        'return sum(': lambda S, B, r: ('每个数的贡献 = `(2^i − 2^(n-1-i)) × x`：' + ' + '.join(f'({S.pow2[i]}−{S.pow2[-1-i]})×{x}' for i, x in enumerate(S.nums)) + ('，逐项累加' if r is None else f' = =={r}==，再对 `MOD` 取模')),
    },
    cards=dict(
        one_liner='每个数当最大值加、当最小值减，次数都是 2 的幂',
        complexity='时间 `O(n log n)`，空间 `O(n)`（pow2 数组）',
        problem=['宽度 = 子序列最大值 − 最小值，求所有非空子序列的宽度之和（对 `10^9+7` 取模）',
                 '示例：`[2,1,3]` → `6`',
                 '本视频演示：`[2,1,3,5]` → `30`'],
        quote='为什么 x 作为最小值的子序列的个数为 2^(n-1-i)？因为排序后，x 右侧有 n-1-i 个元素，每个元素都可以选或不选。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['排序后顺序不再重要：`nums[i]` 作最大值时，左边 `i` 个数选或不选 → `2^i` 个子序列，要加',
              '作最小值时，右边 `n-1-i` 个数选或不选 → `2^(n-1-i)` 个，要减',
              '重复元素不会重复统计：相等的数只考虑它==左侧==的元素'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`',
                 '易错点：`pow2[-1-i]` 就是 `2^(n-1-i)`；最后别忘了取模',
                 '题解还给了另外三种写法：快速幂 `pow(2,i,MOD)`、用逆元 `INV2` 递推、按 `2^i` 配对 `(nums[i]-nums[n-1-i])` 的贡献',
                 '相关题：把子序列改成子数组 → 2104'],
    ),
)
