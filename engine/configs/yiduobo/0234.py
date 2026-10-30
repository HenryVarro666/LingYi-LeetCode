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
    if 'first' in S:
        return f"整条链表：{_chain(S.get('head'))}　　③ `first` 从表头、`second` 从中心之后同时走"
    if 'prev' in S:
        return '② 翻转中心之后的部分'
    if 'fast' in S:
        return '① 从假头出发做快慢指针：`slow` 走 1 步，`fast` 走 2 步'
    return '① 找中心　② 翻转后半部分　③ 扫描比较'


CONFIG = dict(
    num=234, title='回文链表', difficulty='Easy', category='链表',
    author='yiduobo', technique='假头 + 快慢指针找中心 + 翻转后半部分',
    code='''
class Solution(object):
    def isPalindrome(self, head):
        if not head or not head.next:
            return True

        p_head = ListNode(0)
        p_head.next = head
        fast = slow = p_head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        if fast.next:
            slow = slow.next

        prev = slow.next
        now = prev.next
        prev.next = None

        while now:
            tmp = now.next
            now.next = prev
            prev = now
            now = tmp

        slow.next = prev

        first = head
        second = slow.next
        while second:
            if second.val != first.val:
                return False
            first = first.next
            second = second.next

        return True
''',
    setup='''
import tracer
head = L([1, 2, 3, 2, 1])
for nd in tracer.Lnodes(head):
    r, c = tracer._origin[nd._uid]
    tracer._origin[nd._uid] = (r, c + 1)
''',
    call='Solution().isPalindrome(head)',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=480, draw=_ll({'first': 'orange', 'second': 'cyan', 'slow': 'blue', 'fast': 'pink',
                                              'prev': 'green', 'now': 'orange', 'tmp': 'cyan', 'p_head': 'purple'},
                                             title='链表（最左是假头 p_head；黄色 = 刚改的 next）', place=lambda k, base: (0, k))),
    ],
    watch=['slow', 'fast', 'prev', 'now', 'tmp', 'first', 'second'],
    captions={
        3: '空链表或只有一个节点，一定是回文',
        6: '依照惯例，加一个==假头== `p_head` 接在 head 前面，方便操作',
        7: '`p_head.next = head`',
        8: '`fast`、`slow` 都从假头出发',
        9: lambda S, B, r: ('`fast` 后面还有两个节点 → 继续' if S.fast.next and S.fast.next.next else
                            f'`fast` 后面不足两个节点 → 停。`slow` 停在第 `len/2` 个节点（{S.slow.val}）'),
        10: lambda S, B, r: f'`slow` 走 1 步 → `{S.slow.val}`',
        11: lambda S, B, r: f'`fast` 走 2 步 → `{S.fast.val}`',
        13: lambda S, B, r: ('`fast` 后面还有节点 → 长度是==奇数==，中心是 `slow` 的下一个' if S.fast.next else
                             '`fast` 后面没有节点 → 长度是偶数，`slow` 就是中心'),
        14: lambda S, B, r: f'`slow` 后移一位，停在==中心节点== `{S.slow.val}`',
        16: lambda S, B, r: f'从中心之后开始翻转：`prev` = 中心后的第一个节点 `{S.prev.val}`',
        17: lambda S, B, r: f'`now = prev.next` → `{_v(S.now)}`',
        18: '`prev.next = None`：它将成为翻转后的末尾',
        20: lambda S, B, r: ('`now` 不为空 → 继续翻转' if S.now else '`now` 为空 → 翻转完毕，`prev` 是翻转后的头'),
        21: lambda S, B, r: f'先用 `tmp` 存下 `now.next`（{_v(S.tmp)}）',
        22: lambda S, B, r: f'`{S.now.val}.next = prev`：反过来指向 `prev`（{S.prev.val}）',
        23: lambda S, B, r: f'`prev` 前进到 `{S.prev.val}`',
        24: lambda S, B, r: f'`now` 前进到 `{_v(S.now)}`',
        26: lambda S, B, r: f'`slow.next = prev`：翻转后的部分==接回中心后面== → {_chain(S.head)}',
        28: '`first` 从表头出发',
        29: lambda S, B, r: f'`second` 从中心的下一个出发（`{S.second.val}`，就是原来的最后一个节点）',
        30: lambda S, B, r: ('`second` 不为空 → 继续比较' if S.second else '`second` 走完了，没有发现不同'),
        31: lambda S, B, r: f'比较 `second.val`（{S.second.val}）和 `first.val`（{S.first.val}）→ 相等',
        33: lambda S, B, r: f'`first` → `{_v(S.first)}`',
        34: lambda S, B, r: f'`second` → `{_v(S.second)}`',
        36: '逐个比较全部相等 → ==是回文链表==',
    },
    cards=dict(
        one_liner='加假头找中心，翻转中心之后的部分，再从表头和中心之后逐个比较',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你单链表的头节点 `head`，判断它是不是==回文链表==',
                 '示例：`[1,2,3,2,1]` → `true`；`[1,2]` → `false`',
                 '进阶：`O(n)` 时间、`O(1)` 空间'],
        quote='若链表是回文链表，那么其中心一定位于正中间的节点……一个自然的想法就是==将链表的后半部分反序==，然后从p_head和中心节点开始往后遍历逐个判断。',
        quote_src='—— yiduobo 题解',
        idea=['从假头出发做快慢指针，`slow` 自然停在第 `len/2` 个节点',
              '`fast` 后面还有节点 → 长度是奇数，`slow` 再后移一位作为中心',
              '翻转中心之后的部分并接回：`A→B→C→D→E→A→B→C→D`，一趟扫描比较'],
        summary=['时间 `O(n)`，空间 `O(1)`；三个循环：找中心、翻转后半部分、扫描比较',
                 '奇偶要分开处理：偶数时中心取在 `len/2`，奇数时再后移一位',
                 '翻转前先 `prev.next = None` 断开，否则翻转后成环',
                 '会修改原链表结构',
                 '原文为 Python 2 风格：只删掉类型注释文档字符串，其余原样'],
    ),
)
