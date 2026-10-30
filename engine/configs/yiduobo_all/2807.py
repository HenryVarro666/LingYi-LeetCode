CONFIG = dict(
    num=2807, title='在链表中插入最大公约数', difficulty='Medium', category='链表',
    author='yiduobo', technique='一趟遍历 · 边走边插入',
    tags=['灵神题单·数学算法', '灵神题单·链表树与回溯', '难度分 1279'],
    code='''
class Solution(object):
    def insertGreatestCommonDivisors(self, head):

        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        now = head
        while now.next:
            node = ListNode(gcd(now.val, now.next.val), now.next)
            now.next = node
            now = now.next.next
        
        return head
''',
    setup='head = L([18, 6, 10, 3])',
    call='Solution().insertGreatestCommonDivisors(head)',
    expect=[18, 6, 6, 2, 10, 1, 3],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（运行中新建的节点在下一行）', pointers={'now': 'blue', 'node': 'green'}, h=470),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('node', 'node', 'green')],
    skip=['while y > 0', 'x, y = y, x % y', 'return x'],
    captions={
        'def gcd': '自己写的辗转相除 `gcd`',
        'now = head': '`now` 指向头节点，从这里开始往后走',
        'while now.next': lambda S, B, ret: ('`now` 有后继 → 要在 `now` 和 `now.next` 之间插入新节点' if B.now.next else '`now` 已在链表末尾，没有后继 → ==遍历结束=='),
        'node = ListNode': '求 `gcd({now.val}, {now.next.val})`，造新节点，==让它的 `next` 先指向 `now.next`==（原后继）',
        'now.next = node': '再把 `now.next` 指向 `node`：新节点插入到 `now` 和原后继之间',
        'now = now.next.next': '`now.next` 已经是新节点，不是原后继 → ==要跳两步==才到 `{now.val}`',
        'return head': '头节点没变，返回 `head`',
    },
    cards=dict(
        one_liner='先让新节点指向后继，再让当前节点指向新节点',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['在每对相邻节点之间插入一个节点，值为它们的最大公约数',
                 '示例：`[18,6,10,3]` → `[18,6,6,2,10,1,3]`'],
        quote='需要先将node.next指向到now.next，然后再将now.next指向到node。',
        quote_src='—— yiduobo 题解原文',
        idea=['顺序很重要：先接后面（`node.next`），再接前面（`now.next`）',
              '插完之后 `now.next` 变成了新节点，不再是原来的后继',
              '所以每次移动要把 `now` 置为 `now.next.next`'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '易错点：忘记跳两步，会拿新节点当 `now` 继续插入',
                 '代码里的 `gcd` 是自己写的辗转相除（`while y > 0`），没有用库函数',
                 '原文代码已是 Python 3 可运行写法，没有改动'],
    ),
)
