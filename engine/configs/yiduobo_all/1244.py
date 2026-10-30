def _upd(S):
    if 'v' not in S or 'left' not in S:
        return ''
    return f"定位分数 `v = {S['v']}`：当前区间 `[{S['left']}, {S['right']}]`，节点编号 `now = {S['now']}`"


def _cap_if(S, B, ret):
    v = S.v
    return f'区间 `[{S.left}, {S.right}]`：`v = {v}` 属于哪一半就往哪走，路过的节点 `w`、`s` 都累加'


CONFIG = dict(
    num=1244, title='力扣排行榜', difficulty='Medium', category='设计',
    author='yiduobo', technique='值域线段树（计数 + 求和）',
    code='''
class Leaderboard(object):

    def __init__(self):
        self.w = [0] * 262144
        self.s = [0] * 262144
        self.score_dict = {}

    def update(self, v, delta):
        now = 0
        left, right = 0, 131071
        while left != right:
            self.w[now] += delta
            self.s[now] += v * delta
            mid = (left + right) // 2
            if v <= mid:
                right = mid
                now = now + now + 1
            else:
                left = mid + 1
                now = now + now + 2
        
        self.w[now] += delta
        self.s[now] += v * delta

    def addScore(self, playerId, score):
        if playerId in self.score_dict:
            score += self.score_dict[playerId]
            self.update(self.score_dict[playerId], -1)
        
        self.score_dict[playerId] = score
        self.update(score, 1)

    def top(self, K):
        now = 0
        res = 0
        left = 0
        right = 131071
        while self.w[now] != K and left != right:
            if self.w[now + now + 2] < K:
                K -= self.w[now + now + 2]
                res += self.s[now + now + 2]
                now = now + now + 1
                right = (left + right) // 2
            else:
                now = now + now + 2
                left = (left + right) // 2 + 1
        
        if left == right:
            return res + left * K
        return res + self.s[now]

    def reset(self, playerId):
        
        self.update(self.score_dict[playerId], -1)
        self.score_dict.pop(playerId)
''',
    setup='''
class _Z(dict):
    def __missing__(self, k):
        return 0


class _Sparse(list):
    # 仅用于加速追踪：长度 262144 的数组每步都被深拷贝，这里让拷贝只含非零项；读写行为与普通 list 一致
    def __init__(self, base):
        super().__init__(base)
        self.nz = {}

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if v:
            self.nz[k] = v
        else:
            self.nz.pop(k, None)

    def __deepcopy__(self, memo):
        return _Z(self.nz)


_orig_init = Leaderboard.__init__


def _init(self):
    _orig_init(self)
    self.w = _Sparse(self.w)
    self.s = _Sparse(self.s)


Leaderboard.__init__ = _init
''',
    call='''lb = Leaderboard()
lb.addScore(1, 5)
lb.addScore(2, 3)
[lb.top(1), lb.top(2)]''',
    expect=[5, 8],
    views=[
        dict(type='map', var='self.score_dict', label='score_dict（playerId → 当前总分）', fmt=lambda k, v: f'玩家 {k} → {v} 分', h=150),
        dict(type='text', h=110, fn=_upd, size=26),
        dict(type='text', h=110, fn=lambda S: f"线段树根节点：`w[0] = {S['self.w'][0]}` 人，`s[0] = {S['self.s'][0]}` 分之和（整棵树的人数和总分）" if 'self.w' in S else ''),
        dict(type='calls', label='正在执行', h=160),
    ],
    watch=[('v', 'v', 'yellow'), 'left', 'right', 'now', ('w[0] 总人数', 'self.w[0]', 'green'), ('s[0] 总分', 'self.s[0]', 'cyan')],
    skip=[11, 12, 13, 14, 16, 17, 19, 20, 36, 37, 40, 41, 42, 43, 45, 46],
    max_steps=44,
    captions={
        'self.w = [0]': '`w[node]`：这个分数区间里有==多少个==玩家（线段树，值域 0..131071）',
        'self.s = [0]': '`s[node]`：这个区间里所有玩家的==分数之和==',
        'self.score_dict = {}': '再用哈希表记每个 id 当前的分数，方便删改',
        'now = 0': '从根节点出发，区间 `[0, 131071]`',
        'if v <= mid': _cap_if,
        'self.w[now] += delta\n        self.s': '到达叶子：这个分数的人数和总分也要加上 `delta`',
        22: '到达叶子（区间只剩一个分数 `{v}`）：人数 `w` 加 `{delta}`',
        23: '叶子的分数和 `s` 加 `{v} × {delta}` = `{v * delta}`',
        'if playerId in self.score_dict': lambda S, B, r: f'`{S.playerId}` 已在榜上 → 先把旧分数删掉，再按新总分加回去' if S.playerId in S.self.score_dict else f'`{S.playerId}` 是新玩家 → 直接新增',
        'score += self.score_dict': '新总分 = 旧分数 + 新增 = `{score}`',
        'self.update(self.score_dict[playerId], -1)': '==修改 = 删除 + 新增==：先在旧分数 `{self.score_dict[playerId]}` 的叶子上 `delta = -1`',
        'self.score_dict[playerId] = score': '记录 `{playerId}` 的新总分 `{score}`',
        'self.update(score, 1)': '在新分数 `{score}` 的叶子上 `delta = +1`',
        'now = 0\n        res': '',
        'res = 0': '`res` 累计已经确定在 top K 里的分数和',
        'while self.w[now] != K': lambda S, B, r: (f'这棵子树人数 `w[{S.now}] = {S.self.w[S.now]}` ≠ `K = {S.K}` 且还没到叶子 → 继续往下找第 K 大' if S.self.w[S.now] != S.K and S.left != S.right else f'`w[{S.now}] = {S.self.w[S.now]}` = `K = {S.K}`（或到叶子）→ 停止'),
        'if self.w[now + now + 2] < K': lambda S, B, r: f'右子树（分数更大）只有 `{S.self.w[S.now + S.now + 2]}` 个 < `K = {S.K}` → 右边整棵都在 top K 里，去左边找剩下的' if S.self.w[S.now + S.now + 2] < S.K else f'右子树有 `{S.self.w[S.now + S.now + 2]}` 个 ≥ `K = {S.K}` → 第 K 大在右边，往右走',
        'K -= self.w': '右边整棵都算上：`K` 减去它的人数 → `{K}`',
        'res += self.s': '`res` 加上右子树的分数和 → `{res}`',
        'now = now + now + 1': '走向左子节点 `{now}`',
        'right = (left + right) // 2': '区间缩成左半：`[{left}, {right}]`',
        'now = now + now + 2': '走向右子节点 `{now}`',
        'left = (left + right) // 2 + 1': '区间缩成右半：`[{left}, {right}]`',
        'return res + left * K': '到叶子：同分的人有好几个，只取 `K = {K}` 个：`{res} + {left} × {K}` = =={ret}==',
        'return res + self.s[now]': '这棵子树人数恰好等于 `K` → 整棵子树的分数和全要：`{res} + {self.s[now]}` = =={ret}==',
    },
    cards=dict(
        one_liner='按分数建线段树，记人数和分数和，top K 就是“找第 K 大”',
        complexity='每次操作 `O(log C)`，C = 分数上限（这里 131072）',
        problem=['设计排行榜：`addScore(id, score)` 给玩家加分（没有则新增），`top(K)` 返回前 K 名分数之和，`reset(id)` 把玩家清零',
                 '分数范围 1..100，最多 1000 次操作，总分不超过 100000',
                 '本视频：`add(1,5)`、`add(2,3)`，然后 `top(1) = 5`、`top(2) = 8`'],
        quote='涉及到数据的增、删、改、查，以及top k的求解，王道做法自然是平衡树。注意到本题score的取值范围在1到100之间，且最多只会进行1000次操作，因此score不会超过100000，那么在这里使用线段树来维护每种分数出现的次数也是可行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['线段树的下标是==分数==，每个节点存区间内的人数 `w` 和分数和 `s`',
              '改分 = 删旧分数 + 加新分数；再用 `score_dict` 记 id 到分数',
              '`top(K)`：右子树人数不够 K 就整棵吃掉，去左边补；够就进右边找'],
        summary=['`update` 和 `top` 都是 `O(log C)`；数组开 `262144` = 2 × 131072',
                 '==`top` 在叶子上要乘 K==：同一分数可能有很多人，只取剩下的 K 个',
                 '没演示改分和 `reset`：都是对旧分数 `update(.., -1)`（改分再加新分数）',
                 'setup 里把两个大数组换成追踪友好的 list 子类（行为不变，仅加速）；作者代码未改',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 3 处），否则 Python 3 里下标会变成浮点数'],
    ),
)
