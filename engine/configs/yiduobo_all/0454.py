_last = [None]


def _p(x):
    return f'({x})' if x < 0 else str(x)


def _loop(var, arr, tag, inner, done):
    def f(S, B, ret):
        prev = _last[0]
        _last[0] = tag
        if prev == inner and S[var] == B[var]:
            return done
        return f'从 {arr} 取 `{var} = {S[var]}`'
    return f


def _body(tag, fn):
    def f(S, B, ret):
        _last[0] = tag
        return fn(S, B, ret)
    return f


def _ptr(arr, var, color):
    return dict(type='array', var=arr, label=arr, cell=90, h=115,
                color=lambda S, i, v, a=arr, x=var, c=color: c if _active(S, a) and x in S and S[a][i] == S[x] else None)


def _active(S, arr):
    """A/B 在第一段循环里亮，C/D 在第二段循环里亮"""
    second = 'res' in S
    return (arr in ('C', 'D')) == second


def _txt(S):
    if 'res' not in S:
        if 'num2' in S:
            return f'`num1 + num2 = {S["num1"]} + {S["num2"]} = {S["num1"] + S["num2"]}`，计入 sum'
        return '第一段：统计 A、B 所有组合的和'
    if 'num2' in S and S.get('_line') in (11, 12):
        x = S['num1'] + S['num2']
        return f'`x = {S["num1"]} + {S["num2"]} = {x}`，查 `sum[{-x}]` = =={S["sum"].get(-x, 0)}=='
    return '第二段：枚举 C、D，查 −x 出现的次数'


CONFIG = dict(
    num=454, title='四数相加 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='A+B 组合计数 · C+D 查 −x',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def fourSumCount(self, A, B, C, D):

        sum = {}
        for num1 in A:
            for num2 in B:
                sum[num1 + num2] = sum.get(num1 + num2, 0) + 1

        res = 0
        for num1 in C:
            for num2 in D:
                res += sum.get(-num1 - num2, 0)

        return res
''',
    call='Solution().fourSumCount([1,2], [-2,-1], [-1,2], [0,2])',
    expect=2,
    views=[
        _ptr('A', 'num1', 'blue'),
        _ptr('B', 'num2', 'pink'),
        _ptr('C', 'num1', 'blue'),
        _ptr('D', 'num2', 'pink'),
        dict(type='map', var='sum', label='sum（组合值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', fn=_txt, size=28, h=70),
    ],
    watch=[('num1', 'num1', 'blue'), ('num2', 'num2', 'pink'), ('res', 'res', 'green')],
    captions={
        'sum = {}': '`sum`：A、B 两两组合后，==每种和出现的次数==',
        'for num1 in A': _loop('num1', 'A', 'o1', 'i1', 'A 枚举完，所有组合统计好了'),
        'for num2 in B': _loop('num2', 'B', 'i1', 'b1', 'B 走完一轮，换下一个 `num1`'),
        'sum[num1 + num2]': _body('b1', lambda S, B, ret: f'组合值 `{S.num1} + {_p(S.num2)} = {S.num1 + S.num2}` 又出现一次 → `sum[{S.num1 + S.num2}] = {S.sum[S.num1 + S.num2]}`'),
        'res = 0': '统计完 A、B 的所有组合；`res` 开始累计答案',
        'for num1 in C': _loop('num1', 'C', 'o2', 'i2', 'C 枚举完'),
        'for num2 in D': _loop('num2', 'D', 'i2', 'b2', 'D 走完一轮，换下一个 `num1`'),
        'res += sum.get': _body('b2', lambda S, B, ret: (f'`x = {S.num1 + S.num2}`：A、B 的组合中 `−x = {-S.num1 - S.num2}` 出现 `{S.res - B.res}` 次 → `res = {S.res}`'
                                                         if S.res > B.res else f'`x = {S.num1 + S.num2}`：A、B 的组合里没有 `{-S.num1 - S.num2}` → 加 0，`res` 仍为 {S.res}')),
        'return res': '共 =={ret}== 个元组',
    },
    cards=dict(
        one_liner='A、B 两两组合存 dict，C、D 组合去查相反数',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['四个长度都为 n 的数组 A、B、C、D，各选一个元素使四数之和为 0',
                 '求满足条件的元组 `(i, j, k, l)` 个数',
                 '示例：`A=[1,2] B=[-2,-1] C=[-1,2] D=[0,2]` → `2`'],
        quote='如果将A和B，C和D两两组合，那么就相当于从两个长度不超过25000的数组中各选取一个元素，使他们的和等于0。对于这个问题，很自然就想到==用dict来统计每种组合值出现的次数==。',
        quote_src='—— yiduobo 题解原文',
        idea=['和第 18 题四数之和不同：这里==每个数组必须各选一个==',
              'A、B 两两组合变成一个「数组」，C、D 同理 → 退化成两数之和',
              '枚举 C、D 的和 x，`sum.get(−x, 0)` 就是能配对的个数'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '`sum.get(key, 0)`：没出现过的组合值按 0 次处理',
                 '注意原文变量名 `sum` 覆盖了内置函数，这里只当 dict 用',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神用 `Counter` + 生成器写成两行，思路相同'],
    ),
)
