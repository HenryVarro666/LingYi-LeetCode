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


def _chain(node, limit=8):
    out, seen = [], set()
    while node is not None and node._uid not in seen and len(out) < limit:
        seen.add(node._uid)
        out.append(str(node.val))
        node = node.next
    return ' → '.join(out) if out else '空'


def _upto(node, end):
    out, seen = [], set()
    while node is not None and node._uid not in seen:
        seen.add(node._uid)
        out.append(str(node.val))
        if node is end:
            break
        node = node.next
    return ' → '.join(out)


def _lists(S):
    if 'now_even' not in S:
        return '奇数位置在上排，偶数位置在下排'
    if S['now_odd'].next is S.get('even'):
        return f"结果：=={_chain(S['odd'])}=="
    return f"已连好的奇链：=={_upto(S['odd'], S['now_odd'])}==　　偶链：=={_upto(S['even'], S['now_even'])}=="


def _v(x):
    return 'None' if x is None else str(x.val)


CONFIG = dict(
    num=328, title='奇偶链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='奇偶两条链交替穿针 · 最后拼接',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def oddEvenList(self, head):
        if not head or not head.next or not head.next.next:
            return head

        odd = head
        even = head.next

        now_odd = odd
        now_even = even
        while now_even.next:
            now_odd.next = now_even.next
            now_odd = now_odd.next
            now_even.next = now_odd.next
            if now_even.next:
                now_even = now_even.next

        now_odd.next = even
        return odd
''',
    setup='''
import tracer
a = L([2, 1, 3, 5, 6, 4, 7])
for k, nd in enumerate(tracer.Lnodes(a)):
    tracer._origin[nd._uid] = (k % 2, k // 2)
''',
    call='Solution().oddEvenList(a)',
    expect=[2, 3, 6, 7, 1, 5, 4],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_lists, size=26),
        dict(type='custom', h=520, draw=_ll({'now_odd': 'blue', 'now_even': 'green', 'odd': 'purple', 'even': 'pink'},
                                             title='上排：第 1、3、5、7 个节点　下排：第 2、4、6 个（黄 = 刚改的 next）')),
    ],
    watch=[('now_odd', 'now_odd', 'blue'), ('now_even', 'now_even', 'green')],
    captions={
        'if not head or': '至少有 3 个节点，需要重排（少于 3 个直接返回）',
        'odd = head': '`odd` 指向第一个节点：==奇数链表==的头',
        'even = head.next': '`even` 指向第二个节点：==偶数链表==的头，最后要接在奇链末尾',
        'now_odd = odd': '`now_odd`：奇链当前的末尾',
        'now_even = even': '`now_even`：偶链当前的末尾',
        'while now_even.next': lambda S, B, ret: (f'`now_even.next = {B.now_even.next.val}` 不为空 → 后面还有节点要分'
                                                  if B.now_even.next else
                                                  '`now_even.next` 为空 → 链表走到结尾（==奇数、偶数长度都这样判断==）'),
        'now_odd.next = now_even.next': lambda S, B, ret: (
            f'`odd->next = even->next`：`{S.now_odd.val}` 的下一个应该是 `{S.now_odd.next.val}`（跳过偶数节点）'),
        'now_odd = now_odd.next': '`now_odd` 移到 `{now_odd.val}`',
        'now_even.next = now_odd.next': lambda S, B, ret: (
            f'`even->next = odd->next`：`{S.now_even.val}` 的下一个是 `{_v(S.now_even.next)}`'
            + ('' if S.now_even.next else '（后面没有偶数节点了）')),
        'if now_even.next': lambda S, B, ret: (f'`now_even.next` 不为空 → `now_even` 可以后移' if S.now_even.next
                                               else '`now_even.next` 为空 → `now_even` 不动，下次 while 就结束'),
        'now_even = now_even.next': '`now_even` 移到 `{now_even.val}`：==情况又变回初始状态==',
        'now_odd.next = even': lambda S, B, ret: f'把整条偶数链（从 `{S.even.val}` 开始）接在奇数链末尾 `{S.now_odd.val}` 后面',
        'return odd': lambda S, B, ret: f'返回 `odd` → =={_chain(ret)}==',
    },
    cards=dict(
        one_liner='奇偶节点各连成一条链，最后把偶链接到奇链后面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把单链表中==第奇数个==节点放在一起，后面接上==第偶数个==节点，返回重排后的链表',
                 '要求 `O(1)` 额外空间、`O(n)` 时间；组内相对顺序不变',
                 '示例：`[2,1,3,5,6,4,7]` → `[2,3,6,7,1,5,4]`'],
        quote='odd的下一个节点应该是第三个节点，即even的下一个节点，于是有 ==odd->next = even->next==……even的下一个节点应该是第四个节点，即新odd的下一个节点，于是有 ==even->next = odd->next==。',
        quote_src='—— yiduobo 题解',
        idea=['两个指针分别指向第一、第二个节点',
              '交替执行 `odd->next = even->next`、`even->next = odd->next` 并各自后移',
              '`even->next` 为空就到结尾了；最后奇链末尾接上偶链头'],
        result='运行结束：返回 `[2,3,6,7,1,5,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`：只改指针，不新建节点',
                 '必须提前保存偶链头 `even`，否则最后接不回去',
                 '奇数长度时 `now_even.next` 会变成空：用 `if` 防止 `now_even` 走成 None',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释'],
    ),
)
