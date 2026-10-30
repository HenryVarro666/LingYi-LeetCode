CONFIG = dict(
    num=922, title='按奇偶排序数组 II', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='even / odd 双指针找错位再交换', tags=['灵神题单'],
    code='''
class Solution(object):
    def sortArrayByParityII(self, nums):

        even = 0
        odd = 1
        while even < len(nums) and odd < len(nums):
            while even < len(nums) and nums[even] % 2 == 0:
                even += 2
            while odd < len(nums) and nums[odd] % 2 == 1:
                odd += 2
            if even < len(nums) and odd < len(nums):
                nums[even], nums[odd] = nums[odd], nums[even]
                even += 2
                odd += 2
        
        return nums
''',
    call='Solution().sortArrayByParityII([3,6,4,1,8,5,2,7])',
    expect=[6, 3, 4, 1, 8, 5, 2, 7],
    views=[
        dict(type='array', var='nums', pointers={'even': 'blue', 'odd': 'pink'}, h=300,
             color=lambda S, k, v: ('red' if (k % 2 == 0 and v % 2 == 1) or (k % 2 == 1 and v % 2 == 0) else 'green')),
        dict(type='text', fn=lambda S: '红色 = 位置和奇偶不符，绿色 = 已正确', size=26),
    ],
    watch=[('even', 'even', 'blue'), ('odd', 'odd', 'pink')],
    captions={
        'even = 0': '`even`：偶数位上==最左边的奇数==的下标，从 0 开始找',
        'odd = 1': '`odd`：奇数位上==最左边的偶数==的下标，从 1 开始找',
        'while even < len(nums) and odd': lambda S, B, r: (f'`even = {S.even}`、`odd = {S.odd}` 都没到末尾 → 继续找下一对错位的' if S.even < len(S.nums) and S.odd < len(S.nums) else f'`even = {S.even}`、`odd = {S.odd}` 有指针到了末尾 → 结束'),
        'while even < len(nums) and nums[even]': lambda S, B, r: (f'`nums[{S.even}] = {S.nums[S.even]}` 是偶数，偶数位正合适 → `even` 往后跳两位' if S.even < len(S.nums) and S.nums[S.even] % 2 == 0
                                                                   else (f'`nums[{S.even}] = {S.nums[S.even]}` 是奇数 → 偶数位上的错位数，`even` 停在这里' if S.even < len(S.nums) else '`even` 走出数组，偶数位全部正确')),
        'while odd < len(nums) and nums[odd]': lambda S, B, r: (f'`nums[{S.odd}] = {S.nums[S.odd]}` 是奇数，奇数位正合适 → `odd` 往后跳两位' if S.odd < len(S.nums) and S.nums[S.odd] % 2 == 1
                                                                 else (f'`nums[{S.odd}] = {S.nums[S.odd]}` 是偶数 → 奇数位上的错位数，`odd` 停在这里' if S.odd < len(S.nums) else '`odd` 走出数组，奇数位全部正确')),
        'if even < len(nums) and odd': lambda S, B, r: (f'两个指针都在数组内：错位的一对是 `nums[{S.even}]={S.nums[S.even]}` 和 `nums[{S.odd}]={S.nums[S.odd]}`' if S.even < len(S.nums) and S.odd < len(S.nums)
                                                        else '有指针已走出数组：没有可交换的了，不再交换'),
        'nums[even], nums[odd] =': '交换这一对，两个位置同时修正',
        'even += 2': '`even` → {even}，继续找下一组',
        'odd += 2': '`odd` → {odd}',
        'return nums': '返回 `{nums}`',
    },
    cards=dict(
        one_liner='两个指针各找一个错位的数，成对交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组里一半奇数、一半偶数',
                 '重排后：偶数下标放偶数，奇数下标放奇数',
                 '示例：`[4,2,5,7]` → `[4,5,2,7]`'],
        quote='维护两个指针even和odd，分别表示当前最左边的偶数位上的奇数的下标以及最左边的奇数位上的偶数的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`even` 从 0 出发，跳过偶数位上的偶数，停在第一个奇数上',
              '`odd` 从 1 出发，跳过奇数位上的奇数，停在第一个偶数上',
              '两个都找到就交换，然后各自再往后两位重复'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '内层 while 也要判 `< len(nums)`，防止越界',
                 '交换前必须确认两个指针都没走出数组',
                 '对比灵神：灵神用 if/elif 一步一步走，这里用两个内层 while 各自跑到停'],
    ),
)
