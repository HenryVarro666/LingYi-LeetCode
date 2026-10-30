CONFIG = dict(
    num=1836, title='从未排序的链表中移除重复元素', difficulty='Medium', category='链表',
    author='yiduobo', technique='哈希表记录首次出现的前置节点',
    tags=['哈希表'],
    code='''
class Solution(object):
    def deleteDuplicatesUnsorted(self, head):

        prev = {}
        p_head = ListNode()
        p_head.next = head

        now = p_head
        while now.next:
            if now.next.val not in prev:
                prev[now.next.val] = now
                now = now.next
            elif prev[now.next.val] is None:
                now.next = now.next.next
            else:
                remove_target = prev[now.next.val].next
                if remove_target == now:
                    now = prev[now.val]
                    now.next = now.next.next.next
                else:
                    prev[remove_target.next.val] = prev[now.next.val]
                    prev[now.next.val].next = remove_target.next
                    now.next = now.next.next

                prev[remove_target.val] = None

        return p_head.next
''',
    setup='head = L([3,2,2,1,3,2,4])',
    call='Solution().deleteDuplicatesUnsorted(head)',
    expect=[1, 4],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（prev 指向的是“前置节点”）', pointers={'now': 'blue', 'p_head': 'purple'}, h=300),
        dict(type='map', var='prev', label='prev：值 -> 它首次出现位置的前置节点（None = 已删除）',
             fmt=lambda k, v: f'{k} -> ' + ('None' if v is None else f'前置 {v.val}'),
             h=240),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('now.next', 'now.next.val if now.next else None', 'cyan'),
           ('remove_target', lambda S: S['remove_target'].val if S.get('remove_target') else None, 'pink')],
    captions={
        'prev = {}': '`prev` 记录：每种值第一次出现位置的==前置节点==（删节点要靠前置节点）',
        'p_head = ListNode()': '加==假头== `p_head`：这样首个节点被删时也有前置节点可用',
        'while now.next': lambda S, B, r: ('`now.next` 存在，继续检查下一个节点' if B.now.next else '`now.next` 为空 → 走到链表尾，结束'),
        'if now.next.val not in prev': lambda S, B, r: (f'`{B.now.next.val}` 没出现过 → ==首次出现==，记下前置节点' if B.now.next.val not in B.prev
                                                         else f'`{B.now.next.val}` 已在 `prev` 中，不是首次出现'),
        'prev[now.next.val] = now': '记 `prev[{now.next.val}]` = 当前节点 `{now.val}`，然后 `now` 后移',
        'now = now.next': lambda S, B, r: f'`now` 后移到 `{S.now.val}`',
        'elif prev[now.next.val] is None': lambda S, B, r: ('`prev[{}]` 是 None：首次出现的那个已被删，只需删掉当前这个'.format(B.now.next.val) if B.prev[B.now.next.val] is None
                                                         else '`prev[{}]` 不是 None：首次出现的节点还在链表里，要把它也删掉'.format(B.now.next.val)),
        14: '删掉 `now.next`：`now.next` 指向再下一个',
        'remove_target = prev': '`remove_target` = 首次出现节点 = `prev[{now.next.val}].next`（值 {remove_target.val}）',
        'if remove_target == now': lambda S, B, r: ('首次出现的节点恰好就是 `now`：两个要删的节点相邻' if S.remove_target is S.now
                                                    else '首次出现的节点不是 `now`：它在前面，分开删'),
        'now = prev[now.val]': '`now` 要先退回 `now` 的前置节点，再一起删掉相邻两个',
        'now.next = now.next.next.next': '跳过相邻的两个节点（首次出现 + 当前重复）',
        'prev[remove_target.next.val] = prev[now.next.val]': '`remove_target` 要被删，它后一个节点的前置节点变成 `remove_target` 的前置：==先修正 prev==',
        'prev[now.next.val].next = remove_target.next': '删除 `remove_target`：它的前置节点直接连到它的后一个',
        23: '再删掉当前重复节点 `now.next`',
        'prev[remove_target.val] = None': '`prev[{remove_target.val}]` = None：标记该值已处理，之后的同值节点直接删',
        'return p_head.next': '返回 `p_head.next`：真正的头节点',
    },
    cards=dict(
        one_liner='用哈希表记住“首次出现位置的前置节点”，一趟遍历删光重复值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['链表未排序；==只要某个值出现了不止一次，该值的所有节点都要删掉==，返回链表',
                 '示例：`[3,2,2,1,3,2,4]` → `[1,4]`（3 和 2 都重复）'],
        quote='最直观的思路就是使用哈希表记录每种元素值第一次出现位置的前置节点。在这里记录前置节点的理由是删除某个节点的操作实际上是通过其前置节点来完成的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`prev[值]` = 首次出现节点的前置节点；`None` 表示该值的首个节点已删',
              '再遇到同值：首个还在就连它一起删，已删就只删当前',
              '删首个节点时，它后一个节点的前置节点变了，要先修正 `prev`'],
        summary=['时间 `O(n)`，空间 `O(n)`；一趟遍历',
                 '==假头节点==让删除头部不用特判',
                 '相邻情况（首个就是 `now`）要先让 `now` 退回前置节点',
                 '删除首个节点后，要修正它后继节点在 `prev` 里的前置，并把该值置 None'],
    ),
)
