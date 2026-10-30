CONFIG = dict(
    num=2807, title='在链表中插入最大公约数', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='遍历链表 · 原地插入',
    tags=['灵神题单·数学算法', '灵神题单·链表树与回溯', '难度分 1279'],
    code='''
class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur.next:
            cur.next = ListNode(gcd(cur.val, cur.next.val), cur.next)
            cur = cur.next.next
        return head
''',
    setup='head = L([18, 6, 10, 3])',
    call='Solution().insertGreatestCommonDivisors(head)',
    expect=[18, 6, 6, 2, 10, 1, 3],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f"当前相邻两个数：`gcd({S['cur'].val}, {S['cur'].next.val})` = =={__import__('math').gcd(S['cur'].val, S['cur'].next.val)}==" if S.get('cur') is not None and S['cur'].next is not None and S['_line'] == 4 else ''), h=80, size=32),
        dict(type='linked', label='链表（新建节点在下一行）', pointers={'cur': 'blue'}, h=420),
    ],
    watch=[('cur', 'cur.val if cur else None', 'blue')],
    captions={
        'cur = head': '`cur` 从头节点出发',
        'while cur.next': lambda S, B, ret: ('`cur.next` 存在 → 后面还有相邻节点，需要在两者之间插入 gcd' if B.cur.next else '`cur.next` 为空 → ==没有相邻节点了==，结束'),
        'cur.next = ListNode': '新建 gcd 节点 `{cur.next.val}`，它的 `next` 指向 `cur` 原来的下一个节点，再让 `cur.next` 指向它：==先接后面，再接前面==，不会断链',
        'cur = cur.next.next': '`cur.next` 现在是刚插入的 gcd 节点，所以要跳两步，到达原来的下一个节点 `{cur.val}`',
        'return head': '头节点没变，直接返回 `head`',
    },
    cards=dict(
        one_liner='在当前节点后插入 gcd 节点，再跳过它走两步',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['在链表每对==相邻节点==之间，插入一个值为两者最大公约数的新节点',
                 '示例：`[18,6,10,3]` → `[18,6,6,2,10,1,3]`',
                 '只有一个节点时没有相邻对，原样返回'],
        quote='在当前节点 cur 后面插入 gcd 节点，同时 gcd 节点指向 cur 的下一个节点。插入后，cur 更新为 cur.next.next。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ListNode(gcd(...), cur.next)`：新节点一出生就指向 `cur` 的下一个节点',
              '再把 `cur.next` 改成新节点，链表不会断',
              '插入后 `cur.next` 是新节点，所以 `cur` 要跳两步回到原节点'],
        summary=['时间 `O(n log U)`（每次 gcd 要 `O(log U)`），空间 `O(1)`',
                 '易错点：`cur = cur.next` 只走一步会走到新节点，造成死循环或重复插入',
                 '循环条件是 `cur.next`，不是 `cur`：最后一个节点后面不插入',
                 '头节点不会变，不需要哨兵节点'],
    ),
)
