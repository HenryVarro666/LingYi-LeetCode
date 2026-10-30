CONFIG = dict(
    num=2816, title='翻倍以链表形式表示的数字', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='逐位翻倍 · 只看下一位是否 > 4',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution:
    def doubleIt(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head.val > 4:
            head = ListNode(0, head)
        cur = head
        while cur:
            cur.val = cur.val * 2 % 10
            if cur.next and cur.next.val > 4:
                cur.val += 1
            cur = cur.next
        return head
''',
    call='Solution().doubleIt(L([1,8,9]))',
    expect=[3, 7, 8],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（高位在左）', pointers={'head': 'green', 'cur': 'blue'}, h=330),
        dict(type='text', fn=lambda S: ('当前位：`原值 × 2 % 10`，再看下一位是否 > 4 → 进位 +1' if 'cur' in S and S.get('cur') is not None else '')),
    ],
    watch=[('cur', 'cur.val if cur else None', 'blue')],
    captions={
        'if head.val > 4': lambda S, B, ret: (f'头节点 `{B.head.val}` > 4：翻倍会进位 → 需要在前面补一个新节点' if B.head.val > 4 else f'头节点 `{B.head.val}` ≤ 4：翻倍不会进位到更高位，不用补节点'),
        'head = ListNode(0, head)': '在前面插入值为 0 的新节点：它只会收到进位 → 变成 1',
        'while cur': lambda S, B, ret: ('`cur` 不为空 → 处理这一位' if B.cur else '`cur` 为空 → 所有位处理完'),
        'cur.val = cur.val * 2 % 10': '本位翻倍：`{B.cur.val} × 2 % 10` = =={cur.val}==（本位自己产生的进位已交给上一位）',
        'if cur.next and cur.next.val > 4': lambda S, B, ret: (
            f'下一位 `{B.cur.next.val}` > 4：它翻倍会进位 → 本位要 +1' if B.cur.next and B.cur.next.val > 4
            else ('下一位不大于 4：不会进位，本位不变' if B.cur.next else '没有下一位，不会有进位')),
        'cur.val += 1': '收到进位：`cur.val` → =={cur.val}==',
        'cur = cur.next': '`cur` 移到下一位',
        'return head': '返回 `head`（可能是新插入的节点）',
    },
    cards=dict(
        one_liner='翻倍只有下一位 > 4 才会进位，不用反转链表',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表每个节点是数字的一位，高位在前，不含前导零',
                 '把这个数翻倍，返回结果链表的头节点',
                 '示例：`[1,8,9]` → `[3,7,8]`（189 × 2 = 378）'],
        quote='如果不考虑进位，就是每个节点的值乘以 2。什么时候会受到进位的影响呢？只有下一个节点大于 4 的时候，才会因为进位多加一。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['每一位先 `val * 2 % 10`',
              '下一位 ≥ 5，翻倍必进 1；否则不进位',
              '链表头 > 4 时，最高位会进位，要在前面补一个节点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '灵神方法一：反转链表后当作「自己加自己」，再反转回来，同样 `O(n)`',
                 '方法二不用反转：进位只由下一位决定，一次遍历搞定',
                 '易错：头节点 > 4 时要补新节点；进位判断是 `> 4` 而不是 `> 5`'],
    ),
)
