CONFIG = dict(
    num=1913, title='两个数对之间的最大乘积差', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序 · 最大两数乘积减最小两数乘积（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def maxProductDifference(self, a: List[int]) -> int:
        a.sort()
        n = len(a)
        return a[n - 1] * a[n - 2] - a[0] * a[1]
''',
    call='Solution().maxProductDifference([5,6,2,7,4])',
    expect=34,
    views=[
        dict(type='text', fn=lambda S: ('先把数组从小到大排好' if 'n' not in S else f"最大两个：`{S['a'][-1]} × {S['a'][-2]}` = {S['a'][-1]*S['a'][-2]}　最小两个：`{S['a'][0]} × {S['a'][1]}` = {S['a'][0]*S['a'][1]}"), size=30),
        dict(type='array', var='a', label='a（绿 = 最大两个，粉 = 最小两个）', cell=110, h=300,
             color=lambda S, k, v: ('pink' if k < 2 else 'green' if k >= len(S['a']) - 2 else None) if 'n' in S else None),
        dict(type='text', fn=lambda S: ('' if 'n' not in S else f"乘积差 = {S['a'][-1]*S['a'][-2]} − {S['a'][0]*S['a'][1]} = =={S['a'][-1]*S['a'][-2]-S['a'][0]*S['a'][1]}=="), size=30),
    ],
    watch=[('n', 'n')],
    captions={
        'a.sort()': '排序后：`{a}`，最小的数在最左，最大的在最右',
        'n = len(a)': '`n = {n}`，最大两个数的下标是 `n-1`、`n-2`',
        'return a[n - 1]': '数都是正数：被减数越大越好 → ==最大两数相乘==；减数越小越好 → ==最小两数相乘==。`{a[n-1]}×{a[n-2]} − {a[0]}×{a[1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='乘积差要最大：最大两数之积，减去最小两数之积',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['选 4 个不同下标，组成两个数对 `(a,b)`、`(c,d)`',
                 '乘积差 = `a*b - c*d`，求最大值',
                 '示例：`[5,6,2,7,4]` → `6*7 - 2*4 = 34`'],
        quote='sort.Ints(a); n := len(a); return a[n-1]*a[n-2] - a[0]*a[1]',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['数全是正数，所以乘积越大越好、被减的乘积越小越好',
              '排序后，最大的两个数在末尾，最小的两个数在开头',
              '直接算 `a[n-1]*a[n-2] - a[0]*a[1]`'],
        after=[dict(heading='为什么只看这四个数', lines=[
            '乘积差 = 第一对乘积 − 第二对乘积',
            '都是正数：第一对取最大的两个，乘积最大',
            '第二对取最小的两个，乘积最小，差就最大',
            '排序一步就把这四个数放到了两端'])],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Ints(a)` 对应 `a.sort()`）',
                 '时间 `O(n log n)`；一趟扫描维护四个数可以做到 `O(n)`',
                 '易错：`nums[i] >= 1`，全是正数，这个贪心才成立',
                 '题目保证 `n >= 4`，所以两对下标不会重叠'],
    ),
)
