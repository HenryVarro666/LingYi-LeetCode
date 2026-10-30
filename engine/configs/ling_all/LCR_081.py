_I = lambda S: S['_inner'].get('i')


CONFIG = dict(
    num='LCR 081', title='组合总和', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='回溯：选或不选 + 排序剪枝',
    tags=[],
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
    call='Solution().combinationSum([3, 2, 4], 6)',
    expect=[[3, 3], [2, 4], [2, 2, 2]],
    views=[
        dict(type='array', var='candidates', label='candidates（排序后；i = 当前考虑的数）', cell=64, h=120,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='text', h=60, fn=lambda S: (f"path = `{S['path']}`，和 = {sum(S['path'])}，还差 left = =={S['_inner']['left']}==" if 'left' in S['_inner'] else '')),
        dict(type='calls', h=190),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('left', lambda S: S['_inner'].get('left'), 'yellow'), 'path'],
    skip=['ans = []', 'path = []'],
    captions={
        'candidates.sort': '先排序 → `{candidates}`：后面的数只会更大，才能剪枝',
        'if left == 0': lambda S, B, ret: ('`left == 0`：==和刚好等于 target== → 找到合法组合' if S['left'] == 0 else f'`left = {S["left"]} > 0`：还差一些，继续'),
        'ans.append': '复制 `path = {path}` 加入答案（共 `{len(ans)}` 个）',
        'if i == len': lambda S, B, ret: ('越界或 `left < candidates[i]`：==后面的数更大，不可能凑出 left== → 剪枝返回' if (S.i == len(S.candidates) or S.left < S.candidates[S.i])
                                          else f'`left = {S.left} >= candidates[{S.i}] = {S.candidates[S.i]}`：还能选，继续'),
        'dfs(i + 1, left)': '不选 `candidates[{i - 1}]`：递归 `dfs({i}, {left})`',
        'path.append': '选 `{candidates[i]}` → `path = {path}`',
        'dfs(i, left - ': '选了之后 ==i 不变==（可重复选）：递归 `dfs({i}, {left})`',
        'path.pop': '恢复现场：弹出 `{B.path[-1]}`',
        'dfs(0, target)': '从 `dfs(0, {target})` 开始',
        'return ans': '共 `{len(ret)}` 个组合',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个数选或不选；选了不动 i，所以能重复选',
        complexity='时间约为 `O(分拆数)`，空间 `O(target)`（不计返回值）',
        problem=['给定无重复正整数数组 `candidates` 和 `target`，找出和为 `target` 的所有不同组合',
                 '同一个数可以无限次选取；示例：`[2,3,6,7], 7` → `[[7],[2,2,3]]`',
                 '本视频：`[3,2,4], 6`'],
        quote='选：递归到 dfs(i, left - candidates[i])。注意 i 不变，表示在下次递归中可以继续选 candidates[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, left)`：考虑 `candidates[i]`，还差 `left`',
              '不选 → `dfs(i+1, left)`；选 → `dfs(i, left - x)`，i 不变',
              '排序后，`left < candidates[i]` 说明后面都太大，直接剪枝'],
        summary=['时间复杂度和分拆数有关，题目保证答案不超过 150 个，所以很快；空间 `O(target)`',
                 '易错点：选了之后递归 `i` 而不是 `i + 1`',
                 '易错点：`left == 0` 要先于越界判断，且答案要 `path.copy()`',
                 '题解另有方法二（for 枚举选哪个）和方法三（完全背包预处理做可行性剪枝）'],
    ),
)
