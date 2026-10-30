def _nums(S):
    return list(range(1, S['right'] + 1)) if 'right' in S else list(range(1, 11))


def _color(S, i, v):
    a, b, x = S['a'], S['b'], S.get('mid')
    if v % a and v % b:
        return None
    if x is None:
        return 'cyan'
    return 'blue' if v <= x else None


def _dim(S, i, v):
    x = S.get('mid')
    return x is not None and v > x


def _txt(S):
    a, b, n = S['a'], S['b'], S['n']
    if 'lcm' not in S:
        return f'神奇数字 = 能被 `{a}` 或 `{b}` 整除的数，求第 `{n}` 个'
    x = S.get('mid')
    if x is None:
        return f"开区间 `({S['left']}, {S['right']})`：`left` 不够 `n` 个，`right` 够 `n` 个"
    c = x // a + x // b - x // S['lcm']
    return f'`{x}//{a} + {x}//{b} − {x}//{S["lcm"]}` = `{x // a} + {x // b} − {x // S["lcm"]}` = =={c}== 个 `≤ {x}`，要 `≥ n = {n}`'


CONFIG = dict(
    num=878, title='第 N 个神奇数字', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 容斥计数',
    tags=['难度分 1897'],
    code='''
class Solution:
    def nthMagicalNumber(self, n: int, a: int, b: int) -> int:
        lcm = math.lcm(a, b)
        left = min(a, b) + n - 2
        right = min(a, b) * n  # 开区间 (left, right)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if mid // a + mid // b - mid // lcm >= n:
                right = mid  # 范围缩小到 (left, mid)
            else:
                left = mid  # 范围缩小到 (mid, right)
        return right % 1_000_000_007
''',
    call='Solution().nthMagicalNumber(5, 2, 3)',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var=_nums, label='数轴 1..right（青 = 神奇数字；蓝 = 神奇且 ≤ mid；暗 = 已超出 mid）',
             color=_color, dim=_dim, h=250),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', 'lcm', ('n', 'n', 'green')],
    captions={
        'lcm = math.lcm': '`lcm({a}, {b}) = {lcm}`：同时被 a、b 整除的数每 `{lcm}` 个出现一次，计数时要去重',
        'left = min': '神奇数字最小是 `{min(a, b)}`，第 `n` 个至少是 `{min(a, b) + n - 1}`，再减一一定不够：`left = {left}`',
        'right = min': '全是 `min(a,b)` 的倍数就有 `n` 个：`right = {right}` 一定够',
        'while left + 1': lambda S, B, r: (f'`left + 1 < right`（{S.left} + 1 < {S.right}）：开区间不空 → 继续' if S.left + 1 < S.right
                                           else f'开区间空了：`right = {S.right}` 就是第 `n` 个'),
        'mid = (': '取中点 `mid = ({left} + {right}) // 2 = {mid}`',
        'if mid // a': lambda S, B, r: (f'`≤ {S.mid}` 的神奇数字：`{S.mid // S.a} + {S.mid // S.b} − {S.mid // S.lcm}` = {S.mid // S.a + S.mid // S.b - S.mid // S.lcm}'
                                        f'，{"≥" if S.mid // S.a + S.mid // S.b - S.mid // S.lcm >= S.n else "<"} n = {S.n} → {"够" if S.mid // S.a + S.mid // S.b - S.mid // S.lcm >= S.n else "不够"}（减去 lcm 倍数是容斥去重）'),
        'right = mid': '够 `n` 个 → 答案 `≤ mid`，==不能直接返回==，继续二分：`right = mid = {right}`',
        'left = mid': '不够 `n` 个 → 答案一定 `> mid`：`left = mid = {left}`',
        'return right': '`right = {right}`，对 `10^9 + 7` 取模后 = =={right % 1_000_000_007}=='
    },
    cards=dict(
        one_liner='二分猜 x，用容斥算出 ≤ x 的神奇数字有几个',
        complexity='时间 `O(log(min(a,b)·n))`，空间 `O(1)`',
        problem=['能被 `a` 或 `b` 整除的正整数是神奇数字，求第 `n` 个，结果对 `10^9 + 7` 取模',
                 '示例：`n=4, a=2, b=3` → `6`',
                 '本视频：`n=5, a=2, b=3` → `8`（2,3,4,6,8）'],
        quote='设答案为 x，循环结束时，≤ x 的神奇数字有 n 个，而 ≤ x-1 的神奇数字不足 n 个。只有当 x 是一个神奇数字时，才会出现这种情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 越大，神奇数字越多 → ==二分答案==',
              '`≤ x` 的个数 = `x // a + x // b − x // lcm`（==容斥==：公倍数被数了两次）',
              '开区间 `(min+n-2, min·n)`：左端必不够，右端必够'],
        summary=['时间 `O(log(min(a,b)·n))`，空间 `O(1)`',
                 '易错：个数恰好等于 `n` 时==不能直接返回==，要继续二分才能保证落在神奇数字上',
                 '`lcm = a·b / gcd(a,b)`，Python 3.9+ 有 `math.lcm`',
                 '取模只在最后做，二分过程中用的是真实值',
                 '库函数写法：`bisect_left(range(right), True, lo=left, key=check)`；同类题 1201 丑数 III'],
    ),
)
