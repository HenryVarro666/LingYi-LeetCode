# ---- 自定义视图：画出“力扣评测机怎么调用你的代码”（灵神题解答疑的内容），当前测试数据和返回值实时填进去
TESTS = [((12, 5), 17), ((-10, 4), -6)]


def _p(x):
    return f'({x})' if x < 0 else str(x)


def _case(S):
    a, b = S.get('num1'), S.get('num2')
    for k, ((x, y), want) in enumerate(TESTS):
        if (x, y) == (a, b):
            return k, want
    return None, None


def draw_judge(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    k, want = _case(S)
    cv.text((x0 + 18, y0 + 4), '力扣评测机内部（你看不到的 main 函数）', 24, T['muted'], bold=True)
    boxes = [('for 每个测试数据', T['purple']), ('obj = Solution()', T['cyan']),
             ('ret = obj.sum(num1, num2)', T['orange']), ('ret == 正确答案 ?', T['green'])]
    bx0, bw, bh, gap = x0 + 40, x1 - x0 - 80, 62, 34
    y = y0 + 50
    for i, (txt, c) in enumerate(boxes):
        hot = i == 2
        cv.rect((bx0, y, bx0 + bw, y + bh), fill=T['panel2'], outline=c, width=4 if hot else 2, r=12)
        cv.text((bx0 + 24, y + bh / 2), txt, 26, c if hot else T['text'], anchor='lm', bold=True, mono=True)
        if i == 0 and k is not None:
            cv.text((bx0 + bw - 20, y + bh / 2), f'示例 {k + 1}：num1 = {S["num1"]}, num2 = {S["num2"]}', 22,
                    T['muted'], anchor='rm', mono=True)
        if i == 1:
            cv.text((bx0 + bw - 20, y + bh / 2), '每个数据都新建一个对象', 20, T['muted'], anchor='rm')
        if i == 2:
            cv.text((bx0 + bw - 20, y + bh / 2), '← 你只需要写这个方法', 22, T['orange'], anchor='rm', bold=True)
        if i == 3 and k is not None:
            got = S['num1'] + S['num2']
            cv.text((bx0 + bw - 20, y + bh / 2), f'{got} == {want}  通过', 24, T['green'], anchor='rm', bold=True, mono=True)
        if i < len(boxes) - 1:
            cx = bx0 + bw / 2
            cv.arrow((cx, y + bh + 2), (cx, y + bh + gap - 4), T['muted'], 3, 11)
        y += bh + gap


CONFIG = dict(
    num=2235, title='两整数相加', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='梦开始的地方 · 只写核心逻辑',
    tags=['List.md', '字节30天'],
    code='''
# 请选择 Python3 提交代码，而不是 Python（即 Python2），后者已经被淘汰了
class Solution:
    def sum(self, num1: int, num2: int) -> int:
        return num1 + num2
''',
    call=f'[Solution().sum{TESTS[0][0]}, Solution().sum{TESTS[1][0]}]',
    expect=[17, -6],
    views=[
        dict(type='text', fn=lambda S: f"`num1 + num2` = `{S['num1']} + {_p(S['num2'])}` = =={S['num1'] + S['num2']}=="
             if 'num1' in S else '', h=60),
        dict(type='custom', draw=draw_judge, h=440),
    ],
    watch=['num1', 'num2'],
    captions={
        'return num1 + num2': lambda S, B, r: (f'示例 {_case(S)[0] + 1}：评测机调用 `sum({S.num1}, {S.num2})`，'
                                               f'我们返回 `{S.num1} + {_p(S.num2)}` = =={r}=='),
    },
    cards=dict(
        one_liner='梦开始的地方：只需编写核心逻辑，返回正确结果',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你两个整数 `num1` 和 `num2`，返回它们的和',
                 '示例 1：`num1 = 12, num2 = 5` → `17`',
                 '示例 2：`num1 = -10, num2 = 4` → `-6`；数据范围 `-100 ≤ num ≤ 100`'],
        before=[dict(heading='问：为什么没有 main 函数？', lines=[
            '力扣评测机内部有 `main` 函数，会调用你写的 `sum` 方法，传入测试数据',
            '然后判断 `sum` 的==返回值==是否等于正确答案',
            '对于所有测试数据，返回值都正确 → 判定通过',
        ])],
        quote='力扣评测机内部有 main 函数，里面会调用你写的 sum 函数（方法）……所以，我们==只需编写核心逻辑==，保证返回结果计算正确即可。',
        quote_src='—— 灵茶山艾府题解「答疑」',
        idea=['核心逻辑只有一行：`return num1 + num2`',
              '不用自己读输入、打印输出：==参数就是输入，返回值就是输出==',
              '代码第一行注释：请选择 ==Python3== 提交，Python2 已经被淘汰了'],
        result='两个示例依次返回 `17` 和 `-6` ✓',
        after=[dict(heading='如何在本地测试代码？', lines=[
            '在 `Solution` 类的下面自己写调用代码：',
            '`print(Solution().sum(12, 5))   # 示例 1`',
            '`print(Solution().sum(-10, 4))  # 示例 2`',
            '力扣评测机对==每个测试数据==，都会重新创建一个 `Solution` 对象',
        ])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '力扣只要求实现类里的方法：参数是输入，返回值是输出',
                 '易错：不要 `print` 结果来代替 `return`',
                 '数据范围很小，Python 整数也不存在溢出问题'],
    ),
)
