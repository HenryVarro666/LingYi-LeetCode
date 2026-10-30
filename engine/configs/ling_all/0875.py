PILES = [3, 6, 7, 11]
H = 8


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _hours(S):
    if 'mid' not in S or S['_line'] not in (7, 8, 9, 11):
        return []
    m = S['mid']
    return [(p - 1) // m + 1 for p in PILES]


def _top(S):
    if 'mid' in S and S['_line'] in (8, 9, 10, 11):
        m = S['mid']
        hs = _hours(S)
        tot = sum(hs)
        ok = tot <= H
        return f"速度 `k = {m}`：每堆要 `{' + '.join(map(str, hs))}` = `{tot}` 小时 {'≤' if ok else '>'} `h = {H}` → {'==能吃完==' if ok else '吃不完'}"
    if 'left' not in S:
        return f'`h = {H}`：速度越快越能吃完 → ==二分猜答案=='
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面 `{r - l - 1}` 个速度还==不知道==能否吃完'
    return f'`left + 1 == right`：`{l}` 吃不完，`{r}` 能吃完 → 答案 =={r}=='


def _while(S, B, ret):
    l, r = S.left, S.right
    if l + 1 < r:
        return f'开区间 `({l}, {r})` 不为空 → 继续二分'
    return f'`left + 1 == right = {r}`：开区间为空，==每个速度都有了结论=='


def _if(S, B, ret):
    m = S.mid
    t = S.n + sum((p - 1) // m for p in S.piles)
    if t <= S.h:
        return f'`k = {m}` 要 `{t}` 小时 ≤ `{S.h}`：能吃完 → 答案 ==≤ {m}==，更快的也都能吃完'
    return f'`k = {m}` 要 `{t}` 小时 > `{S.h}`：吃不完 → 答案 ==> {m}==，更慢的也都吃不完'


CONFIG = dict(
    num=875, title='爱吃香蕉的珂珂', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['labuladong', '灵神题单·二分算法', '难度分 1766'],
    code='''
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        n = len(piles)
        left = 0  # 恒为 False
        right = max(piles)  # 恒为 True
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if n + sum((p - 1) // mid for p in piles) <= h:
                right = mid  # 循环不变量：恒为 True
            else:
                left = mid  # 循环不变量：恒为 False
        return right  # 最小的 True
''',
    call=f'Solution().minEatingSpeed({PILES}, {H})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(max(PILES) + 1)),
             label='候选速度 k（红 = 吃不完 False，绿 = 能吃完 True，灰 = 未知）',
             cell=70, index=False, color=_color, pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='piles', label='piles：每堆香蕉数', cell=100, h=170),
        dict(type='array', var=_hours, label='以速度 mid 吃完每堆要的小时数 ceil(p / mid) = (p−1)//mid + 1',
             cell=100, index=False, h=170),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'), 'n', 'h'],
    captions={
        'n = len': '`n = {n}` 堆香蕉',
        'left = 0': '`left = 0`：速度 0 根本吃不了，==恒为 False==',
        'right = max': '`right = max(piles) = {right}`：每小时吃完一堆，`n ≤ h` 一定来得及，==恒为 True==',
        'while left + 1 < right': _while,
        'mid = (left': '猜一个速度：`mid = ({left} + {right}) // 2 = {mid}`',
        'if n + sum': _if,
        'right = mid': '`right = {right}`：右端点仍然==恒为 True==',
        'left = mid': '`left = {left}`：左端点仍然==恒为 False==',
        'return right': '`right` 是==最小的 True== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='能用 k 吃完，更快也能吃完 → 二分猜答案，判定只要 O(n)',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U = max(piles)`',
        problem=['`n` 堆香蕉，第 `i` 堆 `piles[i]` 根；警卫 `h` 小时后回来',
                 '每小时选一堆吃 `k` 根，不足 k 根就吃完这堆、本小时不再吃',
                 '求 h 小时内吃完的==最小速度 k==；示例：`[3,6,7,11], h = 8` → `4`'],
        quote='如果珂珂能用 k=4 的速度吃掉所有香蕉，那么也能用更快的速度 k=5,6,… 吃掉所有香蕉。……据此，可以==二分猜答案==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题转化成判定：给定 `k`，能否在 `h` 小时内吃完？',
              '一堆 `p` 根要 `ceil(p/k) = (p−1)//k + 1` 小时；求和得 `n + Σ (p−1)//k ≤ h`',
              '开区间 `(0, max(piles))`：left 恒 False，right 恒 True'],
        summary=['时间 `O(n log U)`：二分 `log U` 次，每次 `O(n)`；空间 `O(1)`',
                 '上取整用 `(p − 1) // k + 1`，不用浮点数',
                 '开区间：`check(mid)` 为真时更新 right，最后就返回 right',
                 '另有 `bisect_left(range(...), True, key=check)` 的库函数写法'],
    ),
)
