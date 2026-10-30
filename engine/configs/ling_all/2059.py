def _cand(S, B):
    if 'v' not in S or 'num' not in S or 'step' not in S:
        return ''
    v, n = S['v'], S['num']
    return f"第 `{S['step']}` 步：`v = {v}`，`num = {n}` → 三种结果 `{v}+{n}={v+n}`，`{v}−{n}={v-n}`，`{v}^{n}={v^n}`（目标 `{S['goal']}`）"


CONFIG = dict(
    num=2059, title='转化数字的最小运算数', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='BFS 最短路（Go 原文转写）',
    tags=['灵神题单·图论算法', '难度分 1850'],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int], start: int, goal: int) -> int:
        vis = [False] * 1001
        vis[start] = True
        q = [start]
        step = 1
        while q:
            tmp = q
            q = []
            for v in tmp:
                for num in nums:
                    for x in [v + num, v - num, v ^ num]:
                        if x == goal:
                            return step
                        # 由于超过范围无法继续运算，故不入队
                        if 0 <= x <= 1000 and not vis[x]:
                            vis[x] = True
                            q.append(x)
            step += 1
        return -1
''',
    call='Solution().minimumOperations([2,12], 2, 12)',
    expect=2,
    views=[
        dict(type='text', fn=_cand, h=70, size=26),
        dict(type='queue', var='tmp', label='本层 tmp（已走 step−1 步能到的数）', h=130),
        dict(type='queue', var='q', label='下一层 q（走 step 步能到、范围内且没见过）', h=130),
        dict(type='array', var='[i for i in range(1001) if vis[i]]', label='已访问 vis（只列出为 True 的数）', index=False, h=130),
    ],
    skip=['vis = [False]', 'vis[start] = True', 'vis[x] = True', 'q = []'],
    max_steps=80,
    watch=[('step', 'step', 'blue'), 'v', 'num', ('x', 'x', 'yellow'), ('goal', 'goal', 'green')],
    captions={
        'q = [start]': '起点 `{start}` 入队并标记已访问；每个数是图的一个点，一次运算是一条边',
        'while q': lambda S, B, r: f'队列非空：处理走 `{S.step}` 步能到达的数' if S.q else '队列空了，目标不可达',
        'tmp = q': '`tmp = {tmp}`：本层的数，下面逐个展开',
        'for v in tmp': lambda S, B, r: f'取本层的数 `v = {S.v}`' if B.get('v') != S.v else '本层处理完',
        'for num in nums': lambda S, B, r: f'用 `nums` 里的 `num = {S.num}` 对 `{S.v}` 运算' if B.get('num') != S.num or B.get('v') != S.v else f'`{S.v}` 的所有 `num` 用完了',
        'for x in': lambda S, B, r: f'三种运算依次得到 `x = {S.x}`' if B.get('x') != S.x or B.get('num') != S.num else '三种结果看完了',
        'if x == goal': lambda S, B, r: (f'`x = {S.x}` 等于目标 `{S.goal}` → 当前是第 `{S.step}` 步' if S.x == S.goal else f'`x = {S.x}` ≠ 目标 `{S.goal}`'),
        'if 0 <= x': lambda S, B, r: (f'`{S.x}` 越界：只能用来比较 `goal`，不入队' if not 0 <= S.x <= 1000
                                      else f'`{S.x}` 已经访问过，不重复入队' if S.vis[S.x] else f'`{S.x}` 在 `[0, 1000]` 且没访问过 → 入队，继续运算'),
        'q.append(x)': '标记 `{x}` 已访问并入队：`q = {q}`',
        'step += 1': '这一层没有命中 → 步数 `step` → {step}',
        'return step': '第一次碰到 `goal`，BFS 保证这是最少步数 `{step}`',
        'return -1': '队列耗尽也没碰到 `goal` → `-1`',
    },
    cards=dict(
        one_liner='数字当节点，一次运算当一条边，BFS 求最短路',
        complexity='时间 `O(1001 × n)`，空间 `O(1001)`',
        problem=['`x` 从 `start` 出发，每次可加、减或异或 `nums[i]`',
                 '只有 `0 <= x <= 1000` 时才能继续运算；越界后的值也算，但不能再动',
                 '求变成 `goal` 的最少运算次数，不行返回 `-1`',
                 '示例：`nums=[2,4,12], start=2, goal=12` → `2`；本视频用 `nums=[2,12]`'],
        quote='问题可以抽象成一张图，一次运算对应着图中的一条边。我们要从 start 出发，求到 goal 的最短路，这可以用 BFS 来做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法的点只有 `0..1000`，用 `vis` 去重，每个点最多入队一次',
              '一层 BFS 对应多走一步；`x == goal` 在入队之前判断，因为 `goal` 可以越界',
              '越界的 `x` 只用来判断是否等于 `goal`，不入队'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`[1001]bool` 对应 `[False] * 1001`）',
                 '时间 `O(1001 × n)`，空间 `O(1001)`',
                 '易错点：先判断 `x == goal` 再判断范围，目标可能在 `[0,1000]` 之外',
                 '`start != goal` 保证至少一步，`step` 从 1 开始'],
    ),
)
