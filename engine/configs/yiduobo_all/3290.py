A0 = [3, 2, 5, 6]
B0 = [2, -6, 4, -3, 2]


def _states(S):
    return {k: S.get(k) for k in 'fght'}


def _fmt(k, v):
    return f'{k} = ' + ('None' if v is None else str(v))


def _line_text(S):
    v = S.get('v')
    if v is None:
        return ''
    return f"当前 `v = {v}`，`a = {S['a']}`；更新顺序 ==t → h → g → f=="


CONFIG = dict(
    num=3290, title='最高乘法得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='四个状态变量 · 线性 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1692'],
    code='''
class Solution(object):
    def maxScore(self, a, b):
        f = g = h = t = None
        for v in b:
            if h is not None:
                x = v * a[3] + h
                if t is None or x > t:
                    t = x
            if g is not None:
                x = v * a[2] + g
                if h is None or x > h:
                    h = x
            if f is not None:
                x = v * a[1] + f
                if g is None or x > g:
                    g = x
            x = v * a[0]
            if f is None or x > f:
                f = x
        return t
''',
    call=f'Solution().maxScore({A0}, {B0})',
    expect=26,
    max_steps=110,
    skip=['x = v *'],
    views=[
        dict(type='array', var='b', label='b', h=150, cell=64),
        dict(type='text', fn=_line_text, size=24, h=50),
        dict(type='map', var=_states, label='f / g / h / t：分别是选了 1 / 2 / 3 / 4 个数的最大得分', h=180, font=34,
             fmt=lambda k, v: _fmt(k, v)),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'yellow'), ('t', 't', 'green')],
    captions={
        'f = g = h = t = None': '四个状态都是 `None`：`f/g/h/t` 依次表示选了 1、2、3、4 个数时的最大得分，还没选过就是「没有」',
        'for v in b': lambda S, B, r: (f'考虑 `b` 的下一个数 `v = {S.v}`：它要么当第几个数用，要么不用' if S.v != B.get('v') else '`b` 全部看完'),
        'if h is not None': lambda S, B, r: ('`t` 依赖 `h`：`h` 已经有值，`v` 可以当第 4 个数 → 进入' if S.h is not None
                                             else '`t` 依赖 `h`：前三个数还凑不出（`h` 是 None），`v` 不能当第 4 个 → 跳过'),
        'if t is None or x > t': lambda S, B, r: (f'`x = v×a[3] + h = {S.x}`，`t = {B.t}`：' + ('更大 → 更新（==t 先更新==，不然会用到本轮的 `h`）' if B.t is None or S.x > B.t else '不更大 → 保持')),
        'if g is not None': lambda S, B, r: ('`h` 依赖 `g`：`g` 有值，`v` 可以当第 3 个数 → 进入' if S.g is not None
                                             else '`h` 依赖 `g`：`g` 还是 None → 跳过'),
        'if h is None or x > h': lambda S, B, r: (f'`x = v×a[2] + g = {S.x}`，`h = {B.h}`：' + ('更大 → 更新' if B.h is None or S.x > B.h else '不更大 → 保持')),
        'if f is not None': lambda S, B, r: ('`g` 依赖 `f`：`f` 有值，`v` 可以当第 2 个数 → 进入' if S.f is not None
                                             else '`g` 依赖 `f`：`f` 还是 None → 跳过'),
        'if g is None or x > g': lambda S, B, r: (f'`x = v×a[1] + f = {S.x}`，`g = {B.g}`：' + ('更大 → 更新' if B.g is None or S.x > B.g else '不更大 → 保持')),
        'if f is None or x > f': lambda S, B, r: (f'`v` 当第 1 个数：`x = v×a[0] = {S.x}`，`f = {B.f}`：' + ('更大 → 更新' if B.f is None or S.x > B.f else '不更大 → 保持')),
        't = x': '`t = {t}`：选满 4 个数的最好成绩更新了',
        'h = x': '`h = {h}`：选 3 个数的最好成绩更新了',
        'g = x': '`g = {g}`：选 2 个数的最好成绩更新了',
        'f = x': '`f = {f}`：选 1 个数的最好成绩更新了',
        'return t': '`t` 是选满 4 个数的最大得分 = =={ret}==',
    },
    cards=dict(
        one_liner='f、g、h、t：选 1、2、3、4 个数的最大得分',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`a` 长度为 4，`b` 长度至少 4。从 `b` 里按下标递增选 4 个数，依次乘上 `a[0..3]` 再相加',
                 '求最大得分',
                 '示例：`a=[3,2,5,6]`，`b=[2,-6,4,-3,2]` → `26`'],
        quote='令f[index]表示从b[0]到b[index]中选出i[0]可以得到的最大a[0] * b[i[0]]……g[index]表示从b[0]到b[index]中选出i[0]和i[1]可以得到的最大……',
        quote_src='—— yiduobo 题解',
        idea=['按「已选几个数」拆成 4 个状态 `f/g/h/t`，各自只依赖上一个状态',
              '例如 `g = max(g, f + a[1]×v)`：不选 `v` 保持原样，选 `v` 就接在 `f` 后面',
              '每一轮只用到上一轮的值，所以用变量代替数组，==按 t、h、g、f 的顺序更新=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：更新顺序必须是 t、h、g、f，否则同一个 `v` 会被用两次',
                 '用 `None` 表示还凑不出，所以每次要先判断依赖的状态是否为 `None`',
                 '对比灵神：灵神用 `-inf` 初始化，省掉这些 `None` 判断'],
    ),
)
