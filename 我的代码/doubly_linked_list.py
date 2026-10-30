class DoublyListNode:
    """双向链表节点类"""
    def __init__(self, x):
        self.val = x
        self.next = None
        self.prev = None
        
def createDoublyLinkedList(arr: List[int]) -> Optional[DoublyListNode]:
    """
    根据数组创建双向链表
    """
    if not arr:
        return None
    
    head = DoublyListNode(arr[0])
    cur = head
    
    # 迭代创建双向链表节点
    for val in arr[1:]:
        new_node = DoublyListNode(val)
        cur.next = new_node
        new_node.prev = cur
        cur = cur.next
    
    return head


# ==========================================
# 1. 遍历操作 (Traversal)
# ==========================================

# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])
tail = None

# 从头节点向后遍历双向链表
p = head
while p:
    print(p.val)
    tail = p
    p = p.next

# 从尾节点向前遍历双向链表
p = tail
while p:
    print(p.val)
    p = p.prev


# ==========================================
# 2. 插入操作 (Insertion)
# ==========================================

# --- 2.1 在双向链表头部插入新节点 ---
# 创建一条双向链表
head = create_doubly_linked_list([1, 2, 3, 4, 5])

# 在双向链表头部插入新节点 0
new_head = DoublyListNode(0)
new_head.next = head
head.prev = new_head
head = new_head
# 结果: 0 <-> 1 <-> 2 <-> 3 <-> 4 <-> 5


# --- 2.2 在双向链表尾部插入新节点 ---
# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])

tail = head
# 遍历找到链表的最后一个节点
while tail.next is not None:
    tail = tail.next

# 在双向链表尾部插入新节点 6
newNode = DoublyListNode(6)
tail.next = newNode
newNode.prev = tail
# 更新尾节点引用
tail = newNode

# 结果: 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6


# --- 2.3 在双向链表中间插入新节点 ---
# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])

# 目标：插入到索引 3（即第 4 个节点）的位置
# 需要操作索引 2（即第 3 个节点）的指针
p = head
for _ in range(2):
    p = p.next

# 组装新节点 66
newNode = DoublyListNode(66)
newNode.next = p.next
newNode.prev = p

# 插入新节点并更新前后节点的指针
p.next.prev = newNode
p.next = newNode

# 结果: 1 <-> 2 <-> 3 <-> 66 <-> 4 <-> 5


# ==========================================
# 3. 删除操作 (Deletion)
# ==========================================

# --- 3.1 在双向链表中间删除节点 ---
# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])

# 目标：删除第 4 个节点
# 首先定位到第 3 个节点
p = head
for i in range(2):
    p = p.next

# p 当前指向第 3 个节点，我们将摘除其后续节点
toDelete = p.next

# 将目标节点从链表中摘除
p.next = toDelete.next
toDelete.next.prev = p

# 断开被删除节点的前后指针（推荐做法以防内存泄漏）
toDelete.next = None
toDelete.prev = None

# 结果: 1 <-> 2 <-> 3 <-> 5


# --- 3.2 在双向链表头部删除节点 ---
# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])

# 删除头节点
toDelete = head
head = head.next
head.prev = None

# 清理已删除节点的指针
toDelete.next = None

# 结果: 2 <-> 3 <-> 4 <-> 5


# --- 3.3 在双向链表尾部删除节点 ---
# 创建一条双向链表
head = createDoublyLinkedList([1, 2, 3, 4, 5])

# 寻找尾节点
p = head
while p.next is not None:
    p = p.next

# p 当前指向尾节点
# 将尾节点从链表中摘除
p.prev.next = None

# 断开被删除节点的前后指针（推荐做法）
p.prev = None

# 结果: 1 <-> 2 <-> 3 <-> 4



#######################################################
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

class MyLinkedList:
    # 虚拟头尾节点
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    # ***** 增 *****

    def add_last(self, e):
        x = Node(e)
        temp = self.tail.prev

        temp.next = x
        x.prev = temp
        # temp <-> x

        x.next = self.tail
        self.tail.prev = x
        # temp <-> x <-> tail
        self.size += 1

    def add_first(self, e):
        x = Node(e)
        temp = self.head.next
        # head <-> temp
        temp.prev = x
        x.next = temp

        self.head.next = x
        x.prev = self.head
        # head <-> x <-> temp
        self.size += 1

    def add(self, index, element):
        self.check_position_index(index)
        if index == self.size:
            self.add_last(element)
            return

        # 找到 index 对应的 Node
        p = self.get_node(index)
        temp = p.prev
        # temp <-> p

        # 新要插入的 Node
        x = Node(element)

        p.prev = x
        temp.next = x

        x.prev = temp
        x.next = p

        # temp <-> x <-> p

        self.size += 1

    # ***** 删 *****

    def remove_first(self):
        if self.size < 1:
            raise IndexError("No elements to remove")
        # 虚拟节点的存在是我们不用考虑空指针的问题
        x = self.head.next
        temp = x.next
        # head <-> x <-> temp
        self.head.next = temp
        temp.prev = self.head

        # head <-> temp

        self.size -= 1
        return x.val

    def remove_last(self):
        if self.size < 1:
            raise IndexError("No elements to remove")
        x = self.tail.prev
        temp = x.prev
        # temp <-> x <-> tail

        self.tail.prev = temp
        temp.next = self.tail

        # temp <-> tail

        self.size -= 1
        return x.val

    def remove(self, index):
        self.check_element_index(index)
        # 找到 index 对应的 Node
        x = self.get_node(index)
        prev = x.prev
        next = x.next
        # prev <-> x <-> next
        prev.next = next
        next.prev = prev

        self.size -= 1

        return x.val

    # ***** 查 *****

    def get(self, index):
        self.check_element_index(index)
        # 找到 index 对应的 Node
        p = self.get_node(index)

        return p.val

    def get_first(self):
        if self.size < 1:
            raise IndexError("No elements in the list")

        return self.head.next.val

    def get_last(self):
        if self.size < 1:
            raise IndexError("No elements in the list")

        return self.tail.prev.val

    # ***** 改 *****

    def set(self, index, val):
        self.check_element_index(index)
        # 找到 index 对应的 Node
        p = self.get_node(index)

        old_val = p.val
        p.val = val

        return old_val

    # ***** 其他工具函数 *****

    def size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def get_node(self, index):
        self.check_element_index(index)
        p = self.head.next
        # TODO: 可以优化，通过 index 判断从 head 还是 tail 开始遍历
        for _ in range(index):
            p = p.next
        return p

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

    def display(self):
        print(f"size = {self.size}")
        p = self.head.next
        while p != self.tail:
            print(f"{p.val} <-> ", end="")
            p = p.next
        print("null")

if __name__ == "__main__":
    list = MyLinkedList()
    list.add_last(1)
    list.add_last(2)
    list.add_last(3)
    list.add_first(0)
    list.add(2, 100)

    list.display()
    # size = 5
    # 0 <-> 1 <-> 100 <-> 2 <-> 3 <-> null