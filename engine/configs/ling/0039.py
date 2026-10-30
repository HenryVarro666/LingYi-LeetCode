CONFIG = dict(
    num=39, title='组合总和', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='选或不选 + 排序剪枝（类似完全背包）',
    code='''
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        ans = []
        path = []

        def dfs(i: int, left: int) -> None:
            if left == 0:
                # 找到一个合法组合
                ans.append(path.copy())
                return

            if i == len(candidates) or left < candidates[i]:
                return

            # 不选
            dfs(i + 1, left)

            # 选
            path.append(candidates[i])
            dfs(i, left - candidates[i])
            path.pop()  # 恢复现场

        dfs(0, target)
        return ans
''',
    call='Solution().combinationSum([2, 3, 6, 7], 7)',
    expect=[[7], [2, 2, 3]],
    views=[
        dict(type='array', var='candidates', label='candidates（已排序，蓝 = candidates[i]）', cell=70, h=130,
             color=lambda S, i, v: 'blue' if i == S['i'] else None, dim=lambda S, i, v: i < S['i']),
        dict(type='text', fn=lambda S: (f"还剩 `left = {S['left']}` 要凑；`path` 之和 = {sum(S['path'])}" if 'left' in S else ''), h=50, size=26),
        dict(type='stack', var='path', label='path', h=104),
        dict(type='calls', h=248),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'yellow'), 'path'],
    captions={
        'candidates.sort()': '先排序：`candidates = {candidates}`，后面才能用「`left` 比当前数还小」剪枝',
        'dfs(0, target)': '递归入口 `dfs(0, {left})`：从 `candidates[0]` 开始，还要凑 `{left}`',
        'if left == 0': lambda S, B, ret: (
            f'`left == 0` → ==找到一个合法组合==：`{S.path}`' if S.left == 0 else
            f'`left = {S.left}` 还没凑够'),
        'ans.append': '复制一份 path 加入答案：`{ans[-1]}`',
        11: '记录完答案就返回上一层',
        'if i == len(candidates) or': lambda S, B, ret: (
            f'`i == len(candidates)`：没有数可选了 → 返回' if S.i == len(S.candidates) else
            f'==剪枝==：`left = {S.left} < candidates[{S.i}] = {S.candidates[S.i]}`，后面的数只会更大 → 返回'
            if S.left < S.candidates[S.i] else
            f'`left = {S.left} ≥ candidates[{S.i}] = {S.candidates[S.i]}`，还有希望，继续'),
        14: '这条路走不通 → 返回上一层',
        'dfs(i + 1, left)': '==不选== `candidates[{B.i}] = {candidates[B.i]}`：递归 `dfs({i}, {left})`，`left` 不变',
        'path.append': '==选== `candidates[{i}] = {candidates[i]}`：加入 path → `{path}`',
        'dfs(i, left - candidates[i])': '递归 `dfs({i}, {left})`：==i 不变==，下次还能继续选 `{candidates[i]}`',
        'path.pop()': '恢复现场：弹出 `{B.path[-1]}`，path 回到 `{path}`',
        'return ans': '搜索结束，返回 `{ret}`',
    },
    max_steps=62,
    cards=dict(
        one_liner='选或不选；选了之后 i 不变，同一个数还能接着选',
        complexity='搜索次数很小（target=40 时上界 37271），空间 `O(target)`',
        problem=['`candidates` 无重复元素，每个数可以==无限次==选取，找出所有和为 `target` 的不同组合',
                 '示例：`candidates = [2,3,6,7], target = 7` → `[[2,2,3],[7]]`'],
        quote='选 `candidates[i]`：递归到 `dfs(i, left-candidates[i])`。==注意 i 不变，表示在下次递归中可以继续选 candidates[i]==。',
        quote_src='—— 灵茶山艾府题解「方法一：选或不选」',
        idea=['`dfs(i, left)`：枚举到 `candidates[i]`，还要凑 `left`；不选就 `dfs(i+1, left)`',
              '`left == 0` → 找到答案；`i == n` 或 `left < 0` → 返回',
              '==剪枝==：排序后若 `left < candidates[i]`，后面更大的数都没用'],
        result='找到 `[7]` 和 `[2,2,3]` ✓（中间分支已快进）',
        summary=['复杂度：`target = 40` 的极端数据搜索次数上界也只有 37271；空间 `O(target)`',
                 '思路类似==完全背包==：选了以后留在原地 `dfs(i, …)`',
                 '先判断 `left == 0` 再判断越界/剪枝，顺序不能反',
                 '方法二「枚举选哪个」：`for j in range(i, n)`，递归 `dfs(j, …)`',
                 '方法三：完全背包预处理 `f[i][j]`，保证每一步都往有解的方向走'],
    ),
)
