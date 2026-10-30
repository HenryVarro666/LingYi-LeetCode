CONFIG = dict(
    num=2095, title='删除链表的中间节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='快慢指针 · 慢指针少走一步',
    tags=['灵神题单', '快慢指针'],
    code='''
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 876. 链表的中间结点
        slow = dummy = ListNode(next=head)
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        slow.next = slow.next.next  # 删除 slow 的下一个节点
        return dummy.next
''',
    call='Solution().deleteMiddle(L([1, 3, 4, 7, 1, 2, 6]))',
    expect=[1, 3, 4, 1, 2, 6],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: ('slow 比 876 题的位置往前一格（从 dummy 出发）→ 停在中间节点的==前一个==' if 'slow' in S else '')),
        dict(type='linked', label='链表（最左边是哨兵 dummy）', pointers={'slow': 'blue', 'fast': 'pink', 'dummy': 'purple'}, h=420),
    ],
    watch=[('slow', 'slow.val', 'blue'), ('fast', 'fast.val if fast else None', 'pink')],
    captions={
        'slow = dummy = ListNode': '==写法二==：在头前插 `dummy`，慢指针从 `dummy` 出发，比 876 题的慢指针起点往前一格',
        'fast = head': '快指针从 `head` 出发，和 876 题一样',
        'while fast and fast.next': lambda S, B, r: ('`fast` 和 `fast.next` 都不为空 → 还能走两步' if (B.fast and B.fast.next) else '快指针到头了 → 停止，慢指针刚好在中间节点的前一个'),
        'slow = slow.next': '`slow` 走一步 → {slow.val}',
        'fast = fast.next.next': '`fast` 走两步 → {fast.val if fast else "空"}',
        'slow.next = slow.next.next': '`slow` 后面就是中间节点 `{B.slow.next.val}` → 让 `slow.next` 跳过它，==删除完成==',
        'return dummy.next': '返回 `dummy.next`：`dummy` 让单节点链表也能删，不用特判',
    },
    cards=dict(
        one_liner='让慢指针少走一步，刚好停在中间节点前面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除链表的==中间节点==（从 0 起第 `n // 2` 个），返回头节点',
                 '示例：`[1,3,4,7,1,2,6]` → `[1,3,4,1,2,6]`',
                 '`[2,1]` → `[2]`'],
        quote='为了删除链表的中间节点，我们需要让慢指针少走一步，移动到中间节点的前一个节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删节点要找它的==前一个==：慢指针要比 876 题少走一步',
              '在链表前插 `dummy`，慢指针从 `dummy` 出发：循环次数不变，位置自然靠前一格',
              '`while fast and fast.next` 与 876 题完全一样'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '写法一：特判单节点，让快指针先走两步少循环一次；写法二（本视频）用哨兵更统一',
                 '易错：返回 `dummy.next` 而不是 `head`；单节点时结果是空',
                 '链表题可能删头，优先考虑哨兵节点'],
    ),
)
