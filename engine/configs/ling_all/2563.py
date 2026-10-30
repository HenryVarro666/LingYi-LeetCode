CONFIG = dict(
    num=2563, title='统计公平数对的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针（两次计数相减）',
    tags=['二分算法', '难度分 1721'],
    code='''
class Solution:
    def countFairPairs(self, nums: List[int], lower: int, upper: int) -> int:
        nums.sort()
        def count(upper: int) -> int:
            res = 0
            i, j = 0, len(nums) - 1
            while i < j:
                if nums[i] + nums[j] <= upper:
                    res += j - i
                    i += 1
                else:
                    j -= 1
            return res
        return count(upper) - count(lower - 1)
''',
    call='Solution().countFairPairs([0,1,7,4,4,5], 3, 6)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='排序后的 nums', h=200, cell=90, pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j'), dim=lambda S, k, v: 'i' in S and 'j' in S and not (S['i'] <= k <= S['j'])),
        dict(type='text', size=26, h=60, fn=lambda S: (f"`nums[{S['i']}] + nums[{S['j']}] = {S['nums'][S['i']]} + {S['nums'][S['j']]} = {S['nums'][S['i']] + S['nums'][S['j']]}`，上界 `{S['upper']}`" if 'i' in S and 'j' in S and S['i'] < len(S['nums']) and S['j'] >= 0 and S['i'] < S['j'] else '数对和 `<= upper` 的个数')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('upper', 'upper', 'yellow'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '数对和与顺序无关，先排序：`{nums}`',
        'def count': '`count(u)` = 和 `<= u` 的数对个数；答案 = `count(upper) - count(lower-1)`',
        'i, j = 0': '`i` 在最小处，`j` 在最大处',
        'while i < j': lambda S, B, r: ('`i < j`，还有数对要数' if S.i < S.j else '`i` 与 `j` 相遇，数完了'),
        'if nums[i] + nums[j] <= upper': lambda S, B, r: (f'`{S.nums[S.i]} + {S.nums[S.j]} = {S.nums[S.i]+S.nums[S.j]}`' + (' `<=` ' if S.nums[S.i]+S.nums[S.j] <= S.upper else ' `>` ') + f'`{S.upper}`'),
        'res += j - i': '==`nums[i]` 与 `[i+1, j]` 里的每个数配对都合法==（更小的数和更小）：`res += {j-i}` → {res}',
        'i += 1': '`i` 的配对算完，换下一个：`i` → {i}',
        'j -= 1': '和太大：==`nums[j]` 与 `[i, j-1]` 里任何数都配不了==（它们更大），丢掉 `j` → {j}',
        'return res': '这一轮共 `{res}` 对',
        'return count(upper)': '先数和 `<= upper` 的对数，再数和 `<= lower-1` 的对数，两者相减就是和落在 `[lower, upper]` 的对数',
    },
    cards=dict(
        one_liner='和 ≤ upper 的对数，减去和 ≤ lower-1 的对数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数组 `nums`，数对 `(i, j)`，`i < j` 且 `lower <= nums[i]+nums[j] <= upper`',
                 '返回这样的数对个数',
                 '示例：`[0,1,7,4,4,5]`, `lower=3`, `upper=6` → `6`'],
        quote='如果 nums[i]+nums[j]≤upper，那么对于更小的 j，也同样满足这个不等式。所以 [i+1,j] 范围内的下标 j 都可以和 i 配对，这有 j−i 个，加入答案，然后把 i 加一。',
        quote_src='—— 灵茶山艾府题解（方法三 写法二）',
        idea=['排序不影响答案，排序后用相向双指针',
              '和 `<= upper` 就一次数 `j-i` 个；太大就丢掉 `j`',
              '区间计数 = `count(upper) - count(lower-1)`，联想前缀和'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错：下界要用 `lower - 1`，因为 `count` 数的是 `<=`',
                 '另有二分查找（`bisect`）与三指针写法，同样 `O(n log n)`',
                 '同类题：2824. 统计和小于目标的下标对数目'],
    ),
)
