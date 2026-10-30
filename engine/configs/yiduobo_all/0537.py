CONFIG = dict(
    num=537, title='复数乘法', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按定义直接算',
    code='''
class Solution(object):
    def complexNumberMultiply(self, a, b):

        x1, y1 = a.replace('i', '').split('+')
        x2, y2 = b.replace('i', '').split('+')
        x3 = int(x1) * int(x2) - int(y1) * int(y2)
        y3 = int(x1) * int(y2) + int(y1) * int(x2)
        return '%d+%di' % (x3, y3)
''',
    call="Solution().complexNumberMultiply('1+-2i', '3+4i')",
    expect='11+-2i',
    views=[
        dict(type='string', var='a', label='a', h=150, cell=60),
        dict(type='string', var='b', label='b', h=150, cell=60),
        dict(type='text', size=34, h=120, fn=lambda S: (f"(`{S['x1']}` + `{S['y1']}`i) × (`{S['x2']}` + `{S['y2']}`i)" if 'y2' in S else '')),
        dict(type='text', size=34, h=120, fn=lambda S: (f"实部 `x3` = ==`{S['x3']}`==" if 'x3' in S else '') + (f"　虚部 `y3` = ==`{S['y3']}`==" if 'y3' in S else '')),
    ],
    watch=['x1', 'y1', 'x2', 'y2', ('x3', 'x3', 'green'), ('y3', 'y3', 'green')],
    captions={
        'x1, y1 =': '去掉 `i` 再按 `+` 切开：实部 `x1` = {x1}，虚部 `y1` = {y1}',
        'x2, y2 =': '同样处理 b：实部 `x2` = {x2}，虚部 `y2` = {y2}',
        'x3 =': '实部 = 实×实 − 虚×虚（因为 `i^2 = -1`）：`{x1}×{x2} − ({y1})×({y2})` = =={x3}==',
        'y3 =': '虚部 = 实×虚 + 虚×实：`{x1}×{y2} + ({y1})×{x2}` = =={y3}==',
        'return': '按 `实部+虚部i` 格式拼回字符串：`{ret}`',
    },
    cards=dict(
        one_liner='把字符串拆成实部虚部，按乘法定义算',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['复数写成 `"实部+虚部i"`，`i^2 = -1`',
                 '给两个复数字符串，返回乘积的字符串',
                 '示例：`"1+1i" × "1+1i"` → `"0+2i"`；本视频用 `1+-2i`、`3+4i`'],
        quote='比较基础的题目，题目还很贴心地不需要判断0的情况，直接按定义做就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(x1 + y1 i)(x2 + y2 i)` 展开，`i^2` 换成 `-1`',
              '实部 `x1x2 − y1y2`，虚部 `x1y2 + y1x2`',
              '输入一定形如 `a+bi`，负数写成 `1+-1i`，用 `+` 切开没有歧义'],
        after=[dict(heading='手算验证', lines=['`(1 − 2i)(3 + 4i)` = `3 + 4i − 6i − 8i^2`', '`i^2 = -1` → `3 + 8 + (4 − 6)i`', '= `11 − 2i`，输出 `"11+-2i"`', '虚部为负时仍然保留 `+-` 的写法'])],
        summary=['时间、空间都是常数',
                 '易错：虚部为负时输出 `0+-2i`，不能写成 `0-2i`',
                 '实部的减号别写成加号',
                 '原文本身是 Python 3 可运行的，代码未改动'],
    ),
)
