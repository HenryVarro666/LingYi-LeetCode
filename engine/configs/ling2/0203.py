def _cap_while(S, B, ret):
    nx = B['cur'].next
    if nx is None:
        return '`cur.next` 为空 → ==cur 已是最后一个节点==，后面没有要检查的了'
    return f'`cur.next` 不为空 → 检查 `cur` 的下一个节点 `{nx.val}`'


def _cap_if(S, B, ret):
    v = S['cur'].next.val
    if v == S['val']:
        return f'`cur.next.val = {v} == val` → 要删它。==删除必须在它的前一个节点 cur 处操作=='
    return f'`cur.next.val = {v} != {S["val"]}` → 保留，`cur` 往后走'


def _cap_del(S, B, ret):
    cur, gone = S['cur'], B['cur'].next
    nx = cur.next
    to = f'`{nx.val}`' if nx else '`None`'
    if cur is S['dummy']:
        return f'删的是==头节点== `{gone.val}`：有哨兵，写法和删中间节点一样，`dummy.next` → {to}'
    if nx is not None and nx.val == S['val']:
        return f'`cur.next` 跳过 `{gone.val}` 指向 {to}。==cur 不动==：新的下一个又是 `{nx.val}`，也要删'
    return f'删除下一个节点：`cur.next` 跳过 `{gone.val}`，指向 {to}；cur 不动，下一轮再检查'


CONFIG = dict(
    num=203, title='移除链表元素', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='哨兵节点 + 在前一个节点处删除',
    tags=['字节6个月'],
    code='''
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        cur = dummy = ListNode(next=head)
        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next  # 删除下一个节点
            else:
                cur = cur.next  # 继续向后遍历链表
        return dummy.next
''',
    # setup 只做布局：把运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([6,1,6,6,2])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().removeElements(head, 6)',
    expect=[1, 2],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f'要删除的值 `val = {S["val"]}`；`cur` 负责==检查并删除它的下一个节点==' if 'val' in S else '')),
        dict(type='linked', label='链表（最左边是哨兵 dummy；head 删掉后仍指着旧节点）', pointers={'cur': 'blue', 'dummy': 'purple', 'head': 'red'}, h=300),
    ],
    watch=[('cur', 'cur', 'blue'), ('cur.next', lambda S: S['cur'].next if 'cur' in S else None), 'val'],
    captions={
        'cur = dummy = ListNode': '头节点也可能被删 → 在它前面加一个哨兵 `dummy`，==无需特判头节点==；`cur` 从 `dummy` 出发',
        'while cur.next': _cap_while,
        'if cur.next.val == val': _cap_if,
        'cur.next = cur.next.next': _cap_del,
        'cur = cur.next  # 继续': '下一个不用删，`cur` 向后移动到 `{cur.val}`',
        'return dummy.next': '返回 `dummy.next`：它才是删除后的新头节点（==cur 和 dummy 一开始是同一个节点的引用==）',
    },
    max_steps=40,
    cards=dict(
        one_liner='删除节点要在它的前一个节点操作；头节点可能被删，就加哨兵',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除链表中所有 `Node.val == val` 的节点，返回==新的头节点==',
                 '示例：`head = [1,2,6,3,4,5,6], val = 6` → `[1,2,3,4,5]`',
                 '示例：`head = [7,7,7,7], val = 7` → `[]`（头节点也会被删）',
                 '演示用 `[6,1,6,6,2], val = 6`：==头节点==和==连续两个== 6 都要删'],
        quote='套路 1：要想删除节点 node，==必须在 node 的前一个节点执行删除操作==。套路 2：如果头节点可能被删除，那么要在头节点之前==添加一个哨兵节点==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删 2：在 1 处把 `next` 改成 3 → 所以 `cur` 永远看的是 `cur.next`',
              '头节点前面没有节点 → 加哨兵 `dummy`，删头节点和删中间节点写法一样',
              '删完==不移动== `cur`：新的 `cur.next` 可能也等于 `val`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：删除后若接着 `cur = cur.next`，连续两个要删的节点会==漏删一个==',
                 '易错：返回 `head` 是错的（头可能已被删），要返回 `dummy.next`',
                 '修改 `cur.next` 就是修改 `dummy.next`：开始时二者是同一个节点'],
    ),
)
