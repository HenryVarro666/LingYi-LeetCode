class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        # 存放小于 x 的链表的虚拟头节点
        dummy1 = ListNode(-1)
        # 存放大于等于 x 的链表的虚拟头节点
        dummy2 = ListNode(-1)
        # p1, p2 指针负责生成结果链表
        p1, p2 = dummy1, dummy2
        # p 负责遍历原链表，类似合并两个有序链表的逻辑
        # 这里是将一个链表分解成两个链表
        p = head
        while p:
            if p.val >= x:
                p2.next = p
                p2 = p2.next
            else:
                p1.next = p
                p1 = p1.next
            # 不能直接让 p 指针前进
            # p = p.next
            # 断开原链表中的每个节点的 next 指针
            temp = p.next
            p.next = None
            p = temp
        # 连接两个链表
        p1.next = dummy2.next

        return dummy1.next



### 

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        sml_dummy, big_dummy =. ListNode(0), ListNode(0)
        sml, big = sml_dummy, big_dummy
        while head:
            if head.val < x:
                sml.next = head
                sml = sml.next
            else:
                big.next = head
                big = big.next
            head = head.next
        sml.next = bit_dummy.next
        big.next = None
        return sml_dummy.next
    



### 
# 递归（尾插法）
class Solution:
    # 首先「递」到链表末尾，把末尾节点作为新链表的头节点 rev_head
    # 然后在「归」的过程中，把经过的节点依次插在新链表的末尾（尾插法）
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 判断 head is None 是为了兼容一开始链表就是空的情况
        if head is None or head.next is None:
            return head  # 链表末尾，即下面的 rev_head
        rev_head = self.reverseList(head.next)  # 「递」到链表末尾，拿到新链表的头节点
        tail = head.next  # 在「归」的过程中，head.next 就是新链表的末尾
        tail.next = head  # 把 head 插在新链表的末尾
        head.next = None  # 如果不写这行，新链表的末尾两个节点成环，这俩节点互相指向对方
        return rev_head

# 迭代（头插法）
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre  # 把 cur 插在 pre 链表的前面（头插法）
            pre = cur
            cur = nxt
        return pre