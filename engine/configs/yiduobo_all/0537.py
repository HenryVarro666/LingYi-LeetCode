CONFIG = dict(
    num=537, title='复数乘法', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按定义拆实部虚部相乘',
    tags=[],
    code='''
class Solution(object):
    def complexNumberMultiply(self, a, b):

        x1, y1 = a.replace('i', '').split('+')
        x2, y2 = b.replace('i', '').split('+')
        x3 = int(x1) * int(x2) - int(y1) * int(y2)
        y3 = int(x1) * int(y2) + int(y1) * int(x2)
        return '%d+%di' % (x3, y3)
''',
    call='Solution().complexNumberMultiply("2+3i", "1+1i")',
    expect='-1+5i',
    views=[
        dict(type='text', fn=lambda S: ('`a = "%s"`，`b = "%s"`' % (S['a'], S['b'])) if 'a' in S else '', size=34, h=70),
        dict(type='text', fn=lambda S: ('`a = %s + %si`' % (S['x1'], S['y1'])) if 'x1' in S else '', size=38, h=70),
        dict(type='text', fn=lambda S: ('`b = %s + %si`' % (S['x2'], S['y2'])) if 'x2' in S else '', size=38, h=70),
        dict(type='text', fn=lambda S: ('实部 `x3 = x1×x2 − y1×y2 = %s×%s − %s×%s` = ==%d==' % (S['x1'], S['x2'], S['y1'], S['y2'], S['x3'])) if 'x3' in S else '', size=30, h=70),
        dict(type='text', fn=lambda S: ('虚部 `y3 = x1×y2 + y1×x2 = %s×%s + %s×%s` = ==%d==' % (S['x1'], S['y2'], S['y1'], S['x2'], S['y3'])) if 'y3' in S else '', size=30, h=70),
    ],
    watch=[('x1', 'x1', 'blue'), ('y1', 'y1', 'blue'), ('x2', 'x2', 'pink'), ('y2', 'y2', 'pink'), ('x3', 'x3', 'green'), ('y3', 'y3', 'green')],
    captions={
        'x1, y1 =': '去掉 `i` 再按 `+` 切开：`a = "{a}"` → 实部 `x1 = {x1}`，虚部 `y1 = {y1}`',
        'x2, y2 =': '同样拆开 `b = "{b}"` → `x2 = {x2}`，`y2 = {y2}`',
        'x3 =': '实部：`(x1 + y1·i)(x2 + y2·i)` 里 `i² = -1`，所以 `x1·x2 − y1·y2` = =={x3}==',
        'y3 =': '虚部：两个交叉项相加 `x1·y2 + y1·x2` = =={y3}==',
        'return ': '按 `%d+%di` 拼接：=={ret}==（虚部为负时会出现 `+-`，题目要求就是这样）',
    },
    cards=dict(
        one_liner='直接按复数乘法的定义，拆出实部虚部各算一遍',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['复数写成 `"实部+虚部i"`，`i² = -1`，求两个复数的乘积，输出同样格式',
                 '示例：`"1+1i" × "1+1i"` → `"0+2i"`',
                 '本视频：`"2+3i" × "1+1i"` → `"-1+5i"`'],
        quote='比较基础的题目，题目还很贴心地不需要判断0的情况，直接按定义做就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(x1 + y1 i)(x2 + y2 i) = x1x2 + (x1y2 + y1x2) i + y1y2 i²`',
              '`i² = -1`：实部 `= x1x2 − y1y2`，虚部 `= x1y2 + y1x2`',
              '字符串里 `+` 只有一个（负号带在数字上），去掉 `i` 后按 `+` 切成两半'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：实部是 ==减==（`i² = -1`），虚部才是加',
                 '`"1+-1i"` 里虚部带负号，按 `+` 切开仍然只有两段',
                 '原文为 Python 2 风格，但本题代码无需任何修改',
                 '对比灵神：灵神借助 Go 内置复数类型，这里手工拆成实部虚部'],
    ),
)
