CONFIG = dict(
    num=3447, title='将元素分配给有约束条件的组', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理 · 枚举倍数打标记',
    tags=['灵神题单', '数论', '难度分 1731'],
    code='''
class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        mx = max(groups)
        target = [-1] * (mx + 1)
        for i, x in enumerate(elements):
            if x > mx or target[x] >= 0:  # x 及其倍数一定已被标记，跳过
                continue
            for y in range(x, mx + 1, x):  # 枚举 x 的倍数 y
                if target[y] < 0:  # 没有标记过
                    target[y] = i  # 标记 y 可以被 x 整除（记录 x 的下标）
        return [target[x] for x in groups]  # 回答询问
''',
    call='Solution().assignElements([8,4,3,2,4], [4,2,8])',
    expect=[0, 0, -1, 1, 0],
    views=[
        dict(type='array', var='groups', label='groups', h=130, cell=70),
        dict(type='array', var='elements', label='elements', pointers={'i': 'blue'}, h=200, cell=70),
        dict(type='array', var='target', label='target[y]：最左的因子下标（-1 无）', pointers={'y': 'pink'}, h=200, cell=70,
             color=lambda S, i, v: 'green' if v >= 0 else None),
    ],
    watch=['mx', 'i', 'x', 'y'],
    captions={
        'mx = max': '只需要处理到 `groups` 的最大值 `mx = {mx}`',
        'target = [-1]': '`target[y]` 记录 y 能被哪个元素整除，先全设 `-1`（没有）',
        'for i, x in': '从左到右看 `elements[{i}] = {x}`',
        'if x > mx': lambda S, B, r: (f'`{S.x}` 超过 mx，没有任何组用得上 → 跳过' if S.x > S.mx else (f'`target[{S.x}] = {S.target[S.x]}` 已被更靠左的因子标记过：{S.x} 的倍数也都标记过 → ==跳过== ，不再枚举' if S.target[S.x] >= 0 else f'`target[{S.x}] = -1` 还没标记，是第一次出现这样的因子 → 枚举倍数')),
        'continue': '跳过这个元素，看下一个',
        'for y in range': '枚举 `{x}` 的倍数：`y = {y}`',
        'if target[y] < 0': lambda S, B, r: (f'`target[{S.y}] = -1`：还没人标记过 → 可以标' if S.target[S.y] < 0 else f'`target[{S.y}] = {S.target[S.y]}` 已被更靠左的元素标记 → 不覆盖'),
        'target[y] = i': '`target[{y}] = {i}`：{y} 能被 `elements[{i}] = {x}` 整除',
        'return [': '每个组直接查表：`target[groups[i]]` → =={ret}==',
    },
    cards=dict(
        one_liner='先给 1..mx 每个数标好"最左的因子下标"，再查表',
        complexity='时间 `O(n + U log n + m)`，空间 `O(U)`',
        problem=['`groups[i]` 能被 `elements[j]` 整除，就可以把 j 分给组 i',
                 '多个满足时取最小下标；没有则 `-1`',
                 '示例：`groups=[8,4,3,2,4]`，`elements=[4,2]` → `[0,0,-1,1,0]`'],
        quote='如果我们之前遍历过 x 的因子 d，那么不用枚举 x 的倍数，因为这些数必然已被 d 标记。',
        quote_src='—— 灵茶山艾府题解',
        idea=['预处理每个数 y 能被哪个元素整除，查询就是 `O(1)`',
              '按下标从左到右遍历 `elements`，枚举倍数打标记，==已标记的不覆盖==，保证最左',
              '若 `target[x] >= 0`，x 的倍数早被因子标过，整轮跳过，避免 `[2,2,2,…]` 退化'],
        summary=['调和级数：每个值最多枚举一次倍数，总循环 `O(n + U log n)`',
                 '初始化 `-1` 一举解决"没有合适元素"的情况',
                 '`x > mx` 要先判断，否则 `target[x]` 越界',
                 '数学题单搜「调和级数」还有同类题'],
    ),
)
