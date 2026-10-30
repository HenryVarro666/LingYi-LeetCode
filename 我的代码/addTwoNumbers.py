# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class solution:
    def addTwoNumers(self, l1, l2, carry = 0):
        if l1 is None and l2 is None and carry == 0:
            return None
        
        s = carry
        if l1:
            s += l1.value
            l1 = l1.next
        if l2:
            s += l2.value
            l2 = l2.next
        return (s % 10, self.addTwoNumbers(l1, l2, s // 10))
    

class Solution: # 如果递归中发现 l2 的长度比 l1更长，那么可以交换 l1 和 l2，保证 l1不是空节点，从而简化代码逻辑。
    # l1 和 l2 为当前遍历的节点，carry 为进位
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode], carry=0) -> Optional[ListNode]:
        if l1 is None and l2 is None:  # 递归边界
            return ListNode(carry) if carry else None  # 如果进位了，就额外创建一个节点
        if l1 is None:  # 如果 l1 是空的，那么此时 l2 一定不是空节点
            l1, l2 = l2, l1  # 交换 l1 与 l2，保证 l1 非空，从而简化代码
        s = carry + l1.val + (l2.val if l2 else 0)  # 节点值和进位加在一起
        l1.val = s % 10  # 每个节点保存一个数位（直接修改原链表）
        l1.next = self.addTwoNumbers(l1.next, l2.next if l2 else None, s // 10)  # 进位
        return l1
    
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点
        carry = 0  # 进位
        while l1 or l2 or carry:  # 有一个不是空节点，或者还有进位，就继续迭代
            if l1:
                carry += l1.val  # 节点值和进位加在一起
                l1 = l1.next  # 下一个节点
            if l2:
                carry += l2.val  # 节点值和进位加在一起
                l2 = l2.next  # 下一个节点
            cur.next = ListNode(carry % 10)  # 每个节点保存一个数位
            carry //= 10  # 新的进位
            cur = cur.next  # 下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是头节点