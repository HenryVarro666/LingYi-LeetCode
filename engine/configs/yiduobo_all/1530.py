import re as _re

DONE = {}


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def _rec(fn, record=False, var='now'):
    def cap(S, B, ret):
        n = S.get(var)
        if record and n is not None:
            DONE[n._uid] = ret[0]
        for m in _walk(S.get('self.tree')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _fmt(t):
    def f(S, B, r):
        env = {'B': B, 'ret': r, 'sorted': sorted, 'len': len, 'max': max, 'min': min}
        return _re.sub(r'\{([^{}]+)\}', lambda m: str(eval(m.group(1), env, S)), t)
    return f


def _wrap(d):
    return {k: _rec(v if callable(v) else _fmt(v)) for k, v in d.items()}


def _sum_color(S, n):
    return 'green' if getattr(n, '_d', None) is not None else None


def _badges(cv, S, B, box, T):
    root = S.get('self.tree')
    if root is None:
        return
    x0, y0, x1, y1 = box[0], box[1] - TREE_H, box[2], box[1]
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    for i, n in enumerate(order):
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad
        s = '累计 %d 对' % d
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2 + 0, Y + rad + 12, X + w / 2, Y + rad + 38), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 25), s, 19, T['green'], anchor='mm', bold=True)


TREE_H = 360


CONFIG = dict(
    num=1530, title='好叶子节点对的数量', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='后序 DFS + 距离计数数组',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def countPairs(self, root, distance):

        return self.dfs(root, distance)[0]
    
    def dfs(self, now, distance):
        if not now.left:
            if not now.right:
                res = 0
                dis = [0] * distance
                dis[0] = 1
            else:
                res, right_dis = self.dfs(now.right, distance)
                dis = [0] + [x for x in right_dis[:distance - 1]]
        elif not now.right:
            res, left_dis = self.dfs(now.left, distance)
            dis = [0] + [x for x in left_dis[:distance - 1]]
        else:
            left_res, left_dis = self.dfs(now.left, distance)
            right_res, right_dis = self.dfs(now.right, distance)
            
            for index in range(distance - 1, 0, -1):
                left_dis[index] = left_dis[index - 1]
                right_dis[index] = right_dis[index - 1]
            left_dis[0] = right_dis[0] = 0

            res = left_res + right_res
            s = 0
            for index in range(distance - 1, 0, -1):
                s += left_dis[distance - index]
                res += s * right_dis[index]
            
            dis = [0] * distance
            for index in range(distance):
                dis[index] += left_dis[index] + right_dis[index]
            
        return res, dis
''',
    call='''sol = Solution()
sol.tree = Tr([1,2,3,4,5,None,6,None,None,7,8])
sol.countPairs(sol.tree, 3)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回，标注 = 该子树内的好叶子对数）', pointers={'now': 'blue'}, h=TREE_H, color=_sum_color),
        dict(type='custom', draw=_badges, h=0),
        dict(type='array', var='left_dis', label='left_dis（左子树：距 left 根为 i 的叶子数）', cell=44, h=84),
        dict(type='array', var='right_dis', label='right_dis（右子树）', cell=44, h=84),
        dict(type='array', var='dis', label='dis（当前节点：距 now 为 i 的叶子数）', cell=44, h=84,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='calls', h=132, hide=('sol', 'self', 'distance', 'left_dis', 'right_dis', 'dis', 'res')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green'), ('s', lambda S: S['_inner'].get('s'), 'yellow')],
    captions=_wrap({
        4: lambda S, B, r: DONE.clear() or '`dfs` 返回 `(合法路径数, dis)`；`dis[i]` = 子树里==距根恰好 `i`== 的叶子个数；答案取下标 `0`',
        7: lambda S, B, r: f'节点 `{S.now.val}`：' + ('==没有左孩子==，再看右孩子' if not S.now.left else '有左孩子，再看右孩子'),
        8: lambda S, B, r: f'节点 `{S.now.val}` ' + ('也没有右孩子 → ==叶子==' if not S.now.right else '有右孩子 → 只有右孩子'),
        11: '叶子：自己不构成路径，`res = 0`；距自己为 `0` 的叶子有 1 个 → `dis = {dis}`（只留 `distance` 项，更远的配不成好对）',
        13: lambda S, B, r: '只有右孩子 → 递归右子树，路径不可能经过两边' if 'right_dis' not in S or S.get('res') is None else f'右子树返回：`res = {S.res}`，`right_dis = {S.right_dis}`',
        14: '到当前节点要多走一步：==所有距离 +1==，即 `dis = [0] + 孩子 dis 的前 distance-1 项` = `{dis}`',
        15: lambda S, B, r: f'节点 `{S.now.val}` 有左孩子；' + ('没有右孩子 → 只有左孩子' if not S.now.right else '右孩子也有 → 两边都有'),
        16: lambda S, B, r: '只有左孩子 → 递归左子树' if 'left_dis' not in S or S.get('res') is None else f'左子树返回：`res = {S.res}`，`left_dis = {S.left_dis}`',
        17: '同样所有距离 +1 → `dis = {dis}`',
        19: lambda S, B, r: '两边都有 → 先递归左子树' if 'left_res' not in S else f'左子树：`left_res = {S.left_res}`，`left_dis = {S.left_dis}`',
        20: lambda S, B, r: '再递归右子树' if 'right_res' not in S else f'右子树：`right_res = {S.right_res}`，`right_dis = {S.right_dis}`',
        25: '两边的 dis 整体右移一位（距离 +1，到达当前节点），`[0]` 清零：`left_dis = {left_dis}`，`right_dis = {right_dis}`',
        30: '右边距离 `{index}` 的叶子，能配左边距离 ≤ `{distance - index}` 的（总路程 ≤ `distance`）：==`s` 累计左边这些叶子== = `{s}`',
        31: '经过 `{now.val}` 的好对 += `s * right_dis[{index}]` = `{s} * {right_dis[index]}` → `res = {res}`',
        37: _rec(lambda S, B, r: f'节点 `{S.now.val}` 返回 `(res={r[0]}, dis={r[1]})`：子树里共 `{r[0]}` 对好叶子', True),
    }),
    skip=['res = 0', 'dis = [0] * distance', 'for index in range(distance - 1, 0, -1)', 'left_dis[index] = left_dis[index - 1]', 'right_dis[index] = right_dis[index - 1]', 'for index in range(distance)', 'dis[index] += left_dis', 'res = left_res + right_res', 's = 0'],
    max_steps=100,
    cards=dict(
        one_liner='每个节点只记「各距离上有几个叶子」：左右两边的叶子在这里配对',
        complexity='时间 `O(n * distance)`，空间 `O(n + distance)`',
        problem=['给你二叉树 `root` 和整数 `distance`',
                 '两个叶子之间==最短路径长度 ≤ distance== 就叫一个「好叶子节点对」',
                 '返回树中好叶子节点对的数量',
                 '本视频：`root = [1,2,3,4,5,null,6,null,null,7,8]`，`distance = 3` → `3`'],
        quote='对于以now为根节点的子树而言，所有经过now的合法路径的起点和终点不可能出现在now的同一侧子树当中。',
        quote_src='—— yiduobo 题解',
        idea=['一条经过 `now` 的好路径，两个叶子必须==一个在左子树、一个在右子树==',
              '`distance` 最大只有 10，所以每个节点只维护 `dis[0..distance-1]`：子树里距它为 `i` 的叶子数',
              '两边都有孩子时：`dis` 整体 +1，然后枚举右边距离 `k`，配左边距离 ≤ `distance - k` 的叶子，用前缀和 `s` 优化'],
        result='返回 `3`：叶子 `7、8`，`4、7`，`4、8` 三对，路径长度都 `≤ 3`',
        summary=['时间 `O(n * distance)`，空间 `O(n + distance)`',
                 '四种情况：叶子；只有右孩子；只有左孩子；两边都有（只有最后一种产生新的好对）',
                 '易错：配对时要先把两边 `dis` 右移一位（多走一步到 `now`），再枚举；`s` 是左边距离前缀和',
                 '原文已是 Python 3 可运行写法，无需改动；题面库里缺失，题意按 LeetCode 1530 原题撰写'],
    ),
)
