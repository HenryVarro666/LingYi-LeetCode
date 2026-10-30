NUMS = [11, 1, 13]


def _k(S):
    if 'k' in S['_inner']:
        return S['_inner']['k']
    return None


def _ops(S):
    k = _k(S)
    if not k:
        return []
    return [(x - 1) // k + 1 for x in NUMS]


def _top(S):
    k = _k(S)
    if k:
        ops = _ops(S)
        t = sum(ops)
        if 'right' not in S:
            import math
            return f"`nonPositive({k}) = {' + '.join(map(str, ops))} = {t}` → 上界 `ceil(sqrt({t})) = {math.ceil(math.sqrt(t))}`"
        return f"`k = {k}`：操作次数 `{' + '.join(map(str, ops))} = {t}`，`k² = {k * k}` → {'==满足==' if t <= k * k else '不满足'}"
    if 'right' in S:
        return f"答案在 `[{S['left']}, {S['right']}]` 里：上下界只差 `{S['right'] - S['left']}`"
    if 'left' in S:
        return f"下界 `left = max(ceil(sqrt({len(NUMS)})), ceil(cbrt({sum(NUMS)}))) = {S['left']}`"
    return 'k 越大，操作次数越少、`k²` 越大 → ==二分猜答案=='


def _cand(S, i, v):
    if 'left' not in S:
        return None
    if v < S['left']:
        return 'red'
    if 'right' in S and v > S['right']:
        return None
    if 'right' in S and v == S['right']:
        return 'green'
    return None


def _np(S, B, ret):
    k = S._inner['k']
    head = f'`nonPositive(nums, {k}) = n + Σ (x−1)//{k} = {S.n} + {ret - S.n} = {ret}`'
    if 'right' in S:
        if ret <= k * k:
            return head + f' ≤ `{k}² = {k * k}` → k = {k} ==满足=='
        return head + f' > `{k}² = {k * k}` → k = {k} ==不满足==，答案只能是上界'
    return head + '（每个数==至少操作一次==，先提出 `n`）'


CONFIG = dict(
    num=3824, title='减小数组使其满足条件的最小 K 值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 上下界优化',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1531'],
    code='''
class Solution:
    def minimumK(self, nums: List[int]) -> int:
        n = len(nums)

        def non_positive(k: int) -> int:
            return n + sum((x - 1) // k for x in nums)

        left = max(ceil(sqrt(n)), ceil(cbrt(sum(nums))))  # 答案的下界
        right = ceil(sqrt(non_positive(left)))  # 答案的上界
        return bisect_left(range(right), True, left, key=lambda k: non_positive(k) <= k * k)
''',
    setup='from math import ceil, sqrt, cbrt',
    call=f'Solution().minimumK({NUMS})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(1, 9)),
             label='候选 k（红 = 低于下界，一定不满足；绿 = 上界，一定满足）', cell=84, index=False, color=_cand,
             pointers={'left': 'blue', 'right': 'pink'}, h=240),
        dict(type='array', var='nums', label='nums', cell=110, h=170),
        dict(type='array', var=_ops, label='每个数的操作次数 ceil(x / k) = (x−1)//k + 1', cell=110, index=False, h=170,
             color=lambda S, i, v: 'cyan'),
    ],
    watch=['n', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('k', lambda S: S['_inner'].get('k', ''), 'yellow')],
    captions={
        'n = len': '`n = {n}`',
        'return n + sum': _np,
        'left = max': '下界：每个数至少操作一次 → `k² ≥ n`；又 `Σ x/k ≤ k²` → `k³ ≥ S` ⇒ `left = {left}`',
        'right = ceil': '上界：先算 `nonPositive(left)`，再开根号上取整；`nonPositive(high) ≤ nonPositive(low) ≤ high²`，一定满足',
        'return bisect_left': lambda S, B, r: (f'只需在 `[{S.left}, {S.right})` 里二分：返回第一个满足的 k =={r}==' if r is not None
                                                else f'在 `[{S.left}, {S.right})` 里二分第一个满足 `nonPositive(k) ≤ k²` 的 k'),
    },
    cards=dict(
        result='`k = 3` 不满足，上界 `4` 一定满足 → 返回 ==4==',
        one_liner='k 越大越容易满足：二分答案，再用数学把上下界夹紧',
        complexity='时间 `O(n log(n / cbrt(S)))`，空间 `O(1)`',
        problem=['给正整数数组 `nums`；一次操作把某个 `nums[i]` 减去 `k`',
                 '`nonPositive(nums, k)`：让所有数 ≤ 0 的最少操作次数',
                 '求满足 `nonPositive(nums, k) ≤ k²` 的==最小== k；示例 `[3,7,5]` → `3`'],
        quote='当 k 逐渐增大时，操作次数会变小（或者不变）……另一方面，k² 会随着 k 的增大而增大。……据此，可以==二分猜答案==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['x 要操作 `ceil(x/k) = (x−1)//k + 1` 次，求和得 `n + Σ (x−1)//k`，全程整数',
              '下界 `low = max(ceil(sqrt n), ceil(cbrt S))`：至少 n 次，且 `S/k ≤ k²`',
              '上界 `high = ceil(sqrt(nonPositive(low)))`：单调性保证 high 一定满足'],
        summary=['时间 `O(n log(n / cbrt(S)))`，上下界之差约 `n / (2·cbrt(S))`；空间 `O(1)`',
                 '上取整用 `(x − 1) // k + 1`，避免浮点舍入误差',
                 '`bisect_left(range(right), True, left, key=...)`：在 `[left, right)` 里找第一个 True',
                 '优化前写法：下界 `ceil(sqrt n)`、上界 `max(nums)`，同样开区间二分'],
    ),
)
