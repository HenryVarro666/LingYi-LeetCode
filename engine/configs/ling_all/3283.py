def _mat(S):
    try:
        n = S['n']
        return [[S['dis'][j][x][y] for j in range(n)] for (x, y) in S['positions']]
    except Exception:
        return [[0]]


def _names(S):
    n = S.get('n', 1)
    return [f'兵{j}' for j in range(n)], [f'兵{j}' for j in range(n)] + ['马']


def _hl(S, r, c, v):
    if S.get('_line') is None or 'mask' not in S['_inner']:
        return None
    I = S['_inner']
    i = I.get('i')
    j = I.get('j')
    if i is not None and r == i and j is not None and c == j:
        return 'yellow'
    if i is not None and r == i:
        return 'blue'
    return None


def _pick(S, B, ret):
    I = S['_inner']
    j = I['j']
    pre = ''
    if B.get('res') is not None and 'res' in I and I['res'] != B['res'] and I['j'] > 0 and False:
        pre = ''
    ok = I['mask'] >> j & 1
    t = f'兵 {j} 还在集合里 → 可以选它' if ok else f'兵 {j} 已被吃掉 → 跳过'
    r0, r1 = B.get('res'), I['res']
    if r0 is not None and r0 != r1:
        t = f'上一个选择让 `res` 更新为 =={r1}==；' + t
    return t


def _state(S):
    I = S['_inner']
    if 'mask' not in I or 'n' not in S:
        return '先用 BFS 预处理：`dis[i][x][y]` = 兵 i 到 (x,y) 的马步数'
    n, mask, i = S['n'], I['mask'], I['i']
    left = [str(k) for k in range(n) if mask >> k & 1]
    who = 'Bob（取 min）' if (((1 << n) - 1) ^ mask).bit_count() % 2 else 'Alice（取 max）'
    where = f'兵{i}' if i < n else '起点'
    return f'马在==' + where + f'==，剩余兵 `{{{",".join(left) or "空"}}}`，轮到 =={who}=='


CONFIG = dict(
    num=3283, title='吃掉所有兵需要的最多移动次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP · 记忆化搜索',
    tags=['状压 DP', '难度分 2473'],
    code='''
DIRS = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))

class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        n = len(positions)
        # 计算马到兵的步数，等价于计算兵到其余格子的步数
        dis = [[[-1] * 50 for _ in range(50)] for _ in range(n)]
        for d, (px, py) in zip(dis, positions):
            d[px][py] = 0
            q = [(px, py)]
            step = 1
            while q:
                tmp = q
                q = []
                for p in tmp:
                    for dx, dy in DIRS:
                        x, y = p[0] + dx, p[1] + dy
                        if 0 <= x < 50 and 0 <= y < 50 and d[x][y] < 0:
                            d[x][y] = step
                            q.append((x, y))
                step += 1

        positions.append((kx, ky))
        u = (1 << n) - 1
        @cache
        def dfs(i: int, mask: int) -> int:
            if mask == 0:
                return 0
            odd = (u ^ mask).bit_count() % 2
            res = inf if odd else 0
            op = min if odd else max
            x, y = positions[i]
            for j, d in enumerate(dis):
                if mask >> j & 1:
                    res = op(res, dfs(j, mask ^ (1 << j)) + d[x][y])
            return res
        return dfs(n, u)
''',
    call='Solution().maxMoves(0, 2, [[1,1],[2,2],[3,3]])',
    expect=8,
    skip=['q = [(px', 'step = 1', 'while q', 'tmp = q', 'q = []', 'for p in tmp', 'for dx, dy', 'x, y = p[0]',
          'if 0 <= x', 'd[x][y] = step', 'q.append', 'step += 1', 'd[px][py] = 0', 'u = (1', 'x, y = positions[i]',
          'odd = (u', 'op = min', 'for j, d in enumerate'],
    views=[
        dict(type='text', fn=_state, size=26, h=60),
        dict(type='table', var=_mat, label='dis：行 = 当前位置，列 = 目标兵，值 = 马最少步数（黄 = 正在用）', h=330, cell=96,
             rows=lambda S: _names(S)[1], cols=lambda S: _names(S)[0], color=_hl),
        dict(type='calls', h=300),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'),
           ('mask', lambda S: bin(S['_inner']['mask'])[2:] if 'mask' in S['_inner'] else '', 'cyan'),
           ('j', lambda S: S['_inner'].get('j'), 'pink'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'dis = [[[-1]': '`dis[i][x][y]` = 兵 i 走到 (x,y) 的最少步数，先全设 `-1`',
        'for d, (px, py)': '对每个兵做一次网格 BFS：马走日的路线可以==反过来==走，所以从兵出发算到所有格子的步数',
        'positions.append': '把马的起点当作第 `n` 个位置：现在 `positions[n] = ({kx}, {ky})`，BFS 表已就绪',
        'dfs(i: int, mask': '`dfs({i}, {mask:b})`：马在位置 i，剩余兵集合为 mask → 两人总步数的最优值',
        'if mask == 0': lambda S, B, r: ('`mask == 0`：兵吃完了 → 返回 ==0==' if S['_inner']['mask'] == 0
                                         else '兵还没吃完，继续枚举下一个要吃的兵'),
        'res = inf if odd': lambda S, B, r: ('已吃偶数个 → 轮到 ==Alice==，想让总步数最大：`res` 从 0 起，用 max' if not S['_inner']['odd']
                                              else '已吃奇数个 → 轮到 ==Bob==，想让总步数最小：`res` 从 inf 起，用 min'),
        'if mask >> j & 1': _pick,
        'res = op(res': '吃兵 `{j}`：马走 `dis` = `{d[x][y]}` 步，再加递归 `dfs({j}, {B.mask ^ (1 << j):b})` 里后手的最优 → 用 `op` 更新 `res`',
        'return res': '这个局面的最优总步数 ==`{res}`==',
        'return dfs(n, u)': '从起点、所有兵都在的局面 `dfs(n, u)` 出发，就是答案',
    },
    setup='''
import sys, builtins
def zip(*its):
    # 仅演示用：BFS 预处理有 2 万多次循环，这里让 for 循环体内部不再逐行追踪（代码本身不变）
    fr = sys._getframe(1)
    tr = fr.f_trace
    for t in builtins.zip(*its):
        fr.f_trace = None
        yield t
        fr.f_trace = tr
''',
    max_steps=62,
    cards=dict(
        one_liner='谁先吃哪个兵不重要，重要的是「还剩哪些兵、马在哪」',
        complexity='时间 `O(nL^2 + n^2 2^n)`，空间 `O(nL^2 + n 2^n)`',
        problem=['50×50 棋盘上有一匹马和 ≤15 个兵，Alice、Bob 轮流选一个兵，马用最少步数吃掉它',
                 'Alice 要总步数最大，Bob 要最小，求最优策略下的总步数',
                 '示例：`kx=0, ky=2, positions=[[1,1],[2,2],[3,3]]` → `8`'],
        quote='这两种情况，Bob 面临的局面是完全一样的：前三个兵都被吃掉，马现在在第三个兵的位置。有重复的子问题，就可以用记忆化搜索/递推解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `dfs(i, mask)`：马在第 i 个位置，`mask` 是剩余的兵；起点当作第 n 个位置',
              '步数 `dis` 先用 BFS 算好；已吃兵数的==奇偶性==决定当前是 Alice（max）还是 Bob（min）',
              '`dfs(i, mask) = op_j dfs(j, mask 去掉 j) + dis[j][x][y]`，边界 `mask == 0` 返回 0'],
        summary=['时间 `O(nL^2 + n^2 2^n)`，L = 50；空间 `O(nL^2 + n 2^n)`',
                 '要的是==两人的总步数==，不是 Alice 一个人的',
                 '用 `(u ^ mask).bit_count()` 的奇偶判断轮到谁，省掉一个状态',
                 '灵神还给了 alice/bob 两个互相递归的写法，以及 1:1 翻译的递推（外层 mask 从小到大），本视频只演示记忆化搜索',
                 '本视频用 3 个兵的示例；`bit_count` 需要 Python 3.10+'],
    ),
)
