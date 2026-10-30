CONFIG = dict(
    num=369, title='给单链表加一', difficulty='Medium', category='链表',
    author='yiduobo', technique='找最后一个非 9 节点',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def plusOne(self, head):

        p = None
        now = head
        while now:
            if now.val != 9:
                p = now
            now = now.next
        
        if p is None:
            res = ListNode(val = 1, next = head)
            now = res.next
            while now:
                now.val = 0
                now = now.next
            return res
        else:
            p.val += 1
            now = p.next
            while now:
                now.val = 0
                now = now.next
            return head
''',
    setup='head = L([1, 2, 9, 9])',
    call='Solution().plusOne(head)',
    expect=[1, 3, 0, 0],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（每个节点是数字的一位，高位在前）', pointers={'p': 'pink', 'now': 'blue'}, h=420),
    ],
    watch=[('p（最后一个非9）', 'p', 'pink'), ('now', 'now', 'blue')],
    captions={
        'p = None': '`p` 记录==最后一个不是 9 的节点==，先设为空',
        'now.val != 9': lambda S, B, ret: (f'`now.val` = {B.now.val}，不是 9 → 进位会停在这里，更新 `p` 为这个节点'
                                           if B.now.val != 9 else f'`now.val` = 9 → 加一时它会变成 0 并继续进位，`p` 不动'),
        'p = now': '`p` → 节点 `{p.val}`：目前最后一个非 9 节点',
        'now = now.next': '`now` 向后走一步',
        'if p is None': lambda S, B, ret: ('`p` 为空 → 全是 9，进位会一直传到最高位，要新增头节点' if B.p is None
                                           else f'`p` 不为空 → 进位停在值为 `{B.p.val}` 的节点，不需要新节点'),
        'res = ListNode': '全是 9：在最前面加一个值为 1 的新头节点',
        'p.val += 1': '`p` 这一位加 1：`{B.p.val}` → =={p.val}==（进位在这里停下）',
        'now = p.next': '`p` 后面全是 9，从 `p.next` 开始把它们变成 0',
        'now.val = 0': '`9 + 1` 进位 → 这一位变成 ==0==',
        'return res': '返回新头节点 `res`',
        'return head': '头节点没变，直接返回 `head`',
    },
    cards=dict(
        one_liner='进位只会在最后一个非 9 的位置停下',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表表示一个非负整数，每个节点一位，高位在前',
                 '给这个整数加一，返回新链表',
                 '示例：`1→2→9→9`（1299）→ `1→3→0→0`（1300）'],
        quote='如果出现进位，那么链表的最后若干个值必然都是9，而进位则会在链表中最后一个不为9的位置停下来。',
        quote_src='—— yiduobo 题解',
        idea=['先扫一遍，找出最后一个值不是 9 的节点 `p`',
              '找到了：`p` 加一，它后面的 9 全变成 0',
              '没找到：全是 9，头部补一个 1，其余全置 0'],
        summary=['时间 `O(n)`，空间 `O(1)`，只用两趟遍历，不用反转链表',
                 '易错点：全是 9 时要新增头节点，返回的是 `res` 而不是 `head`',
                 '`p` 找的是最后一个非 9，不是第一个',
                 '同类题：66 加一（数组版）、2 两数相加'],
    ),
)
