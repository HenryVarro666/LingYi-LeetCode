def _wl(S):
    if 'm' not in S or 'min_s' not in S:
        return None
    return S['i'] - S['m'] + 1 if 'i' in S else 0


def _wr(S):
    if 'm' not in S or 'min_s' not in S:
        return None
    return S['i'] if 'i' in S else S['m'] - 1


def _taken(S, i, v):
    l, r = _wl(S), _wr(S)
    if l is None:
        return None
    return 'green' if not (l <= i <= r) else None


def _txt(S):
    if 'min_s' not in S:
        return '拿走 k 张 ⇔ 剩下中间连续的 `n − k` 张；剩下的和越小越好'
    l, r = _wl(S), _wr(S)
    tot = sum(S['cardPoints'])
    w = sum(S['cardPoints'][l:r + 1])
    return (f"剩下 `[{l}..{r}]` 和 `{w}`，拿走 `{tot} − {w}` = =={tot - w}==；"
            f"最小剩余 `min_s = {S['min_s']}`")


def _loop(S, B, ret):
    if 'i' in B and S.i == B.i:
        return '所有长为 m 的窗口都看过了'
    return (f'窗口右移：`cardPoints[{S.i}] = {S.cardPoints[S.i]}` 进来，'
            f'`cardPoints[{S.i - S.m}] = {S.cardPoints[S.i - S.m]}` 出去')


CONFIG = dict(
    num=1423, title='可获得的最大点数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='逆向思维 · 定长滑窗求最小剩余',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1574'],
    code='''
class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        m = n - k
        min_s = s = sum(cardPoints[:m])
        for i in range(m, n):
            s += cardPoints[i] - cardPoints[i - m]
            min_s = min(min_s, s)
        return sum(cardPoints) - min_s
''',
    call='Solution().maxScore([5,2,1,7,3,1,6], 3)',
    expect=13,
    views=[
        dict(type='array', var='cardPoints', label='cardPoints（框 = 剩下的 m 张，绿 = 拿走的）', h=260, cell=100,
             pointers={'i': 'blue'}, window=(_wl, _wr), color=_taken),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=['n', ('m', 'm', 'cyan'), ('s', 's', 'orange'), ('min_s', 'min_s', 'green')],
    captions={
        'n = len': '共 `n = {n}` 张牌',
        'm = n - k': '拿走 `k` 张，==剩下 `m = {m}` 张==，而且剩下的一定是中间连续的一段',
        'min_s = s = sum': '第一个窗口 `[0..{m - 1}]` 的和 `s = {s}`，先当作最小剩余',
        'for i in range': _loop,
        's += cardPoints[i]': '`s += {cardPoints[i]} − {cardPoints[i - m]}` → `{s}`：==O(1)== 得到新窗口的和',
        'min_s = min': lambda S, B, ret: (f'`{S.s} < {B.min_s}`：剩下的更少 → 拿走的更多，`min_s = {S.min_s}`'
                                          if S.min_s < B.min_s else f'`{S.s} ≥ {B.min_s}`：没有更小，`min_s` 不变'),
        'return sum': '总和 `{sum(cardPoints)}` − 最小剩余 `{min_s}` = =={ret}==',
    },
    cards=dict(
        one_liner='拿走的最大 ⇔ 剩下的最小：剩下的是一段连续子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次从 `cardPoints` 的==开头或末尾==拿一张，恰好拿 `k` 张',
                 '求拿到的点数和的最大值',
                 '示例：`[1,2,3,4,5,6,1], k = 3` → `12`（拿右边三张 1+6+5）',
                 '本视频：`[5,2,1,7,3,1,6], k = 3` → `13`（5+2 和 6）'],
        quote='由于拿走的点数和 + 剩下的点数和 = 所有点数和 = 常数，所以为了最大化拿走的点数和，应当==最小化剩下的点数和==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只能从两端拿 → 剩下的 `n − k` 张必然==连续==',
              '问题变成：长为 `m = n − k` 的子数组和的最小值',
              '定长滑窗：`s += cardPoints[i] − cardPoints[i − m]`'],
        summary=['时间 `O(n)`，空间 `O(1)`（忽略切片）',
                 '`k = n` 时 `m = 0`：`range(0, n)` 每次加减同一个数，`min_s = 0`，答案是总和',
                 '题解还给了正向思维：枚举前 `k − i` 个 + 后 `i` 个，时间 `O(k)`',
                 '「逆向思维」同类题：1658. 将 x 减到 0 的最小操作数'],
    ),
)
