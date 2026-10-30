NUMS, K = [4, 1, 3, 7, 2, 5, 9, 1], 3


def _live(S):
    return 'j' in S and 'mx' in S


def _color(S, i, v):
    if not _live(S):
        return None
    j = S['j']
    if i == j:
        return 'blue'
    if i == j - K and S.get('_line') == 5:
        return 'yellow'
    if i <= j - K and v == S['mx']:
        return 'green'
    return None


def _dim(S, i, v):
    return _live(S) and j_gap(S, i)


def j_gap(S, i):
    j = S['j']
    return j - K < i < j or i > j


def _txt(S):
    if not _live(S):
        return f'`k = {K}`：`j − i ≥ k`，所以 i 只能在 ==`[0, j−k]`== 里选'
    j = S['j']
    return (f"`j = {j}`：可选 `i ∈ [0, {j - K}]`，其中最大 `mx = {S['mx']}`；"
            f"`mx + nums[j] = {S['mx']} + {S['nums'][j]} = {S['mx'] + S['nums'][j]}`")


CONFIG = dict(
    num=3979, title='最大有效数对和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 前缀最大值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1328'],
    code='''
class Solution:
    def maxValidPairSum(self, nums: list[int], k: int) -> int:
        ans = mx = 0
        for j in range(k, len(nums)):
            mx = max(mx, nums[j - k])  # nums[i] 的最大值
            ans = max(ans, mx + nums[j])
        return ans
''',
    call=f'Solution().maxValidPairSum({NUMS}, {K})',
    expect=16,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=330, cell=104, pointers={'j': 'blue', 'j - k': 'yellow'},
             pointer_labels={'j - k': 'j−k'}, window=(lambda S: 0 if _live(S) else None, 'j - k'),
             color=_color, dim=_dim, label='nums（框 = i 的可选范围 [0, j−k]，绿 = 其中最大值 mx，蓝 = j）'),
    ],
    watch=[('j', 'j', 'blue'), 'k', ('mx', 'mx', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ans = mx = 0': '`ans = mx = 0`：元素都是正数，0 可以当初始值',
        'for j in range': lambda S, B, r: (f'枚举右：`j = {S.j}`，i 的范围右边界扩到 `j − k = {S.j - S.k}`'
                                           if B.get('j') != S.j else '所有 j 都枚举完了'),
        'mx = max': lambda S, B, r: (f'范围新增一个数 `nums[{S.j - S.k}] = {S.nums[S.j - S.k]}`：'
                                     + (f'==更大==，`mx` → {S.mx}' if S.mx != B.mx else f'不超过 `mx = {S.mx}`，不变')),
        'ans = max': lambda S, B, r: (f'`mx + nums[{S.j}] = {S.mx} + {S.nums[S.j]} = {S.mx + S.nums[S.j]}`，'
                                      + (f'==更新== `ans = {S.ans}`' if S.ans != B.ans else f'不超过 `{S.ans}`，不变')),
        'return ans': '返回最大有效数对和 =={ans}==',
    },
    cards=dict(
        one_liner='枚举 j，nums[i] 取 [0, j−k] 里的最大值',
        complexity='时间 `O(n − k)`，空间 `O(1)`',
        problem=['下标对 `(i, j)` 有效：`i < j` 且 ==`j − i ≥ k`==',
                 '求所有有效对中 `nums[i] + nums[j]` 的最大值',
                 '示例：`[1,3,5,2,8], k = 2` → `13`；本视频 `k = 3` → `16`'],
        quote='j 每增加 1，范围 [0,j−k] 的右边界就增加 1。所以只需考虑用==新增的元素 nums[j−k]== 去更新 mx 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `j`，`nums[i]` 越大越好 → 求 `[0, j−k]` 中的最大值 `mx`',
              '范围每次只往右多一个数，用 `nums[j−k]` 更新 `mx` 即可',
              '再用 `mx + nums[j]` 更新答案'],
        summary=['时间 `O(n − k)`，空间 `O(1)`',
                 '`j` 从 `k` 开始：更小的 `j` 没有合法的 `i`',
                 '先更新 `mx` 再算答案：`i = j − k` 本身也是合法的',
                 '同类：题单「§0.1 枚举右，维护左」'],
    ),
)
