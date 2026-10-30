class ListNode:
    """单向链表节点"""
    def __init__(self, x):
        self.val = x
        self.next = None


class Node:
    """双向链表节点"""
    def __init__(self, prev, element, next):
        self.val = element
        self.next = next
        self.prev = prev


# ==========================================
# 数组转链表工具函数
# ==========================================
class ListNode:
    """单向链表节点（重复定义保留）"""
    def __init__(self, x):
        self.val = x
        self.next = None

def createLinkedList(arr: 'List[int]') -> 'ListNode':
    """
    将给定的数组转换为单向链表。
    :param arr: 输入的整数数组
    :return: 转换后的链表的头节点
    """
    if arr is None or len(arr) == 0:
        return None

    head = ListNode(arr[0])
    cur = head
    for i in range(1, len(arr)):
        cur.next = ListNode(arr[i])
        cur = cur.next

    return head

# def createLinkedList(arr):
#     """（备用实现，无类型提示版）"""
#     if not arr:
#         return None
#     
#     head = ListNode(arr[0])
#     cur = head
#     for i in range(1, len(arr)):
#         cur.next = ListNode(arr[i])
#         cur = cur.next
#     return head



# ==========================================
# 1. 遍历操作 (Traversal)
# ==========================================
head = createLinkedList([1, 2, 3, 4, 5])

# 遍历并打印链表元素（查/改的基础）
p = head
while p is not None:
    print(p.val)
    p = p.next

# ==========================================
# 2. 插入操作 (Insertion)
# ==========================================

# --- 2.1 在单链表头部插入新节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 在单链表头部插入一个新节点 0
newNode = ListNode(0)
newNode.next = head
head = newNode



# --- 2.2 在单链表尾部插入新节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 遍历到链表尾部，插入一个新节点 6
p = head
while p.next is not None:
    p = p.next
p.next = ListNode(6)


# --- 2.3 在单链表中间插入新节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 在第 3 个节点后面插入一个新节点 66
# 步骤 1：寻找前驱节点（即第 3 个节点）
p = head
for _ in range(2):
    p = p.next

# 此时 p 指向第 3 个节点 (val=3)
# 步骤 2：组装新节点，并将其 next 指针指向前驱节点的原始后继节点
new_node = ListNode(66)
new_node.next = p.next

# 步骤 3：将前驱节点的 next 指针指向新节点
p.next = new_node

# 最终链表形态：1 -> 2 -> 3 -> 66 -> 4 -> 5



# ==========================================
# 3. 删除操作 (Deletion)
# ==========================================

# --- 3.1 在单链表中间删除节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 删除第 4 个节点 (val=4)，需要通过操作其前驱节点来完成
# 步骤 1：寻找前驱节点（即第 3 个节点）
p = head
for i in range(2):
    p = p.next

# 此时 p 指向第 3 个节点 (val=3)，即待删除节点的前驱节点
# 步骤 2：跳过待删除节点，直接将前驱节点指向后继节点
p.next = p.next.next

# 最终链表形态：1 -> 2 -> 3 -> 5


# --- 3.2 在单链表尾部删除节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 删除尾节点 (val=5)
p = head
# 步骤 1：遍历寻找到倒数第二个节点
while p.next.next is not None:
    p = p.next

# 此时 p 指向倒数第二个节点 (val=4)
# 步骤 2：将倒数第二个节点的 next 指针置为空，从而摘除尾节点
p.next = None

# 最终链表形态：1 -> 2 -> 3 -> 4



# --- 3.3 在单链表头部删除节点 ---
head = createLinkedList([1, 2, 3, 4, 5])

# 删除头节点 (val=1)
# 直接将头指针向后移动一位即可
head = head.next

# 最终链表形态：2 -> 3 -> 4 -> 5


#############################################
class MyLinkedList2:

    class Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.head = self.Node(None)
        self.tail = self.head
        self.size = 0

    def add_first(self, e):
        new_node = self.Node(e)
        new_node.next = self.head.next
        self.head.next = new_node
        if self.size == 0:
            self.tail = new_node
        self.size += 1

    def add_last(self, e):
        new_node = self.Node(e)
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def add(self, index, element):
        self.check_position_index(index)

        if index == self.size:
            self.add_last(element)
            return

        prev = self.head
        for i in range(index):
            prev = prev.next
        new_node = self.Node(element)
        new_node.next = prev.next
        prev.next = new_node
        self.size += 1

    def remove_first(self):
        if self.is_empty():
            raise Exception("NoSuchElementException")
        first = self.head.next
        self.head.next = first.next
        if self.size == 1:
            self.tail = self.head
        self.size -= 1
        return first.val

    def remove_last(self):
        if self.is_empty():
            raise Exception("NoSuchElementException")

        prev = self.head
        while prev.next != self.tail:
            prev = prev.next
        val = self.tail.val
        prev.next = None
        self.tail = prev
        self.size -= 1
        return val

    def remove(self, index):
        self.check_element_index(index)

        prev = self.head
        for i in range(index):
            prev = prev.next

        node_to_remove = prev.next
        prev.next = node_to_remove.next
        # 删除的是最后一个元素
        if index == self.size - 1:
            self.tail = prev
        self.size -= 1
        return node_to_remove.val

    # ***** 查 *****

    def get_first(self):
        if self.is_empty():
            raise Exception("NoSuchElementException")
        return self.head.next.val

    def get_last(self):
        if self.is_empty():
            raise Exception("NoSuchElementException")
        return self.tail.val

    def get(self, index):
        self.check_element_index(index)
        p = self.get_node(index)
        return p.val

    # ***** 改 *****

    def set(self, index, element):
        self.check_element_index(index)
        p = self.get_node(index)

        old_val = p.val
        p.val = element

        return old_val

    # ***** 其他工具函数 *****
    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def is_element_index(self, index):
        return 0 <= index < self.size

    def is_position_index(self, index):
        return 0 <= index <= self.size

    # 检查 index 索引位置是否可以存在元素
    def check_element_index(self, index):
        if not self.is_element_index(index):
            raise IndexError(f"Index: {index}, Size: {self.size}")

    # 检查 index 索引位置是否可以添加元素
    def check_position_index(self, index):
        if not self.is_position_index(index):
            raise IndexError(f"Index: {index}, Size: {self.size}")

    # 返回 index 对应的 Node
    # 注意：请保证传入的 index 是合法的
    def get_node(self, index):
        p = self.head.next
        for i in range(index):
            p = p.next
        return p

if __name__ == "__main__":
    list = MyLinkedList2()
    list.add_first(1)
    list.add_first(2)
    list.add_last(3)
    list.add_last(4)
    list.add(2, 5)

    print(list.remove_first())  # 2
    print(list.remove_last())   # 4
    print(list.remove(1))       # 5

    print(list.get_first())     # 1
    print(list.get_last())      # 3
    print(list.get(1))          # 3


#######################################################

# 单链表代码中的 tail 是实际的尾节点引用，不是虚拟尾节点。持有尾节点引用可以让 addLast 达到 O(1) 复杂度，这在文章「关键点一」中有解释。