def _terms(S):
    i, x = S['i'], S['x']
    return S['f_max'][i - 1] * x, S['f_min'][i - 1] * x, x


def _cap_max(S, B, ret):
    a, b, x = _terms(S)
    v = S.f_max[S.i]
    if x == 0:
        why = '`x = 0`，三项全是 0'
    elif v == x and x > max(a, b):
        why = '`x` ==单独成段==更大'
    elif v == b and b > a:
        why = '负负得正：==乘积最小的子数组 × 负数== 变成最大'
    else:
        why = '接在乘积最大的子数组后面'
    return f'`f_max[{S.i}] = max({a}, {b}, {x}) = {v}`：{why}'


def _cap_min(S, B, ret):
    a, b, x = _terms(S)
    v = S.f_min[S.i]
    if x == 0:
        why = '前面的乘积到这里==断开==，从 0 重新开始'
    elif v == x and x < min(a, b):
        why = '`x` 单独成段更小'
    elif v == a and a < b:
        why = '==乘积最大的子数组 × 负数== 变成最小，留着给后面的负数用'
    else:
        why = '接在乘积最小的子数组后面'
    return f'`f_min[{S.i}] = min({a}, {b}, {x}) = {v}`：{why}'


def _line(S, kind):
    if 'x' not in S or 'i' not in S or S['i'] < 1:
        return ''
    i, x = S['i'], S['x']
    a, b, _ = _terms(S)
    p, q = S['f_max'][i - 1], S['f_min'][i - 1]
    fn = max if kind == 'max' else min
    return (f"`f_{kind}[{i}]` = {kind}({p}×{x}, {q}×{x}, {x}) = {kind}({a}, {b}, {x}) = =={fn(a, b, x)}==")


def _col(S, r, c, v):
    if 'i' not in S or 'x' not in S:
        return 'yellow' if c == 0 and S.get('f_max', [0])[0] != 0 else None
    if c == S['i']:
        return 'yellow'
    if c == S['i'] - 1:
        return 'blue'
    return None


CONFIG = dict(
    num=152, title='乘积最大子数组', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='DP：同时维护最大 / 最小乘积',
    code='''
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        f_max = [0] * n
        f_min = [0] * n
        f_max[0] = f_min[0] = nums[0]
        for i in range(1, n):
            x = nums[i]
            # 把 x 加到右端点为 i-1 的（乘积最大/最小）子数组后面，
            # 或者单独组成一个子数组，只有 x 一个元素
            f_max[i] = max(f_max[i - 1] * x, f_min[i - 1] * x, x)
            f_min[i] = min(f_max[i - 1] * x, f_min[i - 1] * x, x)
        return max(f_max)
''',
    call='Solution().maxProduct([-2, 1, -3, -4, 0, 5])',
    expect=12,
    views=[
        dict(type='text', fn=lambda S: _line(S, 'max'), h=56, size=26),
        dict(type='text', fn=lambda S: _line(S, 'min'), h=56, size=26),
        dict(type='array', var='nums', label='nums（黄 = 当前右端点 i）', cell=100, pointers={'i': 'yellow'},
             color=lambda S, k, v: 'yellow' if k == S.get('i') and 'x' in S else None),
        dict(type='grid', var=lambda S: [S['f_max'], S['f_min']], label='DP 表（黄 = 正在算的第 i 列，蓝 = 依赖的第 i-1 列）',
             rows=lambda S: ['max', 'min'], cols=lambda S: list(range(len(S['nums']))), cell=100, h=300, color=_col),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'yellow'), ('max(f_max)', 'max(f_max)', 'green')],
    captions={
        'f_max = [0]': '`f_max[i]`：右端点为 `i` 的子数组的==最大==乘积',
        'f_min = [0]': '`f_min[i]`：右端点为 `i` 的子数组的==最小==乘积——负数乘它可能翻身成最大',
        'f_max[0] = f_min[0]': '右端点为 0 的子数组只有 `nums[0]` 自己：`f_max[0] = f_min[0] = {nums[0]}`',
        'for i in range': lambda S, B, ret: ('所有右端点都算完了' if 'i' in B and B.i == S.i
                                            else f'右端点移到 `i = {S.i}`'),
        'x = nums[i]': '`x = {x}`：三种选择——接在最大后、接在最小后、或单独成段',
        'f_max[i] = max': _cap_max,
        'f_min[i] = min': _cap_min,
        'return max(f_max)': '最大乘积子数组可以在任意位置结尾 → `max(f_max)` = =={ret}==',
    },
    cards=dict(
        one_liner='同时维护最大和最小乘积：负负得正',
        complexity='时间 `O(n)`，空间 `O(n)`（滚动变量可到 `O(1)`）',
        problem=['给整数数组 `nums`，求==乘积最大==的非空连续子数组，返回该乘积',
                 '示例：`[2,3,-2,4]` → `6`；`[-2,0,-1]` → `0`',
                 '演示：`[-2,1,-3,-4,0,5]` → `12`（子数组 `[1,-3,-4]` 或 `[-3,-4]`）'],
        before=[dict(heading='寻找子问题：讨论右端点', lines=[
            '本题是 53. 最大子数组和的==乘法版本==',
            '`[-2,1,-3,4]`：`4` 单独成段，或接在右端点为 `-3` 的==乘积最大==子数组后',
            '`[-2,1,-3,-4]`：`-4` 是负数 → 负负得正，接在==乘积最小==子数组后',
        ])],
        quote='也可以在右端点下标为 i−1 的乘积最小子数组之后添加 x。==把这两种都算一下，这样我们就无需判断 x 到底是正还是负了。==',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f_max[i] = max(f_max[i-1]·x, f_min[i-1]·x, x)`',
              '`f_min[i] = min(f_max[i-1]·x, f_min[i-1]·x, x)`',
              '初始 `f_max[0] = f_min[0] = nums[0]`，答案 `max(f_max)`'],
        after=[dict(heading='写法二 / 写法三：空间优化', lines=[
            '只用到第 `i-1` 列 → 两个变量滚动；初始化为 `1`，从下标 0 开始遍历',
            '==两个式子要同时计算==：`f_max, f_min = max(...), min(...)`',
            '写法三：`x < 0` 时先交换 `f_max`、`f_min`，max / min 各少算一项',
        ])],
        summary=['时间 `O(n)`；空间 `O(n)`，滚动后 `O(1)`',
                 '易错：只维护最大值会漏掉负负得正（如 `-3 × -4 = 12`）',
                 '易错：滚动写法若先改 `f_max` 再算 `f_min`，会用到新值',
                 '答案可能是负数：滚动写法里 `ans` 初始化为 `-inf`'],
    ),
)
