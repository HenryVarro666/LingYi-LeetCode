# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        n = 0
        cur = head
        while cur:
            n += 1
            cur = cur.next
        
        dummy = ListNode(next=head)
        p0 = dummy

        cur = head

        while n >= k:
            n -= k
            
            pre = None
            for _ in range(k):
                nxt = cur.next
                cur.next = pre
                pre = cur
                cur = nxt
            
            nxt = p0.next      # 反转前这一组的头，反转后变尾
            nxt.next = cur     # 尾巴接回后面
            p0.next = pre      # p0 接上这一组新的头
            p0 = nxt           # p0 移动到这一组新的尾巴
        return dummy.next
    
# p0
# 当前组前一个节点
# p0.next
# 当前组原来的头（翻转后变尾）
# pre
# 当前组翻转后的头
# cur
# 下一组的起点
