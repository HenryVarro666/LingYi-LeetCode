def _txt(S):
    if 'r' not in S or 'nums' not in S or S['r'] >= len(S['nums']):
        return ''
    r = S['r']
    v = S['nums']
    if 'l' not in S:
        return f"第一阶段：`nums[{r}] + nums[{r}] = {v[r] * 2}`，target = {S['target']}；以 r 为右端点、左端点任意 → `2^r = {2 ** r}` 种"
    l = S['l']
    if l < 0:
        return '`l` 已经移出左边界：没有合法的左端点了'
    return f"第二阶段：`nums[l] + nums[r] = {v[l]} + {v[r]} = {v[l] + v[r]}`，target = {S['target']}；`l` 是最大的合法左端点"


CONFIG = dict(
    num=1498, title='满足条件的子序列数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举右端点 r + 左端点 l 单调左移',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2276'],
    code='''
class Solution(object):
    def numSubseq(self, nums, target):

        n = len(nums)
        mod = 10 ** 9 + 7

        pow2 = [1]
        for index in range(1, n + 1):
            pow2.append(pow2[-1] + pow2[-1])
            if pow2[-1] >= mod:
                pow2[-1] -= mod

        nums = sorted(nums)
        res = 0
        r = 0
        while r < n:
            if nums[r] + nums[r] > target:
                break
            
            res += pow2[r]
            if res >= mod:
                res -= mod
        
            r += 1

        l = r - 1
        while r < n:
            while l >= 0 and nums[l] + nums[r] > target:
                l -= 1
            if l < 0:
                return res
            
            res += pow2[r]
            if res >= mod:
                res -= mod
            res -= pow2[r - l - 1]
            if res < 0:
                res += mod
        
            r += 1

        return res
''',
    call='Solution().numSubseq([4, 7, 3, 2, 6, 3], 12)',
    expect=61,
    skip=['pow2.append', 'if pow2[-1] >= mod', 'pow2[-1] -= mod', 'if res >= mod', 'res -= mod', 'if res < 0', 'res += mod', 'for index'],
    views=[
        dict(type='array', var='nums', h=230, label='nums（排序后；粉 = r，蓝 = l）',
             pointers={'r': 'pink', 'l': 'blue'},
             color=lambda S, i, v: ('pink' if i == S['r'] else 'blue' if i == S.get('l') else None) if 'r' in S else None),
        dict(type='array', var='pow2', h=200, label='pow2[i] = 2^i（预处理）'),
        dict(type='text', fn=_txt),
    ],
    watch=[('r', 'r', 'pink'), ('l', 'l', 'blue'), ('res', 'res', 'green')],
    captions={
        'pow2 = [1]': '先预处理 2 的幂：`pow2[i] = 2^i`，后面直接查表',
        'nums = sorted': '题目只关心最小值和最大值 → ==先排序==，再用双指针定子序列的两端',
        'res = 0': '`res` 累计合法子序列数',
        'r = 0': '从左向右枚举子序列的右边界 `r`',
        'if nums[r] + nums[r] > target': lambda S, B, ret: (
            f'`{S.nums[S.r]} + {S.nums[S.r]} = {S.nums[S.r] * 2} > {S.target}`：连 `nums[r]` 自己当最小最大都不行 → 第一阶段结束'
            if S.nums[S.r] * 2 > S.target else
            f'`{S.nums[S.r]} + {S.nums[S.r]} = {S.nums[S.r] * 2} <= {S.target}`：以 `r` 结尾、左端任意的子序列全部合法'),
        'res += pow2[r]': lambda S, B, ret: (f'先假设左端点不受限：`nums[{S.r}]` 必选，前面 `{S.r}` 个数随便选 → 加 `2^{S.r}`，`res` → {S.res}，下一行再减去不合法的' if 'l' in S
                                             else f'`nums[{S.r}]` 必选，前面 `{S.r}` 个数可选可不选 → `2^{S.r}` 种，`res` → {S.res}'),
        'r += 1': lambda S, B, ret: f'`r` → {S.r}',
        'break': '跳出第一阶段，`r` 停在 {r}',
        'l = r - 1': '`l` 从 `r - 1` 起向左找最大的合法左端点：`l = {l}`',
        'while r < n': lambda S, B, ret: (f'`r = {S.r} < {S.n}`，继续枚举右端点' if S.r < S.n else f'`r = {S.r}` 到头 → 结束'),
        'while l >= 0': lambda S, B, ret: (
            f'`nums[{S.l}] + nums[{S.r}] = {S.nums[S.l] + S.nums[S.r]} > {S.target}`：太大，`l` 往左找' if S.l >= 0 and S.nums[S.l] + S.nums[S.r] > S.target
            else (f'`l = {S.l}` 出界' if S.l < 0 else f'`nums[{S.l}] + nums[{S.r}] = {S.nums[S.l] + S.nums[S.r]} <= {S.target}`：`l` 就停在这里')),
        'l -= 1': '`nums[r]` 变大了，`nums[l]` 必须更小：`l` → {l}',
        'if l < 0': lambda S, B, ret: ('`l < 0`：找不到合法左端点，后面的 `r` 更大更不行 → 直接返回' if S.l < 0 else '`l >= 0`：找到了合法的左端点'),
        'res -= pow2[r - l - 1]': '左端点 `0..{l}` 共 `2^r - 2^(r-l-1)` 种：减掉 `2^{r - l - 1} = {pow2[r - l - 1]}` → `res = {res}`',
        'return res': '返回 `res = {res}`',
    },
    cards=dict(
        one_liner='排序后枚举右端点：左端点 0..l 的方案数合起来是 2^r − 2^(r−l−1)',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['统计 `nums` 中「最小值 + 最大值 `<= target`」的非空子序列个数，对 `10^9+7` 取模',
                 '示例：`nums = [3,5,6,7], target = 9` → `4`',
                 '本视频：`[4,7,3,2,6,3], target = 12` → `61`'],
        quote='对于任意满足nums[r] + nums[r] <= target的r而言，除了nums[r]必选之外，其他的nums[0]到nums[r - 1]共r个数都是可选可不选的，因此这里一共就有2^r种合法的子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后从左向右枚举右边界 `r`：先处理 `2*nums[r] <= target` 的前缀，每个 `r` 贡献 `2^r`',
              '之后 `l` 只左移不回头：`nums[r]` 变大，合法左端点只会更靠左',
              '左端点 `p` 取 `0..l`，方案数求和后化成 `2^r - 2^(r-l-1)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（预处理 `pow2`）',
                 '易错：`l` 出界要直接 `return`，且第二阶段的 `l` 从 `r - 1` 开始',
                 '取模用「加完再减 mod」，减法后若为负要补 mod',
                 '对比灵神：灵神枚举最小值、一次删一端；yiduobo 枚举最大值、用等比求和'],
    ),
)
