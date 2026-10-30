_IDX = '[*zip(nums1, nums2)].index((x1, y1))'
_PREV = '[*zip(nums1, nums2)].index((x1, y1)) - 1'


def _top(S):
    if 'f0' not in S:
        return '`f0`：以 nums1[i] 结尾的最长非递减子数组；`f1`：以 nums2[i] 结尾的'
    return f"以 nums1[i] 结尾 `f0 = {S['f0']}`，以 nums2[i] 结尾 `f1 = {S['f1']}`，答案 `ans = {S['ans']}`"


def _col(S, i, v):
    if 'x1' not in S:
        return None
    k = list(zip(S['nums1'], S['nums2'])).index((S['x1'], S['y1']))
    if i == k:
        return 'blue'
    if i == k - 1:
        return 'pink'
    return None


CONFIG = dict(
    num=2771, title='构造最长非递减子数组', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 滚动变量 f0 / f1',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1792'],
    code='''
class Solution:
    def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
        ans = f0 = f1 = 1
        for (x0, y0), (x1, y1) in pairwise(zip(nums1, nums2)):
            f = g = 1
            if x0 <= x1: f = f0 + 1
            if y0 <= x1: f = max(f, f1 + 1)
            if x0 <= y1: g = f0 + 1
            if y0 <= y1: g = max(g, f1 + 1)
            f0, f1 = f, g
            ans = max(ans, f0, f1)
        return ans
''',
    call='Solution().maxNonDecreasingLength([1,3,2,1], [2,2,3,4])',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='nums1', label='nums1（蓝 = 当前列，粉 = 上一列）', cell=100, h=230,
             pointers={_IDX: 'blue', _PREV: 'pink'}, pointer_labels={_IDX: 'i', _PREV: 'i-1'}, color=_col),
        dict(type='array', var='nums2', label='nums2', cell=100, h=230, index=False, color=_col),
        dict(type='text', fn=lambda S: (f"`f` = 选 nums1[i]={S['x1']} 结尾，`g` = 选 nums2[i]={S['y1']} 结尾；上一列选 nums1={S['x0']} 或 nums2={S['y0']}" if 'x0' in S else ''), size=22, h=60),
    ],
    watch=[('f0', 'f0', 'blue'), ('f1', 'f1', 'pink'), ('f', 'f', 'cyan'), ('g', 'g', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = f0 = f1 = 1': '只有第 0 列时，选哪个都是长度 1：`f0 = f1 = ans = 1`',
        'for (x0, y0)': lambda S, B, r: (f'处理下一列：上一列 `({S.x0}, {S.y0})`，这一列 `({S.x1}, {S.y1})`' if 'x1' not in B or S.x1 != B.x1 or S.y1 != B.y1 or S.x0 != B.x0 else '所有列都处理完了'),
        'f = g = 1': '先假设两种选法都接不上，只有自己：`f = g = 1`',
        'if x0 <= x1': lambda S, B, r: (f'`x0 = {S.x0} ≤ x1 = {S.x1}` → 上一列选 nums1 能接在前面，`f = f0 + 1 = {S.f0 + 1}`'
                                        if S.x0 <= S.x1 else f'`x0 = {S.x0} > x1 = {S.x1}` → 上一列选 nums1 接不上'),
        'if y0 <= x1': lambda S, B, r: (f'`y0 = {S.y0} ≤ x1 = {S.x1}` → 上一列选 nums2 也能接，`f = max(f, f1 + 1)` = =={S.f}=='
                                        if S.y0 <= S.x1 else f'`y0 = {S.y0} > x1 = {S.x1}` → 上一列选 nums2 接不上，`f` 仍为 {S.f}'),
        'if x0 <= y1': lambda S, B, r: (f'`x0 = {S.x0} ≤ y1 = {S.y1}` → 这一列选 nums2，接在 nums1 之后，`g = f0 + 1 = {S.f0 + 1}`'
                                        if S.x0 <= S.y1 else f'`x0 = {S.x0} > y1 = {S.y1}` → 接不上'),
        'if y0 <= y1': lambda S, B, r: (f'`y0 = {S.y0} ≤ y1 = {S.y1}` → 接在 nums2 之后，`g = max(g, f1 + 1)` = =={S.g}=='
                                        if S.y0 <= S.y1 else f'`y0 = {S.y0} > y1 = {S.y1}` → 接不上，`g` 仍为 {S.g}'),
        'f0, f1 = f, g': '滚动：`f0 = {f}`，`f1 = {g}`（上一列的状态被覆盖）',
        'ans = max(ans': '`ans = max({B.ans}, {f0}, {f1})` = =={ans}==',
        'return ans': '最长非递减子数组长度 `{ans}`',
    },
    cards=dict(
        one_liner='f0 / f1 分别记录“这一列选 nums1 / nums2”的最长长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个位置 `nums3[i]` 可以取 `nums1[i]` 或 `nums2[i]`',
                 '求 `nums3` 的==最长非递减子数组==长度',
                 '示例：`[1,3,2,1]` 和 `[2,2,3,4]` → `4`（取 1,2,3,4）'],
        quote='定义 dfs(i,j) 表示以 nums_j[i] 结尾的最长非递减子数组的长度。用“枚举选哪个”来思考：如果 nums1[i-1] ≤ nums_j[i]，那么下一步选 nums1[i-1]……',
        quote_src='—— 灵茶山艾府题解',
        idea=['记忆化搜索 1:1 翻译成递推 `f[i][j]`，再发现只依赖上一列，压成 `f0 / f1`',
              '每一列 2 种选法 × 上一列 2 种选法 = 4 个判断',
              '接得上就在上一列长度上 +1，都接不上就是 1，每列都用来更新 `ans`'],
        result='`(f0, f1)` 依次为 `(2,2) → (3,3) → (1,4)`，`ans = 4` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f0, f1 = f, g` 要同时更新，别用新的 `f` 去算 `g`',
                 '这是子数组（连续），所以接不上就重新从 1 开始',
                 '题解同时给了记忆化搜索和二维递推，本视频演示滚动变量版本',
                 '思考题：改成子序列怎么做？'],
    ),
)
