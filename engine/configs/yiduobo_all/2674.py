def _cyc(res):
    out = []
    for h in res:
        vals, x = [h.val], h.next
        while x is not h:
            vals.append(x.val)
            x = x.next
        out.append(vals)
    return out


CONFIG = dict(
    num=2674, title='拆分循环链表', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='快慢指针找中点 · 断环重连',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def splitCircularLinkedList(self, list):

        fast = list.next
        slow = list

        while fast.next != list:
            slow = slow.next
            fast = fast.next
            if fast.next != list:
                fast = fast.next

        res = [list, slow.next]
        fast.next = slow.next
        slow.next = list
        return res
''',
    call='Solution().splitCircularLinkedList(L([1,5,7,3,9], 0))',
    expect=[[1, 5, 7], [3, 9]],
    result_fn=_cyc,
    views=[
        dict(type='linked', label='循环链表（尾节点指回头节点）', pointers={'list': 'green', 'slow': 'blue', 'fast': 'pink'}, h=420),
        dict(type='text', fn=lambda S: '把环从正中间切成两个环：前半段多一个节点（长度为奇数时）'),
    ],
    watch=[('slow', 'slow.val if slow else None', 'blue'), ('fast', 'fast.val if fast else None', 'pink')],
    captions={
        'fast = list.next': '`fast` 从第二个节点出发（它先领先 `slow` 一步）',
        'slow = list': '`slow` 从头节点出发',
        'while fast.next != list': lambda S, B, ret: ('`fast.next` 还不是头节点 → 没绕回一圈，继续走' if B.fast.next is not B.list
                                                      else '`fast.next` 回到了头节点 → `fast` 已是尾节点，`slow` 在前半段末尾'),
        'slow = slow.next': '`slow` 走一步 → 节点 `{slow.val}`',
        'fast = fast.next': '`fast` 走一步 → 节点 `{fast.val}`',
        'if fast.next != list': lambda S, B, ret: ('`fast.next` 不是头 → 还能再走一步' if B.fast.next is not B.list else '`fast.next` 是头 → 到尾了，不能再走（节点数为奇数时）'),
        'res = [list, slow.next]': '两段的头：前半段头 `{list.val}`，后半段头 `slow.next` = `{slow.next.val}`',
        'fast.next = slow.next': '尾节点 `{fast.val}` 的 next 指向后半段头 → ==后半段自己成环==',
        'slow.next = list': '`slow` 的 next 指回原头 → ==前半段自己成环==',
        'return res': '返回两个环的头节点 `[{res[0].val}, {res[1].val}]`',
    },
    cards=dict(
        one_liner='找到正中间的节点，两处改 next 就拆成两个环',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个循环链表，从正中间切成两段，每段仍是循环链表',
                 '节点数为奇数时，==前半段多一个节点==',
                 '本视频：`[1,5,7,3,9]` → `[1,5,7]` 和 `[3,9]`'],
        quote='因此本题实际上就是要找出这中间的两个节点。……一种经典的处理方法是快慢指针。',
        quote_src='—— yiduobo 题解原文',
        idea=['前半段最后一个节点 `slow`，它的下一个就是后半段头',
              '`fast` 每轮走两步、`slow` 走一步，`fast` 到尾时 `slow` 在中间',
              '先记下两个头，再让 `fast.next` 指后半段头、`slow.next` 指原头'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '顺序不能错：必须先用 `slow.next` 记下后半段头，再改 `slow.next`',
                 '`fast` 的第二步要先判断 `fast.next != list`，否则会越过尾节点',
                 '原文就是 Python 3 可运行的写法，无需修改（形参名 `list` 会遮住内置 list，不影响运行）'],
    ),
)
