SETUP = '''
import tracer


class Node(object):
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
        self._uid = tracer.next_uid()

    def __repr__(self):
        return f'Node({self.val})'


n1, n2, n3, n4, n5, n6 = [Node(v, None, None, None) for v in (1, 2, 3, 4, 5, 6)]
n1.next, n2.prev = n2, n1
n2.next, n3.prev = n3, n2
n2.child = n4
n4.next, n5.prev = n5, n4
n4.child = n6
head = n1
'''

POS = {1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (1, 1), 5: (2, 1), 6: (1, 2)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '多级链表（灰箭头 = next，橙虚线 = child，蓝 = now，粉 = prev_node，黄框 = 栈里待处理）', 21, T['muted'], bold=True)
    roots = [S.get('head')] + list(S.get('stack') or []) + [S.get('now'), S.get('prev_node')]
    seen = {}
    todo = [r for r in roots if r is not None]
    while todo:
        n = todo.pop()
        if n.val in seen:
            continue
        seen[n.val] = n
        todo += [m for m in (n.next, n.child) if m is not None]
    W, H = 150, 96
    gx = (x1 - x0 - 120) / 2
    gy = (y1 - y0 - 110) / 2
    gx = min(gx, 230)
    sx = x0 + 60 + ((x1 - x0 - 120) - gx * 2) / 2
    sy = y0 + 70

    def C(v):
        c, r = POS[v]
        return sx + c * gx, sy + r * (gy * 0.78) + 30

    def edge(a, b, color, dashed=False):
        (ax, ay), (bx, by) = C(a), C(b)
        dx, dy = bx - ax, by - ay
        d = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / d, dy / d
        k = min(W / 2 / abs(ux) if ux else 1e9, H / 2 / abs(uy) if uy else 1e9) / 1.0
        p0 = (ax + ux * (k + 4), ay + uy * (k + 4))
        p1 = (bx - ux * (k + 8), by - uy * (k + 8))
        if dashed:
            cv.dashed(p0, p1, color, 4)
            cv.arrow((p1[0] - ux * 14, p1[1] - uy * 14), p1, color, 4)
        else:
            cv.arrow(p0, p1, color, 4)

    for v, n in seen.items():
        if n.child is not None:
            edge(v, n.child.val, T['orange'], True)
        if n.next is not None:
            edge(v, n.next.val, T['muted'])
    stack = [n.val for n in (S.get('stack') or [])]
    for v, n in seen.items():
        X, Y = C(v)
        fill = T['panel2']
        if S.get('now') is n:
            fill = T['blue']
        elif S.get('prev_node') is n:
            fill = T['pink']
        outline = T['yellow'] if v in stack else T['border']
        cv.rect((X - W / 2, Y - H / 2, X + W / 2, Y + H / 2), fill=fill, outline=outline, width=5 if v in stack else 2, r=14)
        cv.text((X, Y), v, 44, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=430, title='扁平化多级双向链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='栈 + 先 next 后 child 入栈',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def flatten(self, head):

        if not head:
            return head

        stack = [head]
        prev_node = None
        while stack:
            now = stack.pop()
            now.prev = prev_node
            if prev_node:
                prev_node.next = now

            if now.next:
                stack.append(now.next)
            if now.child:
                stack.append(now.child)
                now.child = None
            prev_node = now

        return head
''',
    setup=SETUP,
    call='Solution().flatten(head)',
    expect=[1, 2, 4, 6, 5, 3],
    result_fn=list_vals,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='stack', var='stack', label='栈 stack（栈顶在右，先 pop 的是 child）', fmt=lambda x: str(x.val), h=130),
    ],
    watch=[('now', 'now', 'blue'), ('prev_node', 'prev_node', 'pink')],
    captions={
        'if not head': '空链表直接返回',
        'stack = [head]': '栈里先放头节点：栈里存的是==下一个要处理的节点==',
        'prev_node = None': '`prev_node` 记住上一个处理的节点，用来接 `prev` 和 `next`',
        'while stack': lambda S, B, ret: ('栈不空 → 还有节点没处理' if B.stack else '栈空了 → 全部处理完，链表已经压平'),
        'now = stack.pop()': '弹出栈顶 `{now.val}`：它就是压平后的==下一个节点==',
        'now.prev = prev_node': '`now.prev` 指向上一个处理的节点（`{B.prev_node.val if B.prev_node else None}`）',
        'if prev_node': lambda S, B, ret: (f'有上一个节点 → 把 `{B.prev_node.val}.next` 改成 `{B.now.val}`' if B.prev_node else '`prev_node` 为空 → 这是头节点，不用接'),
        'prev_node.next = now': '`prev_node.next` → `{now.val}`：按栈弹出的顺序串成一条链',
        'if now.next': lambda S, B, ret: (f'有 next `{B.now.next.val}` → 先入栈（后处理）' if B.now.next else '没有 next，不入栈'),
        'stack.append(now.next)': '`next` 节点 `{now.next.val}` 先入栈：它要排在整段 child 的后面',
        'if now.child': lambda S, B, ret: (f'有 child `{B.now.child.val}` → 后入栈，这样先被弹出' if B.now.child else '没有 child，不入栈'),
        'stack.append(now.child)': '`child` 节点 `{now.child.val}` 后入栈 → 下一个就处理它',
        'now.child = None': '题目要求压平后 `child` 置空',
        'prev_node = now': '`prev_node` 更新为当前节点 `{now.val}`',
        'return head': '返回原头节点：整条链已按「先 child、后 next」压平',
    },
    cards=dict(
        one_liner='先入栈 next，再入栈 child，栈顶永远是下一个',
        complexity='时间 `O(n)`，空间 `O(d)`（`d` 为嵌套深度，最坏 `O(n)`）',
        problem=['多级双向链表，节点除 `prev` / `next` 外还有 `child`',
                 '把 child 扶正到 next 的位置，原来的 next 接在 child 链末尾',
                 '压平后所有 `child` 置空',
                 '示例：`1→2→3`，2 的 child 是 `4→5`，4 的 child 是 `6` → `1→2→4→6→5→3`'],
        quote='每处理到一个节点，先将其next节点入栈，然后将其child节点入栈，接下来从栈顶弹出一个节点作为下一个节点进行处理。',
        quote_src='—— yiduobo 题解',
        idea=['压平后的顺序：先走完 child 这一整段，再回到原来的 next',
              '所以先压 next，再压 child：栈顶就是 child，后进先出',
              '用 `prev_node` 记住上一个节点，顺便把 `prev` 和 `next` 接好'],
        summary=['时间 `O(n)`，空间 `O(d)`；每个节点进栈出栈一次',
                 '易错点：入栈顺序别反了，必须先 next 后 child',
                 '易错点：别忘了 `now.child = None`，也要维护 `prev`',
                 '原文开头的 Node 类只是题面注释（docstring），在 setup 里补成真实类',
                 '同类题：114 二叉树展开为链表（也可用栈迭代）'],
    ),
)
