def _kids(n):
    out, c = [], getattr(n, 'child', None)
    while c is not None and len(out) < 12:
        out.append(c)
        c = getattr(c, 'brother', None)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '家族树（蓝线 = child 第一个孩子，橙箭头 = brother 下一个兄弟）', 22, T['muted'], bold=True)
    root = S.get('self.root')
    if root is None:
        cv.text((x0 + 18, y0 + 60), '（还没有国王）', 24, T['dim'])
        return
    dead = S.get('self.death_set') or set()
    res = S.get('self.res') or []
    cur = S.get('now')
    pos, depth, cnt = {}, {}, [0]

    def lay(n, d):
        ks = _kids(n)
        depth[id(n)] = d
        if not ks:
            pos[id(n)] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                lay(k, d + 1)
            pos[id(n)] = (pos[id(ks[0])] + pos[id(ks[-1])]) / 2
    lay(root, 0)
    nl = max(1, cnt[0])
    md = max(depth.values()) + 1
    cw = min(150, (x1 - x0 - 60) / nl)
    sx = x0 + 30 + ((x1 - x0 - 60) - cw * nl) / 2 + cw / 2
    top, gap = y0 + 70, min(95, (y1 - y0 - 110) / max(1, md - 1 if md > 1 else 1))
    bw, bh = min(118, cw - 14), 42

    def P(n):
        return sx + pos[id(n)] * cw, top + depth[id(n)] * gap
    allnodes = []

    def walk(n):
        allnodes.append(n)
        for k in _kids(n):
            walk(k)
    walk(root)
    for n in allnodes:
        X, Y = P(n)
        ks = _kids(n)
        if ks:
            X2, Y2 = P(ks[0])
            cv.line([(X, Y + bh / 2), (X2, Y2 - bh / 2)], T['blue'], 3)
        for a, b in zip(ks, ks[1:]):
            xa, ya = P(a)
            xb, yb = P(b)
            cv.arrow((xa + bw / 2 + 3, ya), (xb - bw / 2 - 3, yb), T['orange'], 3, 10)
    for n in allnodes:
        X, Y = P(n)
        nm = n.name
        isdead = nm in dead
        if n is cur:
            fill, outline, tc = T['yellow'], T['yellow'], T['bg']
        elif nm in res:
            fill, outline, tc = T['green'], T['green'], T['bg']
        else:
            fill, outline, tc = T['panel2'], T['border'], T['dim'] if isdead else T['text']
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=fill, outline=outline, width=2, r=12)
        cv.text((X, Y), nm, 22, tc, anchor='mm', bold=True)
        if isdead:
            cv.line([(X - bw / 2 + 8, Y), (X + bw / 2 - 8, Y)], T['red'], 3)
    cv.text((x1 - 20, y1 - 4), '黄 = 正在访问，绿 = 已进入顺序，红线 = 已去世', 19, T['dim'], anchor='rb')


CONFIG = dict(
    num=1600, title='皇位继承顺序', difficulty='Medium', category='设计',
    author='yiduobo', technique='孩子兄弟表示法 + 先序 dfs',
    tags=[],
    code='''
class TreeNode(object):

    def __init__(self, name):
        self.name = name
        self.child = self.brother = self.little_child = None

class ThroneInheritance(object):

    def __init__(self, kingName):
        self.root = TreeNode(kingName)
        self.death_set = set()
        self.node_dict = {}
        self.node_dict[kingName] = self.root

    def birth(self, parentName, childName):
        new_child = TreeNode(childName)
        self.node_dict[childName] = new_child
        parent = self.node_dict[parentName]
        if parent.child is None:
            parent.child = new_child
            parent.little_child = new_child
        else:
            little_child = parent.little_child
            little_child.brother = new_child
            parent.little_child = new_child

    def death(self, name):
        self.death_set.add(name)

    def getInheritanceOrder(self):
        self.res = []
        self.dfs(self.root)
        return self.res

    def dfs(self, now):
        if now.name not in self.death_set:
            self.res.append(now.name)
        if now.child:
            self.dfs(now.child)
        if now.brother:
            self.dfs(now.brother)
''',
    call='''t = ThroneInheritance("king")
t.birth("king", "andy")
t.birth("king", "bob")
t.birth("andy", "matthew")
first = t.getInheritanceOrder()
t.death("bob")
[first, t.getInheritanceOrder()]''',
    expect=[['king', 'andy', 'matthew', 'bob'], ['king', 'andy', 'matthew']],
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='array', var='self.res', label='self.res（继承顺序，先序遍历的结果）', cell=104, h=120),
        dict(type='calls', h=150, hide=('now',), label='dfs 调用栈'),
    ],
    watch=[('now', 'now.name', 'yellow'), ('res', 'self.res', 'green'), ('dead', 'sorted(self.death_set)', 'red')],
    max_steps=110,
    skip=['self.name = name', 'self.child = self.brother', 'self.res = []', 'self.node_dict = {}'],
    captions={
        'self.root = TreeNode': '国王 `{kingName}` 是树根',
        'self.death_set = set()': '`death_set` 只记谁死了，不改树',
        'self.node_dict = {}': '`node_dict`：名字 → 节点，==O(1) 找到父亲==',
        'self.node_dict[kingName]': '把国王也登记进 `node_dict`',
        'new_child = TreeNode': '新生儿 `{childName}` 是一个新节点',
        'self.node_dict[childName]': '登记 `{childName}`，以后他也能当父亲',
        'parent = self.node_dict': '通过哈希表直接找到父亲 `{parentName}`',
        'if parent.child is None': lambda S, B, ret: (f'`{S.parentName}` 还没有孩子 → 新生儿成为==长子==' if S.parent.child is None
                                                      else f'`{S.parentName}` 已有孩子 → 新生儿接在最小的孩子后面'),
        'parent.child = new_child': '长子 `child` = `{childName}`',
        'parent.little_child = new_child': '`little_child` 指向 `{childName}`（现在最小的孩子）',
        'little_child = parent.little_child': '`little_child` 是最小的孩子 `{little_child.name}`，==不用遍历所有孩子==',
        'little_child.brother = new_child': '`{little_child.name}` 的 `brother` 接上 `{childName}`：O(1) 插入',
        'self.death_set.add': '`{name}` 死亡，只加入 `death_set`，==继承顺序里跳过他==，但树不变',
        'self.res = []': '每次查询先清空 `res`',
        'self.dfs(self.root)': '从国王开始先序遍历',
        'return self.res': '返回继承顺序 `{self.res}`',
        'if now.name not in self.death_set': lambda S, B, ret: (
            f'访问 `{S.now.name}`：没死 → 先把他排进继承顺序' if S.now.name not in S.self.death_set
            else f'访问 `{S.now.name}`：已死亡 → ==不入列，但他的后代仍要继续遍历=='),
        'self.res.append(now.name)': '`{now.name}` 加入顺序：`{self.res}`',
        'if now.child': lambda S, B, ret: (f'`{S.now.name}` 有孩子 → 先去长子 `{S.now.child.name}`（先孩子后兄弟）' if S.now.child
                                           else f'`{S.now.name}` 没有孩子，不用下探'),
        'self.dfs(now.child)': '递归进入长子 `{B.now.child.name}`',
        'if now.brother': lambda S, B, ret: (f'`{S.now.name}` 的下一个兄弟是 `{S.now.brother.name}`，孩子都排完了再轮到他' if S.now.brother
                                             else f'`{S.now.name}` 没有下一个兄弟，返回上一层'),
        'self.dfs(now.brother)': '递归进入兄弟 `{B.now.brother.name}`',
    },
    cards=dict(
        one_liner='孩子兄弟表示法：先孩子后兄弟，一遍 dfs 就是继承顺序',
        complexity='`birth` / `death` 均 `O(1)`，`getInheritanceOrder` 为 `O(n)`，空间 `O(n)`',
        problem=['设计 `ThroneInheritance`：`birth(父, 子)` 新生儿，`death(名)` 去世，`getInheritanceOrder()` 返回当前继承顺序（不含死者）',
                 '规则：有孩子先传长子，否则传兄弟',
                 '本视频：king 生 andy、bob，andy 生 matthew；查询一次，bob 去世后再查一次',
                 '结果：`[king,andy,matthew,bob]`，然后 `[king,andy,matthew]`'],
        quote='对于某个节点，其在二叉树中的左孩子为该节点在多叉树中的第一个孩子节点，而其在二叉树中的右孩子则为该节点在多叉树中的下一个兄弟节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个节点只存 `child`（长子）和 `brother`（下一个兄弟），多叉树变成二叉树',
              '再额外存 `little_child`（最小的孩子）：新孩子接到它后面，不用遍历兄弟',
              '先序 dfs 恰好是继承顺序；死者用 `death_set` 在输出时跳过，树结构不变'],
        summary=['`birth` / `death` `O(1)`，`getInheritanceOrder` `O(n)`',
                 '易错：死者要==跳过输出但继续遍历==，他的后代仍然有继承权',
                 '易错：新孩子要接在 `little_child` 后并更新它，不然顺序会乱',
                 '`node_dict` 让按名字找父亲 `O(1)`；原文无需改动即可在 Python 3 运行'],
    ),
)
