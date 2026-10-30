CONFIG = dict(
    num=3232, title='判断是否可以赢得数字游戏', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 比较两个和',
    code='''
class Solution(object):
    def canAliceWin(self, nums):

        x = y = 0
        for v in nums:
            if v < 10:
                x += v
            else:
                y += v
        
        return x != y
''',
    call='Solution().canAliceWin([5,5,5,25])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 个位数，橙 = 两位数）', h=220, pointers={},
             color=lambda S, i, v: 'green' if v < 10 else 'orange',
             dim=lambda S, i, v: 'v' in S and 'x' in S and False),
        dict(type='text', fn=lambda S: f"个位数之和 `x = {S.get('x', 0)}`，两位数之和 `y = {S.get('y', 0)}`", size=32, h=100),
    ],
    watch=[('v', 'v', 'blue'), ('x 个位和', 'x', 'green'), ('y 两位和', 'y', 'orange')],
    captions={
        'x = y = 0': '`x` 记个位数之和，`y` 记两位数之和，都从 0 开始',
        'if v < 10': '`v = {v}`：小于 10 吗？{"是个位数，累加到 x" if v < 10 else "是两位数，累加到 y"}',
        'x += v': '个位数 `{v}` 加到 `x` → ==x = {x}==',
        'y += v': '两位数 `{v}` 加到 `y` → ==y = {y}==',
        'return x != y': '`x = {x}`，`y = {y}`：{"不相等" if x != y else "相等"} → Alice {"能赢" if x != y else "赢不了"}，返回 ==`{ret}`==',
    },
    cards=dict(
        one_liner='Alice 自由选择，只输在两个和恰好相等',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 选所有个位数或所有两位数，剩下的归 Bob，和严格大者赢',
                 '问 Alice 是否能赢',
                 '本视频：`[5,5,5,25]` → `true`（选两位数 25 > 15）'],
        quote='alice只输一手个位数之和恰好等于两位数之和。',
        quote_src='—— yiduobo 题解原文',
        idea=['个位数之和大就选个位数，两位数之和大就选两位数',
              '所以==只有两个和相等==时 Alice 才会输',
              '一趟遍历算出两个和，返回 `x != y`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：严格大于，相等时 Alice 输',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 `s1 − s2` 一个变量；yiduobo 分开存两个和再比较'],
    ),
)
