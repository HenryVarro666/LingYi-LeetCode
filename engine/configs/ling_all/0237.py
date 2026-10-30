CONFIG = dict(
    num=237, title='删除链表中的节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='复制后继节点再删后继',
    tags=['删除节点'],
    code='''
class Solution:
    def deleteNode(self, node: ListNode) -> None:
        node.val = node.next.val
        node.next = node.next.next
''',
    setup='''
head = L([4,5,1,9])
node = head.next
''',
    call='Solution().deleteNode(node)\nlist_vals(head)',
    expect=[4, 1, 9],
    views=[
        dict(type='linked', label='链表（拿不到 head，只给了 node）', pointers={'node': 'blue'}, h=300),
        dict(type='text', fn=lambda S: f"`node.val` = =={S['node'].val}==，`node.next.val` = =={S['node'].next.val if S['node'].next else '-'}=="
                                       if 'node' in S else '', size=34),
    ],
    watch=[('node.val', 'node.val', 'blue')],
    captions={
        'node.val = node.next.val': '不知道前一个节点 → 无法改它的 `next`。改用：把后继的值抄过来，`node.val` = =={node.val}==，看上去 5 已经不见了',
        'node.next = node.next.next': '现在有两个相同的节点，删掉后面那个：`node.next` 跳过它 → ==链表少了一个节点==',
    },
    cards=dict(
        one_liner='拿不到前一个节点？把后一个节点的值抄过来，再删后一个',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['只给你要删除的节点 `node`（不是尾节点），==拿不到 head==',
                 '删除后：链表值少一个，其余顺序不变',
                 '示例：`[4,5,1,9]`，删 `5` → `[4,1,9]`'],
        quote='本题只告诉我们当前节点 node，我们不知道 node 的前一个节点是谁。难道就没法删除了吗？注意题目的要求：我们只需让链表「看上去」删除了 node。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把 `node.val` 换成 `node.next.val`：`4→1→1→9`',
              '再让 `node.next = node.next.next`，删掉多出的那个 → `4→1→9`',
              '本质是“删后继”，题目保证了 node 不是尾节点'],
        after=[dict(heading='链表是怎么变的', lines=['看上去的链表：`4→5→1→9` 被改成 `4→1→1→9`，再变成 `4→1→9`', '打印整条链表只会看到 `4,1,9`，题目就认为 `5` 被删除了', '真正被丢弃的是原来 `1` 那个节点对象，`node` 自己留了下来'])],
        summary=['时间、空间都是 `O(1)`',
                 '==不是真的删掉 node，而是让链表“看上去”少了它的值==',
                 '前提：node 不是尾节点，否则没有后继可抄',
                 '灵神注：支持解引用的语言可以直接把 node 更新成下一个节点'],
    ),
)
