NUMS = [4, 7, 6, 7]


def _skip_or_take(S, B, ret):
    nums, i, now = B.nums, B.index, B.now
    x = nums[i]
    if x in B.used_set:
        return f'`{x}` 在这一层==已经试过== → 跳过，否则子序列重复'
    if x < now[-1]:
        return f'`{x} < {now[-1]}`：接上去不递增 → 跳过'
    return f'`{x} ≥ {now[-1]}` 且这一层没用过 → 接到 `{now}` 后面'


def _for_inner(S, B, ret):
    if S.get('index') != B.get('index'):
        i = S.index
        if i == S.pos + 1:
            return f'从 `pos + 1 = {i}` 开始往后枚举：试 `nums[{i}] = {S.nums[i]}`'
        return f'往后枚举：试 `nums[{i}] = {S.nums[i]}`'
    return f'`now = {S.now}` 这层枚举完 → 返回'


def _for_outer(S, B, ret):
    if S.get('index') != B.get('index'):
        return f'枚举子序列的==第一个数==：`nums[{S.index}] = {S.num}`'
    return '所有开头都枚举完了'


CONFIG = dict(
    num=491, title='递增子序列', difficulty='Medium', category='回溯',
    author='yiduobo', technique='DFS + 每层 used_set 去重',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findSubsequences(self, nums):
        res = []
        used_set = set()
        for index, num in enumerate(nums):
            if num not in used_set:
                self.dfs(nums, index, [num], res)
                used_set.add(num)
        return res

    def dfs(self, nums, pos, now, res):
        if len(now) >= 2:
            res.append(now[:])

        used_set = set()
        for index in range(pos + 1, len(nums)):
            if nums[index] not in used_set and nums[index] >= now[-1]:
                self.dfs(nums, index, now + [nums[index]], res)
                used_set.add(nums[index])
''',
    call=f'Solution().findSubsequences({NUMS})',
    expect=[[4, 7], [4, 7, 7], [4, 6], [4, 6, 7], [7, 7], [6, 7]],
    views=[
        dict(type='array', var='nums', label='nums（暗 = 下标 ≤ pos，不能再选）', cell=84, h=190,
             pointers={'pos': 'blue', 'index': 'pink'},
             dim=lambda S, i, v: 'pos' in S and i <= S['pos']),
        dict(type='stack', var='now', label='now（当前子序列）', h=100),
        dict(type='set', var='used_set', label='used_set（这一层已经试过的数）', h=96),
        dict(type='calls', label='递归调用栈', hide=('nums', 'res'), h=190),
        dict(type='stack', var='res', label='res', h=100, fmt=lambda x: '[' + ','.join(map(str, x)) + ']'),
    ],
    watch=[('pos', 'pos', 'blue'), ('index', 'index', 'pink'), ('now', 'now', 'yellow'), ('答案数', lambda S: len(S['res']), 'green')],
    captions={
        4: '最外层的 `used_set`：==当过开头==的数不再当开头',
        5: _for_outer,
        6: lambda S, B, ret: (f'`{S.num}` 还没当过开头 → 以 `[{S.num}]` 开始搜索（搜完记进 `used_set`）' if S.num not in S.used_set
                              else f'`{S.num}` 已经当过开头 → ==跳过==，去重'),
        7: lambda S, B, ret: f'`dfs(pos = {B.index}, now = [{B.num}])`：从 `[{B.num}]` 开始往后接',
        8: '记下 `{num}` 已经当过开头',
        9: '搜索结束，一共 `{len(ret)}` 个不同的递增子序列',
        12: lambda S, B, ret: (f'进入新的一层：`now = {S.now}` 长度 ≥ 2 → ==是一个答案==，拷贝进 `res`' if len(S.now) >= 2
                               else f'进入新的一层：`now = {S.now}` 长度不到 2，还不是答案（每层都会新建自己的 `used_set`）'),
        13: '把 `{now}` 的拷贝放进 `res`',
        16: _for_inner,
        17: _skip_or_take,
        18: lambda S, B, ret: f'递归：`now + [{B.nums[B.index]}]` = `{B.now + [B.nums[B.index]]}`（新列表，不用回溯）',
        19: lambda S, B, ret: f'本层记下 `{S.nums[S.index]}` 用过了',
    },
    skip=[3, 8, 13, 15],
    max_steps=70,
    cards=dict(
        one_liner='DFS 往后接不小于末尾的数，每一层用 used_set 去重',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计答案）',
        problem=['给你整数数组 `nums`，找出所有==不同的==递增子序列，长度至少为 2',
                 '数组可能有重复元素；两个相等的数也算递增',
                 '示例：`[4,6,7,7]` → 8 个；本视频：`[4,7,6,7]` → 6 个'],
        quote='从当前子序列最后一个数字在原数组中位置的下一个位置开始进行枚举，若当前枚举的数字大于等于现有子序列的最后一个数字，且在这一轮的搜索中没有用过，那么就将其加入到现有子序列中',
        quote_src='—— yiduobo 题解',
        idea=['每进入一层 dfs：`now` 长度 ≥ 2 就先存进答案',
              '下一个数从 `pos + 1` 往后选，且要 `≥ now[-1]` 才能保持递增',
              '「这一轮没有用过」：每层一个 `used_set`，==相同的数在同一层只试一次== → 去重'],
        result='`[4,7] [4,7,7] [4,6] [4,6,7] [7,7] [6,7]`：第二个 `7` 当开头被去重 ✓',
        summary=['时间 `O(n·2^n)`：最多 `2^n` 个子序列，每个复制 `O(n)`',
                 '不能先排序再去重：会打乱原数组顺序，所以用每层的 `used_set`',
                 '`used_set` 只管==同一层==：`[4,7,7]` 里两个 7 在不同层，可以同时选',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring'],
    ),
)
