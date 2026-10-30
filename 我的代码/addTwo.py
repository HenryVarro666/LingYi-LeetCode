# l1 和 l2 为当前遍历的节点，carry 为进位
def addTwo(self, l1: Optional[ListNode], l2: Optional[ListNode], carry=0) -> Optional[ListNode]:
    if l1 is None and l2 is None:  # 递归边界：l1 和 l2 都是空节点
        return ListNode(carry) if carry else None  # 如果进位了，就额外创建一个节点
    if l1 is None:  # 如果 l1 是空的，那么此时 l2 一定不是空节点
        l1, l2 = l2, l1  # 交换 l1 与 l2，保证 l1 非空，从而简化代码
    carry += l1.val + (l2.val if l2 else 0)  # 节点值和进位加在一起
    l1.val = carry % 10  # 每个节点保存一个数位
    l1.next = self.addTwo(l1.next, l2.next if l2 else None, carry // 10)  # 进位
    return l1


def addTwo(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点
        carry = 0  # 进位
        while l1 or l2 or carry:  # 有一个不是空节点，或者还有进位，就继续迭代
            if l1: carry += l1.val  # 节点值和进位加在一起
            if l2: carry += l2.val  # 节点值和进位加在一起
            cur.next = ListNode(carry % 10)  # 每个节点保存一个数位
            carry //= 10  # 新的进位
            cur = cur.next  # 下一个节点
            if l1: l1 = l1.next  # 下一个节点
            if l2: l2 = l2.next  # 下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是头节点