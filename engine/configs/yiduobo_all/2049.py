PARENTS = [-1, 2, 0, 2, 0, 4, 4]


def _kids(S):
    c = S.get('childs')
    return c if isinstance(c, dict) else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '这棵树（数字 = 节点编号，蓝 = 正在处理的 now）', 22, T['muted'], bold=True)
    ps = S.get('parents')
    if ps is not None:
        ch = {}
        for i in range(1, len(ps)):
            ch.setdefault(ps[i], set()).add(i)
    else:
        ch = _kids(S)
        if ch is None:
            return
    order, depth = [], {}

    def ino(v, d):
        depth[v] = d
        kids = sorted(ch.get(v, ()))
        mid = (len(kids) + 1) // 2
        for k in kids[:mid]:
            ino(k, d + 1)
        order.append(v)
        for k in kids[mid:]:
            ino(k, d + 1)
    ino(0, 0)
    sp = min(110, (x1 - x0 - 60) / len(order))
    maxd = max(depth.values()) + 1
    dy = min(110, (y1 - y0 - 100) / max(1, maxd))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {v: (sx + i * sp, y0 + 80 + depth[v] * dy) for i, v in enumerate(order)}
    for v, kids in ch.items():
        for k in kids:
            cv.line([pos[v], pos[k]], T['border'], 3)
    now = S['_inner'].get('now') if '_inner' in S else None
    for v, (X, Y) in pos.items():
        cur = (v == now)
        fill = T['blue'] if cur else T['panel2']
        cv.rect((X - 26, Y - 26, X + 26, Y + 26), fill=fill, outline=T['yellow'] if cur else T['border'], width=3, r=26)
        cv.text((X, Y), v, 28, T['bg'] if cur else T['text'], anchor='mm', bold=True)


def _info(S):
    I = S.get('_inner', {})
    n = S.get('n')
    if 'cnt' not in I or 'score' not in I:
        return ''
    return f"节点 `{I.get('now')}`：子树大小 `cnt = {I['cnt']}`，目前得分 `score = {I['score']}`"


def _cap_leaf(S, B, ret):
    return f'节点 `{S.now}` 没有孩子：它自己的子树大小是 1；删掉它，其余 `n - 1 = {S.n - 1}` 个节点连成一棵'


def _cap_for(S, B, ret):
    return f'递归每个孩子 `{S.child}`，拿到它的子树大小 `child_cnt = {S.child_cnt}`'


def _cap_score(S, B, ret):
    return f'删掉 `{S.now}` 后，这个孩子的那棵子树整个留下，大小 `{S.child_cnt}` → 乘进 `score = {S.score}`'


def _cap_rest(S, B, ret):
    if S.n != S.cnt:
        return f'还有“上面那一块”：`n - cnt = {S.n} - {S.cnt} = {S.n - S.cnt}` 个节点 → `score = {S.score}`'
    return f'`n == cnt = {S.n}`：`{S.now}` 是整棵树的根，没有“上面那一块” → `score` 不再乘'


def _cap_cmp(S, B, ret):
    m = S['self.max_score']
    if S.score > m:
        return f'`score = {S.score}` > 目前最高 `{m}` → 刷新最高分，==计数重置为 1=='
    return f'`score = {S.score}` 没有超过目前最高 `{m}`，不是新纪录'


def _cap_eq(S, B, ret):
    m = S['self.max_score']
    if S.score == m:
        return f'`score = {S.score}` == 最高分 `{m}` → 又多一个并列，`res` 加 1'
    return f'`score = {S.score}` 低于最高分 `{m}` → 不计'


CONFIG = dict(
    num=2049, title='统计最高分的节点数目', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='dfs 子树大小 + 分数乘积',
    tags=['灵神题单', '链表树与回溯', '难度分 1912'],
    code='''
class Solution(object):
    def countHighestScoreNodes(self, parents):

        n = len(parents)
        self.max_score = 0
        self.res = 0

        childs = {}
        for index in range(1, n):
            fa = parents[index]
            if fa not in childs:
                childs[fa] = set()
            childs[fa].add(index)

        self.dfs(0, childs, n)
        return self.res

    def dfs(self, now, childs, n):
        if now not in childs:
            cnt = 1
            score = n - 1
        else:
            cnt = 1
            score = 1
            for child in childs[now]:
                child_cnt = self.dfs(child, childs, n)
                cnt += child_cnt
                score *= child_cnt
        
            if n != cnt:
                score *= (n - cnt)
        
        if score > self.max_score:
            self.res = 1
            self.max_score = score
        elif score == self.max_score:
            self.res += 1

        return cnt
''',
    call='Solution().countHighestScoreNodes([-1, 2, 0, 2, 0, 4, 4])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=_info, size=26, h=56),
        dict(type='map', var='childs', label='childs：父节点 → 孩子集合', font=22, h=190),
        dict(type='calls', h=210, hide=('childs',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow'),
           ('score', lambda S: S['_inner'].get('score'), 'orange'),
           ('max_score', 'self.max_score', 'green'), ('res', 'self.res', 'green')],
    captions={
        'n = len(parents)': '`n = {n}` 个节点，`parents[i]` 是 `i` 的父亲',
        'self.max_score = 0': '`max_score` 记录目前见过的最高分',
        'self.res = 0': '`res` 记录得到最高分的节点数',
        'fa = parents[index]': '节点 `{index}` 的父亲是 `{fa}`',
        'if fa not in childs': lambda S, B, r: (f'`{S.fa}` 还没有孩子集合 → 新建' if S.fa not in B.childs else f'`{S.fa}` 已有孩子集合'),
        'childs[fa] = set()': '`childs[{fa}] = set()`',
        'childs[fa].add': '把 `{index}` 加入 `{fa}` 的孩子：`childs[{fa}] = {childs[fa]}`',
        'self.dfs(0': '建好孩子表；从根 `0` 出发 dfs，==后序==统计每个节点的子树大小和分数',
        'if now not in childs': lambda S, B, r: (f'`{S.now}` 不在 `childs` 里 → ==叶子==' if S.now not in S.childs else f'`{S.now}` 有孩子 → 先递归孩子'),
        'score = n - 1': _cap_leaf,
        'score = 1': '分数先取 1，往后乘每个孩子子树的大小',
        'for child in childs[now]': lambda S, B, r: f'处理 `{S.now}` 的孩子 `{S.child}`',
        'child_cnt = self.dfs': _cap_for,
        'cnt += child_cnt': '`{now}` 的子树大小 `cnt` 加上孩子的 `{child_cnt}` → `{cnt}`',
        'score *= child_cnt': _cap_score,
        'if n != cnt': lambda S, B, r: (f'`n = {S.n}`，`cnt = {S.cnt}`：不相等 → 删掉 `{S.now}` 后上面还剩一块' if S.n != S.cnt
                                        else f'`n == cnt = {S.n}`：整棵树都在 `{S.now}` 下 → 它是根'),
        'score *= (n - cnt)': _cap_rest,
        'if score > self.max_score': _cap_cmp,
        'self.res = 1': '创新纪录：之前的并列作废，`res = 1`',
        'self.max_score = score': lambda S, B, r: f'最高分更新：`max_score = {S["self.max_score"]}`',
        'elif score == self.max_score': _cap_eq,
        'self.res += 1': lambda S, B, r: f'并列最高分：`res` 加 1 → {S["self.res"]}',
        'return cnt': lambda S, B, r: f'把 `{S.now}` 的子树大小 `{r}` 返回给父亲',
        'return self.res': lambda S, B, r: f'最高分 `{S["self.max_score"]}` 共有 {r} 个节点取得 → 返回 =={r}==',
    },
    skip=['cnt = 1'],
    cards=dict(
        one_liner='删掉一个点 = 左子树 × 右子树 × 剩下那一块，一趟 dfs 全算出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`parents[i]` 是节点 `i` 的父亲，根是 `0`',
                 '删掉一个节点和相连的边，剩下若干非空子树；该节点的分数 = ==这些子树大小的乘积==',
                 '返回得到最高分的节点数',
                 '本视频：`[-1,2,0,2,0,4,4]`，节点 0 得 9 分，独占最高 → `1`',
                 '题例 `[-1,2,0,2,0]` → `3`'],
        quote='去除其他任意节点都会有上面提到的剩余的其他节点构成的以整棵树原始根节点为根节点的子树。',
        quote_src='—— yiduobo 题解原文',
        idea=['删掉 `now`，最多剩三块：左子树、右子树、以及==剩余的其他节点==',
              '设以 `now` 为根的子树大小为 `cnt`，则剩余那块大小是 `n - cnt`',
              '叶子：`cnt = 1`，分数 `n - 1`；非叶子：孩子子树大小连乘，再乘 `n - cnt`（根除外）',
              '边算边更新 `max_score` 和 `res`，一趟 dfs 结束就有答案'],
        result='运行结束，最高分 9 只有节点 `0` 取得 → 返回 `1`',
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈 + 孩子表）',
                 '易错：根没有“剩余那一块”，`n == cnt` 时不能再乘 `0`',
                 '易错：新纪录要把 `res` ==重置为 1==，而不是累加',
                 '分数最大约 `n^3/27`，Python 整数不会溢出（其他语言用 long）',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串'],
    ),
)
