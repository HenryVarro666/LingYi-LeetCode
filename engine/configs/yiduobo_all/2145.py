def _ps(S):
    s = [0]
    for x in S['differences']:
        s.append(s[-1] + x)
    return s


def _txt(S):
    if 'min_start' in S:
        return f'`hidden[0]` ∈ `[{S["min_start"]}, {S["max_start"]}]`，个数 = `{S["max_start"]} − ({S["min_start"]}) + 1` = =={max(0, S["max_start"] - S["min_start"] + 1)}=='
    if 'max_start' in S:
        return f'`hidden[0] ≤ upper − max_delta = {S["upper"]} − {S["max_delta"]} = {S["max_start"]}`'
    return f'已扫描：`max_delta = {S["max_delta"]}`，`min_delta = {S["min_delta"]}`'


CONFIG = dict(
    num=2145, title='统计隐藏数组数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='差值累加 · 求 hidden[0] 范围',
    tags=['灵神题单', '数学算法', '难度分 1614'],
    code='''
class Solution(object):
    def numberOfArrays(self, differences, lower, upper):

        max_delta = min_delta = 0
        now = 0
        for diff in differences:
            now += diff
            max_delta = max(max_delta, now)
            min_delta = min(min_delta, now)
        
        max_start = upper - max_delta
        min_start = lower - min_delta

        return max(0, max_start - min_start + 1)
''',
    call='Solution().numberOfArrays([1,-3,4], 1, 6)',
    expect=2,
    views=[
        dict(type='array', var='differences', label='differences', h=190,
             color=lambda S, i, v: 'yellow' if 'diff' in S and 'max_start' not in S and v == S['diff'] else None),
        dict(type='array', var=lambda S: _ps(S), label='delta：hidden[i] − hidden[0]（delta[0] = 0）', h=230,
             color=lambda S, i, v: ('pink' if v == S['max_delta'] and i > 0 or (i == 0 and v == S['max_delta'] == 0) else 'blue' if v == S['min_delta'] else None) if 'max_delta' in S else None),
        dict(type='text', fn=_txt, size=34, h=120),
    ],
    watch=['now', ('max_delta', 'max_delta', 'pink'), ('min_delta', 'min_delta', 'blue'), 'lower', 'upper'],
    captions={
        'max_delta = min_delta = 0': '设 `delta[0] = 0`，所以最大、最小 delta 一开始都是 `0`',
        'now += diff': '`now` 是 `hidden[i] − hidden[0]`：累加差值 `{diff}` → =={now}==',
        'max_delta = max': '最大 delta：`max({B.max_delta}, {now})` = =={max_delta}==',
        'min_delta = min': '最小 delta：`min({B.min_delta}, {now})` = =={min_delta}==',
        'max_start = ': '最大值不能超过 upper：`hidden[0] + {max_delta} ≤ {upper}` → `hidden[0] ≤ {max_start}`',
        'min_start = ': '最小值不能低于 lower：`hidden[0] + ({min_delta}) ≥ {lower}` → `hidden[0] ≥ {min_start}`',
        'return max': '`hidden[0]` 在 `[{min_start}, {max_start}]` 里每个数都可用：`{max_start} − ({min_start}) + 1` = =={ret}==（为负则取 0）',
    },
    cards=dict(
        one_liner='hidden[0] 定下来，整个数组就定了：算它能取几个值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`differences[i] = hidden[i+1] − hidden[i]`，hidden 里每个数都在 `[lower, upper]`',
                 '求符合条件的 hidden 数组个数',
                 '本视频：`[1,-3,4]`，`lower=1, upper=6` → `2`'],
        quote='根据上面两个不等式就可以计算出hidden[0]的上限和下限，即 lower - min_delta <= hidden[0] <= upper - max_delta',
        quote_src='—— yiduobo 题解原文',
        idea=['写成 `hidden[index] = hidden[0] + delta[index]`，约定 `delta[0] = 0`',
              '所有数都在范围内 ⇔ ==最小值 ≥ lower 且 最大值 ≤ upper==',
              '只需要扫一遍，记下最大、最小的 delta'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`max_delta`、`min_delta` 初值为 0，对应 `delta[0] = 0`',
                 '用 `max(0, …)` 兜住无解的情况',
                 '对比灵神：灵神用 `accumulate` 前缀和两遍求最值，yiduobo 一边累加一边更新'],
    ),
)
