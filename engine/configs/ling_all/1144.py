def _cost(S):
    if S.get('_line') != 7 or 'left' not in S or 'right' not in S:
        return ''
    i, x, l, r = S['i'], S['x'], S['left'], S['right']
    m = min(l, r)
    return f"`nums[{i}] = {x}`，邻居较小值 `{m}`：需减 `max({x} − {m} + 1, 0)` = =={max(x - m + 1, 0)}==（下标奇偶 → s[{i % 2}]）"


CONFIG = dict(
    num=1144, title='递减元素使数组呈锯齿状', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='奇偶分别贪心',
    tags=['灵神题单', '难度分 1559'],
    code='''
class Solution:
    def movesToMakeZigzag(self, nums):
        s = [0] * 2
        for i, x in enumerate(nums):
            left = nums[i - 1] if i else inf
            right = nums[i + 1] if i < len(nums) - 1 else inf
            s[i % 2] += max(x - min(left, right) + 1, 0)
        return min(s)
''',
    call='Solution().movesToMakeZigzag([9,6,1,6,2])',
    expect=4,
    views=[
        dict(type='text', fn=_cost),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if i % 2 == 0 else 'purple')),
        dict(type='array', var='s', label='s（s[0] = 偶数下标要减的总次数，s[1] = 奇数下标）', h=160)
    ],
    watch=['i', 'x', 'left', 'right', ('s', 's', 'green')],
    captions={
        's = [0]': '`s[0]`：只减偶数下标（让奇数下标当“高峰”）的操作数；`s[1]` 反过来',
        'left = nums': '左邻居 `{left}`（没有左邻居时当作无穷大）',
        'right = nums': '右邻居 `{right}`（越界时当作无穷大）',
        's[i % 2] +=': '`nums[{i}]` 要比两边都小：目标 `min({left}, {right}) − 1`，需减 `max({x} − min({left}, {right}) + 1, 0)` → `s[{i % 2}] = {s[i % 2]}`',
        'return min': '两种锯齿形取少的一种：`min({s[0]}, {s[1]}) = {ret}`',
    },
    cards=dict(
        one_liner='只能减小：谷底才需要减，减到刚好比邻居小就停',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可把一个元素减 1，使数组成为锯齿数组（谷、峰交替）',
                 '两种形态：偶数下标是峰，或奇数下标是峰，求最少操作数',
                 '示例：`[9,6,1,6,2]` → `4`'],
        quote='如果你想把 x≤y 改成 x>y 的话，减少 x 是毫无意义的，只能减少 y。……nums[0],nums[2],⋯ 是一定不需要的。',
        quote_src='—— 灵茶山艾府题解（提示 1、3-2）',
        idea=['只能减：峰一定不用动，只有谷（另一种奇偶）要减',
              '谷要减到 `min(左, 右) − 1`，次数 `max(x − min + 1, 0)`',
              '越界邻居视为无穷大；用 `s[i % 2]` 一趟同时算出两种形态'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`s[i % 2]` 累加的是“把下标 i 当谷”的代价，最后取 `min(s)`',
                 '易错点：首尾元素只有一个邻居，缺的那边当 `inf`',
                 '加 1 是因为要严格小于邻居'],
    ),
)
