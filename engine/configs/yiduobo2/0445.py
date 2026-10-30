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


def _ll(ptrs, title='链表', place=None, deco=None, inner=False):
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
            v = (S.get('_inner') or {}).get(name) if inner else S.get(name)
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
        PS = (S.get('_inner') or {}) if inner else S
        nones = [n for n in ptrs if n in PS and PS[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _chain(node, limit=8):
    out, seen = [], set()
    while node is not None and node._uid not in seen and len(out) < limit:
        seen.add(node._uid)
        out.append(str(node.val))
        node = node.next
    return ' → '.join(out) if out else '空'


def _v(x):
    return 'None' if x is None else str(x.val)


def _cap_if1(S, B, ret):
    if B.now_len == B.len1:
        return f'`now_len == len1 = {B.len1}` → 这一位 `l1` 有数字 `{B.l1.val}`'
    return f'`now_len = {B.now_len} ≠ len1 = {B.len1}`：`l1` 没有这么高的位 → 不处理 l1'


def _cap_if2(S, B, ret):
    if B.now_len == B.len2:
        return f'`now_len == len2 = {B.len2}` → 这一位 `l2` 有数字 `{B.l2.val}`'
    return f'`now_len = {B.now_len} ≠ len2 = {B.len2}`：`l2` 没有这么高的位 → 不处理 l2'


def _cap_ifgt(S, B, ret):
    if S.now_len > 1:
        return f'`now_len = {S.now_len} > 1`：还没到最低位 → 先递归算第 `{S.now_len - 1}` 位，拿回结果链表和进位'
    return '`now_len = 1`：已经是最低位（个位）→ 没有低位进位'


CONFIG = dict(
    num=445, title='两数相加 II', difficulty='Medium', category='链表',
    author='yiduobo', technique='不翻转链表 · 按位数对齐递归',
    tags=['热题173'],
    code='''
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        now = l1
        len1 = 0
        while now:
            len1 += 1
            now = now.next

        now = l2
        len2 = 0
        while now:
            len2 += 1
            now = now.next

        add, res = self.dfs(max(len1, len2), l1, len1, l2, len2)
        if add:
            tmp = ListNode(1)
            tmp.next = res
            return tmp
        else:
            return res

    def dfs(self, now_len, l1, len1, l2, len2):
        val = 0
        if now_len == len1:
            val += l1.val
            len1 -= 1
            l1 = l1.next
        if now_len == len2:
            val += l2.val
            len2 -= 1
            l2 = l2.next

        if now_len > 1:
            add, res = self.dfs(now_len - 1, l1, len1, l2, len2)
        else:
            add, res = 0, None

        val += add
        tmp = ListNode(val % 10)
        tmp.next = res
        res = tmp
        return val // 10, res
''',
    setup='''
import tracer
a, b = L([9, 2, 4]), L([8, 6])
for k, nd in enumerate(tracer.Lnodes(a)):
    tracer._origin[nd._uid] = (0, 1 + k)
for k, nd in enumerate(tracer.Lnodes(b)):
    tracer._origin[nd._uid] = (1, 2 + k)
''',
    call='Solution().addTwoNumbers(a, b)',
    expect=[1, 0, 1, 0],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: '`924 + 86 = 1010`：`now_len` = 当前处理第几位（从高位往低位递归）', size=24),
        dict(type='custom', h=430, draw=_ll({'l1': 'cyan', 'l2': 'yellow', 'tmp': 'green', 'res': 'pink', 'now': 'blue'},
                                             title='上两行：l1、l2（按个位对齐）　最下行：结果（递归返回时从低位往高位生成）',
                                             place=lambda k, base: (base, 3 - k), inner=True)),
        dict(type='calls', h=170, hide=('l1', 'l2')),
    ],
    watch=[('now_len', lambda S: S['_inner'].get('now_len'), 'blue'), ('len1', lambda S: S['_inner'].get('len1'), 'cyan'),
           ('len2', lambda S: S['_inner'].get('len2'), 'yellow'), ('val', lambda S: S['_inner'].get('val'), 'green'),
           ('add', lambda S: S['_inner'].get('add'), 'orange')],
    skip=['len1 = 0', 'len2 = 0', 'while now:', 'len1 += 1', 'len2 += 1', 'now = now.next'],
    captions={
        'now = l1': '先数出两个链表的长度（数位个数）',
        'now = l2': '`len1 = {len1}`；再数 `l2`',
        'add, res = self.dfs(max(len1, len2)': '`len2 = {len2}`：答案的位数先取较大的 `{max(len1, len2)}`，从==最高位==开始递归',
        'val = 0': lambda S, B, ret: f'处理第 `{S.now_len}` 位（`len1 = {S.len1}`，`len2 = {S.len2}`）',
        'if now_len == len1': _cap_if1,
        'val += l1.val': '`val += {B.l1.val}` → `{val}`',
        'len1 -= 1': '`l1` 剩下的位数 `len1 = {len1}`',
        'l1 = l1.next': lambda S, B, ret: f'`l1` 后移 → `{_v(S.l1)}`',
        'if now_len == len2': _cap_if2,
        'val += l2.val': '`val += {B.l2.val}` → `{val}`',
        'len2 -= 1': '`l2` 剩下的位数 `len2 = {len2}`',
        'l2 = l2.next': lambda S, B, ret: f'`l2` 后移 → `{_v(S.l2)}`',
        'if now_len > 1': _cap_ifgt,
        'add, res = self.dfs(now_len - 1': lambda S, B, ret: f'递归计算第 `{S.now_len}` 位',
        'add, res = 0, None': '个位以下没有结果：`add = 0`，`res = None`',
        'val += add': lambda S, B, ret: (f'低位返回：进位 `add = {S.add}`，结果链表 `{_chain(S.res)}`；`val = {S.val}`'
                                         if S.res is not None else f'加上进位 `add = {S.add}` → `val = {S.val}`'),
        'tmp = ListNode(val % 10)': '当前位：`{val} % 10 = {val % 10}`',
        'tmp.next = res': lambda S, B, ret: (f'新的最高位 `1` 接在结果前面 → `{_chain(S.tmp)}`' if 'now_len' not in S
                                             else f'把低位的结果链表接在后面 → `{_chain(S.tmp)}`' if S.res is not None
                                             else '`res` 为空：`tmp` 是结果的最后一位（个位）'),
        'res = tmp': lambda S, B, ret: f'`res` 指向当前位：`{_chain(S.res)}`',
        'return val // 10, res': lambda S, B, ret: f'返回进位 `{S.val} // 10 = {ret[0]}` 和结果 `{_chain(ret[1])}`（原文 `/` 已改为 `//`）'
                                  if S.now_len == 1 else f'返回进位 `{ret[0]}` 和结果 `{_chain(ret[1])}`',
        'if add:': lambda S, B, ret: (f'最高位还有进位 `add = {S.add}` → 要多一位' if S.add else '最高位没有进位'),
        'tmp = ListNode(1)': '新建最高位 `1`',
        '            return tmp': lambda S, B, ret: f'返回 =={_chain(ret)}==',
        '            return res': lambda S, B, ret: f'返回 =={_chain(ret)}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='用位数对齐两个链表，递归到个位后从低往高返回进位',
        complexity='时间 `O(m+n)`，空间 `O(max(m,n))`（递归栈）',
        problem=['两个==非空==链表表示两个非负整数，==最高位在表头==，每个节点存一位',
                 '把两数相加返回和的链表；进阶：==不能翻转==输入链表',
                 '示例：`[7,2,4,3] + [5,6,4]` → `[7,8,0,7]`；本视频 `924 + 86`'],
        quote='只有当now_len与len1相等时才处理链表l1……若now_len大于零，说明还未处理到最低位，此时==递归计算now_len - 1位，获取返回的计算结果链表以及进位值==。',
        quote_src='—— yiduobo 题解',
        idea=['加法要从最低位算起，又不能翻转 → 用==递归==（或栈）',
              '`now_len`：当前答案第几位；`len1/len2`：l1、l2 还剩几位',
              '`now_len == len1` 时 l1 才出这一位，短的链表就这样自动对齐'],
        result='运行结束：返回 `[1,0,1,0]`，即 924 + 86 = 1010 ✓',
        summary=['时间 `O(m+n)`，空间 `O(max(m,n))` 递归栈',
                 '对齐的关键：按“剩余位数”判断该不该处理，而不是同时往后走',
                 '最高位的进位在主函数里补一个 `ListNode(1)`',
                 '原文为 Python 2 写法：`val / 10` 改为 `val // 10`，并删去 docstring',
                 '对比灵神：灵神直接反转链表套第 2 题；yiduobo 不翻转，用递归'],
    ),
)
