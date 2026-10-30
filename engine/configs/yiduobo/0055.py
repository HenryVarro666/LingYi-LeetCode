def _reach(S):
    nums = S.get('nums') or []
    k = S.get('index', -1)
    return [i + v if i <= k else None for i, v in enumerate(nums)]


def _reach_color(S, i, v):
    if v is None:
        return None
    r = _reach(S)
    first = r.index(S['max_bound']) if S.get('max_bound') in r else -1
    return 'green' if i == first else None


CONFIG = dict(
    num=55, title='跳跃游戏', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贪心 · 能跳多远就跳多远',
    code='''
class Solution(object):
    def canJump(self, nums):
        if not nums:
            return False

        max_bound = 0
        for index, num in enumerate(nums):
            if index > max_bound:
                return False
            if index + nums[index] > max_bound:
                max_bound = index + nums[index]

        return True
''',
    call='Solution().canJump([2, 3, 1, 1, 4])',
    expect=True,
    views=[
        dict(type='text', h=52, size=26, text='青框 = `[0, max_bound]`，目前能跳到的范围'),
        dict(type='array', var='nums', cell=110, h=235, pointers={'index': 'yellow'},
             window=('0', 'min(max_bound, len(nums) - 1)')),
        dict(type='array', var=_reach, label='index + nums[index]：从这里最远能跳到哪（绿 = 当前边界）', cell=110, h=170,
             color=_reach_color),
    ],
    watch=[('index', 'index', 'yellow'), 'num', ('max_bound', 'max_bound', 'cyan')],
    captions={
        'if not nums': '空数组直接返回 `False`；这里不是空的',
        'max_bound = 0': '`max_bound`：==目前能跳到的最远边界==，一开始是 0',
        'for index, num in enumerate': lambda S, B, ret: ('扫完了，每个位置都在边界内' if B.get('index') == S['index']
                                                          else f'扫到 `index = {S["index"]}`，这里最多跳 `{S["num"]}` 步'),
        'if index > max_bound': lambda S, B, ret: (f'`{S["index"]} > max_bound = {S["max_bound"]}`：这个位置跳不到' if S['index'] > S['max_bound']
                                                   else f'`{S["index"]} ≤ max_bound = {S["max_bound"]}`：能跳到这里，可以从这里继续跳'),
        'if index + nums[index] > max_bound': lambda S, B, ret: (
            f'`{S["index"]} + {S["nums"][S["index"]]} = {S["index"] + S["nums"][S["index"]]} > {S["max_bound"]}`：==能跳得更远== → 推进边界'
            if S['index'] + S['nums'][S['index']] > S['max_bound']
            else f'`{S["index"]} + {S["nums"][S["index"]]} = {S["index"] + S["nums"][S["index"]]} ≤ {S["max_bound"]}`：不比现在远，边界不变'),
        'max_bound = index + nums[index]': lambda S, B, ret: (
            f'`max_bound = {S["max_bound"]}`' + ('：已经够到终点 `n-1 = ' + str(len(S['nums']) - 1) + '`' if S['max_bound'] >= len(S['nums']) - 1 else '')),
        'return True': '没有遇到跳不到的位置，返回 `True`',
        'return False': '返回 `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='从左往右扫，能跳多远就跳多远，看边界能不能盖住终点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['站在下标 0，`nums[i]` 是在位置 `i` ==最多==能跳的步数',
                 '判断能否到达最后一个下标',
                 '示例：`[2,3,1,1,4]` → `true`（0 → 1 → 4）'],
        quote='不是很懂leetcode题目的顺序是怎么排出来的，前面45题是这个55题的升级版。于是沿用45题的思路，从左往右开始，能跳多远就跳多远，直到跳到终点或者发现有位置跳不到为止。',
        quote_src='—— yiduobo 题解',
        idea=['`max_bound`：从已扫过的位置出发，最远能跳到的边界',
              '若 `index > max_bound` → 这个位置跳不到，直接 `False`',
              '否则用 `index + nums[index]` 把边界==往右推=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只关心“最远能到哪”，不用枚举具体的跳法',
                 '`enumerate` 已给出 `num`，原文用的 `nums[index]` 与它等价',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
