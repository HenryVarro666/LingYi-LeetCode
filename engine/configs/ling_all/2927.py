N, LIM = 6, 2
ARGS = [N + 2, N - LIM + 1, N - 2 * LIM, N - 3 * LIM - 1]
COEF = [1, -3, 3, -1]
NAMES = ['全部方案（无限制）', '至少 1 人超 limit（A/B/C）', '至少 2 人超 limit（AB/AC/BC）', '3 人都超 limit（ABC）']


def _c2(a):
    return a * (a - 1) // 2 if a > 1 else 0


def _prog(S):
    """返回 (已完成的项数, 正在算的项下标或 None)"""
    inner = S.get('_inner', {})
    if 'limit' in inner:  # 在 distributeCandies 里
        return (4, None) if S.get('_line') else (0, None)
    a = inner.get('n')
    if a in ARGS:
        k = ARGS.index(a)
        done = k + (1 if inner.get('_ret') else 0)
        return k, k
    return 0, None


def _term(k):
    def fn(S):
        inner = S.get('_inner', {})
        in_c2 = 'limit' not in inner and inner.get('n') in ARGS
        cur = ARGS.index(inner['n']) if in_c2 else None
        if in_c2:
            reached = cur
        else:
            reached = 4 if S.get('_line') == 7 or 'self' in inner else 0
        sign = '+' if COEF[k] > 0 else '−'
        c = abs(COEF[k])
        v = c * _c2(ARGS[k])
        head = f'{NAMES[k]}：`{sign} {c} × C({ARGS[k]}, 2)`'
        if k < reached or (in_c2 and k == cur and S.get('_line') == 3 and False):
            return head + f' = =={sign}{v}=='
        if in_c2 and k == cur:
            return f'==▶== ' + head + f' → `c2({ARGS[k]})` = {_c2(ARGS[k])}'
        return head
    return fn


def _total(S):
    inner = S.get('_inner', {})
    in_c2 = 'limit' not in inner and inner.get('n') in ARGS
    if in_c2:
        r = ARGS.index(inner['n'])
    elif 'self' in inner and S.get('_line') == 7:
        r = 4
    else:
        return '容斥：全部 − 至少一个超 + 至少两个超 − 三个都超'
    s = sum(COEF[k] * _c2(ARGS[k]) for k in range(r))
    if r == 4:
        return f'四项相加 = =={s}== 种方案（n={N}, limit={LIM}）'
    return f'已算出的前 {r} 项之和 = {s}'


CONFIG = dict(
    num=2927, title='给小朋友们分糖果 III', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='隔板法 + 容斥原理',
    tags=['灵神题单·数学算法'],
    code='''
def c2(n: int) -> int:
    return n * (n - 1) // 2 if n > 1 else 0

class Solution:
    def distributeCandies(self, n: int, limit: int) -> int:
        return c2(n + 2) - 3 * c2(n - limit + 1) + 3 * c2(n - 2 * limit) - c2(n - 3 * limit - 1)
''',
    call=f'Solution().distributeCandies({N}, {LIM})',
    expect=1,
    views=[
        dict(type='text', fn=_total, size=30, h=90),
        dict(type='text', fn=_term(0), size=28, h=90),
        dict(type='text', fn=_term(1), size=28, h=90),
        dict(type='text', fn=_term(2), size=28, h=90),
        dict(type='text', fn=_term(3), size=28, h=90),
    ],
    watch=['n', 'limit'],
    captions={
        'return n * (n - 1)': lambda S, B, ret: (
            f'`c2({S.n})`：`{S.n}` ≤ 1，没有选法 → ==0==（负数不能直接代入公式）' if S.n <= 1
            else f'`C({S.n}, 2) = {S.n}×{S.n - 1}/2` = =={ret}=='),
        'return c2(n + 2)': '从左到右依次算四项：全部 − 至少一个超 + 至少两个超 − 三个都超',
    },
    cards=dict(
        one_liner='先算全部方案，再用容斥原理减去超限的',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗，问有多少种分法',
                 '示例：`n = 5, limit = 2` → `3`',
                 f'本视频：`n = {N}, limit = {LIM}` → `1`（只有 2+2+2）'],
        quote='要计算合法方案数，可以先计算所有方案数（没有 limit 限制），再减去不合法的方案数（至少一个小朋友分到的糖果超过 limit）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['所有方案：隔板法，`n` 个球 + 2 个隔板放进 `n+2` 个位置 → `C(n+2, 2)`',
              '某人超限：先给他 `limit+1` 颗，剩下随便分 → `C(n-limit+1, 2)`，A/B/C 共 3 种',
              '两人同时超限被多减了一次，要加回来；三人都超限又要减掉 → ==容斥原理=='],
        summary=['时间、空间都是 `O(1)`',
                 '`C(m, 2)` 在 `m < 2` 时必须当作 0，否则负数会算出错误的正数',
                 '四项系数依次是 +1、−3、+3、−1，对应「至少 k 人超限」',
                 '同类题：2928 / 2929（数据范围小，可以直接枚举）'],
    ),
)
