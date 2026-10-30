def _span(S):
    l, r = S.get('left'), S.get('right')
    if l is None or r is None or 'n_father' in S and S['n_father'].next is not l:
        return ''
    d, x = 1, l
    while x is not None and x is not r and d < 20:
        x, d = x.next, d + 1
    if 'n_father' in S and d != S.get('n'):
        return ''  # 指针一前一后移动的中间态，不显示
    return f'`left` 到 `right` 一共覆盖 =={d}== 个节点（目标 `n` = {S.get("n")}）'


CONFIG = dict(
    num=19, title='删除链表的倒数第 N 个结点', difficulty='Medium', category='链表',
    author='yiduobo', technique='双指针 + 记录前驱',
    code='''
class Solution(object):
    def removeNthFromEnd(self, head, n):
        left = head
        right = head
        for index in range(n - 1):
            right = right.next

        if right.next is None:
            return head.next
        else:
            n_father = head
            while right.next is not None:
                n_father = left
                left = left.next
                right = right.next

            n_father.next = n_father.next.next
            return head
''',
    call='Solution().removeNthFromEnd(L([1,2,3,4,5]), 2)',
    expect=[1, 2, 3, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_span),
        dict(type='linked', pointers={'left': 'blue', 'right': 'pink', 'n_father': 'green'}, h=420),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('n_father', 'n_father', 'green'), 'n'],
    captions={
        3: '`left` 从头开始“正常走”',
        4: '`right` 也从头出发，但它要“按特定的方法走”：先走 `n-1` 步',
        'for index in range(n - 1)': lambda S, B, ret: ('`right` 先往后走 `n-1` 步：第 {} 步'.format(S.index + 1)
                                                        if 'index' not in B or S.index != B.index else
                                                        '`right` 走完 `n-1` 步 → `left` 到 `right` 正好 `n` 个节点'),
        6: '`right` → `{right.val}`',
        'if right.next is None': lambda S, B, ret: ('`right` 已经是最后一个 → `left`（头）就是倒数第 `n` 个，删头特殊处理'
                                                    if B.right.next is None else
                                                    '`right.next` 不为空 → 要删的不是头节点，走一般情况'),
        'return head.next': '删除头节点：直接返回 `head.next`',
        'n_father = head': '`n_father` 用来记录 `left` 的前一个节点：先指向 `head`，进循环后会跟上',
        'while right.next is not None': lambda S, B, ret: ('`right` 还没到末尾 → 三个指针一起后移'
                                                           if B.right.next is not None else
                                                           '`right` 到末尾了 → `left` ==就是倒数第== `n` ==个==，`n_father` 是它左边'),
        'n_father = left': '先让 `n_father` 跟上 `left`（=`{n_father.val}`）',
        'left = left.next': '`left` → `{left.val}`',
        15: '`right` → `{right.val}`，`left` 到 `right` 始终是 `n` 个节点',
        'n_father.next = n_father.next.next': '要删除节点左侧的 `next` 指向 `next.next`：跳过 `{B.n_father.next.val}`，删除完成',
        'return head': '头节点没被删，返回 `head`',
    },
    cards=dict(
        one_liner='right 先走 n-1 步，再一起走；right 到尾时 left 就是倒数第 n 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除链表的==倒数第== `n` ==个==节点，返回头节点',
                 '示例：`head = [1,2,3,4,5], n = 2` → `[1,2,3,5]`'],
        quote='链表位置相关的问题的一个经典处理方法就是双指针法，简单来说就是一个从头开始正常走，另一个按特定的方法走，当一个走到头时另一个就是要找的节点。',
        quote_src='—— yiduobo 题解',
        idea=['`left` 从头开始，`right` 先往后走 `N` 位（代码里是 `n-1` 步，两端都落在节点上）',
              '然后一起一位一位往后走：`right` 到末尾时，`left` ==就是倒数第== `N` ==个==',
              '删除要改左侧节点的 `next`，所以额外用 `n_father` 记录 `left` 的前驱'],
        summary=['时间 `O(n)`，空间 `O(1)`，一趟扫描',
                 '没有哨兵：`right` 走完就在末尾 ⇒ 删的是头，==单独返回== `head.next`',
                 '易错：`right` 只先走 `n-1` 步，因为 `left` 自己就占了一个节点',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串，逻辑未改'],
    ),
)
