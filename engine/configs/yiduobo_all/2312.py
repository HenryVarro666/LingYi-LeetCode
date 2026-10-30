PR = [[1, 1, 2], [2, 1, 3]]
M, N = 2, 2


def _cell(S, r, c, v):
    h, w = S.get('h'), S.get('w')
    if h is None:
        return None
    if (r, c) == (h, w):
        return 'yellow'
    if r == 0 or c == 0:
        return None
    return 'green' if v != -1 else None


def _txt(S):
    h, w = S.get('h'), S.get('w')
    if h is None:
        return '`f[h][w]` = 高 h 宽 w 的木头最多卖多少钱，`-1` 表示还没算'
    return f'正在算 `dfs({h}, {w})`：先看能不能整块卖，再试==水平切==（拆高）、==竖直切==（拆宽）'


CONFIG = dict(
    num=2312, title='卖木头块', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 记忆化搜索',
    tags=['其他线性 DP', '难度分 2363'],
    code='''
class Solution(object):
    def sellingWood(self, m, n, prices):

        f = [[-1] * (n + 1) for _ in range(m + 1)]
        price_dict = {}

        for h, w, price in prices:
            price_dict[(h, w)] = price

        def dfs(h, w, f):
            if f[h][w] == -1:
                if (h, w) in price_dict:
                    f[h][w] = price_dict[(h, w)]
                else:
                    f[h][w] = 0

                for index in range(1, h):
                    f[h][w] = max(f[h][w], dfs(index, w, f) + dfs(h - index, w, f))
                
                for index in range(1, w):
                    f[h][w] = max(f[h][w], dfs(h, index, f) + dfs(h, w - index, f))
            
            return f[h][w]
            
        return dfs(m, n, f)
''',
    call=f'Solution().sellingWood({M}, {N}, {PR!r})',
    expect=8,
    skip=['for h, w, price', 'price_dict[(h, w)] = price', 'f = [[-1]', 'price_dict = {}'],
    max_steps=90,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='table', var='f', label='f[h][w]（黄 = 正在算，绿 = 已算好，-1 = 未算）', h=260, cell=84,
             rows=lambda S: [str(k) for k in range(len(S['f']))], cols=lambda S: [str(k) for k in range(len(S['f'][0]))],
             color=_cell),
        dict(type='calls', h=220, hide=('f', 'prices')),
    ],
    watch=[('h', 'h', 'blue'), ('w', 'w', 'pink'), ('index', 'index', 'yellow'), ('f[h][w]', 'f[h][w]', 'green')],
    captions={
        'if f[h][w] == -1': lambda S, B, r: (f'`f[{S.h}][{S.w}]` 是 `-1` → ==还没算过==，往下算' if S.f[S.h][S.w] == -1
                                             else f'`f[{S.h}][{S.w}] = {S.f[S.h][S.w]}` ==已经算过==，直接返回（记忆化）'),
        'if (h, w) in price_dict': lambda S, B, r: (f'`({S.h}, {S.w})` 恰好是一种标价尺寸，可以整块卖掉' if (S.h, S.w) in S.price_dict
                                                    else f'`({S.h}, {S.w})` 没有标价，整块卖不了，先记 0'),
        'f[h][w] = price_dict': '整块卖：`f[{h}][{w}] = {price_dict[(h, w)]}`',
        'f[h][w] = 0': '不能整块卖，`f[{h}][{w}]` 先记为 `0`，再看切开能不能更赚',
        'for index in range(1, h)': '水平切：枚举上半部分的高度 `index`（`1 ≤ index < {h}`）',
        'for index in range(1, w)': '竖直切：枚举左半部分的宽度 `index`（`1 ≤ index < {w}`）',
        'dfs(index, w, f)': lambda S, B, r: f'水平切 `index = {B.index}`：先递归求 `({B.index}, {B.w})`，再求 `({B.h - B.index}, {B.w})`，两块相加后和 `f[{B.h}][{B.w}]` 取 `max`',
        'dfs(h, index, f)': lambda S, B, r: f'竖直切 `index = {B.index}`：先递归求 `({B.h}, {B.index})`，再求 `({B.h}, {B.w - B.index})`，两块相加后和 `f[{B.h}][{B.w}]` 取 `max`',
        'return f[h][w]': '`dfs({h}, {w})` 算完，返回 `{f[h][w]}` → 回到上一层，加进切法的总和里',
        'return dfs(m, n, f)': lambda S, B, r: ('从整块 `dfs(m, n)` 开始递归' if r is None else f'整块 `{S.m} × {S.n}` 最多卖 =={r}=='),
    },
    cards=dict(
        one_liner='整块卖、水平切、竖直切，三者取最大',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn)`',
        problem=['`m × n` 的木块，每次沿整条边切一刀；`prices` 给出各尺寸卖价，不能旋转',
                 '求能卖到的==最多钱数==，不用全卖完',
                 '示例：`m=3, n=5` → `19`；视频用 `m=2, n=2`'],
        quote='由于f[i][j]可能依赖所有i或j更小的状态，因此在这里使用记忆化搜索而非常规的递推式动态规划会更方便一些。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]` = 高 i 宽 j 的木头最多卖多少钱',
              '三种来源：整块卖 `p[(i,j)]`；水平切 `f[index][j] + f[i-index][j]`；竖直切 `f[i][index] + f[i][j-index]`',
              '依赖的状态顺序不固定，用 `-1` 标记未算，递归时按需计算'],
        summary=['时间 `O(mn(m+n))`：mn 个状态，每个枚举 `m+n` 个切点',
                 '易错：`-1` 才表示未算，`0` 是合法答案；不能旋转木块',
                 '这里没有只枚举一半，两边对称各算了一次，结果相同',
                 '本题可改成按 i、j 从小到大的递推'],
    ),
)
