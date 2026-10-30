CONFIG = dict(
    num=2191, title='将杂乱无章的数字排序', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按位映射 · 下标排序',
    code='''
class Solution(object):
    def sortJumbled(self, mapping, nums):

        mapped_nums = []
        for num in nums:
            digit_list = []
            while True:
                digit_list.append(mapping[num % 10])
                num //= 10
                if num == 0:
                    break
            
            for digit in digit_list[::-1]:
                num = num * 10 + digit
            
            mapped_nums.append(num)

        return [nums[index] for index in sorted(range(len(nums)), key=lambda d:(mapped_nums[d], d))]
''',
    call='Solution().sortJumbled([8,9,4,0,2,1,3,5,7,6], [991,338,38])',
    expect=[338,38,991],
    views=[
        dict(type='array', var='mapping', label='mapping（数位 i 映射成 mapping[i]）', h=150, pointers={},),
        dict(type='array', var='nums', label='nums', h=150),
        dict(type='array', var='digit_list', label='digit_list（映射后的数位，低位在前）', h=150),
        dict(type='array', var='mapped_nums', label='mapped_nums（映射后的数）', h=150),
    ],
    watch=['num', ('digit', 'digit', 'cyan')],
    captions={
        'for num in nums': '处理下一个数 `num = {num}`',
        'digit_list = []': '准备收集 `{num}` 每一位映射后的数位',
        'digit_list.append': '取最低位 `{num} % 10 = {num % 10}`，映射成 `{mapping[num % 10]}`，加入列表',
        'num //= 10': '去掉最低位：`num` = {num}',
        'if num == 0': '`num == 0` → {num == 0}（{"所有数位处理完" if num == 0 else "还有高位，继续"}；用 while True 保证 0 也会处理一次）',
        'for digit in': '列表是低位在前，倒着取，从高位开始拼回数字',
        'num = num * 10': '拼接：`num` = {num}',
        'mapped_nums.append': '映射后的数 `{num}` 存入 `mapped_nums`',
        'return [nums': lambda S, B, r: f'按 (映射后的值, 下标) 排序下标，再取原数：`{r}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='先把每个数按映射改写，再按映射后的值给下标排序',
        complexity='时间 `O(n log n + n·d)`，空间 `O(n)`',
        problem=['`mapping[i]` 表示数位 `i` 被映射成什么数位',
                 '把 `nums` 里每个数的每一位替换后得到映射值，按映射值非递减排序',
                 '映射值相同则保持原来的相对顺序，返回的是原数（不是映射值）',
                 '示例：`mapping=[8,9,4,0,2,1,3,5,7,6], nums=[991,338,38]` → `[338,38,991]`'],
        quote='直接按照题目的描述进行模拟就行了。首先对nums进行一趟遍历，将每个数字的数位都拆分出来，找到映射然后拼成映射后的数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位拆数：`%10` 取最低位、`//10` 去掉，得到的数位低位在前',
              '倒序拼回去就是映射后的数；`while True` 保证数字 0 也处理',
              '排序下标 `0..n-1`，主关键字映射值、副关键字下标，保证稳定'],
        summary=['时间 `O(n log n + n·d)`，空间 `O(n)`',
                 '映射后前导零会消失，如 `38 → 07 → 7`，直接按数值拼就行',
                 '副关键字下标保证映射值相同时保持原顺序',
                 '原文为 Python 2 写法，其中整数除法 `num /= 10` 已改为 `num //= 10`'],
    ),
)
