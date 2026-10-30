_I = lambda S: S['_inner'].get('i')
_J = lambda S: S['_inner'].get('j')


def _ncolor(S, k, v):
    i, j = _I(S), _J(S)
    if i is None or j is None:
        return None
    if k == i:
        return 'blue'
    if k == j:
        return 'pink'
    return None


def _dim(S, k, v):
    i, j = _I(S), _J(S)
    return i is not None and j is not None and not (i <= k <= j)


def _formula(S, B):
    I = B['_inner']
    i, j, t = I.get('i'), I.get('j'), I.get('target')
    if i is None or j is None:
        return '三种首操作各定一个 `target`，之后每步的和都必须等于它'
    ln = B.get('_line')
    nums = S['nums']
    if i >= j:
        return f'区间 `[{i}, {j}]` 至多剩 1 个数：无法再操作 → ==0=='
    if ln == 13:
        return f'删前两个：`{nums[i]} + {nums[i + 1]}` 对比 `target = {t}`'
    if ln == 15:
        return f'删后两个：`{nums[j - 1]} + {nums[j]}` 对比 `target = {t}`'
    if ln == 17:
        return f'删头尾：`{nums[i]} + {nums[j]}` 对比 `target = {t}`'
    return f'`dfs({i}, {j}, {t})`：区间 `[{i}, {j}]` 最多还能操作几次（`target = {t}`）'


CONFIG = dict(
    num=3040, title='相同分数的最大操作数目 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='区间 DP（记忆化搜索 + 提前剪枝）',
    tags=['灵神题单', '动态规划', '难度分 1709'],
    code='''
class Solution:
    def maxOperations(self, nums: List[int]) -> int:
        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, j: int, target: int) -> int:
            nonlocal done
            if done:
                return 0
            if i >= j:
                done = True
                return 0
            res = 0
            if nums[i] + nums[i + 1] == target:  # 删除前两个数
                res = max(res, dfs(i + 2, j, target) + 1)
            if nums[j - 1] + nums[j] == target:  # 删除后两个数
                res = max(res, dfs(i, j - 2, target) + 1)
            if nums[i] + nums[j] == target:  # 删除第一个和最后一个数
                res = max(res, dfs(i + 1, j - 1, target) + 1)
            return res

        done = False
        n = len(nums)
        res1 = dfs(2, n - 1, nums[0] + nums[1])  # 删除前两个数
        res2 = dfs(0, n - 3, nums[-2] + nums[-1])  # 删除后两个数
        res3 = dfs(1, n - 2, nums[0] + nums[-1])  # 删除第一个和最后一个数
        return max(res1, res2, res3) + 1  # 加上第一次操作
''',
    call='Solution().maxOperations([3, 2, 1, 2, 3, 4])',
    expect=3,
    skip=['done = False', 'n = len(nums)', 'res = 0', 'nonlocal done'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = i，粉 = j，暗 = 已删掉）', h=190, cell=76,
             pointers={_I: 'blue', _J: 'pink'}, pointer_labels={_I: 'i', _J: 'j'},
             color=_ncolor, dim=_dim),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='calls', h=260),
    ],
    watch=[('i', _I, 'blue'), ('j', _J, 'pink'), ('target', lambda S: S['_inner'].get('target'), 'yellow'),
           ('done', 'done', 'orange')],
    captions={
        'if done': lambda S, B, r: ('`done = True`：已经能把数组删光（操作次数达到上限 `n // 2`），后面不用算了 → 直接返回 0'
                                    if B.done else '`done = False`：还没找到“能删光”的方案，继续'),
        'if i >= j': lambda S, B, r: (f'`i = {B.i} ≥ j = {B.j}`：==至多剩一个数==，无法操作；而能走到这里说明前面每步都合法 → 能删到极限，`done = True`'
                                      if B.i >= B.j else f'`i = {B.i} < j = {B.j}`：还有 ≥ 2 个数，继续枚举操作'),
        'dfs(i + 2, j, target)': '和等于 `target`：删前两个，子问题 `dfs({B.i+2}, {B.j})`，次数 +1',
        'dfs(i, j - 2, target)': '和等于 `target`：删后两个，子问题 `dfs({B.i}, {B.j-2})`，次数 +1',
        'dfs(i + 1, j - 1, target)': '和等于 `target`：删头尾，子问题 `dfs({B.i+1}, {B.j-1})`，次数 +1',
        'done = True': '标记 `done = True`：已经删到了上限 `n // 2` 次，其它方案不可能更多，后面的递归全部可以直接返回',
        'return 0': '返回 0（再往里已经没有数可以删）',
        'return res': '区间 `[{i}, {j}]`（`target = {target}`）最多还能操作 =={ret}== 次',
        'res1 = dfs': '第一次删前两个数，`target = nums[0] + nums[1] = {nums[0] + nums[1]}`，从 `dfs(2, n-1)` 开始',
        'res2 = dfs': '第一次删后两个数，`target = nums[-2] + nums[-1] = {nums[-2] + nums[-1]}`；若 `done` 已为真，这里直接返回 0',
        'res3 = dfs': '第一次删头尾，`target = nums[0] + nums[-1] = {nums[0] + nums[-1]}`；若 `done` 已为真，这里直接返回 0',
        'return max(res1': '三种首操作取最大 `max({res1}, {res2}, {res3})`，再 `+ 1`（第一次操作）= =={ret}==',
    },
    cards=dict(
        one_liner='第一次操作定下 target，之后用区间 DP 数最多能删几次',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['每次可删==前两个==、==后两个==、或==首尾两个==，分数 = 被删元素之和',
                 '要求==所有操作分数相同==，求最多能操作几次',
                 '示例：`[3,2,1,2,3,4]` → `3`；`[3,2,6,1,4]` → `2`'],
        quote='无论怎么删除，剩下的都是连续子数组，都是和原问题相似的，规模更小的子问题。……当你发现子问题是从两侧向内缩小的，就可以往区间 DP 上想了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j, target)`：区间 `[i, j]` 在固定分数 `target` 下最多还能删几次',
              '三种首操作只会产生==至多三个 target==，各跑一遍区间 DP',
              '剪枝：答案上限是 `n // 2`，一旦走到 `i ≥ j` 就设 `done`，后面全部直接返回'],
        summary=['时间 `O(n^2)`：状态数 `O(n^2)` × 转移 `O(1)`（`target` 只有 3 种，且互不重叠）',
                 '易错：入口是 `dfs(2,n-1)`、`dfs(0,n-3)`、`dfs(1,n-2)`，最后==别忘了 +1==',
                 '三次区间 DP 可共用同一个 `@cache`：不同 target 不会递归到同一 `(i, j)`',
                 '题解还给了不带剪枝的“优化前”写法，以及 1:1 翻译成递推的写法（随机数据下递推更慢）'],
    ),
)
