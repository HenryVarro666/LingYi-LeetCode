def _ring(head):
    out, seen, x = [], set(), head
    while x is not None and id(x) not in seen and len(out) < 8:
        seen.add(id(x))
        out.append(x)
        x = x.right
    return out


def _lists(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'head_dict：每个 freq 一条双向循环链表（head = 最近操作的，head.left = 最旧的）', 22, T['muted'], bold=True)
    hd = S.get('self.head_dict')
    if hd is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    mf = S.get('self.min_freq')
    node, head = S.get('node'), S.get('head')
    placed = set()
    rows = sorted(hd)
    bw, bh, gap = 110, 56, 70
    for r, f in enumerate(rows):
        Y = y0 + 60 + r * 120
        is_min = f == mf
        cv.text((x0 + 30, Y + bh / 2), f'freq={f}', 24, T['orange'] if is_min else T['text'], anchor='lm', bold=True, mono=True)
        if is_min:
            cv.text((x0 + 30, Y + bh / 2 + 28), 'min_freq', 18, T['orange'], anchor='lm', bold=True, mono=True)
        ring = _ring(hd[f])
        sx = x0 + 170
        for i, nd in enumerate(ring):
            placed.add(id(nd))
            X = sx + i * (bw + gap)
            c = T['blue'] if nd is node else (T['pink'] if nd is head else None)
            cv.rect((X, Y, X + bw, Y + bh), fill=c or T['panel2'], r=10, outline=T['border'], width=2)
            cv.text((X + bw / 2, Y + bh / 2), f'{nd.key}:{nd.val}', 24, T['bg'] if c else T['text'], anchor='mm', bold=True, mono=True)
            tags = []
            if i == 0:
                tags.append('head')
            if nd is hd[f].left and len(ring) > 1:
                tags.append('最旧')
            if tags:
                cv.text((X + bw / 2, Y - 4), ' / '.join(tags), 17, T['muted'], anchor='mb', bold=True)
            if i + 1 < len(ring):
                cv.arrow((X + bw + 4, Y + bh / 2 - 8), (X + bw + gap - 4, Y + bh / 2 - 8), T['muted'], 3, 10)
                if ring[i + 1].left is nd:
                    cv.arrow((X + bw + gap - 4, Y + bh / 2 + 10), (X + bw + 4, Y + bh / 2 + 10), T['dim'], 2, 9)
        if ring:
            last = ring[-1]
            Xl = sx + (len(ring) - 1) * (bw + gap) + bw
            if last.right is ring[0]:
                cv.text((Xl + 10, Y + bh / 2), '（左右都指向自己）' if len(ring) == 1 else '→ 回到 head', 20, T['dim'], anchor='lm')
    # 被抽出来、暂时不在任何链表里的 node
    for name, nd, c in (('node', node, 'blue'),):
        if nd is not None and hasattr(nd, 'key') and id(nd) not in placed:
            X, Y = x1 - 170, y0 + 50
            cv.rect((X, Y, X + bw, Y + bh), fill=T[c], r=10, outline=T['border'], width=2)
            cv.text((X + bw / 2, Y + bh / 2), f'{nd.key}:{nd.val}', 24, T['bg'], anchor='mm', bold=True, mono=True)
            cv.text((X + bw / 2, Y + bh + 6), f'{name}（已抽出）', 18, T[c], anchor='mt', bold=True)


def _cap_eq(S, B, ret):
    if S.node is S.head:
        return f'`node` 就是这条链表的 head（`{S.node.key}`）'
    return f'`node`（`{S.node.key}`）不是 head（head 是 `{S.head.key}`）→ 直接把它左右两边接起来'


def _cap_only(S, B, ret):
    if S.head.left is S.head:
        return f'head 的左边还是自己：freq={S.freq} 的链表==只有它一个== → 整条链表删掉'
    return '链表里还有别的节点'


def _cap_in(S, B, ret):
    f = S.node.freq
    if f in S['self.head_dict']:
        return f'已有 freq={f} 的链表 → 插到它的 head 左边，==成为新的 head=='
    return f'还没有 freq={f} 的链表 → 自己成环'


def _cap_min(S, B, ret):
    if S['self.min_freq'] == S.freq and S.freq not in S['self.head_dict']:
        return f'`min_freq == {S.freq}` 且 freq={S.freq} 的链表==已被删光== → `min_freq` 加一'
    if S['self.min_freq'] != S.freq:
        return f'`min_freq = {S["self.min_freq"]}` ≠ `{S.freq}` → 不变'
    return f'freq={S.freq} 的链表还在 → `min_freq` 不变'


def _cap_full(S, B, ret):
    n, cap = len(S['self.key_dict']), S['self.capacity']
    if n < cap:
        return f'`{n} < capacity = {cap}`：还放得下 → 新建节点'
    return f'已有 `{n}` 个 = capacity：要淘汰一个'


CONFIG = dict(
    num=460, title='LFU 缓存', difficulty='Hard', category='设计',
    author='yiduobo', technique='key_dict + head_dict（每个频率一条双向循环链表）',
    tags=['热题173'],
    code='''
class ListNode(object):

    def __init__(self, key, val):
        self.left = None
        self.right = None
        self.key = key
        self.val = val
        self.freq = 1

class LFUCache(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.min_freq = None
        self.key_dict = {}
        self.head_dict = {}

    def get(self, key):
        if key not in self.key_dict:
            return -1

        node = self.key_dict[key]
        freq = node.freq
        head = self.head_dict[freq]
        if node == head:
            if head.left == head:
                self.head_dict.pop(freq)
            else:
                head.left.right = head.right
                head.right.left = head.left
                self.head_dict[freq] = head.right
        else:
            node.left.right = node.right
            node.right.left = node.left

        node.freq += 1
        if node.freq in self.head_dict:
            head = self.head_dict[node.freq]
            head.left.right = node
            node.left = head.left
            node.right = head
            head.left = node
        else:
            node.left = node.right = node
        self.head_dict[node.freq] = node

        if self.min_freq == freq and freq not in self.head_dict:
            self.min_freq += 1

        return node.val

    def put(self, key, value):

        if key in self.key_dict:
            node = self.key_dict[key]
            freq = node.freq
            head = self.head_dict[freq]
            if node == head:
                if node.left == head:
                    self.head_dict.pop(freq)
                else:
                    head.left.right = head.right
                    head.right.left = head.left
                    self.head_dict[freq] = head.right
            else:
                node.left.right = node.right
                node.right.left = node.left

            node.freq += 1
            if node.freq in self.head_dict:
                head = self.head_dict[node.freq]
                head.left.right = node
                node.left = head.left
                node.right = head
                head.left = node
            else:
                node.left = node.right = node
            self.head_dict[node.freq] = node

            if self.min_freq == freq and freq not in self.head_dict:
                self.min_freq += 1

            node.val = value

        else:
            if len(self.key_dict) < self.capacity:
                node = ListNode(key, value)
            elif self.capacity > 0:
                head = self.head_dict[self.min_freq]
                node = head.left
                if node == head:
                    self.head_dict.pop(self.min_freq)
                else:
                    node.left.right = node.right
                    node.right.left = node.left
                self.key_dict.pop(node.key)

                node.key = key
                node.val = value
                node.freq = 1
            else:
                return

            if 1 not in self.head_dict:
                self.min_freq = 1
                node.left = node.right = node
            else:
                head = self.head_dict[1]
                head.left.right = node
                node.left = head.left
                node.right = head
                head.left = node
            self.head_dict[1] = node
            self.key_dict[key] = node
''',
    call='''c = LFUCache(2)
c.put(1, 1)
c.put(2, 2)
c.get(1)
c.get(2)
c.put(3, 3)
c.get(1)''',
    expect=-1,
    views=[
        dict(type='custom', draw=_lists, h=330),
        dict(type='map', var=lambda S: S.get('self.key_dict'), label='key_dict（key → 节点 key:val, freq）',
             fmt=lambda k, v: f'{k} → {v.key}:{v.val} f={v.freq}', h=100),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['key', 'value', 'freq', ('min_freq', 'self.min_freq', 'orange')],
    skip=['self.left = None', 'self.right = None', 'self.key = key', 'self.val = val', 'self.freq = 1',
          'node.val = value', 'node.freq = 1',
          29, 30, 33, 39, 40, 41, 62, 63, 66, 72, 73, 74, 94, 109, 110, 111],  # 改指针的几行只展示最后一行（指针全部接好时）
    captions={
        'self.capacity = capacity': '`LFUCache({capacity})`：容量 `{capacity}`',
        'self.min_freq = None': '`min_freq`：当前最小的频率',
        'self.key_dict = {}': '`key_dict`：key → 链表节点',
        'self.head_dict = {}': '`head_dict`：freq → 这条链表的==头部节点==（最近操作过的）',
        'if key not in self.key_dict': lambda S, B, ret: (f'==get({S.key})==：`{S.key}` 不在缓存里' if S.key not in S['self.key_dict']
                                                         else f'==get({S.key})==：`{S.key}` 在缓存里'),
        'return -1': '返回 `-1`',
        'node = self.key_dict[key]': '通过 key_dict 找到节点 `{node.key}:{node.val}`',
        'freq = node.freq': '它的频率 `freq = {freq}`；先把它从 freq={freq} 的链表里==删掉==',
        'head = self.head_dict[freq]': '这条链表的 head 是 `{head.key}`',
        'if node == head': _cap_eq,
        'if head.left == head': _cap_only,
        'if node.left == head': _cap_only,
        'self.head_dict.pop(freq)': '`head_dict.pop({freq})`：freq={freq} 的链表没了',
        'self.head_dict[freq] = head.right': '把 head 的左右邻居接起来（head 被抽出），`head.right` 成为新 head',
        'node.right.left = node.left': '`node` 的左右邻居直接相连：`node` 被抽出',
        'node.freq += 1': '频率 +1 → `{node.freq}`，插入 freq={node.freq} 的链表',
        'if node.freq in self.head_dict': _cap_in,
        'head = self.head_dict[node.freq]': '那条链表的 head 是 `{head.key}`',
        'head.left = node': '插在 head 的左边（循环链表的“末尾”），四根指针接好',
        'node.left = node.right = node': '`node` 左右都指向自己，自成一个环',
        'self.head_dict[node.freq] = node': '`head_dict[{node.freq}] = node`：最新操作的节点做 head',
        'if self.min_freq == freq': _cap_min,
        'self.min_freq += 1': '`min_freq` → {self.min_freq}',
        'return node.val': '返回 `{ret}`',
        'if key in self.key_dict': lambda S, B, ret: (f'==put({S.key}, {S.value})==：key 已存在 → 和 get 一样升频' if S.key in S['self.key_dict']
                                                     else f'==put({S.key}, {S.value})==：新 key'),
        'if len(self.key_dict) < self.capacity': _cap_full,
        'node = ListNode(key, value)': '新建节点 `{key}:{value}`，freq = 1',
        'head = self.head_dict[self.min_freq]': '找 min_freq={self.min_freq} 那条链表，head 是 `{head.key}`',
        'node = head.left': '`head.left` 就是这条链表里==最久没操作的== `{node.key}` → 淘汰它',
        'elif self.capacity > 0': '容量大于 0 → 淘汰==最小频率==链表里最旧的节点',
        'self.head_dict.pop(self.min_freq)': '链表只剩它 → 整条删掉',
        'self.key_dict.pop(node.key)': 'key_dict 删掉旧 key',
        'node.key = key': '==节点复用==：直接改成新的 key、val、freq = 1',
        'if 1 not in self.head_dict': lambda S, B, ret: ('没有 freq=1 的链表 → 新节点自成一环，`min_freq = 1`' if 1 not in S['self.head_dict']
                                                        else '已有 freq=1 的链表 → 插到它的 head 左边'),
        'self.min_freq = 1': '新插入的节点频率一定是 1 → `min_freq = 1`',
        'head = self.head_dict[1]': 'freq=1 链表的 head 是 `{head.key}`',
        'self.head_dict[1] = node': '`head_dict[1] = node`：新节点成为 freq=1 的 head',
        'self.key_dict[key] = node': 'key_dict 记下 `{key}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='每个频率一条双向循环链表，淘汰最小频率链表里最久没用的',
        complexity='`get` / `put` 均 `O(1)`，空间 `O(capacity)`',
        problem=['实现 `LFUCache(capacity)`、`get(key)`、`put(key, value)`，都要 `O(1)`',
                 '满了再插入新 key：淘汰==使用次数最少==的；次数相同淘汰==最久未使用==的',
                 '`get` / `put` 已有的 key 都会让它的使用次数 +1'],
        quote='这一题的删除操作必然是插入操作引发的，而在删除频率最小的节点之后，新插入的节点频率必然为1，即此时的最小频率必然是1，因此……使用一个min_freq来储存当前最小的频率值。',
        quote_src='—— yiduobo 题解',
        idea=['`key_dict`：key → 节点；`head_dict`：freq → 那条链表的 head（最近操作的）',
              '升频：从 freq 链表删除（分 3 种情况），插到 freq+1 链表 head 的左边并成为新 head',
              '淘汰：min_freq 链表的 `head.left`（最旧的）；之后 `min_freq` 必为 1'],
        result='`get(1)` 返回 `-1`：1、2 频率都是 2，1 更久没用 → 放 3 时被淘汰',
        summary=['`get` / `put` 均 `O(1)`',
                 '易错：删除节点要分“不是 head / 是唯一节点 / 是 head 但还有别人”三种情况',
                 '易错：只有 freq 链表被删光且 `min_freq == freq` 时才 `min_freq += 1`',
                 '原文为 Python 2 风格：删去了 docstring 和 LeetCode 模板注释，代码未改',
                 '对比灵神：灵神用 `OrderedDict` 代替手写链表，代码短得多'],
    ),
)
