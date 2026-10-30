# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(next=head)
        right = dummy
        for _ in range(n):
            right = right.next

        
        left = dummy
        ## 1 → 2 → 3 → 4 → 5
        ## n = 2
        ## 用 while right.next， right → 5 left  → 3
        ## 用 while right， right → None left  → 4
        # while right.next 是为了让 slow 指针停在“删除节点的前一个”
        while right.next:
            left = left.next
            right = right.next
        left.next = left.next.next
        return dummy.next