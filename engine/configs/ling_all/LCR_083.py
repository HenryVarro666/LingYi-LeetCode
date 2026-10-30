_J = lambda S: S['_inner'].get('j')


CONFIG = dict(
    num='LCR 083', title='全排列', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='排列型回溯（on_path 标记）',
    tags=[],
    code='''
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        path = [0] * n
        on_path = [False] * n
        def dfs(i: int) -> None:
            if i == n:
                ans.append(path.copy())
                return
            for j, on in enumerate(on_path):
                if not on:
                    path[i] = nums[j]
                    on_path[j] = True
                    dfs(i + 1)
                    on_path[j] = False  # 恢复现场
        dfs(0)
        return ans
''',
    call='Solution().permute([1, 2, 3])',
    expect=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 已填入排列）', cell=64, h=130,
             pointers={_J: 'pink'}, pointer_labels={_J: 'j'},
             color=lambda S, i, v: 'green' if S['on_path'][i] else None),
        dict(type='array', var='path', label='path（暗 = 还没填 / 旧值）', cell=64, h=130, pointers={'i': 'blue'},
             dim=lambda S, i, v: i >= S['i']),
        dict(type='calls', h=150),
        dict(type='stack', var='ans', label='ans', h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'), 'on_path'],
    skip=['ans = []', 'n = len(nums)', 'for j, on in enumerate', '                return'],
    captions={
        'path = [0] * n': '`path` 长度固定为 `n`，填的时候直接覆盖',
        'on_path = [False] * n': '`on_path[j]` 表示 `nums[j]` 是否已经填入排列',
        'if i == n': lambda S, B, ret: ('`i == n` → ==填完了==，得到一个排列' if S.i == S.n else f'`i = {S.i} < n`：枚举 `nums[j]` 填入 `path[{S.i}]`'),
        'ans.append': '复制 `path = {path}` 记入答案（共 `{len(ans)}` 个）',
        'if not on': lambda S, B, ret: (f'`nums[{S.j}] = {S.nums[S.j]}` 还没用 → 可以填入 `path[{S.i}]`' if not S.on
                                        else f'`nums[{S.j}] = {S.nums[S.j]}` ==已经在排列里== → 跳过'),
        'path[i] = nums[j]': '填入排列：`path[{i}] = {nums[j]}` → `{path}`',
        'on_path[j] = True': '标记 `nums[{j}]` 已用，下面几层不能再选它',
        'dfs(i + 1)': '递归 `dfs({i})`：填排列的下一个数',
        'on_path[j] = False': '恢复现场：`nums[{j}]` 重新可用；path 不用恢复，下次直接覆盖',
        'dfs(0)': '从 `dfs(0)` 开始：先决定 `path[0]` 填什么',
        'return ans': '共 `{len(ret)}` 个排列 = `3!`',
    },
    max_steps=64,
    cards=dict(
        one_liner='每一位从没用过的数里挑一个，回溯时把标记还回去',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（不计返回值）',
        problem=['给定不含重复数字的数组 `nums`，返回所有全排列，顺序任意',
                 '示例：`[1,2,3]` → `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`',
                 '`nums` 长度不超过 6'],
        quote='每个非叶节点要花费 O(n) 的时间遍历 onPath 数组，每个叶结点也要花费 O(n) 的时间复制 path 数组，因此时间复杂度为 O(n·n!)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i)` 负责填 `path[i]`，从 `nums` 里挑一个没用过的',
              '`on_path[j]` 标记 `nums[j]` 是否已在排列里',
              '递归返回后把 `on_path[j]` 改回 False，才能让别的分支再用它'],
        summary=['时间 `O(n·n!)`：搜索树节点少于 `3·n!`，每个节点 `O(n)`；空间 `O(n)`',
                 '易错点：`path.copy()`，否则答案里都是同一个列表',
                 '易错点：`on_path[j] = False` 恢复现场不能漏',
                 '`path` 长度固定，不需要 pop，直接覆盖 `path[i]`'],
    ),
)
