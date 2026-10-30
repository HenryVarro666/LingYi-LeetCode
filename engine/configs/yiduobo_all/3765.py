def _kind(S):
    d, v = S.get('digits'), S.get('v')
    if not d or v is None or 'p10' not in S:
        return None
    n = len(d)
    t = ''.join(str(c) for c in d[::-1])
    k = len(str(v))
    if v == int(t):
        return 'both', k
    if v == int(t[:k]):
        return 'pre', k
    if v == int(t[-k:]):
        return 'suf', k
    return None


def _col(S, i, x):
    r = _kind(S)
    if r is None:
        return None
    kd, k = r
    n = len(S['digits'])
    if kd == 'both':
        return 'green'
    if kd == 'suf' and i < k:
        return 'pink'
    if kd == 'pre' and i >= n - k:
        return 'blue'
    return None


def _top(S):
    r = _kind(S)
    if r is None:
        return ''
    kd, k = r
    if kd == 'both':
        return f"整个数 `{S['v']}`（最长的前缀 = 最长的后缀）"
    if kd == 'suf':
        return f"后缀：最后 `{k}` 位 = `{S['v']}`（粉）"
    return f"前缀：前 `{k}` 位 = `{S['v']}`（蓝）"


CONFIG = dict(
    num=3765, title='完全质数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数位拆分 + 递推前后缀',
    tags=['灵神题单', '难度分 1378'],
    code='''
class Solution(object):
    def completePrime(self, num):
        
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        
        def check(v):
            if v == 1:
                return False
            
            x = 2
            while x * x <= v:
                if v % x == 0:
                    return False
                x += 1
            
            return True

        v = 0
        p10 = 1
        for d in digits:
            v = v + p10 * d
            p10 *= 10
            if not check(v):
                return False
        
        v = 0
        for d in digits[::-1]:
            v = v * 10 + d
            if not check(v):
                return False
        
        return True
''',
    call='Solution().completePrime(23)',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var='digits', label='digits（个位在前；粉 = 当前后缀用到的数位，蓝 = 当前前缀）', cell=120,
             color=_col, h=230),
        dict(type='text', fn=lambda S: (f"`v = {S['v']}`，`p10 = {S['p10']}`" if 'p10' in S and 'v' in S else ''), size=26),
    ],
    watch=['v', 'p10', ('d', 'd', 'blue')],
    captions={
        'digits = []': '先把 `num` 拆成数位，存进 `digits`（从个位开始）',
        'digits.append': '取出末位 `{digits[-1]}`，`digits = {digits}`',
        'num //= 10': '`num` 去掉末位 → `{num}`',
        'if v == 1': lambda S, B, r: ('`v = 1`：==1 不是质数==' if S.v == 1 else f'`v = {S.v}`，不是 1，继续试除'),
        'x = 2': '从 `x = 2` 开始试除',
        'while x * x <= v': lambda S, B, r: (f'`x×x = {S.x * S.x} <= {S.v}`：继续试除' if S.x * S.x <= S.v
                                              else f'`x×x = {S.x * S.x} > {S.v}`：没有因子了，停止'),
        'if v % x == 0': '`{v} % {x} = {v % x}` → {"==整除，不是质数==" if v % x == 0 else "不整除"}',
        'x += 1': '`x` → {x}',
        11: '`v = 1` 不是质数 → `False`',
        16: '`{v}` 有因子 `{x}` → 不是质数 → `False`',
        19: '试到 `x*x > v` 都没有因子 → `{v}` 是质数 → `True`',
        27: '后缀不是质数 → 完全质数不成立，返回 `False`',
        33: '前缀不是质数 → 完全质数不成立，返回 `False`',
        35: '所有后缀、所有前缀都是质数 → 返回 `True`',
        'v = v + p10 * d': '后缀：上一个后缀 + 数位 × 权重：`{B.v} + {B.p10} × {d}` = =={v}==（最后 {len(str(v))} 位）',
        'p10 *= 10': '`p10` → {p10}，下一位权重再乘 10',
        26: '后缀 `{v}` 是质数吗？不是就立刻 `False`',
        32: '前缀 `{v}` 是质数吗？不是就立刻 `False`',
        'for d in digits[::-1]': lambda S, B, r: (f'倒序遍历 `digits`，从最高位开始：`d = {S.d}`'),
        'v = v * 10 + d': '前缀：上一个前缀 × 10 + 数位：`{B.v} × 10 + {d}` = =={v}==（前 {len(str(v))} 位）',
        21: '`v` 清零：先从个位往高位累加，得到所有==后缀==',
        29: '`v` 清零：再从最高位往低位累加，得到所有==前缀==',
        'p10 = 1': '`p10` 是当前数位的权重，个位是 1',
    },
    cards=dict(
        one_liner='拆出数位，一趟递推出所有后缀，再倒着一趟递推出所有前缀',
        complexity='时间 `O(√num)`，空间 `O(log num)`',
        problem=['`num` 的==所有前缀和所有后缀==都是质数，就称为完全质数',
                 '`num ≤ 10^9`，前缀、后缀最多各 10 个',
                 '示例：`23` → 前缀 2、23，后缀 3、23 都是质数 → `true`'],
        quote='对于num的后缀，最后k位形成的后缀，就等于最后k - 1位形成的后缀，再加上digits[k - 1] * 10^(k - 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `% 10`、`// 10` 把 `num` 拆成 `digits`（个位在前）',
              '正序走：`v += p10 × d`，每步得到一个后缀；`p10` 每次乘 10',
              '倒序走：`v = v × 10 + d`，每步得到一个前缀',
              '每个 `v` 用 `x*x <= v` 试除判质数'],
        summary=['时间 `O(√num)`，最大的数（num 本身）试除次数占主导',
                 '易错：==1 不是质数==，`check` 开头单独排除',
                 '后缀递推要用 `p10`（当前数位权重），前缀递推直接乘 10',
                 '原文代码已是 Python 3 可运行写法（`//` 已写好），未作修改'],
    ),
)
