def _for(S, B, ret):
    n = len(S.candidates)
    if 'index' in S and S.index == S.now_pos and S.now_pos < n - 1:
        return f'从记录的位置 `now_pos = {S.now_pos}` 往后选取：先试 `index = {S.index}`（数字 `{S.candidates[S.index]}`）'
    if 'index' in S and S.index != B.get('index'):
        return f'尝试加入下一个数：`index = {S.index}`（数字 `{S.candidates[S.index]}`）'
    return '`now_pos` 之后的数都试过了 → 这一层结束，回溯'


CONFIG = dict(
    num=39, title='组合总和', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · 记录位置往后选 + 排序后 break',
    code='''
class Solution(object):
    def combinationSum(self, candidates, target):
        res = []
        self.dfs(sorted(candidates), 0, target, [], res)

        return res

    def dfs(self, candidates, now_pos, target, now_choose, res):
        if target == 0:
            res.append([x for x in now_choose])
            return

        for index in range(now_pos, len(candidates)):
            if candidates[index] > target:
                break
            target -= candidates[index]
            now_choose.append(candidates[index])
            self.dfs(candidates, index, target, now_choose, res)
            now_choose.pop()
            target += candidates[index]
''',
    call='Solution().combinationSum([2, 3, 6, 7], 7)',
    expect=[[2, 2, 3], [7]],
    views=[
        dict(type='array', var='candidates', label='candidates（暗 = now_pos 之前，不再选）', cell=70, h=150,
             pointers={'now_pos': 'blue', 'index': 'pink'}, dim=lambda S, i, v: 'now_pos' in S and i < S['now_pos']),
        dict(type='stack', var='now_choose', label='now_choose', h=104),
        dict(type='calls', h=248),
        dict(type='stack', var='res', label='res', h=100),
    ],
    watch=[('now_pos', 'now_pos', 'blue'), ('index', 'index', 'pink'), ('target', 'target', 'yellow')],
    captions={
        'self.dfs(sorted(candidates), 0': '先排序，从位置 `0` 开始搜索；`target = {target}` 表示==还差多少==',
        'if target == 0': lambda S, B, ret: (
            f'`target == 0`：选的数之和正好凑够 → 得到一个解 `{S.now_choose}`' if S.target == 0 else
            f'`target = {S.target}`：还差 `{S.target}`，继续尝试加入一个数'),
        'res.append': lambda S, B, ret: (
            f'`[x for x in now_choose]` 逐个复制：`x = {S.x}`' if len(S.res) == len(B.res) else
            f'复制好的 `{S.res[-1]}` 加入 res'),
        '            return': '等于 target → 回溯',
        'for index in range': _for,
        'if candidates[index] > target': lambda S, B, ret: (
            f'`{S.candidates[S.index]} > target = {S.target}`：已排序，后面的数只会更大' if S.candidates[S.index] > S.target else
            f'`{S.candidates[S.index]} ≤ target = {S.target}`：可以加入'),
        'break': '加入最小的数依然大于 target → ==break==，回溯',
        'target -= candidates[index]': '加入 `{candidates[index]}`：`target` 减掉它 → 还差 `{target}`',
        'now_choose.append': '`now_choose` 末尾加入 `{candidates[index]}` → `{now_choose}`',
        'self.dfs(candidates, index': '记录这个数的位置 `{now_pos}`，下一层==从这个位置往后选取==（还能重复选它）',
        'now_choose.pop()': '回溯：弹出 `{B.now_choose[-1]}`，`now_choose` 回到 `{now_choose}`',
        'target += candidates[index]': '`target` 加回 `{candidates[index]}` → `{target}`，然后尝试加入下一个数',
        'return res': '搜索结束，返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='每次尝试加入一个数，凑够或超了就回溯',
        complexity='指数级（题目保证解少于 150 个），空间 `O(target)`',
        problem=['`candidates` 无重复元素，每个数可以==无限次==选取，找出所有和为 `target` 的不同组合',
                 '示例：`candidates = [2,3,6,7], target = 7` → `[[2,2,3],[7]]`'],
        quote='==当等于 target 或者加入最小的数依然大于 target 时就回溯==……选取一个数之后记录下这个数的位置，然后下次选取时==从这个位置往后选取==。',
        quote_src='—— yiduobo 题解',
        idea=['`target` 原地减、回溯时加回：它始终表示==还差多少==',
              '排序后，`candidates[index] > target` 就可以 `break`',
              '下一层从 `index` 开始（不是 `index+1`）：能重复选，又不会出现 `[3,2,2]`'],
        summary=['复杂度随 target 指数增长，但题目保证解少于 150 个，剪枝后很快',
                 '`[2,2,3]` 和 `[3,2,2]` 是同一个解：只往后选就自然去重',
                 '`target -=` 与 `target +=`、`append` 与 `pop` 必须成对',
                 '原文提到：target 不大时也可以用==背包==思路来做',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
