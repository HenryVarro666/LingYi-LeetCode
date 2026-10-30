import sys as _sys
import tracer as _tr


def _up(name, test, depth=16):
    # 取调用栈上层的局部变量（custom 视图只拿到合并后的 S；这里取完整帧列表与全部关键帧）
    f = _sys._getframe(2)
    for _ in range(depth):
        if f is None:
            return None
        v = f.f_locals.get(name)
        if v is not None and test(v):
            return v
        f = f.f_back
    return None


def _reach(frames, S):
    vals = [v for fr in frames for v in fr['locals'].values()] if frames else list(S.values())
    nodes = {}
    for v in vals:
        while isinstance(v, ListNode) and v._uid not in nodes:
            nodes[v._uid] = v
            v = v.next
    return nodes


def _ll(ptrs, title='链表', place=None, deco=None):
    """自绘链表：相邻节点用直箭头（反向链接走下方车道），远距离链接画在节点下方的弧线；
    指针名写在节点上方；这一步改动过的 next 用黄色；已经没有变量指向的节点画成暗色（ghost）。"""
    cache = {}

    def history():
        vid = _up('self', lambda x: hasattr(x, 'keys') and hasattr(x, 'draw_viz'))
        if vid is None:
            return []
        if id(vid) not in cache:
            order, seen = [], set()
            for stt, _, _ in vid.keys:
                S_ = stt.get('_S')
                if S_ is None or id(S_) in seen:
                    continue
                seen.add(id(S_))
                order.append((id(S_), _reach(stt.get('_frames'), S_)))
            cache[id(vid)] = order
        return cache[id(vid)]

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        st = _up('st', lambda x: isinstance(x, dict) and '_S' in x) or {}
        nodes = _reach(st.get('_frames'), S)
        hist = history()
        idx = next((i for i, (k, _) in enumerate(hist) if k == id(S)), None)
        ghost = {}
        if idx is not None:
            for j in range(idx - 1, -1, -1):
                for u, nd in hist[j][1].items():
                    if u not in nodes and u not in ghost:
                        ghost[u] = nd
        bnodes = _reach(None, B)
        if idx:
            for u, nd in hist[idx - 1][1].items():
                bnodes.setdefault(u, nd)
        alln = dict(ghost)
        alln.update(nodes)
        org = _tr._origin
        base = max([r for r, c in org.values()] + [-1]) + 1
        every = set(alln)
        for _, nd in hist:
            every |= set(nd)
        pos = {u: org[u] for u in every if u in org}
        for k, u in enumerate(sorted(u for u in every if u not in org)):
            pos[u] = place(k, base) if place else (base, k)
        allp = list(org.values()) + list(pos.values())
        R = max(r for r, c in allp) + 1
        C = max(c for r, c in allp) + 1
        gap = min(150, (x1 - x0 - 100) / C)
        nw, nh = min(84, gap * 0.58), 60
        top = y0 + 118
        rowh = min(180, (y1 - top - nh - 50) / max(1, R - 1)) if R > 1 else 0
        top = max(top, (y0 + y1) / 2 + 20 - (nh + rowh * (R - 1)) / 2)
        left = x0 + max(50, (x1 - x0 - C * gap) / 2 + (gap - nw) / 2 - 10)

        def xy(u):
            r, c = pos[u]
            return left + c * gap + nw / 2, top + nh / 2 + r * rowh

        fwd, back = set(), set()
        for u, nd in alln.items():
            r, c = pos[u]
            p2 = pos.get(getattr(nd.next, '_uid', None))
            if nd.next is None or p2 == (r, c + 1):
                fwd.add((r, c))
            elif p2 == (r, c - 1):
                back.add((r, c - 1))
        both = fwd & back
        for u, nd in alln.items():
            X, Y = xy(u)
            r, c = pos[u]
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else ((T['dim'], 2) if u in ghost else (T['muted'], 3))
            if nx is None:
                cv.text((X + nw / 2 + 8, Y - (11 if (r, c) in both else 0)), '∅', 24,
                        T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r2, c2 = pos[nx._uid]
            if r2 == r and c2 == c + 1:
                d = -11 if (r, c) in both else 0
                cv.arrow((X + nw / 2, Y + d), (X2 - nw / 2 - 2, Y2 + d), lc, lw, 12)
            elif r2 == r and c2 == c - 1:
                d = 11 if (r, c2) in both else 0
                cv.arrow((X - nw / 2, Y + d), (X2 + nw / 2 + 2, Y2 + d), lc, lw, 12)
            elif r2 == r:
                cv.arc_arrow((X, Y + nh / 2), (X2, Y2 + nh / 2 + 2), -(34 + abs(X2 - X) * 0.1), lc, lw, 12)
            else:
                if abs(X2 - X) < 1:  # 竖直箭头往右偏一点，避开节点上方的指针名
                    X, X2 = X + nw * 0.3, X2 + nw * 0.3
                dx, dy = X2 - X, Y2 - Y
                t0 = min((nw / 2) / abs(dx) if dx else 9e9, (nh / 2) / abs(dy) if dy else 9e9)
                t1 = t0 + 4 / math.hypot(dx, dy)
                cv.arrow((X + dx * t0, Y + dy * t0), (X2 - dx * t1, Y2 - dy * t1), lc, lw, 12)
        hit = {}
        for name, cc in ptrs.items():
            v = S.get(name)
            if isinstance(v, ListNode):
                hit.setdefault(v._uid, []).append((name, T[cc]))
        for u, nd in alln.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            bn = bnodes.get(u)
            vch = bn is not None and bn.val != nd.val
            gh = u in ghost
            fill = hs[0][1] if hs else ((24, 28, 35) if gh else T['panel2'])
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['yellow'] if vch else T['border'], width=4 if vch else 2)
            cv.text((X, Y), str(nd.val), 30, T['bg'] if hs else (T['dim'] if gh else T['text']), anchor='mm', bold=True)
            for k, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 6 - k * 26), name, 22, cc, anchor='mb', bold=True)
        if deco:
            deco(cv, S, alln, xy, T)
        nones = [n for n in ptrs if n in S and S[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _v(x):
    return '∅' if x is None else str(x.val)


def _chain(node):
    vals = list_vals(node)
    return ' → '.join(map(str, vals)) if vals else '空'


def _info(S):
    if 'pre' in S:
        return f"② 反转后半段：新链表 `pre` = =={_chain(S.get('pre'))}=="
    if 'slow' in S:
        return '① 快慢指针：`slow` 每次走 1 步，`fast` 每次走 2 步'
    if 'head2' in S:
        return f"③ `head` 链：{_chain(S.get('head'))}　　`head2` 链：=={_chain(S.get('head2'))}=="
    return '① 找中间节点　② 反转后半段　③ 两头同时比较'


CONFIG = dict(
    num=234, title='回文链表', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='找中间节点 + 反转后半段',
    code='''
class Solution:
    # 876. 链表的中间结点
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    # 206. 反转链表
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        mid = self.middleNode(head)
        head2 = self.reverseList(mid)
        while head2:
            if head.val != head2.val:  # 不是回文链表
                return False
            head = head.next
            head2 = head2.next
        return True
''',
    call='Solution().isPalindrome(L([1, 2, 2, 1]))',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=420, draw=_ll({'head2': 'cyan', 'head': 'orange', 'mid': 'purple', 'slow': 'blue',
                                              'fast': 'pink', 'pre': 'pink', 'cur': 'blue', 'nxt': 'green'},
                                             title='链表（黄色 = 这一步刚改的 next）')),
        dict(type='calls', h=150),
    ],
    watch=[('head', 'head', 'orange'), ('head2', 'head2', 'cyan'), 'mid', 'slow', 'fast', 'pre', 'cur'],
    captions={
        'mid = self.middleNode': '① 先找==中间节点==（876 题）：进入 `middleNode`',
        'slow = fast = head': '快慢指针都从头节点出发',
        'while fast and fast.next': lambda S, B, r: ('`fast` 还能再走两步 → 继续' if S.fast and S.fast.next else
                                                     '`fast` 走到了空节点（节点数为偶数）→ `slow` 停在中间'),
        'slow = slow.next': lambda S, B, r: f'`slow` 走 1 步 → `{_v(S.slow)}`',
        'fast = fast.next.next': lambda S, B, r: f'`fast` 走 2 步 → `{_v(S.fast)}`',
        'return slow': '偶数个节点时，`slow` 停在==正中间偏右==的节点：从它开始就是后半段',
        'head2 = self.reverseList': '② 把==中间节点到末尾==反转（206 题）：进入 `reverseList`',
        'pre, cur = None, head': '`pre = None`，`cur` 从中间节点出发',
        'while cur': lambda S, B, r: ('`cur` 不为空 → 继续头插' if S.cur else '`cur` 为空 → 后半段反转完毕'),
        'nxt = cur.next': lambda S, B, r: f'先记住下一个节点 `nxt = {_v(S.nxt)}`',
        'cur.next = pre': lambda S, B, r: (f'`{S.cur.val}.next = None`：中间节点成为反转后的末尾。'
                                           '==前半段指向它的那条边并不会断开==' if S.pre is None else
                                           f'`{S.cur.val}.next` 指向 `pre`（{S.pre.val}）：头插法'),
        'pre = cur': lambda S, B, r: f'`pre` 前进到 `{S.pre.val}`',
        'cur = nxt': lambda S, B, r: f'`cur` 前进到 `{_v(S.cur)}`',
        'return pre': lambda S, B, r: f'返回反转后的头 `{r.val}`：从它出发就是==从右往左==访问原链表',
        'while head2': lambda S, B, r: ('`head2` 不为空 → 继续比较' if S.head2 else
                                        '`head2` 走完了（==注意判断的是 head2==，`head` 链还多一个节点）'),
        'if head.val != head2.val': lambda S, B, r: f'对称位置比较：`{S.head.val}` vs `{S.head2.val}` → 相等，继续',
        'head = head.next': lambda S, B, r: f'`head` 往右走 → `{_v(S.head)}`',
        'head2 = head2.next': lambda S, B, r: f'`head2` 往右走（相当于原链表往左）→ `{_v(S.head2)}`',
        'return True': '一路都相等，没有返回 False → ==是回文链表==',
    },
    cards=dict(
        one_liner='找到中间节点，把后半段反转，再从两头同时往中间比较',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你单链表的头节点 `head`，判断它是不是==回文链表==',
                 '示例：`[1,2,2,1]` → `true`；`[1,2]` → `false`',
                 '进阶：`O(n)` 时间、`O(1)` 空间'],
        quote='然后，==把中间节点到链表末尾反转==……这样我们就能从 head2 开始，依次访问原链表的最后一个节点、倒数第二个节点、倒数第三个节点……',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['判断回文要从两头往中间比，可单链表没法从右往左走',
              '拼两道前置题：876 找中间节点（偶数个时取==正中间偏右==）+ 206 反转后半段',
              '反转后前半段末尾仍指向中间节点，所以循环条件==判断 head2 而不是 head=='],
        summary=['时间 `O(n)`，空间 `O(1)`；代码会修改输入链表',
                 '为什么不反转整个链表？前半段结构会被破坏，没法再从 `head` 往后走',
                 '写成 `while head` 会在偶数长度时多比一次，访问 `head2.val` 报空指针',
                 '灵神的另一种写法：递归，在「归」的过程中从右往左比较，空间 `O(n)`'],
    ),
)
