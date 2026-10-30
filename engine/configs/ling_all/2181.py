CONFIG = dict(
    num=2181, title='合并零之间的节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='原地累加 · tail 复用节点',
    tags=['灵神题单', '链表树与回溯', '遍历链表'],
    code='''
class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        tail = head
        cur = head.next
        while cur.next:
            if cur.val:
                tail.val += cur.val
            else:
                tail = tail.next
                tail.val = 0
            cur = cur.next
        tail.next = None
        return head
''',
    setup='head = L([0,3,1,0,4,5,2,0])',
    call='Solution().mergeNodes(head)',
    expect=[4, 11],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（tail 是答案链表的末尾，cur 往后扫）', pointers={'tail': 'blue', 'cur': 'pink'}, h=300),
        dict(type='text', fn=lambda S: f"当前段累加值 `tail.val` = =={S['tail'].val}==" if S.get('tail') is not None else ''),
    ],
    watch=[('tail.val', 'tail.val', 'blue'), ('cur.val', 'cur.val', 'pink')],
    captions={
        'tail = head': '把原链表头节点当作答案链表的末尾 `tail`：==直接在原节点上累加，不新建节点==',
        'cur = head.next': '`cur` 从第二个节点开始扫',
        'while cur.next': lambda S, B, r: ('`cur.next` 不为空：`cur` 还不是最后那个 0，继续' if S.cur.next is not None else '`cur.next` 为空：`cur` 是最后一个 0 → 遍历结束'),
        'if cur.val': lambda S, B, r: (f'`cur.val = {S.cur.val}` 非 0：属于当前这段，累加到 tail' if S.cur.val else '`cur.val = 0`：当前这段结束，要开始下一段'),
        'tail.val += cur.val': '`tail.val += {cur.val}` → =={tail.val}==',
        'tail = tail.next': '`tail` 前进一个节点：这个节点已被 cur 走过，可以拿来存下一段的和',
        'tail.val = 0': '把 `tail.val` 清零，准备累加新的一段',
        'cur = cur.next': '`cur` 右移一格',
        'tail.next = None': '`tail` 之后的节点（多余的原节点）全部断开，答案链表到此为止',
        'return head': '返回 `head`：链表变成 `[4, 11]`',
    },
    cards=dict(
        one_liner='每段的和存回前面已走过的节点，原地合并',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表由 `0` 分隔，首尾都是 `0`，相邻两个 `0` 之间的节点合并为一个（值为和）',
                 '合并后不能含有 `0`，返回头节点',
                 '示例：`[0,3,1,0,4,5,2,0]` → `[4,11]`'],
        quote='累加两个 0 之间的节点值，加到哪里？ 可以把 3,1 的和填到第一个节点 0 上，把 4,5,2 的和填到第二个节点 3 上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cur` 走在前面，`tail` 走在后面：==tail 永远不会超过 cur==',
              '遇到非 0 就累加进 `tail`；遇到 0，`tail` 换到下一个已走过的节点并清零',
              '最后断开 `tail.next`，丢掉多余节点'],
        summary=['时间 `O(n)`，空间 `O(1)`，没有创建新节点',
                 '`tail = tail.next` 一定存在：答案链表比原链表短',
                 '`while cur.next` 停在最后一个 0 上，它不属于答案',
                 '别忘了 `tail.next = None`，否则链表尾部残留旧节点'],
    ),
)
