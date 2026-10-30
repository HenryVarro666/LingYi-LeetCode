_J = lambda S: S.get('j')


def _fml(S):
    i = S['_inner'].get('i')
    if i is None:
        return '开第 `i` 把锁时：`x = 1 + i·k`，用时 `ceil(s / x)`'
    t = S['_inner'].get('time', 0)
    x = 1 + i * S['k']
    return f'已开 `{i}` 把锁，当前 `x = 1 + {i}×{S["k"]} = {x}`，累计用时 ==`{t}`==，历史最优 `{S.get("ans", "inf")}`'


def _cost(S, B, ret):
    s, x = S.s, S.x
    return f'开 `strength[{S.j}] = {s}`：`({s} − 1) // {x} + 1 = {(s - 1) // x + 1}` 分钟，递归时累计 `{S.time} + {(s - 1) // x + 1}`'


CONFIG = dict(
    num=3376, title='破解锁的最少时间 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='排列型回溯 + 最优性剪枝',
    tags=['图论算法', '动态规划', '难度分 1793'],
    code='''
class Solution:
    def findMinimumTime(self, strength: List[int], k: int) -> int:
        n = len(strength)
        ans = inf
        done = [False] * n
        def dfs(i: int, time: int) -> None:
            nonlocal ans
            # 最优性剪枝：答案不可能变小
            if time >= ans:
                return
            if i == n:
                ans = time
                return
            x = 1 + i * k
            for j, s in enumerate(strength):
                if not done[j]:
                    done[j] = True  # 已开锁
                    dfs(i + 1, time + (s - 1) // x + 1)
                    done[j] = False  # 恢复现场
        dfs(0, 0)
        return ans
''',
    call='Solution().findMinimumTime([3, 4, 1], 1)',
    expect=4,
    views=[
        dict(type='text', fn=_fml, size=26, h=70),
        dict(type='array', var='strength', label='strength（绿 = 这条分支里已开的锁，粉 = 正在尝试的锁）', cell=90, h=170,
             pointers={_J: 'pink'}, pointer_labels={_J: 'j'},
             color=lambda S, i, v: 'green' if S['done'][i] else None),
        dict(type='calls', h=230),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('time', lambda S: S['_inner'].get('time'), 'yellow'), ('ans', 'ans', 'green')],
    skip=['n = len(strength)', 'for j, s in enumerate', 'if not done[j]', 'x = 1 + i * k', 'done[j] = True', '                return', 'ans = time'],
    captions={
        'ans = inf': '`ans` 记录目前见过的最少用时，一开始是无穷大',
        'done = [False]': '`done[j]` 标记第 `j` 把锁是否已经开过，排列里每把锁只能用一次',
        'if time >= ans': lambda S, B, ret: (f'`time = {S.time} >= ans = {S.ans}`：用时只增不减，这条分支==不可能更优== → 剪枝返回'
                                              if S.time >= S.ans else f'`time = {S.time} < ans = {S.ans}`：还有希望，继续往下搜'),
        'if i == n': lambda S, B, ret: (f'`i == n`：{S.n} 把锁全开完，总用时 `{S.time}` → ==ans = {S.time}=='
                                         if S.i == S.n else f'`i = {S.i} < n`：还有锁没开，继续枚举下一把'),
        'ans = time': '`ans = {time}`：找到更快的开锁顺序',
        'x = 1 + i * k': '已开 `{i}` 把锁，每开一把 `x` 加 `k`，所以现在 `x = 1 + {i}×{k} = {x}`',
        'if not done[j]': lambda S, B, ret: (f'第 `{S.j}` 把锁（需要 `{S.s}`）还没开 → 可以作为第 `{S.i + 1}` 把来开' if not S.done[S.j]
                                              else f'第 `{S.j}` 把锁已经开过 → 跳过'),
        'done[j] = True': '先标记第 `{j}` 把锁已开，下面几层不能再选它',
        'dfs(i + 1': lambda S, B, ret: f'选第 `{S.j}` 把（`strength = {S.s}`，此时 `x = {S.x}`）：`({S.s} − 1) // {S.x} + 1` = =={(S.s - 1) // S.x + 1}== 分钟 → 递归，累计 `{S.time + (S.s - 1) // S.x + 1}`',
        'done[j] = False': '回溯：撤销 `done[{j}]`，换下一把锁作为这一位',
        'dfs(0, 0)': '从 `dfs(0, 0)` 开始：一把锁都没开，用时 0',
        'return ans': '所有顺序枚举完（剪枝掉的不可能更优），最少 `{ret}` 分钟',
    },
    max_steps=52,
    cards=dict(
        one_liner='枚举开锁顺序，用时超过已知最优就剪枝',
        complexity='时间 `O(n·n!)`，空间 `O(n)`',
        problem=['`strength[i]` 是开第 `i` 把锁所需能量；每分钟剑的能量加 `x`，开锁后能量清零、`x` 增加 `k`',
                 '`x` 初始为 1，求开完所有锁的最少分钟数',
                 '示例：`strength = [3,4,1], k = 1` → `4`'],
        quote='设当前开了 i 把锁，那么 x=1+k·i。枚举开第 j 把锁，需要的时间为 strength[j] 除以 x 再上取整。',
        quote_src='—— 灵茶山艾府题解',
        idea=['开锁顺序决定每把锁面对的 `x`，所以直接==枚举全排列==（`n ≤ 8`）',
              '上取整用 `(s - 1) // x + 1`，对正整数等价于 ceil(s / x)',
              '用时 `time` 只会增大：一旦 `time >= ans` 就不用再往下了'],
        summary=['时间 `O(n·n!)`，空间 `O(n)`；最优性剪枝让实际远快于全排列',
                 '上取整别写成 `s // x`，要用 `(s - 1) // x + 1`',
                 '`done[j]` 回溯时必须恢复现场',
                 '题解另给了状压 DP `O(n·2^n)`（`f[i]` = 剩余集合为 `i` 的最少用时）和最小费用流（二分图最小带权匹配，`n` 更大时用）'],
    ),
)
