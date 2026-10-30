_INV = {0: 1, 1: 2, 2: 3}


def _st(x):
    return ''.join(str(_INV.get((x >> (3 * k)) & 7, '?')) for k in range(3))


def _dec(S, x, n=None):
    mp = S.get('mp')
    if mp is None or x is None:
        return None
    n = n or S['n']
    inv = {v: k for k, v in mp.items()}
    return [inv.get((x >> (3 * k)) & 7, '?') for k in range(n)]


def _f(S, x):
    d = _dec(S, x)
    return ''.join(str(v) for v in d) if d else str(x)


def _top(S):
    if 'val2' not in S:
        return ''
    return (f"起点 `{_f(S, S['val1'])}` → 终点 `{_f(S, S['val2'])}`（数组编码成 3 位一组的整数，如 `{S['val1']}`）")


def _ops(S):
    if 'c' in S and 'b' in S and 'a' in S and S['_line'] >= 20:
        return f"`a = {_f(S, S['a'])}` → 去掉段后 `b` → 插到位置 `i = {S['i']}` → `c = {_f(S, S['c'])}`"
    if 'sub' in S and 'a' in S and 'l' in S:
        return f"`a = {_f(S, S['a'])}`，移出下标 `[{S['l']}, {S['r']})`，被移出的段 `sub` 共 `{S['r'] - S['l']}` 个"
    return ''


CONFIG = dict(
    num=3690, title='拆分合并数组', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='BFS 最短路 + 位运算编码',
    tags=['灵神题单', '位运算', '难度分 1982'],
    code='''
class Solution:
    def minSplitMerge(self, nums1: List[int], nums2: List[int]) -> int:
        if nums1 == nums2:
            return 0

        n = len(nums1)
        mp = {x: i for i, x in enumerate(set(nums1))}  # 用于离散化的映射表
        val1 = sum(mp[x] << (i * 3) for i, x in enumerate(nums1))
        val2 = sum(mp[x] << (i * 3) for i, x in enumerate(nums2))

        vis = {val1}
        q = [val1]
        for ans in count(1):
            tmp = q
            q = []
            for a in tmp:
                for r in range(1, n + 1):  # 为方便实现，先枚举 r，再枚举 l
                    v = a & ((1 << (r * 3)) - 1)
                    for l in range(r):
                        sub = v >> (l * 3)
                        b = a & ((1 << (l * 3)) - 1) | a >> (r * 3) << (l * 3)  # 从 a 中移除 sub
                        for i in range(n - r + l + 1):
                            c = b & ((1 << (i * 3)) - 1) | sub << (i * 3) | b >> (i * 3) << ((i + r - l) * 3)
                            if c == val2:
                                return ans
                            if c not in vis:
                                vis.add(c)
                                q.append(c)
''',
    setup='from itertools import count',
    call='Solution().minSplitMerge([3, 1, 2], [1, 2, 3])',
    expect=1,
    views=[
        dict(type='text', fn=_top, size=22, h=70),
        dict(type='text', fn=_ops, size=22, h=80),
        dict(type='queue', var='q', fmt=_st, label='q：下一层待扩展的数组', h=170),
        dict(type='set', var='vis', fmt=_st, label='vis：见过的数组', h=220),
    ],
    watch=[('ans', lambda S: S.get('ans'), 'green'), ('r', lambda S: S.get('r'), 'pink'), ('l', lambda S: S.get('l'), 'blue'), ('i', lambda S: S.get('i'), 'cyan'), ('c', lambda S: S.get('c'), 'yellow')],
    max_steps=60,
    captions={
        'if nums1 == nums2': '起点就是终点，一次操作都不用 → 直接返回 0',
        'mp = {x': '离散化：把元素值映射到 `0 ~ 5`，每个值只要 3 个比特。`mp = {mp}`',
        'val1 = ': '`nums1` 编码成整数：第 `i` 个元素放在第 `3i ~ 3i+2` 位。`val1 = {val1}`',
        'val2 = ': '`nums2` 同样编码：`val2 = {val2}`（终点）',
        'vis = {val1}': '`vis` 记录访问过的排列，避免重复入队（起点先标记）',
        'q = [val1]': 'BFS 队列从起点开始',
        'for ans in count': '开始第 `{ans}` 层：边权都是 1，BFS 一层一层扩展，层数 = 操作次数',
        'q = []': '新开一个空队列，装下一层的排列',
        'tmp = q': '把上一层的所有排列取出来扩展，`q` 清空准备放新一层',
        'for a in tmp': lambda S, B, r: f"扩展排列 `a = {_f(S, S.a)}`",
        'for r in range': '枚举被移出子数组的右端点 `r`（`[l, r)` 左闭右开）',
        'v = a &': '取出 `a` 的前 `r` 个元素（低 `3r` 位）',
        'for l in range': '枚举左端点 `l`，子数组是 `a[l:r]`',
        'sub = v >>': '`v` 右移 `3l` 位：丢掉前 `l` 个元素，剩下的就是子数组 `sub`',
        'b = a &': '从 `a` 中移除子数组：保留前 `l` 个元素，再拼上 `r` 之后的元素 → 剩余部分 `b`',
        'for i in range': '枚举把 `sub` 插回 `b` 的位置 `i`（`b` 有 `n-(r-l)` 个元素，共 `n-r+l+1` 个插入点）',
        'c = b &': lambda S, B, r: f"把 `sub` 插进 `b` 的位置 `{S.i}`：前 `{S.i}` 个元素 + `sub` + 后面的元素 → `c = {_f(S, S.c)}`",
        'if c == val2': lambda S, B, r: (f"`c = {_f(S, S.c)}` 等于终点 `{_f(S, S.val2)}` → ==找到了==，用的操作数就是当前层数 `{S.ans}`" if S.c == S.val2 else f"`c = {_f(S, S.c)}` 不是终点 `{_f(S, S.val2)}`"),
        'if c not in vis': lambda S, B, r: ('`c` 以前没见过' if S.c not in S.vis else '`c` 之前出现过（更短的路径已经到过），丢弃'),
        'vis.add(c)': '标记 `c` 已访问',
        'q.append(c)': '`c` 加入下一层队列：`q` 现在有 {len(q)} 个排列',
        'return ans': '到达终点，最短操作次数 `{ans}`',
    },
    cards=dict(
        one_liner='排列当节点，一次操作当一条边，BFS 求最短路',
        complexity='时间 `O(n!·n^3)`，空间 `O(n!)`',
        problem=['把 `nums1` 的一个子数组拆出来，插回剩余数组的任意位置，算一次操作',
                 '求把 `nums1` 变成 `nums2`（它的排列）的最少操作次数，`n ≤ 6`',
                 '示例：`[3,1,2] → [1,2,3]`：把 `[3]` 放到末尾，答案 `1`'],
        quote='每次操作相当于从一个数组变成另一个数组。抽象成有向图，把数组视作节点，操作就是在一个点到另一个点之间连一条有向边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 6`，排列最多 `6! = 720` 个：直接把每个排列当图的节点',
              '边权都是 1 → 用 BFS，层数就是操作次数',
              '位运算优化：元素离散化到 `0~5`，每个 3 比特，一个数组塞进一个整数；拆、拼都用移位和掩码，每次 `O(1)`'],
        result='第 1 层就搜到了 `[1,2,3]`，返回 `1` ✓',
        after=[dict(heading='为什么一定有解？', lines=[
            '把任意一个元素当子数组抽出来，插到任意位置——像洗扑克牌',
            '所以 `nums1` 能变成它的任何排列',
            '而 `nums2` 保证是 `nums1` 的排列 → BFS 一定能到'])],
        summary=['时间 `O(n!·n^3)`：`O(n!)` 个状态，每个状态 `O(n^3)` 种操作，拼接 `O(1)`；空间 `O(n!)`',
                 '易错：枚举 `[l, r)`，`r` 从 1 到 n；插入点个数是 `n-r+l+1`',
                 '易错：位运算里先 `& mask` 取低位、右移后再左移拼接，别写错位数',
                 '优化前的写法用 `tuple` 当 `vis` 的键、直接切片拼数组，慢一些；到达终点可以在入队前判断（这里就是）'],
    ),
)
