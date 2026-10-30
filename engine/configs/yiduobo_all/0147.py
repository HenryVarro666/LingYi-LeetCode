CONFIG = dict(
    num=147, title='对链表进行插入排序', difficulty='Medium', category='链表',
    author='yiduobo', technique='假头 + 已排序尾指针',
    tags=['排序'],
    code='''
class Solution(object):
    def insertionSortList(self, head):

        if not head or not head.next:
            return head

        p_head = ListNode(0)
        p_head.next = head
        now = head.next
        tail = head
        while now:
            if now.val >= tail.val:
                tail = tail.next
                now = now.next
            else:
                tmp = p_head
                while tmp.next != now and tmp.next.val < now.val:
                    tmp = tmp.next

                tail.next = now.next
                now.next = tmp.next
                tmp.next = now
                now = tail.next

        return p_head.next
''',
    setup='head = L([4,2,5,1,3])',
    call='Solution().insertionSortList(head)',
    expect=[1, 2, 3, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（tail 之前是已排好的部分）', pointers={'now': 'blue', 'tail': 'green', 'tmp': 'orange', 'p_head': 'purple'}, h=380),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('tail', 'tail.val', 'green'),
           ('tmp', lambda S: S['tmp'].val if S.get('tmp') else None, 'orange')],
    captions={
        'if not head or not head.next': '空链表或只有一个节点，本来就有序，直接返回',
        'p_head = ListNode(0)': '放一个==假头== `p_head`：插到最前面时也有前驱可用',
        'now = head.next': '`now` 是待插入节点，`tail` 是已排序部分的最后一个：初始只有 `head`',
        'while now': lambda S, B, r: ('`now` 不为空，还有节点没处理' if B.now else '`now` 为空 → 全部处理完'),
        'if now.val >= tail.val': lambda S, B, r: (f'`{B.now.val} >= {B.tail.val}`：比已排序部分的最后一个还大 → 已经在正确位置'
                                                   if B.now.val >= B.tail.val else f'`{B.now.val} < {B.tail.val}`：比已排序的末尾小 → 需要往前找位置插入'),
        'tail = tail.next': '`now` 就在 `tail` 后面：`tail` 和 `now` 一起后移',
        'now = now.next': '`now` → {now.val if now else None}',
        'tmp = p_head': '`tmp` 从假头开始，往后找第一个 `tmp.next.val >= now.val` 的位置',
        'while tmp.next != now': lambda S, B, r: ('`tmp.next` 还比 `now` 小，继续后移' if (B.tmp.next is not B.now and B.tmp.next.val < B.now.val)
                                                  else '找到插入位置：`tmp` 后面就是该放 `now` 的地方'),
        'tmp = tmp.next': '`tmp` 后移到 `{tmp.val}`',
        'tail.next = now.next': '先把 `tail.next` 接到 `now` 的后继：==保存下一个待处理节点==，同时把 `now` 摘出来',
        'now.next = tmp.next': '`now` 指向 `tmp` 的后一个',
        'tmp.next = now': '`tmp` 指向 `now`：==插入完成==，`tail` 不用动',
        'now = tail.next': '`now` 取 `tail.next`，即刚才保存的下一个待处理节点',
        'return p_head.next': '返回 `p_head.next`：新链表的头',
    },
    cards=dict(
        one_liner='tail 之前已排好序：新节点不小于 tail 就放行，否则从头找位置插入',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['用==插入排序==对单链表排序，返回排序后的链表头',
                 '每次取一个节点，插入到已排序部分的正确位置',
                 '本视频：`[4,2,5,1,3]` → `[1,2,3,4,5]`'],
        quote='使用指针now从头往后扫描：如果now.val大于等于当前已经排好的部分的最后一个节点tail.val，那么说明now已经在正确的位置上了，此时将now与tail同时往后移动即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`tail` 是已排序部分的末尾，`now` = `tail.next` 是待处理节点',
              '否则从假头往后找第一个 `p.next.val >= now.val`，把 `now` 插入 `p` 与 `p.next` 之间',
              '插入前先 `tail.next = now.next` 保存后继，`tail` 保持不动'],
        summary=['时间 `O(n^2)`（最坏每个节点都从头扫），空间 `O(1)`',
                 '==假头==让“插到最前面”不用特判',
                 '`now` 插入后不能 `now = now.next`（已经改了），要用 `tail.next`',
                 '内层 `while` 的 `tmp.next != now` 保证不会越过自己'],
    ),
)
