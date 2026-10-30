NUMS, K = [4, 1, 3, 7, 2, 5, 9, 1], 3


def _live(S):
    return 'index' in S and 'v' in S


def _color(S, i, v):
    if not _live(S):
        return None
    idx = S['index']
    if i == idx + K:
        return 'blue'
    if i <= idx and v == S['ma']:
        return 'green'
    if i == idx:
        return 'yellow'
    return None


def _dim(S, i, v):
    if not _live(S):
        return False
    idx = S['index']
    return idx < i < idx + K or i > idx + K


def _txt(S):
    if not _live(S):
        return f'`nums[k:]` 从下标 `k = {K}` 开始，`index` 从 0 开始：==正好差 k=='
    idx = S['index']
    return f"`index = {idx}`，`j = index + k = {idx + K}`，可用前缀 `nums[0..{idx}]`"


CONFIG = dict(
    num=3979, title='最大有效数对和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀最大值 · enumerate(nums[k:])',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1328'],
    code='''
class Solution(object):
    def maxValidPairSum(self, nums, k):

        p = 0
        ma = 0
        res = 0
        for index, v in enumerate(nums[k:]):
            ma = max(ma, nums[index])
            res = max(res, v + ma)

        return res
''',
    call=f'Solution().maxValidPairSum({NUMS}, {K})',
    expect=16,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=330, cell=104, pointers={'index': 'yellow', 'index + k': 'blue'},
             pointer_labels={'index + k': 'j'}, window=(lambda S: 0 if _live(S) else None, 'index'),
             color=_color, dim=_dim, label='nums（框 = 可用前缀 [0, j−k]，绿 = 前缀最大 ma，蓝 = j）'),
        dict(type='array', var=lambda S: S['nums'][S['k']:] if 'k' in S else None, h=200, cell=104,
             pointers={'index': 'blue'}, label='nums[k:]（enumerate 遍历的切片，下标就是 index）',
             color=lambda S, i, v: 'blue' if _live(S) and i == S['index'] else None),
    ],
    watch=[('index', 'index', 'yellow'), ('v', 'v', 'blue'), ('ma', 'ma', 'green'), ('res', 'res', 'orange')],
    captions={
        'p = 0': '`p` 在后面没有用到',
        'ma = 0': '`ma`：当前可用前缀的最大值',
        'res = 0': '`res = 0`：元素都是正数',
        'for index, v in': lambda S, B, r: (f'切片第 `{S.index}` 个 `v = {S.v}` 就是 `nums[j]`，`j = {S.index + S.k}`；'
                                            f'它==刚好==多出一个可用的 `nums[{S.index}]`'
                                            if B.get('index') != S.index else '遍历结束'),
        'ma = max': lambda S, B, r: (f'`nums[index] = nums[{S.index}] = {S.nums[S.index]}`（即 `nums[j − k]`）加入前缀：'
                                     + (f'==更大==，`ma` → {S.ma}' if S.ma != B.ma else f'不超过 `ma = {S.ma}`')),
        'res = max': lambda S, B, r: (f'`v + ma = {S.v} + {S.ma} = {S.v + S.ma}`，'
                                      + (f'==更新== `res = {S.res}`' if S.res != B.res else f'不超过 `{S.res}`，不变')),
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='j 对应的可用前缀越来越长：只需比较旧最大值和 nums[j−k]',
        complexity='时间 `O(n)`，空间 `O(n − k)`（切片）',
        problem=['下标对 `(i, j)` 有效：`0 ≤ i < j < n` 且 ==`j − i ≥ k`==',
                 '求所有有效对中 `nums[i] + nums[j]` 的最大值',
                 '示例：`[1,3,5,2,8], k = 2` → `13`；本视频 `k = 3` → `16`'],
        quote='每个j对应的前缀最大值都可以通过==对比前一个j的前缀最大值以及nums[j - k]==得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定 `j`，可配对的 `i` 满足 `0 ≤ i ≤ j − k`，取这个前缀的最大值',
              '`enumerate(nums[k:])`：`v = nums[j]`，而 `index = j − k`',
              '先用 `nums[index]` 更新 `ma`，再用 `ma + v` 更新答案'],
        summary=['时间 `O(n)`；切片 `nums[k:]` 额外占 `O(n − k)` 空间',
                 '下标技巧：切片的 `index` 恰好等于 `j − k`，不用再算下标',
                 '变量 `p` 在原代码中未使用',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未作改动'],
    ),
)
