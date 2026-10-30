# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# 创建新节点
class solution:
    def addTwoNumers(self, l1, l2, carry = 0):
        if l1 is None and l2 is None and carry == 0:
            return None
        
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        return (s % 10, self.addTwoNumbers(l1, l2, s // 10))
    
# 原地修改
class Solution: 
    # 如果递归中发现l2的长度比l1更长，那么可以交换l1和l2，保证l1不是空节点，从而简化代码逻辑。
    # l1 和 l2 为当前遍历的节点，carry 为进位
    def addTwoNumbers(self, l1, l2, carry=0):
        if l1 is None and l2 is None:  # 递归边界
            return ListNode(carry) if carry else None  # 如果进位了，就额外创建一个节点
        if l1 is None:  # 如果 l1 是空的，那么此时 l2 一定不是空节点
            # 把“两个链表的情况”统一成“至少有一个链表存在”的情况
            # 始终只需要处理 l1（保证存在） + l2（可能为空）
            l1, l2 = l2, l1  # 交换 l1 与 l2，保证 l1 非空，从而简化代码
        s = carry + l1.val + (l2.val if l2 else 0)  # 节点值和进位加在一起
        l1.val = s % 10  # 每个节点保存一个数位（直接修改原链表）
        l1.next = self.addTwoNumbers(l1.next, l2.next if l2 else None, s // 10)  # 进位
        return l1


# 迭代
class Solution:
    def addTwoNumbers(self, l1, l2):
       cur = dummy = ListNode()
       carry = 0
       while l1 or l2 or carry:
            if l1:
                carry += l1.val
                l1 = l1.next
            if l2:
                carry += l2.val
                l2 = l2.next
            
            cur.next = ListNode(carry % 10)
            carry //= 10
            cur = cur.next 
        return dummy.next