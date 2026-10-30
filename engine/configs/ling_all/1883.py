def _J1(S):
    j = S.get('j')
    return None if j is None else j + 1


def _txt(S):
    if 'i' not in S:
        return '`f[j]` ÷ `speed` = 走完前 `j` 条路所需的最少小时数（先乘 speed，避免小数）'
    sp = S['speed']
    f = S['f']
    if S.get('j') is None:
        return f'最多跳过 ==`{S["i"]}`== 次：`f[j]` 是走完前 j 条路的最少用时 × `{sp}`'
    return f'最多跳 ==`{S["i"]}`== 次，走完前 `{S["j"] + 1}` 条路：`f[{S["j"] + 1}] = {f[S["j"] + 1]}`，即 `{f[S["j"] + 1]}/{sp}` = {f[S["j"] + 1] / sp:g} 小时'


CONFIG = dict(
    num=1883, title='准时抵达会议现场的最小跳过休息次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多维 DP · 递推 + 空间优化',
    tags=['其他线性 DP', '多维 DP', '难度分 2588'],
    code='''
class Solution:
    def minSkips(self, dist: List[int], speed: int, hoursBefore: int) -> int:
        if sum(dist) > speed * hoursBefore:
            return -1
        f = [0] * len(dist)
        for i in count(0):
            pre = 0
            for j, d in enumerate(dist[:-1]):
                tmp = f[j + 1]
                f[j + 1] = (f[j] + d + speed - 1) // speed * speed
                if i:
                    f[j + 1] = min(f[j + 1], pre + d)
                pre = tmp
            if f[-1] + dist[-1] <= speed * hoursBefore:
                return i
''',
    call='Solution().minSkips([7, 3, 5, 5], 2, 10)',
    expect=2,
    setup='from itertools import count',
    views=[
        dict(type='array', var='dist', label='dist（蓝 = 正在走的道路 j，最后一条不用休息）', cell=84, h=210,
             pointers={'j': 'blue'}, color=lambda S, k, v: 'blue' if k == S.get('j') else None),
        dict(type='array', var='f', label='f（f[j+1] = 走完 dist[0..j] 的最少用时 × speed）', cell=96, h=210,
             pointers={_J1: 'pink'}, pointer_labels={_J1: 'j+1'},
             color=lambda S, k, v: 'pink' if k == _J1(S) else None),
        dict(type='text', fn=_txt, size=26, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('d', 'd', 'yellow'), ('pre', 'pre', 'pink'), ('speed', 'speed', 'orange')],
    skip=['tmp = f[j + 1]', 'for j, d in enumerate'],
    captions={
        'if sum(dist)': '全程总路程 `{sum(dist)}`，最快也要 `{speed*hoursBefore}` 才赶得上：{"总路程超过 → 即使全跳也到不了，返回 -1" if sum(dist) > speed*hoursBefore else "总路程不超过 → 一定有解"}',
        'f = [0] * len': '`f[0] = 0`：还没走任何路，用时 0（对应记忆化的递归边界 `j = -1`）',
        'for i in count': '`i = {i}`：枚举最多跳过 `i` 次，从小到大，第一个能准时到的就是最小跳过次数',
        'pre = 0': '`pre` 暂存上一轮的 `f[j]`，也就是 ==跳过次数少一次== 的状态；`f[j+1]` 被覆盖前先保存',
        'f[j + 1] = (f[j]': '不跳过：走完 `{d}` 后==等到整点== → `ceil(({B.f[j]}+{d})/{speed})×{speed}` = =={f[j+1]}==',
        'if i:': '{"`i = 0`：不允许跳过，只有“不跳过”一种选择" if i == 0 else "`i = " + str(i) + "`：还可以选择跳过这次休息，试试看更小的"}',
        'f[j + 1] = min': '跳过 `dist[{j}]` 的休息：上一轮的 `pre + d = {pre}+{d} = {pre+d}`；和不跳过 `{B.f[j+1]}` 取小 → =={f[j+1]}==',
        'pre = tmp': '`pre` 换成这格旧值 `{pre}`，留给下一格用',
        'if f[-1] + dist[-1]': lambda S, B, r: (f'最后一条路不用休息：`{S.f[-1]} + {S.dist[-1]} = {S.f[-1]+S.dist[-1]}` ≤ `{S.speed*S.hoursBefore}`？'
                                                f'{"==成立== → 最少跳过 " + str(S.i) + " 次" if S.f[-1]+S.dist[-1] <= S.speed*S.hoursBefore else "不成立，多允许跳一次再试"}'),
        'return i': '最小跳过次数 ==`{i}`==',
    },
    max_steps=90,
    cards=dict(
        one_liner='枚举最多跳 i 次，算最早到达时间，第一个来得及的 i 就是答案',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['依次走 `n` 条路，每走完一条要休息到下一个整点；可以跳过某些休息，求准时（`hoursBefore` 小时内）到达的最少跳过次数',
                 '最后一条路后不用休息；到不了返回 -1',
                 '示例：`dist=[7,3,5,5], speed=2, hoursBefore=10` → `2`'],
        quote='把 dfs(i,j) 的定义改成在同等时间下用 speed 速度能走的距离……这样就完全不涉及浮点运算了！',
        quote_src='—— 灵茶山艾府题解（三、避免浮点误差）',
        idea=['“选或不选”：不跳过则 `ceil` 到整点；跳过则用“少跳一次”的状态直接加上 `d`',
              '用时乘以 `speed`，上取整变成 `(x + speed - 1) // speed * speed`，全程整数',
              '`f[i]` 只用到 `f[i-1]`，一维数组加变量 `pre` 即可滚动'],
        summary=['时间 `O(n^2)`：最多 `n` 轮，每轮 `O(n)`；空间优化后 `O(n)`',
                 '易错：`dist[-1]` 不用休息，所以循环只到 `dist[:-1]`，最后单独加上',
                 '易错：`pre` 要在覆盖 `f[j+1]` 前保存旧值（`tmp`），否则用错状态',
                 '题解还给了记忆化搜索和二维递推写法，本视频演示空间优化版'],
    ),
)
