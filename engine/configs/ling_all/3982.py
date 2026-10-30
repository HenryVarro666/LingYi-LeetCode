def _txt(S):
    if 'x' not in S or 's' not in S or 'r' not in S:
        return ''
    s = S['s']
    return f"`x = {S['x']}`：最大数字 `{max(s)}`，最小数字 `{min(s)}`，数字范围 `r = {S['r']}`，当前最大范围 `{S['max_range']}`"


def _cmp(S, B, ret):
    r, mr, x = S.r, S.max_range, S.x
    if r > B.max_range:
        return f'`r = {r} > max_range = {B.max_range}`：出现更大的范围，==更新 max_range=={mr}，答案重新累加'
    if r == B.max_range:
        return f'`r = {r} == max_range`：范围一样大，把 `{x}` ==加进答案=='
    return f'`r = {r} < max_range = {B.max_range}`：范围不够大，跳过'


CONFIG = dict(
    num=3982, title='最大数字范围的整数之和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='维护最大范围 · 重置/累加', tags=[],
    code='''
class Solution:
    def maxDigitRange(self, nums: list[int]) -> int:
        ans = max_range = 0

        for x in nums:
            s = str(x)  # 不用字符串的写法，见另一份代码
            r = ord(max(s)) - ord(min(s))
            if r > max_range:
                max_range = r
                ans = x  # 重新累加
            elif r == max_range:
                ans += x

        return ans
''',
    call='Solution().maxDigitRange([5724, 111, 350])',
    expect=6074,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（蓝 = 当前数字）', cell=100, pointers={'nums.index(x)': 'blue'}, pointer_labels={'nums.index(x)': 'x'},
             color=lambda S, i, v: 'blue' if S.get('x') == v else None, h=230),
        dict(type='text', fn=lambda S: (f"答案 `ans = {S['ans']}`，最大范围 `max_range = {S['max_range']}`" if 'ans' in S else ''), size=28),
    ],
    watch=[('x', 'x', 'blue'), ('r', 'r', 'pink'), ('max_range', 'max_range', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = max_range': '`max_range`：目前见过的最大数字范围；`ans`：范围等于它的数之和',
        'for x in nums': lambda S, B, ret: (f'取 `x = {S.x}`' if S.get('x') is not None and S.x != B.get('x') else '遍历完了'),
        's = str': '`s = str(x)` = `"{s}"`，转成字符串方便取最大、最小字符',
        'r = ord': lambda S, B, ret: f"`'{max(S.s)}' − '{min(S.s)}'`：最大数字减最小数字，`r = {S.r}`",
        'if r > max_range': lambda S, B, ret: (f'`r = {S.r}` 比 `max_range = {S.max_range}` 大吗？' if S.r <= S.max_range else f'`r = {S.r} > max_range`：更大的范围 → 进入更新'),
        'max_range = r': '更新 `max_range = {max_range}`',
        'ans = x': '之前累加的数范围都不够大，作废；==重新累加==：`ans = {x}`',
        'elif r == max_range': lambda S, B, ret: (f'`r = {S.r}`，`max_range = {S.max_range}`：相等吗？' + ('相等' if S.r == S.max_range else '不等，跳过')),
        'ans += x': '范围相同，`ans += {x}` → {ans}',
        'return ans': '范围最大的数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='边遍历边维护最大范围：更大就重置，相等就累加',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['整数的==数字范围==：最大数字 − 最小数字，如 `5724` 的范围是 `7 − 2 = 5`',
                 '求所有数字范围等于==最大范围==的整数之和',
                 '示例：`[5724,111,350]` → `6074`（5724 与 350 的范围都是 5）'],
        quote='遍历的同时，维护数字范围的最大值 maxRange。如果 nums[i] 的数字范围比 maxRange 还大，那么更新 maxRange，同时重置答案为 nums[i]（重新累加）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不必先找最大范围再求和，一趟遍历就够',
              '范围更大：`max_range = r`，`ans = x` 重新累加',
              '范围相等：`ans += x`；更小：什么都不做'],
        summary=['时间 `O(n log U)`，空间 `O(1)`，`U` 是最大值',
                 '更大时是 `ans = x`（重置），不是 `ans += x`',
                 '范围为 0 的数（如 111）在全体范围都是 0 时也会被累加',
                 '灵神另给了不用字符串的写法：`divmod(v, 10)` 逐位取最大最小数字'],
    ),
)
