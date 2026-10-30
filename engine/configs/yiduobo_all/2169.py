CONFIG = dict(
    num=2169, title='得到 0 的操作数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='更相减损术 → 辗转相除',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def countOperations(self, num1, num2):

        x, y = num1, num2
        if x < y:
            x, y = y, x
        
        res = 0
        while y:
            res += x // y
            x, y = y, x % y
        
        return res
''',
    call='Solution().countOperations(3, 10)',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"`x = {S['x']}`（大），`y = {S['y']}`（小），累计 `res = {S['res']}`" if 'res' in S else (f"`x = {S['x']}`，`y = {S['y']}`" if 'x' in S else '')), size=36),
    ],
    watch=['num1', 'num2', ('x', 'x', 'orange'), ('y', 'y', 'cyan'), ('res', 'res', 'green')],
    captions={
        'x, y = num1, num2': '取 `x = {x}`，`y = {y}`',
        'if x < y': '`{x} < {y}` → {"成立，要让 x 是较大的" if x < y else "不成立"}',
        'x, y = y, x': '交换后 `x = {x}` 大，`y = {y}` 小',
        'res = 0': '`res` 累计减法次数',
        'while y': lambda S, B, r: (f'`y = {S.y}` 非零，继续' if S.y else '`y = 0`：算到头了，结束'),
        'res += x // y': '这一步的商 `{x} // {y} = {x//y}` 就是更相减损术要做的减法次数 → `res = {res}`',
        'x, y = y, x % y': '辗转相除：`({B.x}, {B.y})` → `({x}, {y})`',
        'return res': '所有商之和 = `{res}`',
    },
    cards=dict(
        one_liner='更相减损术的次数 = 辗转相除每一步的商之和',
        complexity='时间 `O(log max(x,y))`，空间 `O(1)`',
        problem=['每步用大数减小数，直到其中一个变成 0，求操作数',
                 '示例：`num1 = 10, num2 = 10` → `1`',
                 '本视频：`(3, 10)` → 3 轮商 `3 + 3` = `6`'],
        quote='题目描述的是我国古老的求最大公约数的算法更相减损术，问求出最大公约数所需要的计算次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目就是==更相减损术==，直接模拟会很慢',
              '连续减法等价于一次除法，商就是减法次数',
              '用辗转相除法，把每步的商累加'],
        summary=['时间 `O(log max(x,y))`，空间 `O(1)`',
                 '先保证 `x >= y`，之后每步 `x, y = y, x % y` 自然保持大小关系',
                 '原文为 Python 2 写法，`res += x / y` 的整数除法已改为 `//`',
                 '对比灵神：灵神靠交换处理 `x < y`，这里在开头先交换一次'],
    ),
)
