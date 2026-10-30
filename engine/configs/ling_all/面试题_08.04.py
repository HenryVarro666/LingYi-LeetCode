def _dfs(S, B, ret):
    i = S.i
    if i == S.n:
        return f'`i = {i} = n`：每个数都决定完了 → ==子集构造完毕=='
    return f'`i = {i} < n`：现在决定 `nums[{i}] = {S.nums[i]}` 选还是不选'


CONFIG = dict(
    num='面试题 08.04', title='幂集', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='输入的视角 · 选或不选',
    tags=[],
    code='''
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = []
        path = []
        n = len(nums)
        
        def dfs(i: int) -> None:
            if i == n:  # 子集构造完毕
                ans.append(path.copy())  # 复制 path，也可以写 path[:]
                return
                
            # 不选 nums[i]
            dfs(i + 1)
            
            # 选 nums[i]
            path.append(nums[i])
            dfs(i + 1)
            path.pop()  # 恢复现场
            
        dfs(0)
        return ans
''',
    call='Solution().subsets([1, 2, 3])',
    expect=[[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在决定的 nums[i]）', cell=64, h=130, pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('i') else None),
        dict(type='array', var='path', label='path（当前选了哪些数）', cell=64, h=130),
        dict(type='calls', h=210),
        dict(type='stack', var='ans', label='ans（已收集的子集）', h=170),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), 'path'],
    skip=['ans = []', 'path = []', 'n = len(nums)'],
    captions={
        'dfs(0)': '从 `dfs(0)` 开始：先决定 `nums[0]` 选不选',
        'if i == n': _dfs,
        'ans.append': lambda S, B, ret: f'记录答案 `{S.ans[-1]}`（==复制== path，否则之后 path 变了答案也会跟着变）',
        13: '==不选== `nums[{i - 1}]`：`path` 不变，直接 `dfs({i})` 决定下一个数',
        17: '选了 `nums[{i - 1}]` 之后：`dfs({i})` 决定下一个数',
        10: '子集 `{ans[-1]}` 已记录 → 返回上一层',
        'path.append(nums[i])': '选 `nums[{i}] = {nums[i]}`：`path` 变成 `{path}`',
        'path.pop()': '恢复现场：弹出 `{B.path[-1]}`，`path` 回到 `{path}`，回溯到上一层',
        'return ans': '枚举结束：共 `{len(ret)}` 个子集 = `2^3`',
    },
    max_steps=110,
    cards=dict(
        one_liner='每个数选或不选，2^n 个子集',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['给定不含重复元素的集合 `nums`，返回它的所有子集（幂集）',
                 '示例：`[1,2,3]` → 8 个子集，从 `[]` 到 `[1,2,3]`',
                 '本视频：`[1,2,3]`'],
        quote='对于输入的 nums，考虑每个 nums[i] 是选还是不选，由此组合出 2^n 个不同的子集。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`dfs(i)` 表示现在考虑 `nums[i]`：==先走不选，再走选==',
              '`i == n` 就是一个叶子，把 `path` 复制进答案',
              '选了之后要 `pop` 恢复现场，才能回到上一层继续'],
        result='共 8 个子集，对应搜索树的 8 个叶子',
        summary=['时间 `O(n·2^n)`：递归 `2^n` 级次，每次复制 `path` 要 `O(n)`',
                 '易错：`ans.append(path.copy())` 必须复制，直接 append `path` 会全变成空',
                 '易错：选完要 `path.pop()` 恢复现场',
                 '方法二「答案的视角」：每次枚举下一个选谁；方法三「二进制枚举」：用 `i >> j & 1` 判断选不选']),
)
