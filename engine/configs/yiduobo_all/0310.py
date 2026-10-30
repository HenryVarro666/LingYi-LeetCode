EDGES = [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]
POS = {0: (0.12, 0.18), 1: (0.12, 0.5), 2: (0.12, 0.82), 3: (0.4, 0.5), 4: (0.66, 0.5), 5: (0.9, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（蓝 = 当前 now，黄 = now_len；绿字 = node / other / 当前最远 res）', 24, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + a * w, y0 + 70 + b * h) for k, (a, b) in POS.items()}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    inner = S.get('_inner') or {}
    now = inner.get('now')
    now_len = inner.get('now_len')
    marks = {}
    for k, nm in (('node', 'node'), ('other_node', 'other'), ('res', 'res'), ('res1', 'res1')):
        v = S.get(k)
        if isinstance(v, int) and k in S and 'g' in S and 'edges' in S:
            marks.setdefault(v, []).append(nm)
    R = 34
    for k, (x, y) in P.items():
        fill = T['blue'] if k == now else T['panel2']
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], width=2, r=R)
        cv.text((x, y), k, 30, T['bg'] if k == now else T['text'], anchor='mm', bold=True)
        if k in marks:
            cv.text((x, y + R + 6), '/'.join(marks[k]), 22, T['green'], anchor='mt', bold=True)
    if now is not None and now_len is not None and now in P:
        x, y = P[now]
        cv.text((x, y - R - 6), f'len={now_len}', 22, T['yellow'], anchor='mb', bold=True)


def _cmp(S, B, ret):
    if S.tmp_len > B.choose_len:
        return f'子树 `{S.next_node}` 最远走到 `{S.tmp_res}`（距离 `{S.tmp_len}`）> 目前最远 `{B.choose_len}` → ==更新=='
    return f'子树 `{S.next_node}` 最远距离 `{S.tmp_len}` 不超过 `{B.choose_len}` → 不更新'


def _aim(S, B, ret):
    if S.aim_len is None:
        return '`aim_len = None`：这一趟是==找最远点=='
    if S.aim_len == S.now_len:
        return f'`now_len == aim_len = {S.aim_len}` → ==走到中点了==，返回 `{S.now}`'
    return f'`now_len = {S.now_len}` 还没走到 `aim_len = {S.aim_len}`，继续往下'


CONFIG = dict(
    num=310, title='最小高度树', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='两次 DFS 求直径，取中点',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def findMinHeightTrees(self, n, edges):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = []
            if y not in g:
                g[y] = []
            g[x].append(y)
            g[y].append(x)

        node, l = self.dfs(0, None, 0, None, g)
        other_node, d = self.dfs(node, None, 0, None, g)

        res, l = self.dfs(node, d // 2, 0, None, g)
        if d % 2 == 1:
            res1, l = self.dfs(node, d // 2 + 1, 0, None, g)
            return [res, res1]
        return [res]

    def dfs(self, now, aim_len, now_len, fa, g):
        if aim_len is not None:
            if aim_len == now_len:
                return now, now_len

        res = now
        choose_len = now_len

        for next_node in g.get(now, []):
            if next_node != fa:
                tmp_res, tmp_len = self.dfs(next_node, aim_len, now_len + 1, now, g)
                if tmp_len > choose_len:
                    choose_len = tmp_len
                    res = tmp_res
        
        return res, choose_len
''',
    call=f'Solution().findMinHeightTrees(6, {EDGES})',
    expect=[4, 3],
    max_steps=75,
    skip=['for x, y in edges', 'if x not in g', 'if y not in g', 'g[x] = []', 'g[y] = []', 'g[x].append',
          'g[y].append', 'res = now', 'choose_len = now_len', 'for next_node in', 'if next_node != fa',
          'if aim_len is not None', 'res = tmp_res'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=230, hide=('g', 'self')),
    ],
    watch=[('node', 'node', 'green'), ('other_node', 'other_node', 'green'), ('d', 'd', 'yellow'),
           ('choose_len', 'choose_len', 'cyan')],
    captions={
        'g = {}': '先用邻接表 `g` 存图',
        'node, l = self.dfs(0': '第 1 趟：从任意点 `0` 出发，找离它==最远的点== `node`',
        'other_node, d = self.dfs(node': lambda S, B, r: f'第 2 趟：从 `node = {B.node}` 出发再找最远点 → 两者之间就是==直径==',
        'res, l = self.dfs(node, d // 2': lambda S, B, r: f'直径长度 `d = {B.d}`；第 3 趟：从端点 `{B.node}` 沿直径走 `d // 2 = {B.d // 2}` 步',
        'if d % 2 == 1': lambda S, B, r: (f'`d = {S.d}` 是奇数 → 直径上有==两个==中点' if S.d % 2 else f'`d = {S.d}` 是偶数 → 只有一个中点'),
        'res1, l = self.dfs(node, d // 2 + 1': lambda S, B, r: f'第 4 趟：走 `d // 2 + 1 = {B.d // 2 + 1}` 步，找第二个中点',
        'return [res, res1]': '答案：`{ret}`',
        'return [res]': '答案：`{ret}`',
        'if aim_len == now_len': _aim,
        'return now, now_len': '返回中点 `{now}`',
        'tmp_res, tmp_len = self.dfs': lambda S, B, r: f'从 `{B.now}` 走到邻居 `{S.now}`，距离 +1',
        'if tmp_len > choose_len': _cmp,
        'choose_len = tmp_len': '`choose_len` → {choose_len}，`res` 记为 `{tmp_res}`',
        'return res, choose_len': '`{now}` 的子树里最远点是 `{res}`，距离 `{choose_len}` → 返回上一层',
    },
    cards=dict(
        one_liner='最小高度树的根，就是树的直径的中点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个节点的树（无向、无环），任选一个节点当根',
                 '让树的高度最小的根叫最小高度树，返回所有这样的根',
                 '本视频：`n = 6`，`edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3,4]`（顺序任意）'],
        quote='直观的想法就是先找到树中距离最远的两个点，然后==选择这两个点的中点作为根节点==。……可以通过两次dfs获得。',
        quote_src='—— yiduobo 题解原文',
        idea=['从任意点 M 出发找最远点 N，再从 N 出发找最远点 O：==N 到 O 就是直径==',
              '从 N 沿直径走 `d // 2` 步就是中点；`d` 为奇数时有两个中点',
              '同一个 `dfs` 兼两用：`aim_len = None` 找最远点，否则走到指定距离就返回'],
        summary=['时间 `O(n)`：常数趟 DFS',
                 '为什么从 N 走 `d//2` 步一定在直径上：越过的分支都没有直径方向长，最远点在直径上',
                 '易错：`n = 1` 时没有边，`g.get(now, [])` 保证不会出错',
                 '原文为 Python 2 写法，整数除法 `d / 2` 已改为 `d // 2`'],
    ),
)
