def _wl(S):
    if 'i' not in S:
        return None
    return max(0, S['i'] - S['minutes'] + 1)


def _wr(S):
    return S.get('i')


def _ccol(S, i, v):
    if 'i' not in S or i > S['i']:
        return None
    return 'pink' if S['grumpy'][i] else 'green'


def _gcol(S, i, v):
    return 'pink' if v else None


def _txt(S):
    if 's' not in S:
        return ''
    s0, s1 = S['s']
    return (f"不生气 `s[0] = {s0}`，窗口内生气 `s[1] = {s1}`，"
            f"`max_s1 = {S['max_s1']}`")


def _if_g(S, B, ret):
    l = S.left
    if S.grumpy[l]:
        return f'`grumpy[{l}] = 1`：最左边是生气时的顾客 `{S.customers[l]}`，要从 `s[1]` 中移出'
    return f'`grumpy[{l}] = 0`：这些顾客算在 `s[0]` 里，==不在窗口统计中==，不用减'


CONFIG = dict(
    num=1052, title='爱生气的书店老板', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='拆成两问 · 定长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1418'],
    code='''
class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        s = [0, 0]
        max_s1 = 0
        for i, (c, g) in enumerate(zip(customers, grumpy)):
            s[g] += c
            left = i - minutes + 1  # 窗口左端点
            if left < 0:  # 窗口长度不足 minutes
                continue
            max_s1 = max(max_s1, s[1])
            if grumpy[left]:
                s[1] -= customers[left]  # 窗口最左边元素离开窗口
        return s[0] + max_s1
''',
    call='Solution().maxSatisfied([1,0,1,2,1,1,7,5], [0,1,0,1,0,1,0,1], 3)',
    expect=16,
    views=[
        dict(type='array', var='customers', label='customers（绿 = 不生气，粉 = 生气；框 = 技巧窗口）', h=240, cell=96,
             pointers={'i': 'blue'}, window=(_wl, _wr), color=_ccol),
        dict(type='array', var='grumpy', label='grumpy', h=150, cell=96, color=_gcol),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left'), ('s[0]', 's[0]', 'green'), ('s[1]', 's[1]', 'pink'),
           ('max_s1', 'max_s1', 'orange')],
    captions={
        's = [0, 0]': '`s[0]`：不生气时的顾客和；`s[1]`：==窗口内==生气时的顾客和',
        'max_s1 = 0': '`max_s1`：长为 minutes 的窗口里 `s[1]` 的最大值',
        'for i, (c, g)': lambda S, B, ret: (f'第 `{S.i}` 分钟：`c = {S.c}` 个顾客，`g = {S.g}`'
                                           if 'i' not in B or S.i != B.i else '遍历结束'),
        's[g] += c': lambda S, B, ret: (f'1. 入：老板生气，`s[1] += {S.c}` → `{S.s[1]}`' if S.g
                                        else f'1. 入：老板不生气，顾客一定满意，`s[0] += {S.c}` → `{S.s[0]}`'),
        'left = i - minutes + 1': '窗口左端点 `left = {i} − {minutes} + 1 = {left}`',
        'if left < 0': lambda S, B, ret: (f'`left = {S.left} < 0`：窗口还不满 {S.minutes} 分钟' if S.left < 0
                                          else f'窗口 `[{S.left}, {S.i}]` 满了'),
        'continue': '继续往右扩',
        'max_s1 = max': lambda S, B, ret: (f'2. 更新：`s[1] = {S.s[1]} > {B.max_s1}` → 在这里用技巧更好，`max_s1 = {S.max_s1}`'
                                           if S.max_s1 > B.max_s1 else f'2. 更新：`s[1] = {S.s[1]} ≤ {B.max_s1}`，`max_s1` 不变'),
        'if grumpy[left]': _if_g,
        's[1] -= customers[left]': '3. 出：`s[1] -= {customers[left]}` → `{s[1]}`',
        'return s[0]': '不生气的 `{s[0]}` + 技巧最多挽回 `{max_s1}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='拆成两半：不生气的必然满意 + 窗口内挽回的生气顾客',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`customers[i]` 是第 i 分钟的顾客数；`grumpy[i] = 1` 时老板生气，顾客不满意',
                 '老板可以让自己==连续 minutes 分钟==不生气（只能用一次），求最多满意顾客数',
                 '示例：`[1,0,1,2,1,1,7,5]`，`[0,1,0,1,0,1,0,1]`，`minutes = 3` → `16`'],
        quote='为什么要分开计算不生气和生气时的顾客？因为==不生气时的顾客可以在窗口外面==，需独立计算。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['`s[0]`：所有不生气时的顾客，在不在窗口里都满意',
              '`s[1]`：长为 minutes 的窗口内生气时的顾客，求最大值',
              '用 `s[g] += c` 一行同时处理两种情况，答案 `s[0] + max_s1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '定长滑窗三步：==入 → 更新答案 → 出==',
                 '出窗口时只有 `grumpy[left] = 1` 才减：不生气的顾客不在 `s[1]` 里',
                 '`left < 0` 时窗口不足 minutes，先 `continue`，但 `s[0]` 照样累加'],
    ),
)
