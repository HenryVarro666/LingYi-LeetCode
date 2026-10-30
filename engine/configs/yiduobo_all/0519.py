R, C = 2, 3


def _used(S):
    d = S.get('self.pos_dict')
    t = S.get('self.tot')
    if d is None or t is None:
        return [[0] * C for _ in range(R)]
    g = [[0] * C for _ in range(R)]
    mid = 'pos' in S.get('_inner', {}) and S.get('_line', 0) < 22   # flip 还没写完：边界槽位 tot 暂不算已用
    for k in range(t + (1 if mid else 0), R * C):
        p = d.get(k, k)
        g[p // C][p % C] = 1
    return g


def _txt(S):
    t = S.get('self.tot')
    if t is None:
        return ''
    return f'右边界 `tot = {t}`：编号 `>= {t}` 的槽位已经被用掉，不再参与随机'


CONFIG = dict(
    num=519, title='随机翻转矩阵', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='随机数映射 · 右边界交换',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.tot = n_rows * n_cols
        self.pos_dict = {}

    def flip(self):
        self.tot -= 1
        pos = random.randint(0, self.tot)
        if pos in self.pos_dict:
            real_pos = self.pos_dict[pos]
        else:
            real_pos = pos
        
        if self.tot in self.pos_dict:
            self.pos_dict[pos] = self.pos_dict[self.tot]
        else:
            self.pos_dict[pos] = self.tot

        self.pos_dict[self.tot] = real_pos

        return real_pos // self.n_cols, real_pos % self.n_cols

    def reset(self):
        self.pos_dict = {}
        self.tot = self.n_rows * self.n_cols
''',
    setup='import random\nrandom.seed(0)',
    call='''s = Solution(2, 3)
out = [s.flip(), s.flip(), s.flip()]
s.reset()
out.append(s.flip())
out''',
    expect=[(1, 0), (1, 2), (0, 0), (0, 2)],
    views=[
        dict(type='grid', var=_used, label='矩阵 2×3（绿 = 已翻成 1 的格子）', h=210, cell=84, values=False,
             color=lambda S, i, j, v: 'green' if v else None),
        dict(type='map', var='self.pos_dict', label='pos_dict（随机下标 → 真实格子编号）', fmt=lambda k, v: f'{k} → {v}', h=190, font=30),
        dict(type='text', h=70, size=28, fn=_txt),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('tot', 'self.tot', 'blue'), ('pos', 'pos', 'yellow'), ('real_pos', 'real_pos', 'green')],
    captions={
        'self.tot -= 1': '剩余可选数少 1：右边界 `tot` → =={self.tot}==（`[0, tot]` 里都是还没翻的）',
        'random.randint': '只在 `[0, {self.tot}]` 里随机一次，抽到 `pos` = =={pos}==',
        'if pos in self.pos_dict': lambda S, B, r: (f'`pos = {S.pos}` 之前被映射过吗？' + ('是 → 它背后的真实格子要查表' if S.pos in S['self.pos_dict'] else '没有 → 它就代表自己')),
        'real_pos = self.pos_dict[pos]': '`pos` 已被映射：真实格子 `real_pos = {real_pos}`',
        'real_pos = pos': '`pos` 没被映射过：真实格子就是自己，`real_pos = {real_pos}`',
        'if self.tot in self.pos_dict': lambda S, B, r: ('右边界 `tot` 自己也被映射过 → 要多跳一次，取它的映射' if S['self.tot'] in S['self.pos_dict'] else '右边界 `tot` 没被映射过 → 它就是它自己'),
        'self.pos_dict[pos] = self.pos_dict[self.tot]': '把 `pos` 指向边界 `tot` 背后的真实格子 `{self.pos_dict[pos]}`：补上被抽走的空位',
        'self.pos_dict[pos] = self.tot': '把 `pos` 映射到边界 `{self.tot}`：下次抽到 `pos` 就当成边界这个数',
        'self.pos_dict[self.tot] = real_pos': '边界槽位 `tot={self.tot}` 记下刚翻过的 `real_pos = {real_pos}`，之后范围缩小它就出局',
        'return real_pos': '格子编号 `{real_pos}` → 行 `{real_pos // self.n_cols}`、列 `{real_pos % self.n_cols}`，返回 `{ret}`',
        7: '映射表一开始是空的：还没有任何格子被翻过',
        27: '重置：清空映射表',
        'self.tot = self.n_rows': '边界恢复成 `{self.tot}`：所有格子重新可选',
    },
    cards=dict(
        one_liner='每次只随机一次：抽到的位置和右边界交换，再把边界缩小',
        complexity='flip 时间 `O(1)`，空间 `O(翻转次数)`；reset `O(1)`',
        problem=['`n_rows × n_cols` 的矩阵全是 0，`flip()` 等概率随机选一个 0 翻成 1，返回其下标 `[行, 列]`',
                 '`reset()` 把所有格子重新变回 0',
                 '规模可达 `10000 × 10000`，不能把一亿个数都存下来',
                 '本视频：`2 × 3`，固定随机种子，翻 3 次、重置、再翻 1 次'],
        quote='首先第一轮，应该是从1到n中随机选一个数，不妨设其为p。在得到p之后，我们将这个数映射到第n个数上，即我们接下来第二轮的随机选取中，我们只从1到n - 1中随机',
        quote_src='—— yiduobo 题解原文',
        idea=['把格子编号成 `0..n-1`，每轮在 `[0, tot]` 里随机，抽到 `p` 就让 `p` 指向边界 `tot`',
              '下一轮范围缩小，`p` 再被抽中时就被当成 `tot`，相当于把已用的数换出范围',
              '边界 `tot` 若之前也被映射过，要==多跳一次==，指到它的映射上',
              '只有被碰过的位置才进字典，所以空间和翻转次数成正比'],
        summary=['`flip` 时间 `O(1)`，空间只和翻转次数有关，`reset` 清空字典即可',
                 '易错点：`tot` 先减 1，再 `randint(0, tot)`（两端都取得到）',
                 '易错点：边界 `tot` 若已被映射，`pos` 要映射到它的映射，不能直接写 `tot`',
                 '原文为 Python 2 写法，`real_pos / self.n_cols` 已改为整数除法 `//`；`random` 在 setup 里导入并固定种子',
                 '同类题：Fisher-Yates 洗牌（交换到末尾再缩小范围）'],
    ),
)
