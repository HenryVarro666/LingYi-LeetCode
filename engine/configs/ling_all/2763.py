def _txt(S):
    ln = S.get('_line', 0)
    if 'r' in S and ln >= 14:
        i, x, r = S['i'], S['x'], S['r']
        l = S['idx'][x - 1]
        return f"`nums[{i}] = {x}` 贡献：左端点 `{i} − {l}` 个 × 右端点 `{r} − {i}` 个"
    if 'x' in S and 7 <= ln <= 9:
        return f"`nums[{S['i']}] = {S['x']}` 往右看：最近的 `{S['x']}` 或 `{S['x'] - 1}` 在哪？没有就是 `n`"
    return '贡献法：数每个 x 在多少子数组里「是排序后相邻差 > 1 的较小数」'


CONFIG = dict(
    num=2763, title='所有子数组中不平衡数字之和', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='贡献法 · 最近下标',
    tags=['灵神题单', '难度分 2700'],
    code='''
class Solution:
    def sumImbalanceNumbers(self, nums: List[int]) -> int:
        n = len(nums)
        right = [0] * n  # nums[i] 右侧的 x 和 x-1 的最近下标（不存在时为 n）
        idx = [n] * (n + 1)
        for i in range(n - 1, -1, -1):
            x = nums[i]
            right[i] = min(idx[x], idx[x - 1])
            idx[x] = i

        ans = 0
        idx = [-1] * (n + 1)
        for i, (x, r) in enumerate(zip(nums, right)):
            # 统计 x 能产生多少贡献
            ans += (i - idx[x - 1]) * (r - i)  # 子数组左端点个数 * 子数组右端点个数
            idx[x] = i
        # 上面计算的时候，每个子数组的最小值必然可以作为贡献，而这是不合法的
        # 所以每个子数组都多算了 1 个不合法的贡献
        return ans - n * (n + 1) // 2
''',
    call='Solution().sumImbalanceNumbers([1,3,3,3,5])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200, label='nums',
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] and 'x' in S else None),
        dict(type='array', var='right', h=200, label='right[i]：右侧最近的 x 或 x−1（没有 = n）',
             color=lambda S, i, v: 'green' if 'i' in S and 'x' in S and i == S['i'] and 'r' not in S and S.get('_line') in (8, 9) else ('blue' if 'r' in S and i == S.get('i') else None)),
        dict(type='array', var='idx', h=200, label='idx[v]：值 v 最近出现的下标',
             color=lambda S, i, v: None if S.get('_line') not in (7, 8, 9, 15, 16) or 'x' not in S else ('yellow' if i == S['x'] else ('orange' if i == S['x'] - 1 else None))),
    ],
    watch=['i', 'x', 'r', ('ans', 'ans', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'right = [0] * n': '`right[i]`：`nums[i]` 右侧，值为 `x` 或 `x−1` 的最近下标；先占位',
        'idx = [n] * (n + 1)': '`idx[v]` 记录值 `v` 最近出现的位置；从右往左扫，初值 `n` = 右侧没有',
        'for i in range(n - 1': lambda S, B, r: ('从右往左扫完了' if 'i' in B and S['i'] == B.i == 0 else f"从右往左：`i = {S['i']}`"),
        'x = nums[i]': '`x = nums[{i}] = {x}`',
        'right[i] = min': '右侧 `x`（`idx[{x}]`）和 `x−1`（`idx[{x-1}]`）谁更近：`min({idx[x]}, {idx[x-1]})` = =={right[i]}==：`right[{i}]` 是右端点的上限（不含）',
        9: '`idx[{x}] = {i}`：值 `{x}` 最近出现的位置更新为当前下标',
        'ans = 0': '`ans` 累加所有贡献',
        'idx = [-1] * (n + 1)': '第二遍从左往右，`idx[v]` 重置为 `-1` = 左侧没有',
        'for i, (x, r) in enumerate': lambda S, B, r: ('从左往右扫完了' if 'i' in B and S['i'] == B.i == len(S['nums']) - 1 else f"从左往右：`nums[{S['i']}] = {S['x']}`，右边界上限 `r = {S['r']}`"),
        'ans += (': '左端点：`i − idx[x−1]` = `{i} − ({idx[x-1]})` = {i - idx[x-1]} 个；右端点：`r − i` = `{r} − {i}` = {r - i} 个 → `ans` 加 {(i - idx[x-1]) * (r - i)}，得 =={ans}==',
        16: '`idx[{x}] = {i}`：记下 `{x}` 最近出现的位置',
        'return ans': '每个子数组的最小值都被多算了一次：`ans − n(n+1)/2 = {ans} − {n * (n + 1) // 2}` = =={ret}==',
    },
    cards=dict(
        one_liner='不数子数组，数每个 x 在多少子数组里贡献 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的「不平衡数字」= 排序后相邻差 `> 1` 的位置个数；求 `nums` 所有子数组的不平衡数字之和',
                 '示例：`[1,3,3,3,5]` → `8`',
                 '`n ≤ 1000`，`1 ≤ nums[i] ≤ n`'],
        quote='上面计算的时候，每个子数组的最小值必然可以作为贡献，而这是不合法的，所以每个子数组都多算了 1 个不合法的贡献。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['把「相邻差 > 1」记到较小数 `x` 头上：子数组里有 `x`，且没有 `x+1`（也不能有重复的 `x` 抢位）',
              '先从右往左求 `right[i]`：右侧最近的 `x` 或 `x−1`，它是右端点的上限',
              '再从左往右：左端点范围 `i − idx[x−1]`，右端点范围 `r − i`，相乘；最后减去 `n(n+1)/2`'],
        summary=['时间 `O(n)`，空间 `O(n)`；方法一是枚举左端点 + 哈希标记的 `O(n²)` 写法，一句话带过',
                 '易错：`right` 同时看 `x` 和 `x−1`，防止重复值重复计数；`idx` 第二遍要重置为 `-1`',
                 '最后要减 `n(n+1)/2`：每个子数组的最小值被当成了「较小数」多算一次',
                 '思考题：差值改成 `> k` 时把 `x−1` 换成 `x−k` 之类的窗口，思路类似'],
    ),
)
