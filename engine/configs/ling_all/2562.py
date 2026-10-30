CONFIG = dict(
    num=2562, title='找出数组的串联值', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 数位左移',
    tags=[],
    code='''
class Solution:
    def findTheArrayConcVal(self, nums: List[int]) -> int:
        ans = 0
        i = 0
        j = len(nums) - 1
        while i < j:  # 相向双指针
            x = nums[i]
            y = nums[j]
            while y:
                x *= 10
                y //= 10
            ans += x + nums[j]
            i += 1
            j -= 1
        if i == j:
            ans += nums[i]
        return ans
''',
    call='Solution().findTheArrayConcVal([5, 14, 13, 8, 12])',
    expect=673,
    views=[
        dict(type='text', fn=lambda S: (f"串联 `{S['nums'][S['i']]}` 和 `{S['nums'][S['j']]}`：`x` 乘 `10` 的次数 = `{S['nums'][S['j']]}` 的位数" if 'x' in S and 'y' in S and S['i'] < S['j'] and S['_line'] in (8, 9, 10, 11, 12) else ''), size=28, h=70),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=300,
             dim=lambda S, i, v: 'j' in S and not (S['i'] <= i <= S['j'])),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'x', 'y', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '串联值 `ans` 从 0 开始',
        'i = 0': '左指针 `i = 0` 指向第一个元素',
        'j = len': '`j = len(nums) - 1 = {j}`，指向最后一个元素',
        'while i < j': lambda S, B, r: (f'`i = {S.i} < j = {S.j}`：首尾各有一个数，可以串联' if S.i < S.j else f'`i = {S.i} ≥ j = {S.j}`：不再有成对的数，退出'),
        'x = nums[i]': '`x = nums[{i}] = {x}`，作串联后的高位部分',
        'y = nums[j]': '`y = nums[{j}] = {y}`，用它的位数决定 `x` 要左移几位',
        'while y': lambda S, B, r: (f'`y = {S.y}` 还有数位 → `x` 再乘 10' if S.y else '`y = 0`：位数数完了，`x` 已经腾出 `nums[j]` 的位置'),
        'x *= 10': '`x` 左移一位 → `{x}`',
        'y //= 10': '`y` 去掉一位 → `{y}`',
        'ans += x + nums[j]': '串联 = `x + nums[j]` = `{x} + {nums[j]}` = `{x + nums[j]}`，加进答案 → `ans = {ans}`',
        'i += 1': '左指针右移，`i = {i}`',
        'j -= 1': '右指针左移，`j = {j}`',
        'if i == j': lambda S, B, r: (f'`i == j = {S.i}`：奇数个元素，中间剩一个' if S.i == S.j else '`i != j`：刚好两两配完，没有剩余'),
        'ans += nums[i]': '只剩一个元素：直接加 `nums[{i}] = {nums[i]}` → `ans = {ans}`',
        'return ans': '串联值 `{ans}`',
    },
    cards=dict(
        one_liner='首尾配对，把左边的数左移右边数的位数再相加',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['每次取首尾两个数拼成一个数，累加到串联值，再删掉它们',
                 '只剩一个数时，直接累加',
                 '示例：`[5,14,13,8,12]` → `512 + 148 + 13 = 673`'],
        quote='由于每次操作都是取出 nums 的第一个元素和最后一个元素串联，所以相向双指针模拟即可。例如 x=15 和 y=49 串联，结果等于 x·10² + y=1549。',
        quote_src='—— 灵茶山艾府题解',
        idea=['首尾配对，用 `i`、`j` 相向双指针模拟',
              '不转字符串：`y` 不断 `//= 10` 数出位数，`x` 同步乘 10，最后 `x + y` 就是串联',
              '最后若 `i == j`，中间那一个单独加'],
        summary=['时间 `O(n log U)`，`U = max(nums)`；空间 `O(1)`',
                 '易错：奇数个元素要在循环外补加 `nums[i]`',
                 '`y` 要用 `nums[j]` 的副本去除 10，别直接改 `nums[j]`（最后还要加它）',
                 '同类：相向双指针模拟题'],
    ),
)
