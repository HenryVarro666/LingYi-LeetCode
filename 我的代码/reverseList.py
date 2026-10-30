def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    pre = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = pre
        pre = cur
        cur = nxt
    return pre


def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head  # 把下一个节点指向自己
        head.next = None  # 断开指向下一个节点的连接，保证最终链表的末尾节点的 next 是空节点
        return new_head