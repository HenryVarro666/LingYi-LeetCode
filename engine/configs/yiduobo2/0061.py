import math
import tracer
import views as V


def _nodes(S):
    return V._all_nodes({k: v for k, v in S.items() if not k.startswith('_')})


def ring_view(cv, S, B, box, T):
    """把链表节点按原始顺序摆在一个圆上：首尾相连后就是 yiduobo 说的“环”"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '把链表摆成一圈（黄色箭头 = 这一步刚改的 next）', 24, T['muted'], bold=True)
    nodes = _nodes(S)
    bnodes = _nodes(B)
    if not nodes:
        return
    n = len(tracer._origin)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 40
    R = min((x1 - x0) / 2 - 120, (y1 - y0) / 2 - 100)
    rad = 34

    def P(u):
        c = tracer._origin[u][1]
        a = -math.pi / 2 + 2 * math.pi * c / n
        return cx + R * math.cos(a), cy + R * math.sin(a), a

    cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(40, 46, 54), width=2)
    for u, nd in nodes.items():
        X, Y, a = P(u)
        bn = bnodes.get(u)
        changed = bn is not None and getattr(bn.next, '_uid', None) != getattr(nd.next, '_uid', None)
        c = T['yellow'] if changed else T['muted']
        if nd.next is None:
            cv.text((X + (rad + 26) * math.cos(a + 1.0), Y + (rad + 26) * math.sin(a + 1.0)), '∅', 28,
                    T['yellow'] if changed else T['dim'], anchor='mm')
            continue
        X2, Y2, _ = P(nd.next._uid)
        d = math.hypot(X2 - X, Y2 - Y)
        ux, uy = (X2 - X) / d, (Y2 - Y) / d
        cv.arrow((X + ux * rad, Y + uy * rad), (X2 - ux * (rad + 4), Y2 - uy * (rad + 4)), c, 5 if changed else 3, 16)
    ptrs = [('head', 'green'), ('now', 'blue')]
    hit = {}
    for name, cc in ptrs:
        v = S.get(name)
        if isinstance(v, tracer.ListNode):
            hit.setdefault(v._uid, []).append((name, T[cc]))
    for u, nd in nodes.items():
        X, Y, a = P(u)
        hs = hit.get(u, [])
        fill = hs[0][1] if hs else T['panel2']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), str(nd.val), 30, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for k, (name, cc) in enumerate(hs):
            lx = X + (rad + 40 + k * 30) * math.cos(a)
            ly = Y + (rad + 30 + k * 30) * math.sin(a)
            cv.text((lx, ly), name, 24, cc, anchor='mm', bold=True)


def _chain(node, limit=8):
    vals, seen = [], set()
    while node is not None and node._uid not in seen and len(vals) < limit:
        seen.add(node._uid)
        vals.append(str(node.val))
        node = node.next
    s = ' → '.join(vals)
    if node is not None:
        s += ' → …（成环）'
    return s


def _info(S):
    line = S['_line']
    if line <= 13:
        return '第一遍：数长度 `l`，`now` 停在尾巴上'
    if line <= 17:
        return '链表成环后，旋转一次 = 头往==前==挪一位；单向链表只能往后走 → 往后挪 `l - k%l` 位'
    if line <= 21:
        return f"`now` 从头往后走 `k - 1` 步（这里的 `k` 已经变成 `l - k%l`）"
    return f"新链表：=={_chain(S['head'])}=="


def _while(S, B, ret):
    if B.now.next is not None:
        return f'`now = {B.now.val}` 后面还有节点 → 继续数'
    return f'`now = {B.now.val}` 是尾巴，链表长 `l = {S.l}`'


def _loop(S, B, ret):
    if 'index' in S and S.get('index') != B.get('index'):
        return f'第 `{S.index + 1}` 步（共 `k - 1 = {S.k - 1}` 步）'
    return f'走完了：`now = {S.now.val}` 是==新的尾巴=='


CONFIG = dict(
    num=61, title='旋转链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='连成环 · 头往后挪 l - k%l 位',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def rotateRight(self, head, k):
        if not head:
            return None

        if not head.next:
            return head

        now = head
        l = 1
        while now.next:
            now = now.next
            l += 1
        now.next = head

        k %= l
        k = l - k
        now = head
        for index in range(k - 1):
            now = now.next
        head = now.next
        now.next = None
        return head
''',
    call='Solution().rotateRight(L([0, 1, 2]), 4)',
    expect=[2, 0, 1],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='custom', h=470, draw=ring_view),
        dict(type='text', fn=lambda S: f"从 `head` 出发读一圈：`{_chain(S['head'])}`" if S.get('head') else '', size=26, h=60),
    ],
    watch=[('k', 'k', 'yellow'), ('l', 'l', 'cyan'), ('now', 'now.val', 'blue'), ('head', 'head.val', 'green')],
    captions={
        'if not head:': '链表非空',
        'if not head.next': '不止一个节点（只有一个节点时怎么转都一样，直接返回）',
        'now = head': lambda S, B, r: ('第二遍：`now` 回到头部，准备往后挪' if S._line == 18 else '`now` 从头出发，`l = 1` 先算上头节点'),
        'while now.next': _while,
        'now = now.next': lambda S, B, r: (f'`now` 往后走到 `{S.now.val}`' if S._line == 20 else f'`now` 走到 `{S.now.val}`'),
        'l += 1': '长度 `l = {l}`',
        'now.next = head': '尾巴 `{now.val}` 的 next 指回头 `{head.val}`：==把链表当成一个环==',
        'k %= l': '样例 2 说明：转 `l` 次等于没转 → `k = {B.k} % {l} = =={k}==',
        'k = l - k': '头往前挪 `{B.k}` 位 = 往后挪 `l - k = {l} - {B.k} = =={k}==` 位',
        'for index in range(k - 1)': _loop,
        'head = now.next': '新尾巴的下一个就是==新的头部==：`head = {head.val}`',
        'now.next = None': '把新尾巴 `{now.val}` 和新头 `{head.val}` ==断开==，环变回链',
        'return head': lambda S, B, r: f'返回新头 → =={_chain(r)}==',
    },
    skip=['l = 1'],
    cards=dict(
        one_liner='把链表连成环，旋转就是把头往后挪 l - k%l 位，再剪开',
        complexity='时间 `O(l)`，空间 `O(1)`',
        problem=['给你链表头节点 `head`，把链表每个节点==向右移动 `k` 个位置==',
                 '示例 1：`head = [1,2,3,4,5], k = 2` → `[4,5,1,2,3]`',
                 '示例 2：`head = [0,1,2], k = 4` → `[2,0,1]`（本视频）'],
        quote='不妨将链表尾部的next指向链表头部，将链表当做一个环，那么==一次操作就意味着将链表的头部往前移动了一位==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['样例 2：长度为 `l` 的链表转 `l` 次==无事发生== → 只需转 `k % l` 次',
              '单向链表不能往前走，等价地==往后移动 `l - k%l` 个位置==找新头',
              '找到新头后，把新尾巴和新头断开'],
        result='返回 `[2,0,1]` ✓ 与示例 2 一致',
        summary=['时间 `O(l)`：一遍数长度连成环，一遍找新头；空间 `O(1)`',
                 '`k % l == 0` 时 `k` 变成 `l`，走 `l-1` 步回到原尾巴，断开后链表不变',
                 '空链表、单节点要先特判（否则 `k %= l` 前就要访问 `head.next`）',
                 '原文为 Python 2 风格：删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
