CONFIG = dict(
    num=3117, title='划分数组得到最小的值之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 选或不选 · 记忆化搜索',
    tags=['灵神题单·位运算', '灵神题单·动态规划', '难度分 2735'],
    code='''
class Solution:
    def minimumValueSum(self, nums: List[int], andValues: List[int]) -> int:
        n, m = len(nums), len(andValues)
        @cache
        def dfs(i: int, j: int, and_: int) -> int:
            if n - i < m - j:  # 剩余元素不足
                return inf
            if j == m:  # 分了 m 段
                return 0 if i == n else inf
            and_ &= nums[i]
            res = dfs(i + 1, j, and_)  # 不划分
            if and_ == andValues[j]:  # 划分，nums[i] 是这一段的最后一个数
                res = min(res, dfs(i + 1, j + 1, -1) + nums[i])
            return res
        ans = dfs(0, 0, -1)
        return ans if ans < inf else -1
''',
    call='Solution().minimumValueSum([1, 4, 3, 2], [0, 3, 2])',
    expect=9,
    max_steps=110,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前考虑的 i）', h=150, cell=80, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None,
             dim=lambda S, k, v: 'i' in S and k < S['i']),
        dict(type='array', var='andValues', label='andValues（粉 = 当前这一段的目标 j）', h=150, cell=80, index=False,
             color=lambda S, k, v: 'pink' if k == S.get('j') else None,
             dim=lambda S, k, v: 'j' in S and k < S['j']),
        dict(type='text', fn=lambda S: (f"`dfs({S['i']}, {S['j']}, and_={S['and_']})`：已分 `{S['j']}` 段，当前段 AND = ==`{S['and_']}`==，目标 `{S['andValues'][S['j']] if S['j'] < len(S['andValues']) else '-'}`" if 'and_' in S and 'j' in S and 'i' in S else ''), size=24, h=70),
        dict(type='calls', h=260),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('and_', 'and_', 'orange'), ('res', 'res', 'green')],
    captions={
        'n, m = len': '`n = {n}` 个数，要分成 `m = {m}` 段',
        'if n - i < m - j': lambda S, B, r: (f'剩余 `{S.n - S.i}` 个数 < 还需 `{S.m - S.j}` 段：不够分 → 返回 ∞' if S.n - S.i < S.m - S.j
                                             else f'剩余 `{S.n - S.i}` 个数 ≥ 还需 `{S.m - S.j}` 段，还有希望'),
        'return inf': lambda S, B, r: ('不可能划分 → `inf`'),
        'if j == m': lambda S, B, r: (f'`j = m`：已经分够 {S.m} 段，看元素是否用完' if S.j == S.m else f'`j = {S.j} < m = {S.m}`：还要继续分'),
        'return 0 if i == n': lambda S, B, r: ('分够了、元素也恰好用完 → 成功，返回 0' if S.i == S.n else '分够了但还有元素剩下 → 失败，返回 ∞'),
        'and_ &= nums[i]': '把 `nums[{i}] = {nums[i]}` 并入当前段：`and_` = {B.and_} & {nums[i]} = =={and_}==',
        'res = dfs(i + 1, j, and_)': '先试「不划分」：`nums[{i}]` 不是段尾，继续往右。结果 `res = {res}`',
        'if and_ == andValues[j]': lambda S, B, r: (f'`and_ = {S.and_}` == `andValues[{S.j}] = {S.andValues[S.j]}`：可以在这里划分，`nums[{S.i}]` 作为段尾'
                                                   if S.and_ == S.andValues[S.j]
                                                   else f'`and_ = {S.and_}` ≠ `andValues[{S.j}] = {S.andValues[S.j]}`：不能在这里划分'),
        'res = min(res, dfs': '划分：`nums[{i}]` 作段尾，答案加上 `{nums[i]}`；下一段从 `-1`（全 1）重新开始，取 `min(不划分, 划分)`',
        'return res': '`dfs({i}, {j}, …)` 的最小和 = =={res}==',
        'ans = dfs(0, 0, -1)': '`ans` = {ans}',
        'return ans if': '`ans = {ans}`：有解就返回，`inf` 说明不可能 → `-1`',
    },
    cards=dict(
        one_liner='选或不选：nums[i] 是不是这一段的最后一个数',
        complexity='时间 `O(nm log U)`，空间 `O(nm log U)`',
        problem=['把 `nums` 分成 `m` 段，第 `i` 段的 AND 必须等于 `andValues[i]`',
                 '每段的「值」是它的最后一个元素，求值之和最小；不可能则 `-1`',
                 '示例：`nums=[1,4,3,3,2], andValues=[0,3,3,2]` → `12`',
                 '本视频：`nums=[1,4,3,2], andValues=[0,3,2]` → `9`'],
        quote='我们并不需要知道这个子数组的前面具体有哪些数，只需要知道前面的元素的 AND 值等于 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j, and_)`：考虑到 `nums[i]`，已分 `j` 段，当前段已 AND 出 `and_`',
              '不划分：`dfs(i+1, j, and_)`；划分（需 `and_ == andValues[j]`）：`dfs(i+1, j+1, -1) + nums[i]`',
              '`and_` 只有 `O(log U)` 种取值（AND 只会变小），所以加 `@cache` 就够快'],
        summary=['时间 `O(nm log U)`，空间 `O(nm log U)`',
                 '新的一段用 `-1`（全 1）开始，与任何数 AND 都是它本身',
                 '剩余元素不足、`j == m` 但没用完，都要返回 `inf`',
                 '本视频演示方法一；题解的方法二是单调队列 + logTrick 的递推，时间同阶、空间 `O(n)`'],
    ),
)
