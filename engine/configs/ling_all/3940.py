CONFIG = dict(
    num=3940, title='限制有序数组中的元素出现次数', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地修改 · 栈思路',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def limitOccurrences(self, nums: list[int], k: int) -> list[int]:
        stack_size = k  # 栈的大小，前 k 个元素默认保留
        for i in range(k, len(nums)):
            if nums[i] != nums[stack_size - k]:  # 和栈的倒数第 k 个数比较
                nums[stack_size] = nums[i]  # 入栈
                stack_size += 1

        del nums[stack_size:]
        return nums
''',
    call='Solution().limitOccurrences([1,1,1,1,2,2,2,3], 2)',
    expect=[1, 1, 2, 2, 3],
    views=[
        dict(type='text', fn=lambda S: (f"栈 = nums[0:{S['stack_size']}]，倒数第 k 个是 `nums[{S['stack_size']-S['k']}] = {S['nums'][S['stack_size']-S['k']]}`" if 'stack_size' in S and S['stack_size'] < len(S['nums']) + 1 and S['stack_size'] - S['k'] < len(S['nums']) else '')),
        dict(type='array', var='nums', pointers={'i': 'blue', 'stack_size': 'pink'}, h=300,
             color=lambda S, i, v: 'green' if 'stack_size' in S and i < S['stack_size'] else None,
             dim=lambda S, i, v: 'stack_size' in S and i >= S['stack_size'] and i < S.get('i', 99)),
    ],
    watch=[('i', 'i', 'blue'), ('stack_size', 'stack_size', 'pink'), 'k'],
    captions={
        'stack_size = k': '前 `k = {k}` 个元素一定能留下，当作栈的初始内容：`stack_size = {stack_size}`',
        'if nums[i] != nums[stack_size - k]': '`nums[{i}] = {nums[i]}` 和栈倒数第 k 个 `nums[{stack_size - k}] = {nums[stack_size - k]}` 比：{"不同 → 可以入栈" if nums[i] != nums[stack_size - k] else "相同 → 数组有序，栈里已有 k 个这个数，丢掉"}',
        'nums[stack_size] = nums[i]': '把 `{nums[i]}` 写到栈顶位置 `nums[{stack_size}]`（原地覆盖）',
        'stack_size += 1': '栈变大：`stack_size` → {stack_size}',
        'del nums[stack_size:]': '栈外的多余元素全部删掉，只剩 `nums[:{stack_size}]`',
        'return nums': '返回 `{nums}`',
    },
    cards=dict(
        one_liner='把结果当成栈：和栈里倒数第 k 个数比，不同才入栈',
        complexity='时间 `O(n-k)`，空间 `O(1)`',
        problem=['有序数组 `nums`，每个不同的数最多保留 `k` 次，原地修改',
                 '示例：`[1,1,1,2,2,3], k=2` → `[1,1,2,2,3]`',
                 '本视频：`[1,1,1,1,2,2,2,3], k=2` → `[1,1,2,2,3]`'],
        quote='和栈的倒数第 k 个数比较',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['数组有序，相同的数连在一起',
              '若 `nums[i]` 等于栈里倒数第 k 个数，栈里最后 k 个数都和它相同，再放就超过 k 次',
              '前 k 个数无条件保留，所以从 `i = k` 开始枚举'],
        summary=['时间 `O(n-k)`，空间 `O(1)`，k=2 时就是第 80 题',
                 '栈大小从 `k` 开始，所以比较的下标 `stack_size - k` 不会越界',
                 '最后别忘了 `del nums[stack_size:]` 截断多余部分'],
    ),
)
