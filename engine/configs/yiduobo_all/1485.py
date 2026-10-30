_POS = {1: (2.0, 0), 2: (1.0, 1), 3: (3.0, 1), 4: (0.5, 2), 5: (1.5, 2)}
_EDGES = [(1, 2), (1, 3), (2, 4), (2, 5)]

SETUP = '''
_ctr = itertools.count(1000)


class Node:
    def __init__(self, val=0, left=None, right=None, random=None):
        self.val = val
        self.left = left
        self.right = right
        self.random = random
        self._uid = next(_ctr)


class NodeCopy:
    def __init__(self, val=0, left=None, right=None, random=None):
        self.val = val
        self.left = left
        self.right = right
        self.random = random
        self._uid = next(_ctr)


_n = {v: Node(v) for v in range(1, 6)}
_n[1].left, _n[1].right = _n[2], _n[3]
_n[2].left, _n[2].right = _n[4], _n[5]
_n[1].random = _n[3]
_n[2].random = _n[1]
_n[3].random = _n[3]
_n[5].random = _n[2]
root = _n[1]
'''


def _ser(r):
    out, q = [], [r]
    for x in q:
        if type(x).__name__ != 'NodeCopy':
            return ['不是 NodeCopy']
        out.append([x.val, x.left.val if x.left else None, x.right.val if x.right else None,
                    x.random.val if x.random else None])
        q += [c for c in (x.left, x.right) if c]
    return out


def _draw(cv, S, B, box, T):
    import math as _m
    x0, y0, x1, y1 = box
    mp = S.get('mapping') or {}
    cur = S['_inner'].get('now')
    half = (x1 - x0) / 2
    sp = (half - 100) / 3.0
    dy = min(88, (y1 - y0 - 130) / 2.0)
    R = 24
    cv.text((x0 + 18, y0 + 4), '原树（绿 = 已克隆，蓝圈 = now，紫箭头 = random）', 20, T['muted'], bold=True)
    cv.text((x0 + half + 10, y0 + 4), '克隆树（青框 = NodeCopy）', 20, T['muted'], bold=True)
    cv.line([(x0 + half, y0 + 40), (x0 + half, y1 - 10)], T['border'], 2)

    def P(v, side):
        sx, d = _POS[v]
        return x0 + side * half + 50 + sx * sp, y0 + 80 + d * dy

    def rnd(a, b, side, c):
        (ax, ay), (bx, by) = P(a, side), P(b, side)
        if a == b:
            cv.d.ellipse((ax + R - 2, ay - R - 14, ax + R + 22, ay - R + 8), outline=c, width=3)
            return
        cv.arc_arrow((ax, ay - R), (bx, by - R - 4), 34, c, width=3, head=11)

    val_of = {}
    for k, c in mp.items():
        val_of[c._uid] = k.val
    for side in (0, 1):
        for a, b in _EDGES:
            if side == 1 and not (a in val_of.values() and b in val_of.values()):
                continue
            if side == 1:
                ka = [c for k, c in mp.items() if k.val == a][0]
                if not ((ka.left and ka.left.val == b) or (ka.right and ka.right.val == b)):
                    continue
            cv.line([P(a, side), P(b, side)], T['border'], 3)
    for k in _POS:
        X, Y = P(k, 0)
        done = k in {n.val for n in mp}
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if done else T['panel2'],
                     outline=T['blue'] if (cur is not None and cur.val == k) else T['border'],
                     width=5 if (cur is not None and cur.val == k) else 2)
        cv.text((X, Y), k, 24, T['bg'] if done else T['text'], anchor='mm', bold=True)
    for n in mp:
        if n.random is not None:
            rnd(n.val, n.random.val, 0, T['purple'])
    for n, c in mp.items():
        X, Y = P(n.val, 1)
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['panel2'], outline=T['cyan'], width=3)
        cv.text((X, Y), c.val, 24, T['text'], anchor='mm', bold=True)
    for n, c in mp.items():
        if c.random is not None and c.random._uid in val_of:
            rnd(n.val, val_of[c.random._uid], 1, T['purple'])


def _bfs(S, B, ret):
    return f'队列非空（`head={S.head}` < `tail={S.tail}`）→ 还有节点没处理' if S.head < S.tail else '队列处理完，树的结构都克隆好了'


def _lc(side):
    def f(S, B, ret):
        c = getattr(S.now, side)
        w = '左' if side == 'left' else '右'
        if c:
            return f'`{S.now.val}` 有{w}孩子 `{c.val}` → 要克隆它'
        return f'`{S.now.val}` 没有{w}孩子，跳过'
    return f


def _ap(S, B, ret):
    return f'孩子入队，之后还要处理它的孩子：`q` = {[x.val for x in S.q]}'


def _lm(side):
    def f(S, B, ret):
        c = getattr(S.now, side)
        return f'克隆父亲的 `{side}` 指向 ==克隆的 {c.val}==：靠 `mapping` 从原节点找到副本'
    return f


def _rd(S, B, ret):
    n = S.node
    if n.random:
        return f'`{n.val}` 的 random 指向 `{n.random.val}` → 副本 `{n.val}` 的 random 要指向 ==副本 {n.random.val}=='
    return f'`{n.val}` 的 random 为空 → 副本不用设'


CONFIG = dict(
    num=1485, title='克隆含随机指针的二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='哈希表 + BFS 两遍克隆',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def copyRandomBinaryTree(self, root):

        if not root:
            return None

        mapping = {}
        q = [root]
        mapping[root] = NodeCopy(root.val)

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            if now.left:
                q.append(now.left)
                tail += 1
                mapping[now.left] = NodeCopy(now.left.val)
                mapping[now].left = mapping[now.left]
            
            if now.right:
                q.append(now.right)
                tail += 1
                mapping[now.right] = NodeCopy(now.right.val)
                mapping[now].right = mapping[now.right]

        for node in mapping:
            if node.random:
                mapping[node].random = mapping[node.random]

        return mapping[root]
''',
    setup=SETUP,
    call='Solution().copyRandomBinaryTree(root)',
    result_fn=_ser,
    expect=[[1, 2, 3, 3], [2, 4, 5, 1], [3, None, None, 3], [4, None, None, None], [5, None, None, 2]],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='map', var='mapping', label='mapping：原节点 → 克隆节点', fmt=lambda k, v: f'{k.val}' if not hasattr(k, 'val') else f'{k.val} → {v.val}', h=140),
        dict(type='queue', var='q', label='q（BFS 队列）', fmt=lambda x: str(x.val), h=100),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'), ('head', 'head', 'cyan'), ('tail', 'tail', 'orange'),
           ('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'purple')],
    captions={
        'if not root': '空树直接返回 None；本例非空',
        'mapping = {}': '`mapping` 建立「原节点 → 克隆节点」的映射，==这是克隆的核心==',
        'q = [root]': '从根开始 BFS，`q` 是队列',
        'mapping[root] = NodeCopy': '先克隆根：`mapping[1]` = 新建的 NodeCopy(1)',
        'head, tail = 0, 1': '`q[head:tail]` 是还没处理的节点：现在只有根',
        'while head < tail': _bfs,
        'now = q[head]': '取出队首原节点 `now = {now.val}`',
        'head += 1': '`head` → {head}，`now` 出队',
        'if now.left': _lc('left'),
        'if now.right': _lc('right'),
        'q.append(now.left)': _ap,
        'q.append(now.right)': _ap,
        'tail += 1': '`tail` → {tail}',
        'mapping[now.left] = NodeCopy': '为左孩子新建副本：`mapping[{now.left.val}]`',
        'mapping[now.right] = NodeCopy': '为右孩子新建副本：`mapping[{now.right.val}]`',
        'mapping[now].left = ': _lm('left'),
        'mapping[now].right = ': _lm('right'),
        'for node in mapping': lambda S, B, r: ('第二遍：所有副本都建好了，现在专门补 `random`（副本必须已存在才能被指向）' if 'node' not in B else ('所有原节点都补完了，退出循环' if S.node.val == B.node.val else f'下一个原节点 `{S.node.val}`')),
        'if node.random': _rd,
        'mapping[node].random': '副本 `{node.val}` 的 random → 副本 `{node.random.val}`（`mapping[{node.random.val}]`）',
        'return mapping[root]': '返回根的副本：整棵克隆树（含 random）就绪',
    },
    cards=dict(
        one_liner='用哈希表把「原节点」一一对应到「克隆节点」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树每个节点除了 `left`、`right`，还有一个 `random`，可指向树中任意节点或为空',
                 '返回这棵树的==深拷贝==：全是新节点（`NodeCopy`），结构和 random 都一样',
                 '本视频：5 个节点，`1.random=3`、`3.random=3`（自指）'],
        quote='利用哈希表建立原节点到克隆节点的映射，然后遍历原数据结构，在过程中就可以利用原数据结构节点间的关系以及哈希表建立起克隆节点间的关系。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍 BFS：每到一个节点就新建副本，用 `mapping` 把父子关系==照搬==到副本上',
              '第二遍：`node1.random = node2`，就让 `mapping[node1].random = mapping[node2]`',
              'random 要放到第二遍：第一遍时被指向的节点可能还没克隆'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：random 可以指向自己、指向祖先或孩子，也可以为空',
                 '`mapping` 的键是节点对象本身（按引用），不是节点值',
                 '同类：138 随机链表的复制，思路完全一样',
                 '原文代码未改动，Python 3 可直接运行；NodeCopy 在 setup 里按题目给出'],
    ),
)
