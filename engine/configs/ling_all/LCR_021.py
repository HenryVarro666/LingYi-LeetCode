def _ruler(S):
    l, r = S.get('left'), S.get('right')
    if l is None or r is None:
        return ''
    d, x = 0, l
    while x is not None and x is not r and d < 20:
        x, d = x.next, d + 1
    if d < S.get('n', 0) and l is not S.get('dummy'):
        return ''  # 左右指针一前一后移动的中间态，不显示
    return f'尺子：`left` → `right` 相距 =={d}== 步（目标 `n` = {S.get("n")}）'


CONFIG = dict(
    num='LCR 021', title='删除链表的倒数第 N 个结点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='前后指针 + 哨兵节点',
    code='''
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # 由于可能会删除链表头部，用哨兵节点简化代码
        left = right = dummy = ListNode(next=head)
        for _ in range(n):
            right = right.next  # 右指针先向右走 n 步
        while right.next:
            left = left.next
            right = right.next  # 左右指针一起走
        left.next = left.next.next  # 左指针的下一个节点就是倒数第 n 个节点，删除之
        return dummy.next
''',
    # setup 只做布局：把运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([1,2,3,4,5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().removeNthFromEnd(head, 2)',
    expect=[1, 2, 3, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_ruler),
        dict(type='linked', label='链表（最左边是哨兵 dummy）', pointers={'left': 'blue', 'right': 'pink', 'dummy': 'purple'}, h=420),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'n'],
    captions={
        'left = right = dummy': '在头节点前插一个哨兵 `dummy`：==删的是头节点也不用特判==，尺子左端从 `dummy` 出发',
        'for _ in range(n)': lambda S, B, ret: (f'右端先走 `n` = {S.n} 步：第 {S._ + 1} 步' if '_' not in B or S._ != B._
                                                else f'右端已经走完 `n` = {S.n} 步，尺子长度就位'),
        'right = right.next  # 右指针先': '`right` 先走一步 → 节点 `{right.val}`：把尺子拉长到 `n` 步',
        'while right.next': lambda S, B, ret: ('`right.next` 不为空 → 右端还没到末尾，尺子继续右移' if B.right.next else
                                               '`right.next` 为空 → ==右端到达末尾==，此时 `left` 停在倒数第 `n+1` 个节点'),
        'left = left.next': '尺子整体右移：`left` → `{left.val}`',
        'right = right.next  # 左右': '`right` → `{right.val}`，两端距离始终是 `n`',
        'left.next = left.next.next': '`left` 的下一个就是倒数第 `n` 个（节点 `{B.left.next.val}`）→ 让 `left.next` 跳过它，==删除完成==',
        'return dummy.next': '返回 `dummy.next`：不能返回 `head`，因为头节点可能被删了',
    },
    cards=dict(
        one_liner='一把长度为 n 的尺子：右端到末尾时，左端就在要删节点的前面',
        complexity='时间 `O(m)`，空间 `O(1)`（`m` 为链表长度）',
        problem=['删除链表的==倒数第== `n` ==个==节点，返回头节点',
                 '示例：`head = [1,2,3,4,5], n = 2` → `[1,2,3,5]`',
                 '进阶：只扫描一趟'],
        quote='想象有一把长度固定的尺子，左端点在链表头部，右端点在正数第 n 个节点。向右移动尺子，当尺子右端点到达链表末尾时，左端点就在倒数第 n 个节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删除要找==前一个==节点：所以左端要停在倒数第 `n+1` 个',
              '在头前加哨兵 `dummy`，左端从 `dummy` 出发 → 删头节点也不特判',
              '`while right.next`：要停在==最后一个==节点，而不是走出链表'],
        summary=['时间 `O(m)`，空间 `O(1)`；`right` 先走 `n` 步，再一起走',
                 '==遇到可能删除头节点的题，加哨兵节点==（灵神原话：请记住这个技巧）',
                 '`while node` 走到最后一个节点之后；`while node.next` 停在最后一个节点',
                 '返回 `dummy.next` 而不是 `head`（`n` 等于长度时头被删）'],
    ),
)
