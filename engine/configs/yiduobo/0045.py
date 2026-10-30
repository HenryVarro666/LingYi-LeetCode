def _levels(nums):
    """离线算出每个位置最少几跳能到（只用于上色）"""
    lv, rb, mrb, res = [0] * len(nums), 0, 0, 0
    for k in range(len(nums)):
        lv[k] = res
        mrb = max(mrb, nums[k] + k)
        if k == rb:
            rb = mrb
            res += 1
    return lv


_LV = ['purple', 'blue', 'cyan', 'pink']


def _color(S, k, v):
    if 'index' not in S or k > S['index']:
        return None
    return _LV[_levels(S['nums'])[k] % 4]


def _reach(S):
    nums = S.get('nums') or []
    k = S.get('index', -1)
    return [i + v if i <= k else None for i, v in enumerate(nums)]


def _src(S):
    r = [x if x is not None else -1 for x in _reach(S)]
    return r.index(max(r))


def _reach_color(S, i, v):
    if v is None or 'index' not in S:
        return None
    return 'green' if i == _src(S) else None


def _cap_new_bound(S, B, ret):
    i, rb, src = S['index'], S['right_bound'], _src(S)
    if i == len(S['nums']) - 1:
        return f'边界更新为 `{rb}`（已经站在终点，不会再跳了）'
    if src == i == 0:
        return f'从起点 0 起跳：这一跳最远到 `right_bound = {rb}`'
    return f'==上一跳应落在位置 {src}==（它下一步跳得最远），再跳一次最远到 `right_bound = {rb}`'


CONFIG = dict(
    num=45, title='跳跃游戏 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贪心 · 每次跳到下一步能跳最远的位置',
    code='''
class Solution(object):
    def jump(self, nums):
        right_bound = 0
        max_right_bound = 0
        res = 0

        for index in range(0, len(nums)):
            max_right_bound = max(max_right_bound, nums[index] + index)
            if index == right_bound:
                right_bound = max_right_bound
                if index != len(nums) - 1:
                    res += 1

        return res
''',
    call='Solution().jump([2, 3, 1, 1, 4])',
    expect=2,
    views=[
        dict(type='text', h=52, size=26, text='颜色 = 几跳能到：==紫== 0 跳，==蓝== 1 跳，==青== 2 跳'),
        dict(type='array', var='nums', cell=120, h=235, pointers={'index': 'yellow'}, color=_color),
        dict(type='array', var=_reach, label='index + nums[index]：从这里下一步最远能到哪（绿 = 最远的那个）', cell=120, h=175,
             color=_reach_color),
    ],
    watch=[('index', 'index', 'yellow'), ('right_bound', 'right_bound', 'cyan'), ('max_right_bound', 'max_right_bound', 'green'), ('res', 'res', 'orange')],
    captions={
        'max_right_bound = 0': '`max_right_bound`：扫过的位置里，==下一跳最远能到哪==',
        'right_bound = 0': '`right_bound`：==当前这一跳能到的最右边界==，一开始站在 0',
        'res = 0': '`res`：跳跃次数',
        'for index in range(0, len(nums))': lambda S, B, ret: ('扫描结束' if B.get('index') == S['index']
                                                               else f'扫到 `index = {S["index"]}`'),
        'max_right_bound = max(': lambda S, B, ret: (
            f'从 {S["index"]} 起跳能到 `{S["nums"][S["index"]]} + {S["index"]} = {S["nums"][S["index"]] + S["index"]}`，'
            f'`max_right_bound = {S["max_right_bound"]}`' + ('　==更远了==' if S['max_right_bound'] > B['max_right_bound'] else '')),
        'if index == right_bound': lambda S, B, ret: (
            (f'`index == right_bound == {S["index"]}`：走到边界，而且这里就是终点' if S['index'] == len(S['nums']) - 1
             else f'`index == right_bound == {S["index"]}`：这一跳的范围扫完了 → ==必须再跳一次==，跳到范围里能跳最远的位置')
            if S['index'] == S['right_bound'] else f'`index = {S["index"]} < right_bound = {S["right_bound"]}`：还在这一跳的范围里，继续扫'),
        'right_bound = max_right_bound': _cap_new_bound,
        'if index != len(nums) - 1': lambda S, B, ret: (
            '还没站在终点 → 这一跳要算上' if S['index'] != len(S['nums']) - 1
            else '`index` 已经是终点 `n-1` → ==不用再跳，不计数=='),
        'res += 1': '`res = {res}`',
        'return res': '最少跳 `{ret}` 次',
    },
    max_steps=60,
    cards=dict(
        one_liner='除非这一跳能直接到终点，否则就跳到“下一步能跳最远”的位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从下标 0 出发，`nums[i]` 是从 `i` ==最多==能往右跳的长度',
                 '求到达最后一个位置的==最少跳跃次数==（保证能到）',
                 '示例：`[2,3,1,1,4]` → `2`（0 → 1 → 4）'],
        before=[dict(heading='为什么是贪心', lines=[
            '乍一看是动态规划，仔细看却是贪心',
            '能落在 `i < j`，且 `i + nums[i] >= j + nums[j]` → 该跳到 `i`',
            '因为从 `j` 能到的位置，从 `i` 都能到；反之则不一定',
            '例：从 0 能跳到 1、2：`1 + 3 = 4`，`2 + 1 = 3` → 跳到 1']),
        ],
        quote='可以得出，除非当前这一跳就能直接跳到结束位置，否则我们在每一步起跳时应该跳到下一步能跳得最远的那个位置。',
        quote_src='—— yiduobo 题解',
        idea=['从头扫描，`right_bound` 是当前这一跳能到的边界',
              '边扫边维护范围内能够到的最远处 `max_right_bound`',
              '扫到边界时再跳一次：新边界 = `max_right_bound`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环会扫到 `n-1`，所以用 `index != len(nums) - 1` 避免在终点多算一跳',
                 '颜色分层其实就是 BFS：第 k 层 = 恰好 k 跳能到的位置',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
