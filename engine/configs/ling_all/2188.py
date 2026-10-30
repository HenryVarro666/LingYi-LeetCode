def _ms(S):
    return S['min_sec'][:7]


def _fc(S, k, v):
    i = S.get('i')
    if i is None or S.get('_line', 0) < 14:
        return None
    if k == i:
        return 'yellow' if S['_line'] >= 15 else 'blue'
    return 'green' if k < i else None


def _best(S):
    i, ms, f = S['i'], S['min_sec'], S['f']
    cands = [(f[i - j] + ms[j], j) for j in range(1, min(18, i + 1))]
    return min(cands)


def _fx(S):
    ln = S.get('_line', 0)
    if 'i' not in S or ln < 14:
        return '`min_sec[x]` = 一条轮胎连续跑 `x` 圈的最小总耗时；`f[i]` = 跑 `i` 圈的最小耗时'
    i, ct = S['i'], S['changeTime']
    if ln == 14:
        return f'`f[{i}] = changeTime + min( f[{i}-j] + min_sec[j] )`：最后一段连续跑 `j` 圈'
    if ln == 15:
        c, j = _best(S)
        return f'最优：最后一段跑 `j = {j}` 圈 → `{ct} + f[{i - j}] + min_sec[{j}]` = `{S["f"][i]}`'
    return '`f[numLaps]` 就是答案'


CONFIG = dict(
    num=2188, title='完成比赛的最少时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='预处理连续圈数 · 线性 DP',
    tags=['其他线性 DP', '难度分 2315'],
    code='''
class Solution:
    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        min_sec = [inf] * 18
        for f, r in tires:
            x, time, s = 1, f, 0
            while time <= changeTime + f:
                s += time
                min_sec[x] = min(min_sec[x], s)
                time *= r
                x += 1

        f = [0] * (numLaps + 1)
        f[0] = -changeTime
        for i in range(1, numLaps + 1):
            f[i] = changeTime + min(f[i - j] + min_sec[j] for j in range(1, min(18, i + 1)))
        return f[numLaps]
''',
    call='Solution().minimumFinishTime([[1,10],[2,2],[3,4]], 6, 5)',
    expect=25,
    views=[
        dict(type='array', var=_ms, label='min_sec[x]（下标 = 连续圈数 x，只画前 7 个）', h=200, cell=90,
             color=lambda S, k, v: 'yellow' if S.get('x') == k and S.get('_line') in (8, 9) else None),
        dict(type='text', fn=_fx, size=26, h=90),
        dict(type='array', var=lambda S: S['f'] if S.get('_line', 0) >= 14 else [], label='f[i]（绿 = 已算好，黄 = 当前 i）', h=200, cell=90, color=_fc),
    ],
    watch=[('x', 'x', 'blue'), ('time', 'time', 'pink'), ('s', 's', 'green'), ('i', 'i', 'orange')],
    captions={
        'min_sec = [inf] * 18': '`min_sec[x]` = 同一条轮胎连续跑 `x` 圈的最小耗时。==x 最多 17==，所以开 18 格',
        'for f, r in tires': '看轮胎 `[f, r] = [{f}, {r}]`：第 `x` 圈耗时 `f × r^(x-1)`',
        'x, time, s = 1, f, 0': '从第 1 圈开始：本圈耗时 `time = {time}`，累计 `s = 0`',
        'while time <= changeTime + f': lambda S, B, r: (f'本圈耗时 `{S.time}` ≤ `changeTime + f` = `{S.changeTime + S.f}`：值得继续跑，不如换胎的话就停' if S.time <= S.changeTime + S.f
                                                       else f'本圈耗时 `{S.time}` > `changeTime + f` = `{S.changeTime + S.f}`：==换新胎更划算==，这条轮胎不再往后跑'),
        's += time': '累计耗时 `s` = =={s}==（连续跑了 {x} 圈）',
        'min_sec[x] = min': '`min_sec[{x}]` = `min(旧值, {s})` = =={min_sec[x]}==',
        'time *= r': '下一圈耗时翻 `r` 倍：`time` = {time}',
        'x += 1': '圈数 `x` = {x}',
        'f = [0] * (numLaps + 1)': '`f[i]` = 跑 `i` 圈的最小耗时',
        'f[0] = -changeTime': '`f[0] = −{changeTime}`：每一段都会加一次 `changeTime`，第一段不用换胎，先抵消掉',
        'for i in range(1, numLaps + 1)': '算 `f[{i}]`：枚举最后一段连续跑了 `j` 圈',
        'f[i] = changeTime + min': lambda S, B, r: (lambda cj: f'`f[{S.i}]` = `{S.changeTime}` + min(...) = =={S.f[S.i]}==：最优是最后一段连续跑 `{cj[1]}` 圈，`f[{S.i - cj[1]}] + min_sec[{cj[1]}]` = `{cj[0]}`')(_best(S)),
        'return f[numLaps]': '跑 {numLaps} 圈最少 =={ret}== 秒',
    },
    cards=dict(
        one_liner='连续用一条胎不会太久：最多 17 圈，再换胎做线性 DP',
        complexity='时间 `O((n+numLaps)k)`，空间 `O(numLaps+k)`，`k = 17`',
        problem=['每种轮胎连续用，第 `x` 圈耗时 `f × r^(x-1)`，换胎花 `changeTime`',
                 '轮胎无限多条，求跑完 `numLaps` 圈的最少时间',
                 '示例：`[[1,10],[2,2],[3,4]]`，`changeTime = 6`，`5` 圈 → `25`'],
        quote='连续使用同一个轮胎 i 跑 x 圈，第 x 圈的耗时不应超过 changeTime + f_i，否则直接更换轮胎会更优。结合提示 1，连续使用同一个轮胎的次数不会很大。',
        quote_src='—— 灵茶山艾府题解（提示 2）',
        idea=['耗时指数增长，第 `x` 圈超过 `changeTime + f` 就该换胎 → 连续圈数 `x ≤ 17`',
              '预处理 `min_sec[x]`：连续跑 `x` 圈的最小总耗时',
              '`f[i] = changeTime + min(f[i-j] + min_sec[j])`，`f[0] = −changeTime` 抵消第一次换胎'],
        summary=['时间 `O((n+numLaps)k)`，`k = 17`；空间 `O(numLaps+k)`',
                 '`f[0] = -changeTime` 是技巧：每段统一加一次换胎时间',
                 '`min_sec` 只记录「不超过 changeTime + f」的圈数，所以数组开 18 就够',
                 '`j` 的范围是 `1 .. min(17, i)`，别越界；`min_sec` 里可能有 `inf`'],
    ),
)
