CONFIG = dict(
    num=1877, title='数组中最大数对和的最小值', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 交换论证',
    tags=['贪心与思维', '难度分 1301'],
    code='''
class Solution:
    def minPairSum(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        return max(nums[i] + nums[-1 - i] for i in range(n // 2))
''',
    call='Solution().minPairSum([5,6,2,4,1,6])',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: ('各对之和：' + '； '.join(f"{S['nums'][i]}+{S['nums'][-1-i]} = =={S['nums'][i]+S['nums'][-1-i]}==" for i in range(len(S['nums'])//2)) + f"  → 最大 =={max(S['nums'][i]+S['nums'][-1-i] for i in range(len(S['nums'])//2))}==") if 'n' in S else ''),
        dict(type='array', var='nums', h=300,
             color=lambda S, i, v: (lambda m: 'green' if i in (m, len(S['nums'])-1-m) else 'blue' if i < len(S['nums'])//2 else 'pink')(max(range(len(S['nums'])//2), key=lambda j: S['nums'][j]+S['nums'][-1-j])) if 'n' in S else None),
    ],
    watch=['n'],
    captions={
        'nums.sort()': '先排序：`{nums}`，设排序后为 `a1 <= a2 <= ... <= an`',
        'n = len': '`n = {n}`（题目保证偶数），共 `{n // 2}` 对',
        'return max': '最小配最大、次小配次大：第 `i` 个与倒数第 `i` 个配对，取所有数对和的最大值 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='为什么 a1 配 an 不会更差', lines=['任取另外两数 `ai`、`aj`，对比 `(a1,ai)+(aj,an)` 与 `(a1,an)+(ai,aj)`',
                                                               '前者最大和 `= aj + an`（因为 `a1 <= aj`、`ai <= an`）',
                                                               '后者 `a1+an` 与 `ai+aj` 都不超过 `aj + an`',
                                                               '所以调整后不会更大，去掉这对，对剩下 `n-2` 个数同理'])],
        one_liner='把最小的数和最大的数配对，依此类推',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['长度为偶数的 `nums` 分成 `n/2` 个数对，每个元素恰好在一个数对中',
                 '使「最大数对和」最小',
                 '示例：`[3,5,2,3]` → `7`；本视频：`[5,6,2,4,1,6]` → `9`'],
        quote='把最小的数和最大的数配对，把第二小的数和第二大的数配对，依此类推。……对于任意最优配对方案，将其调整为 a1 和 an 配对，不会让最大数对和变得更大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先猜结论：最小配最大，次小配次大……', '再用交换论证证明：把 `a1` 换到和 `an` 一组，最大和不会变大', '所以只需要看 `nums[i] + nums[-1-i]` 的最大值'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '倒数第 `i+1` 个元素下标是 `-1 - i`',
                 '`i` 只需枚举前一半：`range(n // 2)`',
                 '交换论证：任意最优方案都能调整成「首尾配对」而不变差',
                 '同类：灵神题单「单序列配对」「交换论证法」'],
    ),
)
