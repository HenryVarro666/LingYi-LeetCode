A1 = [1, -2, -5, 0, 10]
A2 = [0, -2, -1, -7, -4]


def _tbl(S):
    g = lambda k: S.get(k, 0)
    return [[g('max_a'), g('min_a'), g('max_a') - g('min_a')],
            [g('max_b'), g('min_b'), g('max_b') - g('min_b')],
            [g('max_c'), g('min_c'), g('max_c') - g('min_c')],
            [g('max_d'), g('min_d'), g('max_d') - g('min_d')]]


def _q(v):
    return f'({v})' if v < 0 else str(v)


def _forms(S):
    return ('a = arr1 + arr2 + i　　b = arr1 + arr2 − i　　c = arr1 − arr2 + i　　d = arr1 − arr2 − i')


CONFIG = dict(
    num=1131, title='绝对值表达式的最大值', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='拆绝对值 · 四组 max−min',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxAbsValExpr(self, arr1, arr2):

        n = len(arr1)
        max_a = min_a = arr1[0] + arr2[0]
        max_b = min_b = arr1[0] + arr2[0]
        max_c = min_c = arr1[0] - arr2[0]
        max_d = min_d = arr1[0] - arr2[0]
        for index in range(1, n):
            a = arr1[index] + arr2[index] + index
            max_a = max(max_a, a)
            min_a = min(min_a, a)

            b = arr1[index] + arr2[index] - index
            max_b = max(max_b, b)
            min_b = min(min_b, b)

            c = arr1[index] - arr2[index] + index
            max_c = max(max_c, c)
            min_c = min(min_c, c)

            d = arr1[index] - arr2[index] - index
            max_d = max(max_d, d)
            min_d = min(min_d, d)

        return max(max_a - min_a, max_b - min_b, max_c - min_c, max_d - min_d)
''',
    call=f'Solution().maxAbsValExpr({A1!r}, {A2!r})',
    expect=20,
    max_steps=90,
    views=[
        dict(type='array', var='arr1', label='arr1', h=150, cell=70, pointers={'index': 'blue'}, color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='arr2', label='arr2', h=130, cell=70, color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='text', fn=_forms, size=22, h=50),
        dict(type='table', var=_tbl, label='四个式子在 0..index 上的最大 / 最小 / 差（max−min）', h=270, cell=70,
             rows=['a', 'b', 'c', 'd'], cols=['max', 'min', '差']),
    ],
    watch=[('index', 'index', 'blue'), ('a', 'a', 'cyan'), ('b', 'b', 'orange'), ('c', 'c', 'pink'), ('d', 'd', 'purple')],
    captions={
        'n = len(arr1)': '`n = {n}`',
        'max_a = min_a': '从下标 0 开始：`a₀ = arr1[0] + arr2[0] + 0` = `{max_a}`，最大最小值都先取它',
        'max_b = min_b': '`b₀ = arr1[0] + arr2[0] − 0` = `{max_b}`',
        'max_c = min_c': '`c₀ = arr1[0] − arr2[0] + 0` = `{max_c}`',
        'max_d = min_d': '`d₀ = arr1[0] − arr2[0] − 0` = `{max_d}`',
        'for index in range': lambda S, B, r: ('所有下标都扫过了，循环结束' if B.get('index') == S.index else f'扫描下标 `{S.index}`：为四个式子各算一个值'),
        'a = arr1': lambda S, B, r: f'`a = {_q(S.arr1[S.index])} + {_q(S.arr2[S.index])} + {S.index}` = =={S.a}==（对应 s1 / s8）',
        'b = arr1': lambda S, B, r: f'`b = {_q(S.arr1[S.index])} + {_q(S.arr2[S.index])} − {S.index}` = =={S.b}==（对应 s2 / s7）',
        'c = arr1': lambda S, B, r: f'`c = {_q(S.arr1[S.index])} − {_q(S.arr2[S.index])} + {S.index}` = =={S.c}==（对应 s3 / s6）',
        'd = arr1': lambda S, B, r: f'`d = {_q(S.arr1[S.index])} − {_q(S.arr2[S.index])} − {S.index}` = =={S.d}==（对应 s4 / s5）',
        'max_a = max': '和旧最大值比，`max_a` = =={max_a}==',
        'min_a = min': '和旧最小值比，`min_a` = =={min_a}==',
        'max_b = max': '和旧最大值比，`max_b` = =={max_b}==',
        'min_b = min': '和旧最小值比，`min_b` = =={min_b}==',
        'max_c = max': '和旧最大值比，`max_c` = =={max_c}==',
        'min_c = min': '和旧最小值比，`min_c` = =={min_c}==',
        'max_d = max': '和旧最大值比，`max_d` = =={max_d}==',
        'min_d = min': '和旧最小值比，`min_d` = =={min_d}==',
        'return max(': '每组取 `max − min` 再取最大：`{max_a-min_a}, {max_b-min_b}, {max_c-min_c}, {max_d-min_d}` → =={ret}==',
    },
    cards=dict(
        one_liner='把绝对值拆开：8 种符号只剩 4 组 max − min',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给两个等长数组，求 `|arr1[i]−arr1[j]| + |arr2[i]−arr2[j]| + |i−j|` 的最大值',
                 '`0 <= i, j < n`，`n` 最多 40000，要 `O(n)`',
                 '本视频：`arr1 = [1,-2,-5,0,10]`，`arr2 = [0,-2,-1,-7,-4]`'],
        quote='可以发现，括号里面的构成形式是一致的，仅有下标的区别。……最终答案就是 max(max(a) - min(a), max(b) - min(b), max(c) - min(c), max(d) - min(d))',
        quote_src='—— yiduobo 题解原文',
        idea=['三个绝对值展开有 8 种符号组合，其中 4 种是另 4 种的相反数',
              '剩下的 4 种都是 `f(i) − f(j)` 的形式：`a b c d` 四组',
              '每组只要扫一遍求最大、最小，差最大的就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不需要真的去判断 `i`、`j` 的大小：不合法的组合只会更小，取最大值不受影响',
                 '用 `max − min` 同时覆盖了 `i > j` 与 `i < j` 两种情况',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
