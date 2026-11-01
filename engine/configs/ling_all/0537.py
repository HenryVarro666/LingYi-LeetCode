def _c(z):
    return '%d%+di' % (int(z.real), int(z.imag))


CONFIG = dict(
    num=537, title='复数乘法', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='解析成复数再直接相乘（Go 原文转写）',
    tags=[],
    setup='''
import re
import types


def _parse_complex(s, bits=64):
    # 等价于 Go 的 strconv.ParseComplex：把 "实部+虚部i" 解析成复数
    m = re.fullmatch(r'([+-]?\\d+)\\+([+-]?\\d+)i', s)
    return complex(int(m.group(1)), int(m.group(2))), None


strconv = types.SimpleNamespace(ParseComplex=_parse_complex)
''',
    code='''
class Solution:
    def complexNumberMultiply(self, num1: str, num2: str) -> str:
        x, _ = strconv.ParseComplex(num1, 64)
        y, _ = strconv.ParseComplex(num2, 64)
        return "%d+%di" % (int((x * y).real), int((x * y).imag))
''',
    call='Solution().complexNumberMultiply("2+3i", "1+1i")',
    expect='-1+5i',
    views=[
        dict(type='text', fn=lambda S: ('`num1 = "%s"`，`num2 = "%s"`' % (S['num1'], S['num2'])) if 'num1' in S else '', size=34, h=70),
        dict(type='text', fn=lambda S: ('`x = ` ==%s==' % _c(S['x'])) if 'x' in S else '`x` 还没解析', size=40, h=80),
        dict(type='text', fn=lambda S: ('`y = ` ==%s==' % _c(S['y'])) if 'y' in S else '`y` 还没解析', size=40, h=80),
        dict(type='text', fn=lambda S: ('`x × y = ` ==%s==' % _c(S['x'] * S['y'])) if 'y' in S else '', size=40, h=80),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'x, _ = ': '`ParseComplex` 把 `"{num1}"` 解析成复数 `x = {x}`（Python 里虚部写成 `j`）',
        'y, _ = ': '同样解析 `"{num2}"` 得到 `y = {y}`',
        'return ': '`x*y = {x*y}`：实部 `{int((x*y).real)}`，虚部 `{int((x*y).imag)}`，按 `"%d+%di"` 拼成 =={ret}==',
    },
    cards=dict(
        one_liner='把字符串当成复数解析，乘完再按格式输出',
        complexity='时间 `O(1)`（字符串长度有常数上界），空间 `O(1)`',
        problem=['复数写成 `"实部+虚部i"`，`i² = -1`，求两个复数的乘积，输出同样格式',
                 '示例：`"1+1i" × "1+1i"` → `"0+2i"`',
                 '本视频：`"2+3i" × "1+1i"` → `"-1+5i"`'],
        quote='x, _ := strconv.ParseComplex(num1, 64) … return fmt.Sprintf("%d+%di", int(real(x*y)), int(imag(x*y)))',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['Go 标准库自带复数类型，`ParseComplex` 直接把字符串变成复数',
              '乘法交给语言：`x * y` 自动按 `(a+bi)(c+di)` 展开',
              '最后取 `real` 和 `imag` 转成整数，按题目格式拼回去'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Python 没有 `strconv.ParseComplex`（也不认 `i`），在 setup 里补了等价的解析函数，作者代码本身未改',
                 '`real(x*y)` → `(x * y).real`；`fmt.Sprintf` → `%` 格式化',
                 '时间 `O(1)`，空间 `O(1)`',
                 '虚部可以是负数，所以输出可能是 `"0+-2i"` 这种形式，格式串 `"%d+%di"` 不用特殊处理'],
    ),
)
