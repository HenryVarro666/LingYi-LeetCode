CONFIG = dict(
    num='LCP 17', title='速算机器人', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 直接模拟',
    code='''
class Solution(object):
    def calculate(self, s):

        x, y = 1, 0
        for char in s:
            if char == 'A':
                x = x + x + y
            else:
                y = y + y + x
        
        return x + y
''',
    call="Solution().calculate('AABBA')",
    expect=32,
    views=[
        dict(type='string', var='s', label='指令 s（A 改 x，B 改 y）', h=200,
             color=lambda S, i, v: 'blue' if v == 'A' else 'pink'),
        dict(type='text', fn=lambda S: f"x = ==`{S['x']}`==，y = ==`{S['y']}`==，x + y = {S['x'] + S['y']}" if 'x' in S else '', size=40),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'char'],
    captions={
        'x, y = 1, 0': '机器人初始 `x = 1, y = 0`',
        'for char in s': '读下一条指令：`{char}`',
        "if char == 'A'": '指令是 `{char}`：{"A 指令，更新 x" if char == "A" else "B 指令，更新 y"}',
        'x = x + x + y': 'A 指令：`x = x + x + y` = =={x}==（用的是旧的 x、y）',
        'y = y + y + x': 'B 指令：`y = y + y + x` = =={y}==（用的是旧的 x、y）',
        'return x + y': '指令执行完，返回 `x + y = {x} + {y}` = =={x + y}==',
    },
    cards=dict(
        one_liner='指令很短，一趟遍历直接模拟',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['机器人有两个参数 `x=1, y=0`，指令 `A`：`x = 2x + y`，指令 `B`：`y = 2y + x`',
                 '按顺序执行字符串 `s` 的每条指令，求最后的 `x + y`',
                 '本视频：`AABBA` → `32`'],
        quote='由于指令长度很短，那么一趟遍历，模拟计算过程就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用找规律，题目怎么说就怎么算',
              '`x + x + y` 右边用的是更新前的值，所以单个赋值就够，不需要临时变量'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：A 只改 x，B 只改 y，别两个都改',
                 '原文为 Python 2 风格的类写法，在 Python 3 下可直接运行，未改动'],
    ),
)
