TIME = [1, 2, 3]
TOT = 5


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _trips(S):
    if 'mid' not in S or S['_line'] not in (8, 9, 11):
        return []
    return [S['mid'] // t for t in TIME]


def _top(S):
    if 'mid' in S and S['_line'] in (8, 9, 11):
        m = S['mid']
        ts = _trips(S)
        tot = sum(ts)
        ok = tot >= TOT
        return f"用时 `{m}`：每辆车 `{' + '.join(map(str, ts))}` = `{tot}` 趟 {'≥' if ok else '<'} `{TOT}` → {'==够了==' if ok else '不够'}"
    if 'left' not in S:
        return '时间越多，完成的旅途越多 → ==二分猜答案=='
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面的时间还==不知道==够不够'
    return f'`left + 1 == right`：`{l}` 不够，`{r}` 够 → 答案 =={r}=='


def _if(S, B, ret):
    m = S.mid
    t = sum(m // x for x in S.time)
    if t >= S.totalTrips:
        return f'`Σ {m} // time[i] = {t} ≥ {S.totalTrips}`：用时 `{m}` 够了 → 答案 ==≤ {m}==，缩小到 `(left, mid)`'
    return f'`Σ {m} // time[i] = {t} < {S.totalTrips}`：用时 `{m}` 不够 → 答案 ==> {m}==，缩小到 `(mid, right)`'


CONFIG = dict(
    num=2187, title='完成旅途的最少时间', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1641'],
    code='''
class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        min_t = min(time)
        left = min_t - 1  # 循环不变量：sum >= totalTrips 恒为 False
        right = min_t * totalTrips  # 循环不变量：sum >= totalTrips 恒为 True
        while left + 1 < right:  # 开区间 (left, right) 不为空
            mid = (left + right) // 2
            if sum(mid // t for t in time) >= totalTrips:
                right = mid  # 缩小二分区间为 (left, mid)
            else:
                left = mid  # 缩小二分区间为 (mid, right)
        # 此时 left 等于 right-1
        # sum(left) < totalTrips 且 sum(right) >= totalTrips，所以答案是 right
        return right
''',
    call=f'Solution().minimumTime({TIME}, {TOT})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(min(TIME) * TOT + 1)),
             label='候选用时（红 = 不够 False，绿 = 够了 True，灰 = 未知）', cell=90, index=False, color=_color,
             pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='time', label='time：每辆车跑一趟的用时', cell=100, h=170),
        dict(type='array', var=_trips, label='用时 mid 内每辆车完成的趟数 mid // time[i]', cell=100, index=False, h=170),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'), 'min_t', 'totalTrips'],
    captions={
        'min_t = min': '最快的车 `min_t = {min_t}`',
        'left = min_t - 1': '`left = {left}`：这么点时间==一趟都跑不完==，恒为 False',
        'right = min_t * totalTrips': '`right = {min_t} × {totalTrips} = {right}`：光最快的车就能跑完，恒为 True',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                  else f'`left + 1 == right = {S.right}`：开区间为空，二分结束'),
        'mid = (left': '猜一个用时：`mid = ({left} + {right}) // 2 = {mid}`',
        'if sum(': _if,
        'right = mid': '`right = {right}`：右端点仍然恒为 True',
        'left = mid': '`left = {left}`：左端点仍然恒为 False',
        'return right': '`sum(left) < totalTrips` 且 `sum(right) >= totalTrips` → 答案 =={ret}==',
    },
    cards=dict(
        one_liner='时间越多旅途越多：二分猜答案，判定只要 O(n)',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U` 为二分上下界之差',
        problem=['`time[i]` 是第 `i` 辆公交车跑一趟的用时，车可以连续跑、互相独立',
                 '求所有车==总共==完成至少 `totalTrips` 趟的最少时间',
                 '示例：`time = [1,2,3], totalTrips = 5` → `3`（t = 3 时完成 3 + 1 + 1 = 5 趟）'],
        quote='时间越多，可以完成的旅途也就越多；时间越少，可以完成的旅途也就越少。有这样的性质，我们可以==二分猜答案==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['猜答案为 `x`：每辆车能跑 `x // time[i]` 趟，求和与 `totalTrips` 比较',
              '开区间左端点 `min_t − 1`：任何车都跑不完一趟',
              '右端点 `min_t × totalTrips`：只用最快的车也能跑完'],
        summary=['时间 `O(n log U)`：二分 `log U` 次，每次 `O(n)`；空间 `O(1)`',
                 '开区间：`check(mid)` 为真时更新 right，最后就返回 right',
                 '可选优化：用 `ceil(totalTrips / n)` 收紧上下界',
                 '另有 `bisect_left(range(right), True, left, key=check)` 的库函数写法'],
    ),
)
