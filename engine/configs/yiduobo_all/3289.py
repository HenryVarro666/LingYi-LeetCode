CONFIG = dict(
    num=3289, title='数字小镇中的捣蛋鬼', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='求和 + 平方和 · 枚举 x',
    code='''
class Solution(object):
    def getSneakyNumbers(self, nums):

        s, t = 0, 0
        for v in nums:
            s += v
            t += v * v
        
        n = len(nums) - 2
        s -= n * (n - 1) // 2
        t -= (n - 1) * n * (n * 2 - 1) // 6
        for x in range(n):
            y = s - x
            if x * x + y * y == t:
                return [x, y]
        
        return []
''',
    call='Solution().getSneakyNumbers([0,3,2,1,3,2])',
    expect=[2, 3],
    views=[
        dict(type='array', var='nums', label='nums（0..n-1 加上两个重复数）', h=200,
             color=lambda S, i, v: 'blue' if S['_line'] in (6, 7) and v == S.get('v') else None),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"`s` = =={S['s']}==，`t` = =={S['t']}==" + (f"（= x+y、x²+y²）" if S['_line'] >= 11 else '')),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"试 `x = {S['x']}`：`y = {S['y']}`，`x²+y² = {S['x']**2+S['y']**2}`，目标 `t = {S['t']}`" if 'y' in S else ''),
    ],
    watch=['s', 't', 'n', ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        's, t = 0, 0': '`s` 记元素和，`t` 记元素平方和',
        's += v': '`s` = `{B.s} + {v}` = {s}',
        't += v * v': '`t` = `{B.t} + {v}²` = {t}',
        'n = len(nums) - 2': '==注意 n 要减 2==：多出两个重复数，`n = {n}`，原本是 `0..{n-1}`',
        's -= n': '去掉 `0+…+(n−1) = {n*(n-1)//2}`，剩下 `s = x + y` = =={s}==',
        't -= (n - 1)': '去掉 `0²+…+(n−1)² = {(n-1)*n*(n*2-1)//6}`，剩下 `t = x² + y²` = =={t}==',
        'for x in range': '暴力枚举 `x = {x}`（范围 `0..{n-1}`）',
        'y = s - x': '`y = s − x = {s} − {x}` = {y}',
        'if x * x + y * y == t': '检测 `{x}² + {y}² = {x*x+y*y}` 是否等于 `t = {t}`：{"==等于，找到了==" if x*x+y*y == t else "不等，换下一个 x"}',
        'return [x, y]': '捣蛋鬼就是 `{x}` 和 `{y}`，返回 =={ret}==',
    },
    cards=dict(
        one_liner='求和得到 x+y，平方和得到 x²+y²，再枚举 x 验证',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字 `0..n-1` 各出现一次，其中两个数多出现了一次',
                 '找出这两个重复的数',
                 '示例：`[0,3,2,1,3,2]` → `[2,3]`'],
        quote='现在有两个出现了两次的数字x和y，那么就需要至少两个方程。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想只有一个重复数 x：`s − n(n−1)/2` 就是 x',
              '两个未知数要两个方程：`x+y` 和 `x²+y²`',
              '不去解根式，直接枚举 `x`，看有没有对应的 `y` 满足平方和'],
        summary=['时间 `O(n)`，空间 `O(1)`（枚举 x 也是 `O(n)`）',
                 '易错点：`n = len(nums) − 2`，不是 `len(nums)`',
                 '原文提到也可以用哈希表计数，是最直观的 `O(n)` 空间做法',
                 '原文为 Python 2 风格写法，代码无需改动（整数除法本来就是 `//`）'],
    ),
)
