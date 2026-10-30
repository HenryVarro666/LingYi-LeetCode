def _color(S, i, v):
    sz = S.get('stack_size')
    if sz is None:
        return None
    if 'i' in S and i == S['i'] and S['i'] >= sz:
        return 'blue'
    if i == sz - 2:
        return 'purple'
    if i < sz:
        return 'green'
    return None


def _dim(S, i, v):
    sz = S.get('stack_size')
    return sz is not None and 'i' in S and sz < i < S['i']


def _stack_text(S):
    sz = S.get('stack_size')
    if sz is None:
        return '把 `nums` 的前缀 `nums[0:stack_size]` 当成栈'
    nums = S['nums']
    if 'i' not in S or S['i'] >= len(nums):
        return f'栈 = `nums[0:{sz}]`，大小 =={sz}=='
    i = S['i']
    rel = '≠' if nums[i] != nums[sz - 2] else '='
    return f'比较：`nums[{i}] = {nums[i]}` {rel} 栈顶下方 `nums[{sz - 2}] = {nums[sz - 2]}`'


def _if_cap(S, B, ret):
    i, sz, nums = S.i, S.stack_size, S.nums
    a, b = nums[i], nums[sz - 2]
    if a != b:
        return f'`nums[{i}] = {a}` ≠ 栈顶下方 `{b}` → 入栈后不会有三个一样的数，==可以入栈=='
    return f'`nums[{i}] = {a}` = 栈顶下方 `{b}`：栈顶也是 {b}，再入栈就有==三个 {b}== → 跳过'


CONFIG = dict(
    num=80, title='删除有序数组中的重复项 II', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='用栈思考 · 原地实现',
    tags=['面试经典150'],
    code='''
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        stack_size = 2  # 栈的大小，前两个元素默认保留
        for i in range(2, len(nums)):
            if nums[i] != nums[stack_size - 2]:  # 和栈顶下方的元素比较
                nums[stack_size] = nums[i]  # 入栈
                stack_size += 1
        return min(stack_size, len(nums))
''',
    call='''nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]
k = Solution().removeDuplicates(nums)
(k, nums[:k])''',
    expect=(7, [0, 0, 1, 1, 2, 3, 3]),
    views=[
        dict(type='array', var='nums', label='nums（绿 = 栈，紫 = 栈顶下方，蓝 = 当前 i）', cell=100, h=290,
             pointers={'i': 'blue', 'stack_size': 'pink', 'stack_size - 2': 'purple'},
             pointer_labels={'stack_size - 2': 'size-2'},
             window=('0', 'stack_size - 1'), window_color='green', color=_color, dim=_dim),
        dict(type='stack', var=lambda S: S['nums'][:S['stack_size']] if 'stack_size' in S else None,
             label='栈 = nums[0:stack_size]', h=130),
        dict(type='text', fn=_stack_text, size=28, h=70),
        dict(type='text', fn=lambda S: '数组有序：相同的数挨在一起，==和栈顶下方比较==就知道栈顶是不是已经有两个一样的', size=24, h=90, lines=2),
    ],
    watch=[('i', 'i', 'blue'), ('stack_size', 'stack_size', 'pink')],
    captions={
        'stack_size = 2': '数组有序，==前两个数一定满足要求==，直接当作已入栈：`stack_size = 2`',
        'for i in range': lambda S, B, ret: (f'看 `nums[{S.i}] = {S.nums[S.i]}`：能不能入栈？' if S.get('i') != B.get('i')
                                             else '遍历结束'),
        'if nums[i] != nums[stack_size - 2]': _if_cap,
        'nums[stack_size] = nums[i]': '入栈：把 `{nums[i]}` 写到栈顶的下一格 `nums[{stack_size}]`',
        'stack_size += 1': '栈大小 +1 → `{stack_size}`',
        'return min': '返回栈的大小 `min({stack_size}, {len(nums)})` = =={ret}==',
    },
    cards=dict(
        one_liner='把 nums 本身当栈：当前数和栈顶下方那个数不同才入栈',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有序数组 `nums`，==原地==删除重复项，使每个元素==最多出现两次==',
                 '返回新长度 `k`，`nums` 的前 `k` 个元素就是结果；额外空间 `O(1)`',
                 '示例：`[0,0,1,1,1,1,2,3,3]` → `7`，`nums = [0,0,1,1,2,3,3]`'],
        quote='用一个栈记录去重后的元素，==如果当前元素等于栈顶下方那个数（倒数第二个数），那么不能入栈==（否则会有三个一样的数），反之可以入栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组有序 → 相同的数是连续的；栈顶下方 = 栈顶 = x 时，再来 x 就是第三个',
              '为了 `O(1)` 空间，==直接把 nums 当作栈==，`stack_size` 是栈的大小',
              '`nums[stack_size-2]` 是栈顶下方；入栈 = 写 `nums[stack_size]` 再加一'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：比较对象是 ==栈里的== `nums[stack_size-2]`，不是原数组的 `nums[i-2]`',
                 '返回 `min(stack_size, len(nums))`，兼容 `n = 1`',
                 '推广：最多保留 `k` 个，就把 2 换成 `k`（26 题就是 `k = 1`）'],
    ),
)
