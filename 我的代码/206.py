# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre
    

# 这是链表反转最核心的一点：
# 👉 pre 在循环结束时，已经“走到了新链表的头”

# 👉 可以这样理解：
# 	•	cur：还没处理的部分
# 	•	pre：已经反转好的部分（头在 pre）

# 👉 pre 始终指向“反转后链表的头节点”