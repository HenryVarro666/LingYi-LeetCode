CONFIG = dict(
    num='LCP 02', title='分式化简', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从后向前模拟连分数',
    tags=[],
    code='''
class Solution(object):
    def fraction(self, cont):

        x = 1
        y = cont[-1]

        for index in range(len(cont) - 2, -1, -1):
            x += y * cont[index]
            x, y = y, x

            a, b = x, y
            while b:
                a, b = b, a % b

            x //= a
            y //= a
        
        return [y, x]
''',
    call='Solution().fraction([3, 2, 0, 2])',
    expect=[13, 4],
    views=[
        dict(type='array', var='cont', pointers={'index': 'blue'}, h=170, label='cont（连分数的各项，从后向前处理）',
             color=lambda S, i, v: 'green' if 'index' in S and i > S['index'] else None),
        dict(type='text', size=34, fn=lambda S: (
            f"目前的值 = ==`{S['x']} / {S['y']}`==（分子 x，分母 y）" if 'x' in S and 'y' in S and S['y'] else '')),
        dict(type='text', size=28, fn=lambda S: (
            f"求 gcd：`a = {S['a']}, b = {S['b']}`" if 'b' in S and S['_line'] is not None and 'a' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'cyan'), ('y', 'y', 'pink'), 'a', 'b'],
    captions={
        'x = 1': '最内层是 `cont[-1]`，从它开始：分子 `x = 1`',
        'y = cont[-1]': '分母 `y = cont[-1] = {y}`，`x / y = 1 / {y}` 表示「`1 / cont[-1]`」这一层',
        'for index in': '从倒数第二项往前，每次把一项 `cont[index]` 加进来',
        'x += y * cont[index]': '`x/y` 是后面那一层，前面加上 `cont[{index}] = {cont[index]}`：通分得 `({cont[index]}·{B.y} + {B.x}) / {B.y}`，分子 `x` = {x}',
        'x, y = y, x': '这一层还要被 `1 / (…)` 包住 → 取倒数，分子分母交换：`x / y` = ==`{x} / {y}`==',
        'a, b = x, y': '准备用辗转相除求 `{x}` 和 `{y}` 的最大公约数',
        'while b': lambda S, B, r: (f'`b = {S.b}` 非零 → 继续辗转相除' if S.b else f'`b = 0` → 最大公约数 `a = {S.a}`'),
        'a, b = b, a % b': '`(a, b)` → `({a}, {b})`',
        'x //= a': '分子约分：`x` = =={x}==',
        'y //= a': '分母约分：`y` = =={y}==，这一层的分数是 `{x}/{y}`',
        'return [y, x]': '循环结束时 `x/y = {x}/{y}` 是 `1 / 整个连分数`，所以答案是倒数：返回 `[y, x]` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='连分数从最里面往外算，每步通分、颠倒、约分',
        complexity='时间 `O(n log M)`，空间 `O(1)`',
        problem=['`cont` 表示连分数 `cont[0] + 1/(cont[1] + 1/(…))`，每项非负，最后一项不为 0',
                 '返回化简后的最简分数 `[分子, 分母]`',
                 '示例：`cont=[3,2,0,2]` → `[13,4]`'],
        quote='设当前结果的分子为x，分母为y，那么x和y的初始值就是1和cont[-1]。接下来从倒数第二个cont开始向前遍历……x和y分别迭代成y和y * cont[index] + x。',
        quote_src='—— yiduobo 题解原文',
        idea=['手推公式太复杂，作者选择==从后向前模拟==整个计算过程',
              '当前 `x/y`，加上 `cont[index]` 再取倒数：新 `x/y = y/(y·c + x)`',
              '每步用 gcd 约分，数字不会越变越大；分母不会为 0'],
        summary=['时间 `O(n log M)`：每步一次辗转相除',
                 '返回 `[y, x]`：循环里每步都取了倒数，结束时 `x/y` 是答案的倒数',
                 '原文为 Python 2 写法，`x /= a`、`y /= a` 已改为整数除法 `//=`',
                 '易错点：先通分相加、再取倒数，顺序不能反'],
    ),
)
