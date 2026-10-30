def _cap_while(S, B, ret):
    nx = B['now'].next
    if nx is None:
        return '`now.next` 为空 → 扫描到了末尾，结束'
    return f'`now.next` 不为空 → 检测 `now` 的下一个节点 `{nx.val}`'


def _cap_if(S, B, ret):
    v = S['now'].next.val
    if v == S['val']:
        return f'`now.next.val = {v}` 等于 `val` → 需要删去 `now.next`'
    return f'`now.next.val = {v} != {S["val"]}` → 不用删，`now` 往后移'


def _cap_del(S, B, ret):
    gone, nx = B['now'].next, S['now'].next
    to = f'`{nx.val}`' if nx else '`None`'
    tail = '；`now` 留在原地，接着检测新的 `now.next`' if nx else ''
    return f'`now.next = now.next.next`：跳过 `{gone.val}`，直接连到 {to}{tail}'


CONFIG = dict(
    num=203, title='移除链表元素', difficulty='Easy', category='链表',
    author='yiduobo', technique='假头 p_head + 从假头往后扫描',
    tags=['字节6个月'],
    code='''
class Solution(object):
    def removeElements(self, head, val):

        p_head = ListNode(0)
        p_head.next = head

        now = p_head
        while now.next:
            if now.next.val == val:
                now.next = now.next.next
            else:
                now = now.next

        return p_head.next
''',
    # setup 只做布局：把运行中创建的第一个节点（p_head）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([1,2,6,3,4,5,6])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().removeElements(head, 6)',
    expect=[1, 2, 3, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f'删除所有值为 `val = {S["val"]}` 的节点；`now` 站在==待检测节点的前一个==' if 'val' in S else '')),
        dict(type='linked', label='链表（最左边是假头 p_head）', pointers={'now': 'blue', 'p_head': 'purple'}, h=300),
    ],
    watch=[('now', 'now', 'blue'), ('now.next', lambda S: S['now'].next if 'now' in S else None), 'val'],
    captions={
        'p_head = ListNode(0)': '方便起见，弄一个==假头== `p_head`',
        'p_head.next = head': '假头指向 `head`：这样头节点也有了「前一个节点」，删它不用特判',
        'now = p_head': '从 `p_head` 开始往后扫描',
        'while now.next': _cap_while,
        'if now.next.val == val': _cap_if,
        'now.next = now.next.next': _cap_del,
        'now = now.next': '`now` 移动到 `{now.val}`，继续检测',
        'return p_head.next': '返回 `p_head.next`，即删除后的真正头节点：=={ret.val}== 开头',
    },
    max_steps=40,
    cards=dict(
        one_liner='在头节点前放一个假头，从假头开始检测并删除下一个节点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除链表中所有 `Node.val == val` 的节点，返回==新的头节点==',
                 '示例：`head = [1,2,6,3,4,5,6], val = 6` → `[1,2,3,4,5]`',
                 '示例：`head = [7,7,7,7], val = 7` → `[]`'],
        quote='方便起见还是弄一个==假头p_head指向head==，然后从p_head开始往后扫描。若now.next.val等于val，那么需要删去now.next，于是有==now.next = now.next.next==，否则就将now移动到now.next继续检测即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['单链表只能从前一个节点删除，所以 `now` 检测的是 `now.next`',
              '假头 `p_head` 让头节点和其他节点一样处理',
              '等于 `val`：`now.next` 跳过它；否则 `now` 后移'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：删除后 `now` 不能后移，否则连续的待删节点会漏掉（如 `[7,7,7,7]`）',
                 '易错：要返回 `p_head.next`，不是 `head`',
                 '原文为 Python 2 风格（类型写在文档字符串里），已删去文档字符串和 ListNode 定义注释，代码未改'],
    ),
)
