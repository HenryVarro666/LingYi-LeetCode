CONFIG = dict(
    num=2487, title='从链表中移除节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='递归：倒着遍历链表',
    tags=[],
    code='''
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head.next is None:
            return head
        node = self.removeNodes(head.next)  # 返回的链表头一定是最大的
        if node.val > head.val:
            # 执行 head'.next = node 后，我们删除了从 head'（这里的 head' 是更前面的链表节点）到 node 之间的所有节点，包括当前的 head
            return node
        head.next = node
        return head
''',
    setup='head = L([5,2,13,3,8])',
    call='Solution().removeNodes(head)',
    expect=[13, 8],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（递归从后往前返回）', pointers={'head': 'blue', 'node': 'pink'}, h=300),
        dict(type='calls', h=260),
    ],
    watch=[('head', 'head.val', 'blue'), ('node', 'node.val if "node" in S else None', 'pink')],
    captions={
        'if head.next is None': lambda S, B, r: ('`head.next` 为空 → ==递归到最后一个节点==，它右边没有更大的' if S.head.next is None
                                                  else f'`head` = {S.head.val}，后面还有节点，先递归处理后面'),
        4: '最后一个节点一定保留，返回它（值 `{head.val}`）',
        'node = self.removeNodes': '先交给递归处理 `head.next`（节点 `{head.next.val}`）：==返回的链表头一定是最大的==',
        'if node.val > head.val': lambda S, B, r: (f'`{S.node.val} > {S.head.val}` → 右边有更大的，当前 `head` ==要被删=='
                                                    if S.node.val > S.head.val else f'`{S.node.val} > {S.head.val}` → 不成立，当前 `head` 保留'),
        'return node': '直接返回 `node`：当前 `head`（以及它前面递归层里被跳过的节点）都不要了',
        'head.next = node': '`head` 保留，接上右边处理好的链表',
        10: '返回 `head`：它现在是这一段链表的头（值 `{head.val}`）',
    },
    cards=dict(
        one_liner='递归本质是倒着遍历链表：回来时就知道右边的最大值',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给链表头 `head`，移除每个==右侧有更大值==的节点',
                 '示例：`[5,2,13,3,8]` → `[13,8]`',
                 '5、2 被右边的 13 压住，3 被右边的 8 压住'],
        quote='既然要倒着看最大值，那么用递归解决是最合适的，毕竟递归本质就是在倒着遍历链表。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先递归到链表末尾，回溯时从右往左处理',
              '`removeNodes(head.next)` 返回的头==一定是右边最大的==',
              '它比 `head` 大 → 删 `head`，返回 `node`；否则 `head.next = node` 保留'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '另一种写法：反转链表后删掉比前驱小的，再反转回来，空间 `O(1)`',
                 '易错：相等的值不删（要严格更大），所以用 `node.val > head.val`',
                 '同类：单调栈思想（yiduobo 用栈实现）'],
    ),
)
