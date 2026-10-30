CONFIG = dict(
    num=2095, title='删除链表的中间节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='快慢指针 · 假头',
    tags=['灵神题单', '快慢指针'],
    code='''
class Solution(object):
    def deleteMiddle(self, head):

        p_head = ListNode()
        p_head.next = head

        slow = fast = p_head
        while fast.next and fast.next.next:
            fast = fast.next.next
            slow = slow.next
        
        slow.next = slow.next.next
        return p_head.next
''',
    call='Solution().deleteMiddle(L([1, 3, 4, 7, 1, 2, 6]))',
    expect=[1, 3, 4, 1, 2, 6],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: ('fast 每轮两步、slow 每轮一步：fast 到头时 slow 就在中间节点的==前一个==' if 'slow' in S else '')),
        dict(type='linked', label='链表（最左边是假头 p_head）', pointers={'slow': 'blue', 'fast': 'pink', 'p_head': 'purple'}, h=420),
    ],
    watch=[('slow', 'slow.val', 'blue'), ('fast', 'fast.val', 'pink')],
    captions={
        'p_head = ListNode()': '建==假头== `p_head`：链表只有一个节点时也能删',
        'p_head.next = head': '假头接到真正的表头前面',
        'slow = fast = p_head': '`slow`、`fast` 都从假头出发',
        'while fast.next': lambda S, B, r: ('`fast` 后面还有两个节点，能再走两步' if (B.fast.next and B.fast.next.next) else '`fast` 走不动两步了 → 停'),
        'fast = fast.next.next': '`fast` 走两步 → {fast.val}',
        'slow = slow.next': '`slow` 走一步 → {slow.val}',
        'slow.next = slow.next.next': '`slow` 停在中间节点的前一个（{slow.val}）：让它跳过 `{B.slow.next.val}`，==删除中间节点==',
        'return p_head.next': '返回 `p_head.next`：只有一个节点被删时结果为空',
    },
    cards=dict(
        one_liner='快指针到头时，慢指针停在中间节点前一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除链表的中间节点（下标 `n // 2`），返回头节点',
                 '示例：`[1,3,4,7,1,2,6]` → `[1,3,4,1,2,6]`',
                 '`[2,1]` → `[2]`'],
        quote='slow移动了n / 2轮，恰好位于链表中第n / 2 - 1个节点，而答案要求移除的是第n / 2个节点，那么只需要将slow的next指向slow的next的next即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['假头 `p_head` 让两个指针都从“第 0 个节点”出发',
              'fast 每轮两步，slow 每轮一步，共走 `n/2` 轮 → slow 在要删节点的前一个',
              '`slow.next = slow.next.next` 跳过中间节点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环条件 `fast.next and fast.next.next`：保证 fast 还能走两步',
                 '返回 `p_head.next`，单节点链表删完返回空',
                 '原文就是 Python 3 可运行的写法，未做改动'],
    ),
)
