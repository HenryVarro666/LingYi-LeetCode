DIST = [5, 3, 4, 6, 2]
HOUR = 7.5
R0 = 6  # 开区间右端点初始值 (max_dist - 1) // h + 1


def _cand(S, i, v):
    if 'right' not in S or 'h' not in S:
        return None
    if v <= S['left']:
        return 'red'
    if v >= S['right']:
        return 'green'
    return None


def _v(S):
    if 'v' in S['_inner']:
        return S['_inner']['v']
    if 'mid' in S and S['_line'] in (24, 25):
        return S['mid']
    return None


def _times(S):
    v = _v(S)
    if not v:
        return []
    return [str((d - 1) // v + 1) for d in DIST[:-1]] + [f'{DIST[-1]}/{v}']


def _top(S):
    v = _v(S)
    if v:
        t = sum((d - 1) // v + 1 for d in DIST[:-1])
        ok = (t * v + DIST[-1]) * 100 <= round(HOUR * 100) * v
        return f"时速 `{v}`：前 n−1 趟（上取整）共 `{t}` 小时 + 最后一趟 `{DIST[-1]}/{v}` {'≤' if ok else '>'} `{HOUR}` → {'==来得及==' if ok else '迟到'}"
    if 'right' in S and 'h' in S:
        l, r = S['left'], S['right']
        if l + 1 < r:
            return f'开区间 `({l}, {r})`：left 一定迟到，right 一定准时'
        return f'`left + 1 == right`：`{l}` 迟到、`{r}` 准时 → 答案 =={r}=='
    return '时速越大，花的时间越少 → ==二分时速 v=='


def _ret(S, B, ret):
    v = S._inner['v']
    t = S._inner['t']
    lhs, rhs = (t * v + S.dist[-1]) * 100, S.h100 * v
    return f'`({t}×{v} + {S.dist[-1]})×100 = {lhs}` {"≤" if ret else ">"} `h100×v = {rhs}` → `{ret}`：时速 {v} {"==准时==" if ret else "==迟到=="}'


CONFIG = dict(
    num=1870, title='准时到达的列车最小时速', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 全整数判定',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1676'],
    code='''
class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        h100 = round(hour * 100)  # 下面不会用到任何浮点数
        delta = h100 - (n - 1) * 100
        if delta <= 0:  # 无法到达终点
            return -1

        max_dist = max(dist)
        if h100 <= n * 100:  # 特判
            # 见题解中的公式
            return max(max_dist, (dist[-1] * 100 - 1) // delta + 1)

        def check(v: int) -> bool:
            t = n - 1  # n-1 个上取整中的 +1 先提出来
            for d in dist[:-1]:
                t += (d - 1) // v
            return (t * v + dist[-1]) * 100 <= h100 * v

        left = (sum(dist) * 100 - 1) // h100  # 也可以初始化成 0（简单写法）
        h = h100 // (n * 100)
        right = (max_dist - 1) // h + 1  # 也可以初始化成 max_dist（简单写法）
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().minSpeedOnTime({DIST}, {HOUR})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=25, h=80),
        dict(type='array', var=lambda S: list(range(R0 + 1)),
             label='候选时速 v（红 = 迟到，绿 = 准时，灰 = 未知）', cell=84, index=False, color=_cand,
             pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='dist', label='dist：每趟列车的距离', cell=100, h=170,
             color=lambda S, i, v: 'yellow' if 'd' in S['_inner'] and S['_line'] == 17 and i == S['dist'][:-1].index(S['_inner']['d']) else None),
        dict(type='array', var=_times, label='时速 v 下每趟用时（前 n−1 趟上取整 = 含等待，最后一趟不取整）',
             cell=100, index=False, h=170, color=lambda S, i, v: 'cyan'),
    ],
    watch=['h100', 'delta', 'max_dist', ('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow')],
    captions={
        'n = len': '`n = {n}` 趟列车，`hour = {hour}`',
        'h100 = round': '`hour × 100` 再 `round` → `h100 = {h100}`：之后==全用整数==，避免浮点误差',
        'delta = h100': '`delta = h100 − (n−1)×100 = {delta}`：留给最后一趟的时间（×100）',
        'if delta <= 0': lambda S, B, r: (f'`delta = {S.delta} > 0`：hour 严格大于 n−1，有机会准时' if S.delta > 0
                                           else '`delta ≤ 0`：前 n−1 趟每趟至少 1 小时，必迟到'),
        'max_dist = max': '`max_dist = {max_dist}`',
        'if h100 <= n * 100': lambda S, B, r: (f'`h100 = {S.h100} > n×100 = {S.n * 100}`：不走特判，进入二分' if S.h100 > S.n * 100
                                                else '`hour ≤ n`：前 n−1 趟必须各 1 小时 → 直接套公式'),
        'left = (sum': '下界：不算等待也来不及的最大时速 `left = ({sum(dist)}×100 − 1) // {h100} = {left}`，一定迟到',
        'h = h100 //': '`h = {h100} // {n * 100} = {h}`：每趟最多能花 {h} 小时',
        'right = (max_dist': '上界：每趟 {h} 小时跑完 `max_dist` → `right = {right}`，一定准时',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                    else '`left + 1 == right`：开区间为空，结束'),
        'mid = (left': '试时速 `mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：时速 {mid} 能否准时？',
        't = n - 1': '`t = n − 1 = {t}`：把 n−1 个上取整里的 `+1` 先提出来',
        't += (d - 1)': '`d = {d}`：`ceil({d}/{v})` 去掉提出的 1 剩 `({d}−1)//{v} = {(d - 1) // v}` → `t = {t}`',
        'return (t * v': _ret,
        'right = mid': '准时 → 答案 ==≤ {right}==：`right = {right}`',
        'left = mid': '迟到 → 答案 ==> {left}==：`left = {left}`',
        'return right': '`right` 是最小的准时时速 → =={ret}==',
    },
    skip=['for d in dist'],
    cards=dict(
        one_liner='二分时速；hour×100 变整数，彻底和浮点数说拜拜',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['按顺序坐 `n` 趟列车，第 i 趟距离 `dist[i]`；列车==只在整点发车==',
                 '在 `hour` 小时内到达的==最小正整数时速==，做不到返回 `-1`',
                 '示例：`[1,3,2], hour = 2.7` → `3`；本视频 `[5,3,4,6,2], 7.5` → `4`'],
        quote='由于 hour 至多有两位小数，不妨将其乘上 100，得到整数 h100……这样就==和浮点数说拜拜了==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前 n−1 趟用时 `ceil(dist[i]/v)`（含等待），和记为 `t`；最后一趟 `dist[n−1]/v`',
              '判定 `t + dist[n−1]/v ≤ hour` ⇔ `(t·v + dist[n−1])·100 ≤ h100·v`',
              '先特判 `hour ≤ n−1`（返回 -1）和 `hour ≤ n`（公式），再开区间二分'],
        summary=['时间 `O(n log U)`，`U` 为二分上下界之差；空间 `O(1)`',
                 '`2.01 × 100 = 200.99999…`，所以要 `round` 而不是 `int`',
                 '上取整用 `(a − 1) // b + 1`；==最后一趟不取整==',
                 '上下界可以简单写成 `0` 和 `max_dist`；题解还有 `bisect_left` 库函数写法'],
    ),
)
