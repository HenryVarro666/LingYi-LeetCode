def _nv(x):
    return 'None' if x is None else str(x.val)


def _while_now(S, B, ret):
    nx = B['now'].next
    if nx is None:
        return '`now.next` 为空 → 已经走到链表尾部，操作完成'
    return f'`now` 后面还有节点 `{nx.val}` → 设它为 `p`，看它要不要删'


def _while_p(S, B, ret):
    p, v = B['p'], B['now'].next.val
    if p.next and p.next.val == v:
        return f'`p.next` 的值也是 `{v}` → `p` 后移，把它==划进要删的一段=='
    return f'`p.next` 是 `{_nv(p.next)}`，不等于 `{v}` → 相同值的一段到 `p` 为止'


def _if_cap(S, B, ret):
    if S.now.next is not S.p:
        return f'`now.next` 不是 `p`：`p` ==移动过== → `now.next` 到 `p` 这一段值全是 `{S.p.val}`，全部删去'
    return f'`now.next` 就是 `p`：`p` 没动过 → `{S.p.val}` 不重复，需要保留'


def _seg(S):
    if 'p' not in S or S.get('now') is None or S['now'].next is None:
        return '`now` 停在“已确定保留”的节点上，`p` 去找一段相同值的末尾'
    a, p = S['now'].next, S['p']
    if a is p:
        return f'`now.next` 到 `p`：只有一个节点 `{p.val}`'
    cnt, x = 1, a
    while x is not p and x is not None and cnt < 20:
        x, cnt = x.next, cnt + 1
    if x is p:
        return f'`now.next` 到 `p`：==连续 {cnt} 个== `{p.val}`'
    return f'值为 `{p.val}` 的一段已被跳过：`now.next` → `{a.val}`'


CONFIG = dict(
    num=82, title='删除排序链表中的重复元素 II', difficulty='Medium', category='链表',
    author='yiduobo', technique='假头 + 找出相同值的一段',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def deleteDuplicates(self, head):
        new_head = ListNode(0)
        new_head.next = head

        now = new_head
        while now.next:
            p = now.next
            while p.next and p.next.val == now.next.val:
                p = p.next

            if now.next != p:
                now.next = p.next
            else:
                now = p

        return new_head.next
''',
    # setup 只做布局：运行中创建的第一个节点（new_head）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([1,1,1,2,3])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().deleteDuplicates(head)',
    expect=[2, 3],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_seg),
        dict(type='linked', label='链表（最左边是假头 new_head）', pointers={'now': 'blue', 'p': 'pink'}, h=440),
    ],
    watch=[('now', 'now', 'blue'), ('now.next', lambda S: S['now'].next if S.get('now') else None, 'cyan'), ('p', 'p', 'pink')],
    captions={
        'new_head = ListNode(0)': '经典做法：先在 `head` 前加入一个==假头== `new_head`',
        'new_head.next = head': '`new_head.next = head`：头节点被删也不用特判',
        'now = new_head': '`now` 从假头开始：它后面的节点才是要考虑的',
        'while now.next:': _while_now,
        'p = now.next': '`p = now.next = {p.val}`：从这里开始找值相同的一段',
        'while p.next and': _while_p,
        'p = p.next': '`p` → 下一个 `{p.val}`',
        'if now.next != p': _if_cap,
        'now.next = p.next': lambda S, B, ret: f'`now.next = p.next`：整段跳过，`now` 后面直接接上 `{_nv(S.now.next)}`（`now` 不动）',
        'now = p': '`now = p`：`{now.val}` 留在链表里，`now` 前进到它',
        'return new_head.next': '返回 `new_head.next`：原来的头 `1` 已经被删掉了',
    },
    cards=dict(
        one_liner='假头 + 让 p 走到相同值一段的末尾：p 动过就整段删',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个==已排序==链表，把==出现重复的数字全部删除==，只留下没重复过的',
                 '示例：`[1,2,3,3,4,4,5]` → `[1,2,5]`',
                 '本视频：`[1,1,1,2,3]` → `[2,3]`（头节点也要删）'],
        quote='如果now.next还是p，说明p在步骤2中未发生过移动……那么此时p是需要保留在链表中的……否则，说明now.next到p之间的所有节点val都相同，需要删去。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`p` 从 `now.next` 出发，沿着==值相同==的节点一路走到这一段的末尾',
              '`p` 没动 → 这个值只出现一次，保留：`now = p`',
              '`p` 动过 → `now.next = p.next`，整段删掉，`now` 留在原地'],
        summary=['时间 `O(n)`：每个节点只被检测一次，虽然是两重循环',
                 '易错：整段删完后 `now` ==不能前进==，下一段可能又是重复',
                 '用 `now.next != p` 判断 `p` 是否移动过，省掉一个计数变量',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；`ListNode(0)` 原样保留',
                 '对比灵神：灵神看后两个节点是否相同，yiduobo 先找出整段再决定删不删'],
    ),
)
