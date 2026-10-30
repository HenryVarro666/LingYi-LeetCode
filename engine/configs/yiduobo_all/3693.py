def _F(costs):
    f = g = None
    h = 0
    out = [0]
    for c in costs:
        best = c + 1 + h
        if g is not None and g + c + 4 < best:
            best = g + c + 4
        if f is not None and f + c + 9 < best:
            best = f + c + 9
        f, g, h = g, h, best
        out.append(h)
    return out


def _idx(S):
    if 'h' not in S or 'costs' not in S:
        return None
    F = _F(S['costs'])
    if S['h'] not in F:
        return None
    k = F.index(S['h'])
    line = S.get('_line')
    if 5 <= line <= 10:
        return k if k < len(S['costs']) else None
    if line == 11:
        return k - 1
    return None


def _dp(S):
    if 'h' not in S:
        return None
    F = _F(S['costs'])
    k = F.index(S['h'])
    return [F[j] if j <= k else '?' for j in range(len(F))]


def _dp_color(S, j, v):
    k = _idx(S)
    if k is None:
        return None
    if j == k + 1:
        return 'yellow'
    if S.get('_line') in (6, 7, 8, 9, 10) and j in (k, k - 1, k - 2) and j >= 0:
        return 'green'
    return None


def _cost_color(S, j, v):
    k = _idx(S)
    return 'yellow' if k is not None and j == k + 1 else None


def _formula(S):
    k = _idx(S)
    if k is None or 'best' not in S:
        return '`h` = 走到 index-1 的成本，`g` = index-2，`f` = index-3；`None` = 台阶不存在'
    return f'走到台阶 {k + 1}：当前最优 `best` = =={S["best"]}==（`h={S["h"]}`，`g={S["g"]}`，`f={S["f"]}`）'


CONFIG = dict(
    num=3693, title='爬楼梯 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三变量迭代的线性 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1560'],
    code='''
class Solution(object):
    def climbStairs(self, n, costs):
        
        f, g, h = None, None, 0
        for c in costs:
            best = c + 1 + h
            if g is not None and g + c + 4 < best:
                best = g + c + 4
            if f is not None and f + c + 9 < best:
                best = f + c + 9
            f, g, h = g, h, best
            
        return h
''',
    call='Solution().climbStairs(4, [1, 2, 3, 4])',
    expect=13,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var=_dp, label='f[index]：走到该台阶的最小成本（黄 = 正在算，绿 = 能走过来的三级）', h=260, cell=110,
             color=_dp_color),
        dict(type='array', var=lambda S: ['-'] + list(S['costs']), label='costs[index]（下标 = 台阶号）', h=240, cell=110,
             color=_cost_color),
    ],
    watch=[('f', 'f', 'cyan'), ('g', 'g', 'blue'), ('h', 'h', 'green'), ('best', 'best', 'yellow')],
    captions={
        'f, g, h = None': '`h = 0`：站在第 0 级成本为 0；`f, g` 是还不存在的台阶，记作 `None`',
        'for c in costs': lambda S, B, r: ('处理台阶 `%d`，`costs = %d`' % (_idx(S) + 1, S.c) if _idx(S) is not None
                                           else '所有台阶都处理完了，`h` 就是走到第 n 级的最小成本'),
        'best = c + 1 + h': '先假设从前一级走来：`h + 1 + c` = `{h} + 1 + {c}` = =={best}==（这一定存在）',
        'if g is not None': lambda S, B, r: (('从前两级走来：`g + c + 4` = `%s` 比 `best = %s` ==更小==，换掉它' % (S.g + S.c + 4, S.best) if S.g is not None and S.g + S.c + 4 < S.best else
                                              '`g + c + 4` = `%s` 不比 `best = %s` 小，保留' % (S.g + S.c + 4, S.best)) if S.g is not None
                                             else '`g` 是 `None`：前两级的台阶不存在，跳过'),
        'best = g + c + 4': '`best = g + c + 4` = =={best}==',
        'if f is not None': lambda S, B, r: (('从前三级走来：`f + c + 9` = `%s`，==%s==`best = %s`' % (
            S.f + S.c + 9, '更小，换掉' if S.f + S.c + 9 < S.best else '不更小，保留', S.best)) if S.f is not None
                                             else '`f` 是 `None`：前三级的台阶不存在，跳过'),
        'best = f + c + 9': '`best = f + c + 9` = =={best}==',
        'f, g, h = g, h, best': lambda S, B, r: '台阶 %d 的最小成本 ==%s==；三个变量整体左移：`f=%s, g=%s, h=%s`' % (_idx(S) + 1, S.best, S.f, S.g, S.h),
        'return h': '走到第 n 级的最小成本 `h` = =={ret}==',
    },
    cards=dict(
        one_liner='f[index] 从前三级走来，取最小，只留三个变量',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n+1` 级台阶，一步只能走到 `i+1 / i+2 / i+3`，从 `i` 到 `j` 的成本是 `costs[j] + (j-i)^2`',
                 '求从第 0 级走到第 `n` 级的最小成本',
                 '示例：`n=4, costs=[1,2,3,4]`（演示用）→ `13`'],
        quote='对于f[index]，可以从index - 1、index - 2、index - 3走来，对应的成本分别为f[index - 1] + 1 + costs[index]、f[index - 2] + 4 + costs[index]、f[index - 3] + 9 + costs[index]，取其中的最小值作为f[index]即可，当然，这里有一个前提是对应的f值需要存在。',
        quote_src='—— yiduobo 题解',
        idea=['三种来路的距离平方分别是 `1、4、9`，成本再加上 `costs[index]`',
              '前提是对应台阶存在：所以用 `None` 表示还不存在的 `f`、`g`',
              '每一轮只看前三个状态，用 `f, g, h` 迭代，省掉数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f`、`g` 为 `None` 时不能比较，要先判断 `is not None`',
                 '先用「从前一级来」初始化 `best`，因为它一定存在',
                 '更新顺序：先算出 `best`，再 `f, g, h = g, h, best` 整体左移'],
    ),
)
