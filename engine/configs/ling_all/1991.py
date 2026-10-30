CONFIG = dict(
    num=1991, title='找到数组的中间位置', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 2·左和 = 总和 − 当前', tags=['数学算法'],
    code='''
class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        s = sum(nums)
        left_s = 0
        for i, x in enumerate(nums):
            if left_s * 2 == s - x:
                return i
            left_s += x
        return -1
''',
    call='Solution().findMiddleIndex([2,3,-1,8,4])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"左和 `{S['left_s']}`，右和 = `{S['s']} − {S['x']} − {S['left_s']}` = =={S['s']-S['x']-S['left_s']}==" if S.get('_line') == 6 and 'x' in S else '右和 = 总和 − 左和 − 当前数'),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['i'] else 'cyan' if i < S['i'] else None) if 'i' in S else None),
    ],
    watch=['s', ('left_s', 'left_s', 'cyan'), ('x', 'x', 'blue')],
    captions={
        's = sum': '先求总和 `s = {s}`，右侧和就能用 `s − x − left_s` 得到',
        'left_s = 0': '`left_s` 记录 `i` 左侧元素和，一开始左边没有元素：0',
        'if left_s * 2': '`left_s*2 = {left_s*2}`，`s − x = {s-x}`：左右和相等 ⇔ `2·left_s = s − x` → {"成立，找到最左中间位置" if left_s*2==s-x else "不等，继续"}',
        'left_s += x': '把 `{x}` 并入左侧和：`left_s` = {left_s}',
        'return -1': '遍历完都没有平衡点，返回 -1',
        'return i': '`i = {i}` 左右和相等，且是最先遇到的 → 最左中间位置',
    },
    cards=dict(
        one_liner='左和 × 2 = 总和 − 当前数，一遍扫描就能判断',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最左的下标 `i`，使 `i` 左边之和 = 右边之和（空段和为 0）',
                 '示例：`[2,3,-1,8,4]` → `3`（左 4，右 4）'],
        quote='由于左侧元素和等于右侧元素和，所以有 2·leftS = s − nums[i]。从左到右遍历数组，一边遍历，一边累加元素更新 leftS。',
        quote_src='—— 灵茶山艾府题解',
        idea=['右侧和 = 总和 − 当前数 − 左侧和，不用再算一遍后缀', '等式两边化成 `left_s*2 == s - x`，只需维护 `left_s`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先检查再累加：`left_s` 必须不含当前数 `x`',
                 '从左往右扫，第一个满足的就是最左下标',
                 '同类：2574、724，前后缀分解专题'],
    ),
)
