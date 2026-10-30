def _bounds(S):
    mx, mn = S.get('self.maxBound'), S.get('self.minBound')
    return mx, mn


def _cols(S):
    """从 maxBound 沿 right 走到 minBound，返回 [(head, [同列其余节点…])]"""
    mx, mn = _bounds(S)
    if mx is None:
        return None, None, []
    cols, x, seen = [], mx.right, set()
    while x is not None and x is not mn and id(x) not in seen and len(cols) < 6:
        seen.add(id(x))
        col, y = [x], x.down
        while y is not None and y is not x and id(y) not in seen and len(col) < 6:
            seen.add(id(y))
            col.append(y)
            y = y.down
        cols.append(col)
        x = x.right
    return mx, mn, cols


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '横向：不同次数的“表头”（次数从大到小）；竖向：次数相同的 key', 22, T['muted'], bold=True)
    mx, mn, cols = _cols(S)
    if mx is None:
        return
    n = len(cols) + 2
    cw = min(150, (x1 - x0 - 60) / max(n, 1))
    bw, bh = min(84, cw * 0.66), 46
    sx = x0 + 40
    ys = y0 + 110
    gap = 80
    P = {}
    P[id(mx)] = (sx + bw / 2, ys)
    for i, col in enumerate(cols):
        for j, nd in enumerate(col):
            P[id(nd)] = (sx + (i + 1) * cw + bw / 2, ys + j * gap)
    P[id(mn)] = (sx + (len(cols) + 1) * cw + bw / 2, ys)
    heads = [c[0] for c in cols]
    chain = [mx] + heads + [mn]
    for a, b in zip(chain, chain[1:]):
        (ax, ay), (bx, by) = P[id(a)], P[id(b)]
        cv.arrow((ax + bw / 2 + 2, ay), (bx - bw / 2 - 3, by), T['muted'], 3, 10)
    for col in cols:
        for a, b in zip(col, col[1:]):
            (ax, ay), (bx, by) = P[id(a)], P[id(b)]
            cv.line([(ax, ay + bh / 2), (bx, by - bh / 2)], T['dim'], 3)
    names = {'node': ('node', T['blue']), 'head': ('head', T['cyan']), 'left': ('left', T['pink']),
             'right': ('right', T['purple']), 'tmp': ('tmp', T['green'])}
    tags = {}
    for k, (lab, c) in names.items():
        v = S.get(k)
        if v is not None and id(v) in P:
            tags.setdefault(id(v), []).append((lab, c))
    for nd_id, (cx, cy) in P.items():
        pass
    allnodes = [(mx, 'max', True), (mn, 'min', True)] + [(nd, None, False) for col in cols for nd in col]
    for nd, lab, bound in allnodes:
        cx, cy = P[id(nd)]
        fill = T['panel2']
        if bound:
            cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), outline=T['border'], r=9)
            cv.text((cx, cy), lab + 'Bound', 18, T['dim'], anchor='mm', mono=True)
        else:
            tg = tags.get(id(nd), [])
            if any(l == 'node' for l, _ in tg):
                fill = (40, 70, 120)
            cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=fill, outline=T['border'], r=9)
            cv.text((cx, cy), f'{nd.key}', 26, T['text'], anchor='mm', bold=True, mono=True)
            if nd is nd.up and nd is nd.down or nd in [c[0] for c in cols]:
                pass
        # 指针标签
        tg2 = tags.get(id(nd), [])
        wtot = sum(cv.tlen(l, 20, True) + 8 for l, _ in tg2)
        px = cx - wtot / 2
        for lab, c in tg2:
            cv.text((px, cy + bh / 2 + 3), lab, 20, c, anchor='lt', bold=True)
            px += cv.tlen(lab, 20, True) + 8
    for col in cols:
        h = col[0]
        cx, cy = P[id(h)]
        cv.text((cx, cy - bh / 2 - 8), f'次数 {h.val}', 22, T['orange'], anchor='mb', bold=True)
    # 手上还没接进去的节点
    nd = S.get('node')
    if nd is not None and id(nd) not in P:
        cx, cy = x1 - 90, y0 + 90
        cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=(40, 70, 120), outline=T['blue'], width=3, r=9)
        cv.text((cx, cy), f'{nd.key}', 26, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((cx, cy - bh / 2 - 8), f'次数 {nd.val}（未接入）', 20, T['blue'], anchor='mb', bold=True)


def _op(S):
    k = S.get('key')
    if k is None:
        return ''
    return f'当前操作的 key = `{k}`'


CONFIG = dict(
    num=432, title='全 O(1) 的数据结构', difficulty='Hard', category='设计',
    author='yiduobo', technique='双向链表 + 竖向链表 · 十字链表',
    tags=['常用数据结构', '链表树与回溯'],
    code='''
class ListNode(object):

    def __init__(self, key, val=1):
        self.left = self.right = self.up = self.down = None
        self.key = key
        self.val = val

class AllOne(object):

    def __init__(self):
        self.key_dict = {}
        self.head_dict = {}
        self.maxBound = ListNode("", -1)
        self.minBound = ListNode("", -1)
        self.maxBound.right = self.minBound
        self.minBound.left = self.maxBound

    def inc(self, key):
        if key not in self.key_dict:
            node = ListNode(key)
            self.key_dict[key] = node
            tmp = self.minBound.left
            if 1 not in self.head_dict:
                self.head_dict[1] = node
                tmp.right = node
                node.left = tmp
                node.right = self.minBound
                self.minBound.left = node
                node.up = node.down = node
            else:
                tmp.up.down = node
                node.up = tmp.up
                tmp.up = node
                node.down = tmp
        else:
            node = self.key_dict[key]
            head = self.head_dict[node.val]
            left = head.left
            right = head.right
            if head == node:
                if head.down == head:
                    self.head_dict.pop(node.val)
                    left.right = right
                    right.left = left
                else:
                    self.head_dict[node.val] = head.down
                    head.up.down = head.down
                    head.down.up = head.up
                    left.right = head.down
                    right.left = head.down
                    head.down.left = left
                    head.down.right = right
            else:
                node.up.down = node.down
                node.down.up = node.up

            node.val += 1

            if left.val == node.val:
                left.up.down = node
                node.up = left.up
                left.up = node
                node.down = left
                node.left = node.right = None
            else:
                left.right = node
                node.left = left
                if right.left == left:
                    right.left = node
                    node.right = right
                else:
                    right.left.left = node
                    node.right = right.left
                node.up = node.down = node
                self.head_dict[node.val] = node

    def dec(self, key):
        if key not in self.key_dict:
            return

        node = self.key_dict[key]
        head = self.head_dict[node.val]
        left = head.left
        right = head.right
        if node == head:
            if head.down == head:
                self.head_dict.pop(node.val)
                left.right = right
                right.left = left
            else:
                self.head_dict[node.val] = head.down
                head.up.down = head.down
                head.down.up = head.up
                left.right = head.down
                right.left = head.down
                head.down.left = left
                head.down.right = right
        else:
            node.up.down = node.down
            node.down.up = node.up
        
        node.val -= 1
        if node.val == 0:
            self.key_dict.pop(key)
            return
        if right.val == node.val:
            right.up.down = node
            node.up = right.up
            right.up = node
            node.down = right
            node.left = node.right = None
        else:
            right.left = node
            node.right = right
            if left.right == right:
                left.right = node
                node.left = left
            else:
                left.right.right = node
                node.left = left.right
            node.up = node.down = node
            self.head_dict[node.val] = node

    def getMaxKey(self):
        return self.maxBound.right.key

    def getMinKey(self):
        return self.minBound.left.key
''',
    call="""c = AllOne()
res = []
c.inc('a')
c.inc('b')
c.inc('a')
res.append(c.getMaxKey())
c.dec('a')
res.append(c.getMinKey())
res""",
    expect=['a', 'b'],
    views=[
        dict(type='text', fn=_op, size=24),
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var=lambda S: S.get('self.head_dict', {}), label='head_dict：次数 → 该次数这一列的表头', h=110,
             fmt=lambda k, v: f'{k} → {v.key}'),
        dict(type='map', var=lambda S: S.get('self.key_dict', {}), label='key_dict：key → 节点（节点里存 val）', h=110,
             fmt=lambda k, v: f'{k} → {v.key}:{v.val}'),
    ],
    watch=['key', ('node', 'node.val', 'blue')],
    skip=['self.key = key', 'self.val = val', 'self.left = self.right', 'self.minBound = ListNode', 'self.maxBound = ListNode',
          'tmp.right = node', 'node.left = tmp', 'self.minBound.left = node', 'node.up = tmp.up', 'tmp.up = node',
          'head.up.down = head.down', 'head.down.up = head.up', 'head.down.left = left', 'head.down.right = right',
          'node.up = left.up', 'left.up = node', 'node.up = right.up', 'right.up = node', 'node.left = left',
          'node.right = right', 'node.left = node.right = None', 'left.right.right = node', 'node.left = left.right',
          'right.left = node', 'left.right = node', 'self.key_dict[key] = node', 'right.left.left = node', 'node.down.up = node.up',
          'node.up = node.down = node', 'left = head.left', 'right = head.right'],
    max_steps=110,
    captions={
        'self.key_dict = {}': '`key_dict[key]`：直接拿到 key 对应的节点，`O(1)`',
        'self.head_dict = {}': '`head_dict[次数]`：这个次数那一列的表头节点',
        'self.maxBound.right = self.minBound': '两个边界哨兵：`maxBound` 在最左、`minBound` 在最右，次数从大到小排',
        'self.minBound.left = self.maxBound': '于是 `maxBound.right` 永远是最大次数，`minBound.left` 永远是最小次数',
        19: lambda S, B, r: (f'`{S.key}` 不在 `key_dict` → 新 key，次数从 1 开始' if S.key not in B.get('self.key_dict', {}) else f'`{S.key}` 已经存在 → 次数 +1，要换一列'),
        78: lambda S, B, r: ('`{}` 不存在 → 什么也不做，直接返回'.format(S.key) if S.key not in B.get('self.key_dict', {}) else '`{}` 存在 → 次数 -1，要换一列'.format(S.key)),
        'node = ListNode(key)': '新建节点 `{key}`，次数默认是 1',
        'tmp = self.minBound.left': '`tmp`：最右边那一列的表头（次数最小）',
        'if 1 not in self.head_dict': lambda S, B, r: ('`head_dict` 里没有次数 1 的列 → 要新开一列，插在 `minBound` 左边' if 1 not in B['self.head_dict'] else '已有次数 1 的这一列 → 把新节点挂在这一列下面'),
        'self.head_dict[1] = node': '新列的表头就是 `{key}`，登记到 `head_dict[1]`',
        'node.right = self.minBound': '`{key}` 接到 `minBound` 左边：新列建好',
        'node.up = node.down = node': '这一列只有自己，上下都指向自己（竖向是个环）',
        'tmp.up.down = node': '新节点要挂到这一列最后：`tmp.up` 是这一列的最后一个，它的 `down` 先指向新节点',
        'left.right = head.down': '横向链表：左邻居列的 `right` 改指新表头 `{head.down.key}`',
        'right.left = left': '右邻居的 `left` 指回 `left`：这一列已从横向链表中摘掉',
        'right.up.down = node': '`right` 是次数相同的那一列的表头：它的最后一个节点的 `down` 先指向 `{key}`',
        'node.down = right': '`{key}` 接到这一列最后，竖向环回到表头：放置完成',
        'node.down = tmp': '`tmp` 是次数 1 的表头：新节点接到这一列最后（上下指针一起改），竖向环回到表头',
        'node = self.key_dict[key]': '已存在：取出 `{key}` 的节点（现在次数 {node.val}）',
        'head = self.head_dict[node.val]': '找到它所在列的表头 `{head.key}`',
        'left = head.left': '`left` / `right`：这一列左右两边的邻居列，等会儿用来判断要放哪',
        'if head == node': lambda S, B, r: ('`{}` 就是表头 → 要把表头位置交给别人，或整列删除'.format(S.node.key) if S.head == S.node else '`{}` 不是表头 → 直接从竖向链表摘掉就行'.format(S.node.key)),
        'if head.down == head': lambda S, B, r: ('`head.down == head`：这列只剩它一个 → 整列删除' if S.head.down == S.head else '这列还有别人 → 让下一个节点接任表头'),
        'self.head_dict.pop(node.val)': '这列空了，从 `head_dict` 里删除次数 `{node.val}`',
        'left.right = right': '左右邻居列直接相连：这一列从横向链表中消失',
        'self.head_dict[node.val] = head.down': '`head.down` 接任表头：竖向、横向指针都改成它，`head_dict` 同步更新',
        'right.left = head.down': '横向链表上，新表头顶替原表头的位置',
        'node.up.down = node.down': '非表头：把 `up` 和 `down` 接起来，把自己摘出这一列',
        'node.val += 1': '`{key}` 的次数 → ==`{node.val}`==，接下来要放进次数 {node.val} 的那一列',
        'if left.val == node.val': lambda S, B, r: (f'左边邻居列的次数 `{S.left.val}` == `{S.node.val}` → 挂到它下面' if S.left.val == S.node.val else f'左边邻居列次数 `{S.left.val}` != `{S.node.val}` → 没有这个次数的列，要新开一列'),
        'left.up.down = node': '挂到左边列的竖向链表末尾（节点的 `up` / `down` 指针一起接好）',
        'node.down = left': '竖向环接好，新节点成为这一列的最后一个',
        'left.right = node': '新开一列：左邻居列的 `right` 指向新节点，`node.left` 指回去',
        'if right.left == left': lambda S, B, r: ('`right.left == left`：原来那列已经没人了，新列直接夹在 `left` 和 `right` 之间' if S.right.left == S.left else '原来那列还在 → 新列夹在 `left` 和原来那列之间'),
        'self.head_dict[node.val] = node': '新列的表头登记：`head_dict[{node.val}] = {key}`',
        'if node == head': lambda S, B, r: ('`{}` 是表头 → 先把表头交出去或删列'.format(S.node.key) if S.node == S.head else '`{}` 不是表头 → 直接摘出竖向链表'.format(S.node.key)),
        'node.val -= 1': '`{key}` 的次数 → ==`{node.val}`==，要放进右边（次数更小）的列',
        'if node.val == 0': lambda S, B, r: ('次数减到 0 → 从 `key_dict` 删掉，结束' if S.node.val == 0 else '次数还没到 0，要放回数据结构'),
        'if right.val == node.val': lambda S, B, r: (f'右边邻居列的次数 `{S.right.val}` == `{S.node.val}` → 挂到它下面' if S.right.val == S.node.val else f'右边邻居列次数 `{S.right.val}` != `{S.node.val}` → 没有这个次数的列，要新开一列'),
        'return self.maxBound.right.key': '最大次数那一列的表头 → `{ret}`',
        'return self.minBound.left.key': '最小次数那一列的表头 → `{ret}`',
    },
    cards=dict(
        one_liner='横向链表按次数排序，竖向链表串起同次数的 key：改一次只动相邻的列',
        complexity='`inc / dec / getMaxKey / getMinKey` 都是 `O(1)`',
        problem=['设计 `AllOne`：`inc(key)` 次数 +1，`dec(key)` 次数 -1（减到 0 就移除）',
                 '`getMaxKey()` / `getMinKey()` 返回次数最大 / 最小的任意一个 key',
                 '四个操作都要 `O(1)`'],
        quote='注意到这里weight的变化幅度只有1，这意味着相邻的操作，于是很自然就会联想到链表。那么此时的做法就是，维护一个双向链表，初始为两个端点maxBound以及minBound。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表 `key_dict` 找节点、`head_dict` 找“某次数那一列”的表头',
              '横向双向链表从大到小排各列；相同次数的 key 挂在同一列下面，竖向也是环',
              '`inc` / `dec` 只改变 1 次：把节点从原列摘出，放进左邻 / 右邻列，或新开一列',
              '最大 / 最小：直接看 `maxBound.right` / `minBound.left`'],
        summary=['四个操作都是 `O(1)`，空间 `O(n)`',
                 '易错：摘出表头时要让 `head.down` 接任，并同步 `head_dict`',
                 '易错：新开一列时右侧邻居可能是 `head.right`，也可能是接任的新表头，要判断 `right.left == left`',
                 '原文每个方法带 `:type / :rtype` 文档字符串，视频里已删去；代码其余未改动'],
    ),
)
