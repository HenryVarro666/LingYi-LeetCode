_J = lambda S: S['_inner'].get('j')


CONFIG = dict(
    num='LCR 079', title='子集', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='回溯：答案的视角（选哪个数）',
    tags=[],
    code='''
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = []
        path = []
        n = len(nums)
        def dfs(i: int) -> None:
            ans.append(path.copy())  # 固定答案
            if i == n:
                return
            for j in range(i, n):  # 枚举选择的数字
                path.append(nums[j])
                dfs(j + 1)
                path.pop()  # 恢复现场
        dfs(0)
        return ans
''',
    call='Solution().subsets([1, 2, 3])',
    expect=[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]],
    views=[
        dict(type='array', var='nums', label='nums（j = 当前枚举要选的数）', cell=64, h=130,
             pointers={_J: 'pink'}, pointer_labels={_J: 'j'}),
        dict(type='stack', var='path', label='path（当前选了哪些数）', h=100, fmt=lambda x: str(x)),
        dict(type='calls', h=170),
        dict(type='stack', var='ans', label='ans（每进一层就记一个子集）', h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'), 'path'],
    skip=['ans = []', 'path = []', 'n = len(nums)'],
    captions={
        'ans.append': '`path = {path}` 本身就是一个子集 → ==复制==一份记入答案（共 `{len(ans)}` 个）',
        'if i == n': lambda S, B, ret: ('`i == n`：没有数可选了 → 返回' if S.i == S.n else f'`i = {S.i} < n`：还可以从 `nums[{S.i}:]` 里继续选'),
        'for j in range': '枚举下一个要选的数：`j` 从 `{i}` 到 `{n - 1}`',
        'path.append': '选 `nums[{j}] = {nums[j]}` 放进 path → `{path}`',
        'dfs(j + 1)': '递归 `dfs({j + 1})`：之后只能选下标 ==大于 j== 的数，避免重复',
        'path.pop': '恢复现场：弹出 `{B.path[-1]}`，换下一个 j 试',
        'dfs(0)': '从 `dfs(0)` 开始，此时 `path` 为空 → 空集也是子集',
        'return ans': '共得到 `{len(ret)}` 个子集 = `2^n`',
    },
    max_steps=90,
    cards=dict(
        one_liner='答案的视角：每个 path 都是答案，枚举下一个选哪个数',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['给定互不相同的整数数组 `nums`，返回所有子集（幂集），不含重复子集',
                 '示例：`[1,2,3]` → `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`',
                 '顺序任意'],
        quote='答案的视角（选哪个数）：每次递归都把一个数组放入答案，因此会递归 2^n 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i)` 一进来，当前 `path` 就是一个子集，立刻记下',
              '再枚举 `j >= i`：选 `nums[j]`，递归到 `j + 1`',
              '回来后 `pop` 恢复现场，换下一个 j'],
        summary=['时间 `O(n·2^n)`：共 `2^n` 个子集，每个复制 `O(n)`；空间 `O(n)`',
                 '易错点：`ans.append(path.copy())` 必须复制，否则全是同一个列表',
                 '易错点：别忘了 `path.pop()` 恢复现场',
                 '题解还有方法一（输入视角：每个数选或不选），搜索树是满二叉树，同样 `O(n·2^n)`'],
    ),
)
