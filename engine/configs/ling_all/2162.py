def _txt(S, B):
    if 's' not in S:
        return '列出所有合法输入方案，逐个模拟代价'
    return f"按键串 `{S['s']}`：手指在 `{S.get('cur', '?')}`，代价 ==`{S.get('cost', '?')}`=="


CONFIG = dict(
    num=2162, title='设置时间的最少代价', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 借一分钟', tags=['灵神题单', '难度分 1852'],
    code='''
class Solution:
    def minCostSetTime(self, startAt: int, moveCost: int, pushCost: int, sec: int) -> int:
        def calc(s: str) -> int:
            cost = pushCost * len(s)
            cur = startAt
            for ch in s:
                if ord(ch) - ord('0') != cur:
                    cost += moveCost
                    cur = ord(ch) - ord('0')
            return cost

        ans = inf
        if 60 <= sec < 6000: ans = calc(f"{sec // 60}{sec % 60 :02}")
        if sec < 100: ans = min(ans, calc(str(sec)))  # 仅输入秒数
        elif sec % 60 < 40: ans = min(ans, calc(f"{sec // 60 - 1}{sec % 60 + 60}"))  # 借一分钟给秒数
        return ans
''',
    call='Solution().minCostSetTime(1, 2, 1, 600)',
    expect=6,
    views=[
        dict(type='string', var=lambda S: S['s'] if 's' in S else '', label='当前输入的按键串 s', h=200, cell=90),
        dict(type='text', fn=_txt, size=30, h=120),
    ],
    watch=['sec', ('cost', 'cost', 'yellow'), ('cur', 'cur', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'cost = pushCost': '每个数字都要按一次：先记 `pushCost × {len(s)}` = =={cost}==',
        'cur = startAt': '手指一开始在 `{startAt}`',
        'for ch in s': '依次处理按键 `{ch}`',
        'if ord(ch)': lambda S, B, r: (f'按键 `{S.ch}`，手指在 `{S.cur}`：不同 → 要移动，加 `moveCost`' if ord(S.ch) - 48 != S.cur
                                      else f'按键 `{S.ch}`，手指就在 `{S.cur}`：相同 → 不用移动'),
        'cost += moveCost': '移动手指：`cost` = =={cost}==',
        'cur = ord': '手指现在在 `{cur}`',
        'return cost': '这个按键串总代价 =={cost}==',
        'if 60 <= sec < 6000': '`sec = {sec}` 在 60 到 6000 之间：可以写成「分钟 + 两位秒」，试 `{sec // 60}` 分 `{sec % 60:02}` 秒',
        'if sec < 100': lambda S, B, r: ('`sec < 100`：还可以只输入秒数' if S.sec < 100 else f'`sec = {S.sec} ≥ 100`，不能只输秒；看能不能借一分钟'),
        'elif sec % 60 < 40': lambda S, B, r: (f'`sec % 60 = {S.sec % 60} < 40`：秒数加 60 仍不超过 99，可以借 1 分钟' if S.sec % 60 < 40
                                              else f'`sec % 60 = {S.sec % 60} ≥ 40`：借一分钟会超过 99 秒，不行'),
        'return ans': '所有方案里最小代价是 =={ans}==',
    },
    cards=dict(
        one_liner='只有至多三种输入方式，逐一模拟取最小',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['微波炉最多输入 4 位数字，前两位分钟、后两位秒，不足补前导 0',
                 '手指换到别的数字花 `moveCost`，每按一次花 `pushCost`',
                 '示例：`startAt=1, moveCost=2, pushCost=1, sec=600` → `6`'],
        quote='如果 s≥100 且 s mod 60<40，那么我们可以借 1 分钟给秒数，即输入 s/60−1 分 s mod 60+60 秒。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法写法只有：普通「分 + 秒」、只输秒数（< 100）、借一分钟',
              '借一分钟要求秒数 +60 后不超过 99，所以 `sec % 60 < 40`',
              '每种写法按题意模拟：先算按键次数，再数手指移动次数'],
        summary=['时间 `O(1)`：最多 3 个按键串，每串至多 4 位',
                 '易错：秒数要补前导零，如 `9` 分 `0` 秒要写成 `f"{sec % 60 :02}"`',
                 '易错：借一分钟时分钟不能变成负数，由 `sec ≥ 100` 保证',
                 '手指起点是 `startAt`，第一个键相同也不用移动'],
    ),
)
