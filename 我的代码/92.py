# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(next=head)
        p0 = dummy
        for _ in range (left-1):
            # p0 指向 = left 前一个节点
            p0 = p0.next

        pre = None
        cur = p0.next
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt

        # 旧头（现在变尾）接回后面
        p0.next.next = cur
        # p0 接上新的头
        p0.next = pre
        return dummy.next 
        

# 这是一个指针视角问题，核心在于：
# 👉 p0 不是链表头，它只是一个“局部游标”
# 👉 dummy 才是真正代表“新链表头”的指针


# dummy node 的核心作用：
# 	1.	统一处理头节点
# 	2.	避免 left == 1 特判
# 	3.	始终持有链表入口

# 局部操作 → 用 p0
# 返回结果 → 用 dummy

