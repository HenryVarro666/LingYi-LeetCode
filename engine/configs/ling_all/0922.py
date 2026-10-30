CONFIG = dict(
    num=922, title='按奇偶排序数组 II', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地交换双指针', tags=['灵神题单'],
    code='''
class Solution:
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        i, j = 0, 1
        while i < len(nums):
            if nums[i] % 2 == 0:  # 寻找偶数下标中最左边的奇数
                i += 2
            elif nums[j] % 2 == 1:  # 寻找奇数下标中最左边的偶数
                j += 2
            else:
                nums[i], nums[j] = nums[j], nums[i]
                i += 2
                j += 2
        return nums
''',
    call='Solution().sortArrayByParityII([4,2,5,7,3,8,6,1])',
    expect=[4, 5, 2, 7, 8, 3, 6, 1],
    views=[
        dict(type='text', fn=lambda S: (f"偶数下标 `i={S['i']}` 看 ==nums[{S['i']}]=={'' if S['i'] >= len(S['nums']) else '=' + str(S['nums'][S['i']])}；奇数下标 `j={S['j']}`" if 'i' in S else '')),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=300,
             color=lambda S, k, v: ('red' if (k % 2 == 0 and v % 2 == 1) or (k % 2 == 1 and v % 2 == 0) else 'green')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'i, j = 0, 1': '`i` 管偶数下标 0,2,4…，`j` 管奇数下标 1,3,5…，两边互不干扰',
        'while i < len': lambda S, B, r: (f'`i = {S.i}` 还在数组内 → 继续检查' if S.i < len(S.nums) else f'`i = {S.i}` 走出数组 → 偶数下标全是偶数了，结束'),
        'nums[i] % 2 == 0': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}` 是偶数，放在偶数下标正合适 → `i += 2`' if S.nums[S.i] % 2 == 0
                                             else f'`nums[{S.i}] = {S.nums[S.i]}` 是奇数却在偶数下标 → 错位，去奇数下标找一个错位的偶数'),
        'nums[j] % 2 == 1': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]}` 是奇数，在奇数下标没问题 → `j += 2` 继续找' if S.nums[S.j] % 2 == 1
                                             else f'`nums[{S.j}] = {S.nums[S.j]}` 是偶数却在奇数下标 → 错位，两个错位凑成一对'),
        'nums[i], nums[j] =': '`nums[{i}]` 是错位奇数，`nums[{j}]` 是错位偶数 → ==交换==，两边同时修好',
        'i += 2': '`i` → {i}（下一个偶数下标）',
        'j += 2': '`j` → {j}（下一个奇数下标）',
        'return nums': '全部归位，返回 `{nums}`',
    },
    cards=dict(
        one_liner='偶数下标放偶数、奇数下标放奇数：错位的一对互换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组一半偶数一半奇数，要让 `nums[i]` 与 `i` 的奇偶性一致',
                 '返回任意合法结果，最好原地做',
                 '示例：`[4,2,5,7]` → `[4,5,2,7]`'],
        quote='首先，找到 A 中最左边的奇数 nums[i] 和 B 中最左边的偶数 nums[j]，交换这两个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把偶数下标记作 A，奇数下标记作 B，两个集合没有交集',
              'A 里的奇数和 B 里的偶数一一对应，==数量一定相等==',
              '交换后 `i` 之前、`j` 之前都已正确，变成更小的子问题'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`i`、`j` 每次都是步长 2，不要写成 `+= 1`',
                 '因为偶数恰好一半，`i` 走完时 `j` 也一定同步走完，不会越界',
                 '三个分支各只动一个指针或同时动两个，循环条件只看 `i`'],
    ),
)
