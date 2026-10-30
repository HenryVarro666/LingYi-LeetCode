CONFIG = dict(
    num=237, title='删除链表中的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='后继值覆盖 + 删后继',
    tags=['删除节点'],
    code='''
class Solution(object):
    def deleteNode(self, node):

        node.val = node.next.val
        node.next = node.next.next
''',
    setup='''
head = L([4,5,1,9])
node = head.next.next
''',
    call='Solution().deleteNode(node)\nlist_vals(head)',
    expect=[4, 5, 9],
    views=[
        dict(type='linked', label='链表（只给了 node，没有上一个节点）', pointers={'node': 'blue'}, h=300),
        dict(type='text', fn=lambda S: f"`node.val` = =={S['node'].val}==，后继 `node.next.val` = =={S['node'].next.val if S['node'].next else '-'}=="
                                       if 'node' in S else '', size=34),
    ],
    watch=[('node.val', 'node.val', 'blue')],
    captions={
        'node.val = node.next.val': '没有上一个节点，`prev.next = prev.next.next` 用不了。把 `node.next` 的值赋给 `node`：`node.val` = =={node.val}==',
        'node.next = node.next.next': '再删去 `node.next`：此时它和 `node` 值相同，==相当于删掉了原来的 node==',
    },
    cards=dict(
        one_liner='没有前驱就“变相”删除：用后继覆盖自己，再删后继',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['删除链表中给定的节点 `node`，但==没有给上一个节点==',
                 '保证 `node` 不是最后一个节点',
                 '本视频：`[4,5,1,9]`，删值为 `1` 的节点 → `[4,5,9]`'],
        quote='注意到题目保证了给出的节点不是链表中的最后一个节点，于是在这里可以将node->next的值赋给node，然后删去node->next，就相当于变相地删去了node节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典写法 `prev.next = prev.next.next` 需要前驱，这里拿不到',
              '“不是最后一个节点”这个保证，正是提示：用后继顶替自己',
              '两行代码：覆盖值，再摘掉后继'],
        after=[dict(heading='链表是怎么变的', lines=['`node` 指向值为 `1` 的节点，它的后继值为 `9`', '先令 `node.val = 9`：链表变成 `4→5→9→9`', '再令 `node.next = node.next.next`：变成 `4→5→9`，目标值 `1` 消失'])],
        summary=['时间、空间 `O(1)`',
                 '==前提是 node 不是尾节点==，否则 `node.next.val` 会报错',
                 '实际被摘掉的是后继节点对象，只是值看起来像 node 被删'],
    ),
)
