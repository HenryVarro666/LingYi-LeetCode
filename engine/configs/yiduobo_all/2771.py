def _top(S):
    if 'f' not in S:
        return '`f` / `g`：以 nums1[index] / nums2[index] 结尾的最长非递减子数组长度'
    return f"`f = {S['f']}`（选 nums1[{S.get('index', 0)}]），`g = {S['g']}`（选 nums2[{S.get('index', 0)}]），`res = {S['res']}`"


def _col(S, i, v):
    k = S.get('index')
    if k is None:
        return None
    return 'blue' if i == k else 'pink' if i == k - 1 else None


CONFIG = dict(
    num=2771, title='构造最长非递减子数组', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='动态规划 · 变量 f / g 滚动',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1792'],
    code='''
class Solution(object):
    def maxNonDecreasingLength(self, nums1, nums2):

        f = g = res = 1
        for index in range(1, len(nums1)):
            pre_f, pre_g = f, g
            
            f = g = 1

            if nums1[index] >= nums1[index - 1]:
                f = max(pre_f + 1, f)
            if nums1[index] >= nums2[index - 1]:
                f = max(pre_g + 1, f)
            
            if nums2[index] >= nums2[index - 1]:
                g = max(pre_g + 1, g)
            if nums2[index] >= nums1[index - 1]:
                g = max(pre_f + 1, g)
        
            res = max(res, f, g)
        
        return res
''',
    call='Solution().maxNonDecreasingLength([1,3,2,1,1], [2,2,3,4,0])',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='nums1', label='nums1（蓝 = 当前列，粉 = 上一列）', cell=100, h=220,
             pointers={'index': 'blue', 'index - 1': 'pink'}, color=_col),
        dict(type='array', var='nums2', label='nums2', cell=100, h=220, index=False, color=_col),
        dict(type='text', fn=lambda S: (f"上一列：`pre_f = {S['pre_f']}`（nums1 结尾），`pre_g = {S['pre_g']}`（nums2 结尾）" if 'pre_f' in S else ''), size=24, h=60),
    ],
    watch=[('pre_f', 'pre_f', 'blue'), ('pre_g', 'pre_g', 'pink'), ('f', 'f', 'cyan'), ('g', 'g', 'purple'), ('res', 'res', 'green')],
    captions={
        'f = g = res = 1': '第 0 列：`f = g = 1`，答案先是 `res = 1`',
        'for index in range': lambda S, B, r: (f'处理第 `{S.index}` 列：`nums1[{S.index}] = {S.nums1[S.index]}`，`nums2[{S.index}] = {S.nums2[S.index]}`' if 'index' in S and S.get('index') != B.get('index') else '全部处理完'),
        'pre_f, pre_g = f, g': '先把上一列的 `f, g` 存成 `pre_f = {pre_f}`，`pre_g = {pre_g}`，下面要覆盖 f、g',
        'f = g = 1': '先假设谁也接不上，只有自己这一个数：`f = g = 1`',
        'if nums1[index] >= nums1[index - 1]': lambda S, B, r: (f'`{S.nums1[S.index]} ≥ {S.nums1[S.index - 1]}`：nums1 接在上一列 nums1 后面 → `f = pre_f + 1 = {S.pre_f + 1}`'
                                                                if S.nums1[S.index] >= S.nums1[S.index - 1] else f'`{S.nums1[S.index]} < {S.nums1[S.index - 1]}`：nums1 接不上上一列的 nums1'),
        'if nums1[index] >= nums2[index - 1]': lambda S, B, r: (f'`{S.nums1[S.index]} ≥ {S.nums2[S.index - 1]}`：nums1 接在上一列 nums2 后面 → `f = max(pre_g + 1, f)` = =={S.f}=='
                                                                if S.nums1[S.index] >= S.nums2[S.index - 1] else f'`{S.nums1[S.index]} < {S.nums2[S.index - 1]}`：nums1 接不上上一列的 nums2'),
        'if nums2[index] >= nums2[index - 1]': lambda S, B, r: (f'`{S.nums2[S.index]} ≥ {S.nums2[S.index - 1]}`：nums2 接在上一列 nums2 后面 → `g = pre_g + 1 = {S.pre_g + 1}`'
                                                                if S.nums2[S.index] >= S.nums2[S.index - 1] else f'`{S.nums2[S.index]} < {S.nums2[S.index - 1]}`：nums2 接不上上一列的 nums2'),
        'if nums2[index] >= nums1[index - 1]': lambda S, B, r: (f'`{S.nums2[S.index]} ≥ {S.nums1[S.index - 1]}`：nums2 接在上一列 nums1 后面 → `g = max(pre_f + 1, g)` = =={S.g}=='
                                                                if S.nums2[S.index] >= S.nums1[S.index - 1] else f'`{S.nums2[S.index]} < {S.nums1[S.index - 1]}`：nums2 接不上上一列的 nums1'),
        'f = max(pre_f': '`f` → {f}',
        'f = max(pre_g': '`f` → {f}',
        'g = max(pre_g': '`g` → {g}',
        'g = max(pre_f': '`g` → {g}',
        'res = max': '用这一列更新答案：`res = max({B.res}, {f}, {g})` = =={res}==',
        'return res': '最长非递减子数组 `{res}`',
    },
    cards=dict(
        one_liner='每列两个状态：选 nums1 或选 nums2，各自接上一列的两个状态',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个位置可以从 `nums1[i]`、`nums2[i]` 中选一个组成 `nums3`',
                 '求 `nums3` 中最长非递减子数组的长度',
                 '本视频：`[1,3,2,1,1]` 和 `[2,2,3,4,0]` → `4`'],
        quote='令f[i]和g[i]分别表示由nums1[i]和nums2[i]结尾的最长递减子数组长度。……若都不满足，就只能是f[i] = 1，表示这个子数组中只有nums1[i]这一个数。',
        quote_src='—— yiduobo 题解原文（原文“递减”为笔误，应为非递减）',
        idea=['`f[i]`：第 i 位取 nums1 的最长长度；`g[i]`：第 i 位取 nums2',
              '`f` 可以接在上一列的 `f` 或 `g` 后面，只要值不变小，取较大者 +1',
              '`g` 同理；每一列都用 `f, g` 更新答案，并用 `pre_f, pre_g` 省掉数组'],
        result='`(f,g)`：`(2,2)→(3,3)→(1,4)→(2,1)`，最大是 `4` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先把 `f, g` 存成 `pre_f, pre_g`，再重置为 1，避免算 `g` 时用到新的 `f`',
                 '子数组连续：接不上就从 1 重新开始',
                 '原文为 Python 2 风格，Python 3 下无需修改即可运行',
                 '对比灵神：灵神用 `pairwise` 同时取两列，这里用下标 `index`'],
    ),
)
