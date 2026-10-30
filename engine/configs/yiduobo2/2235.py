# ---- 自定义视图：数轴上画 num1（蓝箭头，从 0 出发）再接上 num2（粉箭头），终点就是和
TESTS = [(12, 5), (-10, 4)]
LO, HI = -14, 20


def _p(x):
    return f'({x})' if x < 0 else str(x)


def draw_line(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'num1' not in S:
        return
    a, b = S['num1'], S['num2']
    cv.text((x0 + 18, y0 + 4), '数轴：先走 num1（蓝），再走 num2（粉），停在哪里就是和', 24, T['muted'], bold=True)
    L, R = x0 + 50, x1 - 50
    Y = y0 + 250

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)
    cv.line([(L - 20, Y), (R + 20, Y)], T['border'], 3)
    for v in range(LO, HI + 1):
        big = v % 5 == 0
        cv.line([(X(v), Y - (10 if big else 5)), (X(v), Y + (10 if big else 5))], T['muted'] if big else T['dim'], 2)
        if big:
            cv.text((X(v), Y + 18), str(v), 20, T['muted'], anchor='mt', mono=True)
    cv.dashed((X(a), Y - 140), (X(a), Y), T['dim'], 2)
    cv.dashed((X(a + b), Y - 140), (X(a + b), Y), T['green'], 2)

    def label(xc, yb, s, c):
        w = cv.tlen(s, 24, bold=True, mono=True)
        cv.rect((xc - w / 2 - 6, yb - 32, xc + w / 2 + 6, yb + 2), fill=T['panel'], r=6)
        cv.text((xc, yb), s, 24, c, anchor='mb', bold=True, mono=True)
    cv.arrow((X(0), Y - 70), (X(a), Y - 70), T['blue'], 6, 16)
    label((X(0) + X(a)) / 2, Y - 82, f'num1 = {a}', T['blue'])
    cv.arrow((X(a), Y - 140), (X(a + b), Y - 140), T['pink'], 6, 16)
    label((X(a) + X(a + b)) / 2, Y - 152, f'num2 = {b}', T['pink'])
    cv.d.ellipse((X(a + b) - 12, Y - 12, X(a + b) + 12, Y + 12), fill=T['green'])
    cv.text((X(a + b), Y + 54), f'和 = {a + b}', 28, T['green'], anchor='mt', bold=True)
    cv.d.ellipse((X(0) - 7, Y - 7, X(0) + 7, Y + 7), fill=T['text'])


CONFIG = dict(
    num=2235, title='两整数相加', difficulty='Easy', category='数学',
    author='yiduobo', technique='一行 return',
    tags=['List.md', '字节30天'],
    code='''
class Solution(object):
    def sum(self, num1, num2):
        return num1 + num2
''',
    call=f'[Solution().sum{TESTS[0]}, Solution().sum{TESTS[1]}]',
    expect=[17, -6],
    views=[
        dict(type='text', fn=lambda S: f"`num1 + num2` = `{S['num1']} + {_p(S['num2'])}` = =={S['num1'] + S['num2']}=="
             if 'num1' in S else '', h=60),
        dict(type='custom', draw=draw_line, h=420),
    ],
    watch=['num1', 'num2'],
    captions={
        'return num1 + num2': lambda S, B, r: f'`{S.num1} + {_p(S.num2)}` = =={r}==，直接返回',
    },
    cards=dict(
        one_liner='A + B：一行 return 搞定',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你两个整数 `num1` 和 `num2`，返回它们的和',
                 '示例 1：`num1 = 12, num2 = 5` → `17`',
                 '示例 2：`num1 = -10, num2 = 4` → `-6`；数据范围 `-100 ≤ num ≤ 100`'],
        quote='想不到两千多题了突然冒出来这个，==一般的oj应该都是放在最开始的吧==。。',
        quote_src='—— yiduobo 题解',
        idea=['“A + B” 通常是 OJ 的第一题，用来熟悉输入输出和提交流程',
              '力扣只需要实现类里的方法：`return num1 + num2`',
              '负数也一样：`-10 + 4 = -6`，在数轴上就是往回走'],
        result='两个示例依次返回 `17` 和 `-6` ✓',
        after=[dict(heading='顺便看看 Python 2 风格', lines=[
            '`class Solution(object)`：Python 2 的新式类；Python 3 写不写 `(object)` 都一样',
            '原文用文档字符串标注类型；Python 3 可直接写注解 `num1: int`',
            '本题范围 `-100 ≤ num ≤ 100`，和不会溢出，任何语言直接相加都行',
        ])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '力扣的输入是参数、输出是返回值，不需要自己读写',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神借这题讲了评测机原理和本地测试方法'],
    ),
)
