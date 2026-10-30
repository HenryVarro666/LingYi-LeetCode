def _terms(S):
    n, L = 8, 3  # 与 call 一致（c2 帧里的 n 是形参，不能直接读）
    c = lambda x: x * (x - 1) // 2 if x > 1 else 0
    return [c(n + 2), -3 * c(n - L + 1), 3 * c(n - 2 * L), -c(n - 3 * L - 1)]


def _txt(S):
    t = _terms(S)
    return (f'所有 `{t[0]}`　− 至少一个超限 `{-t[1]}`　+ 至少两个超限 `{t[2]}`　− 三个都超限 `{-t[3]}`　= =={sum(t)}==')


CONFIG = dict(
    num=2929, title='给小朋友们分糖果 II', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='隔板法 + 容斥原理',
    tags=[],
    code='''
def c2(n: int) -> int:
    return n * (n - 1) // 2 if n > 1 else 0

class Solution:
    def distributeCandies(self, n: int, limit: int) -> int:
        return c2(n + 2) - 3 * c2(n - limit + 1) + 3 * c2(n - 2 * limit) - c2(n - 3 * limit - 1)
''',
    call='Solution().distributeCandies(8, 3)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var=_terms, label='四项（依次：所有、−至少一个、+至少两个、−三个）', cell=130, h=190, index=False,
             color=lambda S, i, v: 'green' if i in (0, 2) else 'pink'),
    ],
    watch=[('c2 的参数 n', lambda S: S['_inner'].get('n'), 'blue')],
    captions={
        'return n * (n - 1)': lambda S, B, ret: (f'`c2({S.n})` = `C({S.n}, 2)` = =={ret}==' if S.n > 1
                                                 else f'`n = {S.n} ≤ 1`，没有两个位置可选，`c2` = ==0=='),
        'return c2(n + 2)': lambda S, B, ret: ('`n` 个糖、2 个隔板放进 `n+2` 个位置，选 2 个放隔板：`C(n+2, 2)`' if ret is None
                                              else f'容斥：所有 − 3×至少一个 + 3×至少两个 − 三个 = =={ret}=='),
    },
    max_steps=60,
    cards=dict(
        one_liner='总方案数，减去「某个小朋友超过 limit」的方案，再用容斥补回',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗（可以为 0）',
                 '求总方案数',
                 '示例：`n = 5, limit = 2` → `3`；本视频取 `n = 8, limit = 3` → `3`'],
        quote='要计算合法方案数，可以先计算所有方案数（没有 limit 限制），再减去不合法的方案数（至少一个小朋友分到的糖果超过 limit）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['隔板法：所有方案 `C(n+2, 2)`',
              '某人超限：先给他 `limit+1` 颗，剩下自由分，`C(n-limit+1, 2)`，共 3 种人选',
              '至少两人超限被重复减了，加回；三人都超限又多加了，再减掉'],
        result='`c2(10) − 3·c2(6) + 3·c2(2) − c2(-2)` = 45 − 45 + 3 − 0 = 3',
        summary=['时间、空间 `O(1)`',
                 '易错点：`c2(x)` 在 `x ≤ 1` 时必须是 0，负数不能直接代入公式',
                 '分给超限者 `limit+1` 颗后，还可以继续给他糖',
                 '同类题：见题单「容斥原理」'],
    ),
)
