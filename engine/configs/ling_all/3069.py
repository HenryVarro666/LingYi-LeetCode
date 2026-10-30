CONFIG = dict(
    num=3069, title='将元素分配到两个数组中 I', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='按题意模拟', tags=[],
    code='''
class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        a = nums[:1]
        b = nums[1:2]
        for x in nums[2:]:
            if a[-1] > b[-1]:
                a.append(x)
            else:
                b.append(x)
        return a + b
''',
    call='Solution().resultArray([5,4,3,8,2,9,1])',
    expect=[5, 3, 9, 1, 4, 8, 2],
    views=[
        dict(type='array', var='nums', h=170, label='nums（黄 = 当前 x）', color=lambda S, i, v: 'yellow' if S.get('x') == v and S['_line'] >= 5 else None),
        dict(type='array', var='a', h=170, label='a（= arr1）', color=lambda S, i, v: 'blue' if i == len(S['a']) - 1 else None),
        dict(type='array', var='b', h=170, label='b（= arr2）', color=lambda S, i, v: 'pink' if i == len(S['b']) - 1 else None),
    ],
    watch=[('x', 'x', 'yellow'), ('a[-1]', 'a[-1] if a else None', 'blue'), ('b[-1]', 'b[-1] if b else None', 'pink')],
    captions={
        'a = nums[:1]': '第一次操作：`nums[0]` 进 `a`，`a = {a}`',
        'b = nums[1:2]': '第二次操作：`nums[1]` 进 `b`，`b = {b}`',
        'for x in nums[2:]': '从第三个数开始按规则分配',
        'if a[-1] > b[-1]': '比末尾：`a[-1] = {a[-1]}`，`b[-1] = {b[-1]}` → {"==a 末尾更大，x 去 a==" if a[-1] > b[-1] else "==a 末尾不大于 b，x 去 b=="}',
        'a.append': '`{x}` 追加到 `a`：`a = {a}`',
        'b.append': '`{x}` 追加到 `b`：`b = {b}`',
        'return a + b': '把 `b` 接在 `a` 后面：`{a}` + `{b}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='按题意模拟：谁的末尾更大，数就进谁',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['前两个数分别放进 `arr1`、`arr2`，之后每个数放进末尾更大的那个数组',
                 '`arr1` 末尾更大放 `arr1`，否则放 `arr2`，最后拼接成 `result`',
                 '示例：`[5,4,3,8]` → `[5,3,4,8]`；本视频：`[5,4,3,8,2,9,1]`'],
        quote='按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`a` 和 `b` 分别拿 `nums[:1]`、`nums[1:2]` 作为开头',
              '从 `nums[2:]` 开始，比较 `a[-1]` 与 `b[-1]` 决定去向',
              '最后 `a + b` 拼起来'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '题目下标从 1 开始，代码从 0 开始，别搞混',
                 '条件是 `a[-1] > b[-1]`，不满足就去 `b`（元素互不相同，不会相等）',
                 '用切片 `nums[:1]` 初始化，写起来比 `[nums[0]]` 短'],
    ),
)
