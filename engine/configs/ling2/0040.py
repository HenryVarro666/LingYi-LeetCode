CANDS = [2, 5, 2, 1, 2]


def _arr_color(S, i, v):
    if 'i' not in S or 'n' not in S:
        return None
    if S['_line'] in (30, 31, 32) and 'x' in S and v == S['x'] and i < S['i']:
        # 选过的 x 一定是最前面的几个副本，所以本层的 x 从 first + path.count(x) 开始
        start = S['candidates'].index(S['x']) + S['path'].count(S['x'])
        return 'purple' if i >= start else None  # 正在被跳过的相同元素
    if i == S['i'] and S['i'] < S['n']:
        return 'blue'
    return None


def _skip_cap(S, B, ret):
    if S.i < S.n and S.candidates[S.i] == S.x:
        return f'`candidates[{S.i}] = {S.x}` 和 `x` ==相同== → 也不选，继续跳过'
    if S.i < S.n:
        return f'`candidates[{S.i}] = {S.candidates[S.i]} ≠ {S.x}` → 停下，相同的 `{S.x}` 都跳过了'
    return f'`i = {S.i} = n`：后面全是 `{S.x}`，都跳过了'


CONFIG = dict(
    num=40, title='组合总和 II', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='选或不选 · 不选就跳过所有相同元素',
    tags=['热题173'],
    code='''
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        n = len(candidates)
        ans = []
        path = []

        def dfs(i: int, left: int) -> None:
            # 所选元素之和恰好等于 target
            if left == 0:
                ans.append(path.copy())  # 也可以写 path[:]
                return

            # 没有可以选的数字
            if i == n:
                return

            # 所选元素之和无法恰好等于 target
            x = candidates[i]
            if left < x:
                return

            # 选 x
            path.append(x)
            dfs(i + 1, left - x)
            path.pop()  # 恢复现场

            # 不选 x，那么后面所有等于 x 的数都不选
            # 如果不跳过这些数，会导致「选 x 不选 x'」和「不选 x 选 x'」这两种情况都会加到 ans 中，这就重复了
            i += 1
            while i < n and candidates[i] == x:
                i += 1
            dfs(i, left)

        dfs(0, target)
        return ans
''',
    call=f'Solution().combinationSum2({CANDS}, 5)',
    expect=[[1, 2, 2], [5]],
    skip=['n = len', 'ans = []', 'path = []'],
    views=[
        dict(type='array', var='candidates', label='candidates（已排序；蓝 = candidates[i]，紫 = 正在跳过的相同数）',
             cell=76, h=140, color=_arr_color,
             dim=lambda S, i, v: 'i' in S and i < S['i'] and _arr_color(S, i, v) is None),
        dict(type='text', fn=lambda S: (f"还剩 `left = {S['left']}` 要凑；`path` 之和 = {sum(S['path'])}" if 'left' in S else ''),
             h=50, size=26),
        dict(type='stack', var='path', label='path（已选的数）', h=104),
        dict(type='calls', h=240),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'yellow'), ('x', 'x'), 'path'],
    captions={
        'candidates.sort()': '先排序 → `{candidates}`：==相同的数挨在一起==，才好跳过；也方便剪枝',
        'dfs(0, target)': '递归入口 `dfs(0, {left})`：从 `candidates[0]` 开始，还要凑 `{left}`',
        'if left == 0': lambda S, B, ret: (
            f'`left == 0` → ==找到一个组合==：`{S.path}`' if S.left == 0 else f'`left = {S.left}`，还没凑够'),
        'ans.append': '复制一份 path 加入答案：`{ans[-1]}`（直接 append path 会被后面的修改影响）',
        12: '记录完答案，返回上一层',
        'if i == n': lambda S, B, ret: ('`i == n`：没有数可以选了 → 返回' if S.i == S.n else f'`i = {S.i} < n`，还有数可选'),
        16: '这条路走到头了 → 返回',
        'x = candidates[i]': '当前考虑 `x = candidates[{i}] = {x}`',
        'if left < x': lambda S, B, ret: (
            f'==剪枝==：`left = {S.left} < x = {S.x}`，后面的数只会更大 → 返回' if S.left < S.x else
            f'`left = {S.left} ≥ x = {S.x}`，可以考虑选它'),
        21: '凑不出来了，返回上一层',
        'path.append(x)': '==选== `x = {x}`：加入 path → `{path}`',
        'dfs(i + 1, left - x)': '递归 `dfs({i}, {left})`：每个数只能用一次，所以 ==i + 1==',
        'path.pop()': '恢复现场：弹出 `{B.path[-1]}`，path 回到 `{path}`',
        'i += 1': lambda S, B, ret: (f'==不选== `x = {S.x}`：`i` 先移到 `{S.i}`' if S._line == 30 else
                                     f'跳过下标 `{B.i}` 的 `{S.x}`，`i` → `{S.i}`'),
        'while i < n and candidates[i] == x': lambda S, B, ret: (
            f'`candidates[{S.i}] = {S.x}` 等于 `x` → 不选 x 就==所有 {S.x} 都不选==，跳过' if S.i < S.n and S.candidates[S.i] == S.x
            else (f'`candidates[{S.i}] = {S.candidates[S.i]} ≠ {S.x}`，停止跳过' if S.i < S.n else f'`i = {S.i} = n`，到末尾了')),
        'dfs(i, left)': '递归 `dfs({i}, {left})`：从下一个==不同的数==继续，`left` 不变',
        'return ans': '搜索结束，返回 `{ret}`',
    },
    max_steps=58,
    cards=dict(
        one_liner='选或不选；不选 x，就把后面所有等于 x 的数也跳过',
        complexity='排序 `O(n log n)` + 搜索（target=30 时上界 28629 次）',
        problem=['`candidates` 可能有==重复数字==，每个数字在每个组合中只能用==一次==',
                 '找出所有和为 `target` 的组合，==解集不能包含重复的组合==',
                 '示例：`[2,5,2,1,2], target = 5` → `[[1,2,2],[5]]`'],
        quote='不选 x，那么后面所有等于 x 的数都不选。如果不跳过这些数，会导致「选 x 不选 x\'」和「不选 x 选 x\'」这两种情况都会加到 ans 中，==这就重复了==。',
        quote_src='—— 灵茶山艾府题解「方法一：选或不选」',
        idea=['`dfs(i, left)`：枚举到 `candidates[i]`，还剩 `left` 要凑',
              '选 x → `dfs(i+1, left-x)`；不选 x → 跳过所有相同的数再递归',
              '先排序：相同的数挨在一起，且 `left < x` 时后面都不用看了'],
        result='找到 `[1,2,2]` 和 `[5]` ✓：三个 2 只产生了一个 `[1,2,2]`',
        summary=['复杂度：排序 `O(n log n)`；搜索次数受 target 限制（上界 28629）',
                 '去重关键：==不选 x 时跳过所有等于 x 的数==，不能只 `i + 1`',
                 '选了 x 是 `dfs(i+1, …)`：每个数只能用一次（对比 39 题的 `dfs(i, …)`）',
                 '`ans.append(path.copy())`：必须复制，否则恢复现场会改掉答案',
                 '方法二「枚举选哪个」：`for j in range(i, n)`，`j > i` 且与前一个相同就 `continue`'],
    ),
)
