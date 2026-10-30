def _col(S, i, v):
    if 'target' not in S or 'index' not in S:
        return None
    if i == S.get('pos'):
        return 'green'
    if i <= S['index'] and v == S['target']:
        return 'cyan'
    if i == S['index']:
        return 'yellow'
    return None


def _dim(S, i, v):
    return 'index' in S and 'target' in S and i < S['index'] and v != S['target']


def _info(S):
    if 'target' not in S:
        return '`pick(target)`：在所有等于 target 的下标里==等概率==选一个'
    c = S.get('cnt', 0)
    return f"`target = {S['target']}`：目前遇到 `cnt = {c}` 个等于它的数；第 `k` 个以 `1/k` 的概率取代 `pos`"


def _cap_rand(S, B, ret):
    k = S.cnt + 1
    return f'第 `{k}` 个 target：`randint(0, {S.cnt})` 抽到 0 的概率是 `1/{k}`'


CONFIG = dict(
    num=398, title='随机数索引', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='蓄水池抽样',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
import random

class Solution(object):

    def __init__(self, nums):
        self.nums = nums

    def pick(self, target):
        pos = None
        cnt = 0

        for index, num in enumerate(self.nums):
            if num == target:
                if pos is None:
                    pos = index
                else:
                    if random.randint(0, cnt) == 0:
                        pos = index
                cnt += 1

        return pos
''',
    setup='import random\nrandom.seed(7)',
    call='''s = Solution([1, 2, 3, 3, 3])
[s.pick(3), s.pick(1)]''',
    expect=[4, 0],
    views=[
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='array', var='self.nums', cell=110, h=300,
             label='nums（青 = 已遇到的 target，绿 = 当前选中的 pos，黄 = 正在看）',
             pointers={'index': 'yellow', 'pos': 'green'}, color=_col, dim=_dim),
        dict(type='text', size=24, h=90,
             fn=lambda S: '每个 target 下标最终被选中的概率都是 `1/cnt`（和 382 题同一套蓄水池抽样）'),
    ],
    watch=[('target', 'target', 'pink'), ('index', 'index', 'yellow'), ('cnt', 'cnt', 'cyan'), ('pos', 'pos', 'green')],
    captions={
        'self.nums = nums': '只保存数组，==不做任何预处理==（不建哈希表）',
        'pos = None': '`pick({target})`：`pos` 是当前选中的下标，还没有',
        'cnt = 0': '`cnt`：已遇到多少个等于 target 的数',
        'for index, num in enumerate': lambda S, B, r: (
            f'数组扫完，共 `{S.cnt}` 个 target' if 'index' in B and B['index'] == S.index
            else f'看下标 `{S.index}`：`num = {S.num}`'),
        'if num == target': lambda S, B, r: (f'`{S.num} == {S.target}` → 是一个候选下标' if S.num == S.target
                                             else f'`{S.num} ≠ {S.target}`，跳过'),
        'if pos is None': lambda S, B, r: ('第一个 target，还没选过' if S.pos is None else f'已经选了 `pos = {S.pos}`，要靠抽签决定是否替换'),
        'pos = index': lambda S, B, r: (f'第 1 个 target 必选（概率 `1/1`）：`pos = {S.pos}`' if S.cnt == 0
                                        else f'抽中了 → 用当前下标取代：`pos = {S.pos}`'),
        'if random.randint(0, cnt) == 0': _cap_rand,
        'cnt += 1': lambda S, B, r: (f'`cnt` → {S.cnt}' if S.pos == S.index
                                     else f'没抽中（概率 `{S.cnt - 1}/{S.cnt}`），`pos` 仍是 {S.pos}；`cnt` → {S.cnt}'),
        'return pos': '返回下标 =={ret}==',
    },
    cards=dict(
        one_liner='遇到第 k 个 target，就以 1/k 的概率把答案换成它的下标',
        complexity='每次 `pick` 时间 `O(n)`，额外空间 `O(1)`',
        problem=['给可能含重复数字的数组 `nums`，`pick(target)` 随机返回一个 `nums[i] == target` 的下标 `i`',
                 '每个满足条件的下标被返回的==概率相同==；保证 target 一定存在',
                 '本视频：`nums = [1,2,3,3,3]`，`pick(3)` 再 `pick(1)`（固定随机种子）'],
        quote='又是随机抽样的题目，可以用之前相同的==蓄水池抽样==来解决。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「等于 target 的下标」看成一条长度未知的流，正是 382 题的场景',
              '第 1 个直接选；第 `k` 个以 `1/k` 取代，否则保留原答案',
              '原答案留到最后的概率 `1/(k−1) × (k−1)/k = 1/k`，人人平等'],
        summary=['`pick` 时间 `O(n)`，空间 `O(1)`；也可以用哈希表预存下标，`O(1)` 查询但要 `O(n)` 空间',
                 '易错：`cnt` 只在遇到 target 时才加一；`randint` 两端都包含',
                 '这份代码把「第一个」单独处理，其实 `randint(0, 0)` 恒为 0，合并也对',
                 '原文为 Python 2 风格，代码无需改动；演示中固定了随机种子'],
    ),
)
