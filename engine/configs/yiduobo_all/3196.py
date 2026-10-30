A0 = [1, -2, 3, 4, -5, 2]


def _idx(S):
    v = S.get('v')
    if v is None:
        return None
    return S['nums'].index(v)


def _nc(S, k, v):
    idx = _idx(S)
    if idx is None:
        return 'blue' if k == 0 and S.get('_line') == 3 else None
    return 'blue' if k == idx else None


def _fmt(x):
    return '无' if x is None else str(x)


def _state(S):
    f, g = S.get('f'), S.get('g')
    if f is None:
        return ''
    return f'`f` = 末项为 ==加号== 的最大总成本 = =={_fmt(f)}==　　`g` = 末项为 ==减号== 的最大总成本 = =={_fmt(g)}=='


def _how(S):
    v = S.get('v')
    if v is None:
        return '每个数只能是加号（另起新段）或减号（接在上一个加号后面）'
    f, g, line = S['f'], S['g'], S.get('_line')
    nf = S.get('new_f')
    if line == 5:
        return f'新段从 `{v}` 开始：`f + v` = `{f} + {v}` = =={f + v}=='
    if line in (6, 7) and g is not None:
        return f'`{v}` 接在 `g` 后面（`g` 末项是减号，本项变加号）：`g + v` = `{g} + {v}` = =={g + v}=='
    if line == 8:
        return f'`{v}` 取负号，只能接在 `f` 后面：`f − v` = `{f} − ({v})` = =={f - v}=='
    return f'这一轮的结果：新的 `f` = `{nf}`，新的 `g` 已经算好'


CONFIG = dict(
    num=3196, title='最大化子数组的总成本', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状态机 DP：末项为加 / 为减',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1847'],
    code='''
class Solution(object):
    def maximumTotalCost(self, nums):
        f, g = nums[0], None
        for v in nums[1:]:
            new_f = f + v
            if g is not None:
                new_f = max(new_f, g + v)
            g = f - v
            f = new_f
        return max(f, g)
''',
    call=f'Solution().maximumTotalCost({A0!r})',
    expect=17,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前的 v）', h=170, cell=80, color=_nc),
        dict(type='text', fn=_state, size=26, h=70),
        dict(type='text', fn=_how, size=26, h=70),
    ],
    watch=[('v', 'v', 'blue'), ('f', 'f', 'green'), ('g', 'g', 'pink'), 'new_f'],
    captions={
        'f, g = nums[0], None': '第一个数一定是加号：`f = {f}`；还没有末项为减号的状态，`g = None`',
        'for v in nums[1:]': lambda S, B, r: (f'处理 `v = {S.v}`' if S.get('v') != B.get('v') or 'v' not in B else '`nums` 都处理完了'),
        'new_f = f + v': '`v` 做加号有两种来源。先看接在 `f` 后面：另起一个子数组 → `new_f = {f} + {v}` = =={new_f}==',
        'if g is not None': lambda S, B, r: ('`g` 还是 `None`（第一个数前面没有减号状态），只有 `f + v` 一种来源' if S.g is None else '`g` 已经有值：除了 `f + v`，还要比较接在 `g` 后面的方案'),
        'new_f = max(new_f, g + v)': '再看接在 `g` 后面（前一项是减号，`v` 回到加号）：`max({B.new_f}, {g} + {v})` = =={new_f}==',
        'g = f - v': '`v` 做减号，只能接在 `f` 后面（前一项是加号）：`g = {B.f} − ({v})` = =={g}==',
        'f = new_f': '轮换完毕：`f` 更新成 `{f}`，`g` 是 `{g}`；它们只依赖上一轮，所以用变量就够',
        'return max(f, g)': '最后一项可以是加号也可以是减号，取 `max({f}, {g})` = =={ret}==',
    },
    cards=dict(
        one_liner='每个数的符号只有加或减，两个状态滚着走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组成本 = `nums[l] − nums[l+1] + nums[l+2] − ...` 交替加减',
                 '把数组划分成若干子数组，使总成本最大',
                 '示例：`[1,-2,3,4]` → `10`（本视频用 `[1,-2,3,4,-5,2]` → `17`）'],
        quote='令f[i]表示前i个数进行划分，且最后一项是加号时的最大总成本，g[i]则表示前i个数进行划分，且最后一项是减号时的最大总成本。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = max(f[i-1], g[i-1]) + nums[i]`：另起新段，或接在减号后面再变回加号',
              '`g[i] = f[i-1] − nums[i]`：负号只能接在加号后面',
              '每轮只依赖上一轮，数组压成两个变量 `f`、`g`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`g` 初始没有意义，代码用 `None` 避免第一轮误用',
                 '`g = f − v` 必须在 `f = new_f` 之前，用的是旧的 `f`',
                 '原文代码无需修改即可在 Python 3 运行，仅删去了多余空行'],
    ),
)
