CAND = [5, 8, 6]
K = 3
R0 = min(max(CAND), sum(CAND) // K) + 1


def _cand(S, i, v):
    if 'right' not in S:
        return None
    if v <= S['left']:
        return 'green'
    if v >= S['right']:
        return 'red'
    return None


def _low(S):
    if 'low' in S['_inner']:
        return S['_inner']['low']
    if 'mid' in S and S['_line'] in (8, 9):
        return S['mid']
    return None


def _cnt(S):
    low = _low(S)
    if not low:
        return []
    return [c // low for c in CAND]


def _top(S):
    low = _low(S)
    if low:
        cs = _cnt(S)
        tot = sum(cs)
        return f"每人至少 `low = {low}` 颗：能分出 `{' + '.join(map(str, cs))} = {tot}` 份 {'≥' if tot >= K else '<'} `k = {K}` → {'==能满足==' if tot >= K else '不能满足'}"
    if 'right' not in S:
        return '问：能否让每个小孩==至少==有 `low` 颗？low 越大越难 → 二分猜答案'
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：left 一定满足，right 一定不满足'
    return f'`left + 1 == right`：`{l}` 满足、`{r}` 不满足 → 答案 =={l}=='


def _check(S, B, ret):
    low = S._inner['low']
    tot = sum(c // low for c in S.candies)
    if ret:
        return f'每堆分出 `c // {low}` 份，共 `{tot} ≥ k = {S.k}` → `True`：每人 ==至少 {low} 颗可以=='
    return f'每堆分出 `c // {low}` 份，共 `{tot} < k = {S.k}` → `False`：{low} 颗==分不够=='


CONFIG = dict(
    num=2226, title='每个小孩最多能分到多少糖果', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1646'],
    code='''
class Solution:
    def maximumCandies(self, candies: List[int], k: int) -> int:
        def check(low: int) -> bool:
            return sum(c // low for c in candies) >= k

        left, right = 0, min(max(candies), sum(candies) // k) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call=f'Solution().maximumCandies({CAND}, {K})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(R0 + 1)),
             label='候选 low（绿 = 满足，红 = 不满足，灰 = 未知）', cell=84, index=False, color=_cand,
             pointers={'left': 'green', 'mid': 'yellow', 'right': 'red'}, h=240),
        dict(type='array', var='candies', label='candies：每堆糖果数', cell=110, h=170),
        dict(type='array', var=_cnt, label='每堆能分出几份 low：c // low', cell=110, index=False, h=170,
             color=lambda S, i, v: 'cyan' if v else None),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow'), 'k'],
    captions={
        'left, right = 0': '`left = 0` 不分糖一定满足；`right = min({max(candies)}, {sum(candies)}//{k}) + 1 = {right}` 一定不满足',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                    else '`left + 1 == right`：开区间为空，结束'),
        'mid = (left': '猜每人至少 `mid = ({left} + {right}) // 2 = {mid}` 颗',
        'return sum': _check,
        'if check(mid)': '调用 `check({mid})`：每人 {mid} 颗，能不能凑够 {k} 份？',
        'left = mid': '能满足 → 答案 ==≥ {left}==：`left = {left}`',
        'right = mid': '不能满足 → 答案 ==< {right}==：`right = {right}`',
        'return left': '`left` 是最大的能满足的 low → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='low 越大越难分够：二分猜答案，每堆贡献 c // low 份',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`candies[i]` 是一堆糖果；每堆可以分成任意子堆，==不能合并==',
                 '分给 `k` 个小孩，每人拿==至多一堆==且数量相同，求每人最多拿几颗',
                 '示例：`[5,8,6], k = 3` → `5`；`[2,5], k = 11` → `0`'],
        quote='能否让每个小孩都==至少==有 low 颗糖果？low 越大，越难实现；low 越小，越容易实现。有这样的性质，就可以==二分猜答案==了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一堆 `candies[i]` 能分出 `floor(candies[i] / low)` 堆，满足这么多小孩',
              '总份数 `≥ k` 就增大 left，否则减小 right',
              '右端点优化：`min(max, sum // k) + 1` 一定无法满足'],
        summary=['时间 `O(n log U)`，`U` 为右端点初始值；空间 `O(1)`',
                 '开区间 `(0, right)`：left = 0 不分糖也合法，所以答案可能是 0',
                 '每人拿==至多一堆==，所以只能 `c // low` 下取整，不能把余数拼起来',
                 '题解还给了 `bisect_left` 库函数写法（二分最大的不满足的 low+1）'],
    ),
)
