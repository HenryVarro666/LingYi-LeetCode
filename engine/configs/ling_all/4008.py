def _color(S, i, v):
    if 'i' not in S or S['_line'] < 14:
        return None
    if i == S['i']:
        return 'blue'
    return 'green' if i > S['i'] else None


CONFIG = dict(
    num=4008, title='击败所有怪物的最小初始强度', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='差分 + 逆向递推（二分答案的线性解）',
    tags=['二分答案', '求最小', '一维 DP', '难度分 1776'],
    code='''
class Solution:
    def minInitialStrength(self, monsters: list[int], boosts: list[list[int]]) -> int:
        n = len(monsters)
        bonus = [0] * (n + 1)
        for l, r, v in boosts:
            bonus[l] += v
            bonus[r + 1] -= v

        # 差分数组的前缀和即原数组
        for i in range(1, n):
            bonus[i] += bonus[i - 1]

        f = 0
        for i in range(n - 1, -1, -1):
            if f > 0:
                f += monsters[i]
            else:
                f = max(monsters[i] - bonus[i], 0)
        return f
''',
    call='Solution().minInitialStrength([3,6,2,5,4], [[1,1,2],[3,4,6]])',
    expect=11,
    views=[
        dict(type='text', size=24, fn=lambda S: _txt2(S)),
        dict(type='array', var='monsters', label='monsters（绿 = 已经从后往前处理过）', h=250, color=_color,
             pointers={'i': 'blue'}),
        dict(type='array', var='bonus', label='bonus（差分 → 前缀和后，每只怪物的加成）', h=250, color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('f', 'f', 'green')],
    captions={
        'bonus[l] += v': '差分：区间 `[{l}, {r}]` 加成 `{v}` → `bonus[{l}] += {v}`',
        'bonus[r + 1] -= v': '`bonus[{r + 1}] -= {v}`：区间结束后把加成抵消掉',
        'bonus[i] += bonus[i - 1]': '前缀和还原：`bonus[{i}]` = =={bonus[i]}==，这就是第 `{i}` 只怪物的总加成',
        'f = 0': '`f` 表示只考虑击败 `[i, n−1]` 的怪物所需的最小强度；没有怪物时 `f = 0`',
        'for i in range(n - 1, -1, -1)': lambda S, B, r: ('==倒着想==：先求击败最后一只怪物需要多少强度，再往前推' if B.i == S.i and S.i == len(S.monsters) - 1
                                                         else ('倒着遍历结束，`f` 就是 `f_0`' if B.i == S.i else f'再往前一只：`i = {S.i}`')),
        'if f > 0': lambda S, B, r: (f'`f = {S.f} > 0`：后面的怪物还需要强度，当前这只怪物必须先吃掉 `monsters[{S.i}]`'
                                    if S.f > 0 else
                                    f'`f = 0`：后面的怪物靠加成就够了，只需满足当前这只'),
        'f += monsters[i]': '`f = {B.f} + {monsters[i]}` → =={f}==：要给后面的怪物留 `{B.f}`，再加上当前怪物自己的 `{monsters[i]}`（加成够用，条件 1 自动成立）',
        'f = max(': '`f = max({monsters[i]} − {bonus[i]}, 0)` → =={f}==：只要强度加上加成 `{bonus[i]}` 够打当前怪物就行',
        'return f': '`f_0` 就是答案：最小初始强度 `{f}`',
    },
    cards=dict(
        one_liner='正着不知道该取多少，倒着推：f 一旦大于 0 就一路累加',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`monsters[i]` 是怪物强度，`boosts[i]=[l,r,v]` 让下标 `[l,r]` 的怪物战斗时临时加成 `v`（可叠加）',
                 '打败怪物需 `强度 + bonus >= monsters[i]`，之后强度减 `monsters[i]`，小于 0 则置 0',
                 '求打败所有怪物的最小初始强度',
                 '示例：`[5,10,15], [[1,1,10]]` → `30`'],
        quote='正向思考的困难是，由于不知道后面的怪物信息，无法确定初始强度取多少合适。那么倒着想呢？',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用差分 + 前缀和得到每只怪物的 `bonus`',
              '定义 `f_i`：只打 `[i, n−1]` 所需最小强度。`f_{i+1} > 0` 时 `f_i = f_{i+1} + monsters[i]`',
              '`f_{i+1} = 0` 时 `f_i = max(monsters[i] − bonus[i], 0)`'],
        after=[dict(heading='灵神的其他写法', lines=[
            '方法一：二分答案 —— 初始强度越大越容易通关，单调性成立，`check` 模拟一遍，`O(n log S)`',
            '写法二：`f > 0` 之后一路累加，所以倒序找到第一个 `monsters[i] > bonus[i]`，答案 = 前缀和 − `bonus[i]`',
        ])],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '差分数组要开 `n + 1`，否则 `bonus[r + 1]` 越界',
                 '易错：`f` 为 0 时用 `max(monsters[i] − bonus[i], 0)`，不是直接累加',
                 '二分答案写法的上界取 `sum(monsters)`，开区间左端点 `−1`'],
    ),
)


def _txt2(S):
    if 'bonus' not in S:
        return '先用差分数组求每只怪物的加成 `bonus`'
    if S['_line'] < 13 or 'f' not in S:
        return '差分数组的前缀和 = 每只怪物的加成'
    i, f = S['i'], S['f']
    if S['_line'] == 13:
        return f"`f = {f}`：还没有怪物，需要的最小强度为 0"
    return f"当前怪物 `monsters[{i}] = {S['monsters'][i]}`，加成 `bonus[{i}] = {S['bonus'][i]}`，已知 `f = {f}`（后面所需）"
