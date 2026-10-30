CONFIG = dict(
    num=2130, title='链表最大孪生和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='快慢指针 + 反转后半段',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def pairSum(self, head):

        p_head = ListNode()
        p_head.next = head
        fast = slow = p_head
        while slow.next:
            fast = fast.next
            slow = slow.next.next
        
        now = fast.next
        last = None
        while now.next:
            tmp = now.next
            now.next = last
            last = now
            now = tmp
        now.next = last

        left = head
        right = now
        res = 0
        while right:
            res = max(res, left.val + right.val)
            left = left.next
            right = right.next
        
        return res
''',
    setup='''
import tracer, itertools
head = L([5,4,2,6,1,3])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().pairSum(head)',
    expect=8,
    views=[
        dict(type='linked', label='链表（最左边是哨兵 p_head）', pointers={'fast': 'pink', 'slow': 'blue', 'last': 'purple', 'now': 'cyan', 'left': 'green', 'right': 'orange'}, h=330),
        dict(type='text', fn=lambda S: f"当前孪生和：`{S['left'].val} + {S['right'].val}` = =={S['left'].val + S['right'].val}==" if S.get('res') is not None and S.get('left') is not None and S.get('right') is not None else ''),
    ],
    watch=['res'],
    captions={
        'p_head = ListNode()': '先建一个哨兵节点 `p_head`，让快慢指针都从它出发',
        'p_head.next = head': '哨兵接到原链表头前面',
        'fast = slow = p_head': '`fast`、`slow` 同时从哨兵出发',
        'while slow.next': lambda S, B, ret: ('`slow.next` 不为空 → 还没走到末尾，慢指针一轮走两步' if B.slow.next else '`slow.next` 为空 → `fast` 恰好停在前半段最后一个节点'),
        'fast = fast.next': '`fast` 走一步 → 节点 `{fast.val}`',
        'slow = slow.next.next': '`slow` 走两步，所以 `fast` 只走了它的一半',
        'now = fast.next': '`now` = 后半段的第一个节点 `{now.val}`，从它开始反转',
        'last = None': '`last` 保存已反转部分的头，初始为空',
        'while now.next': lambda S, B, ret: ('`now.next` 不为空 → 还没到尾节点，继续掉头' if B.now.next else '`now` 已是尾节点，退出循环单独处理'),
        'tmp = now.next': '用 `tmp` 记住后继，免得断链',
        'now.next = last': lambda S, B, ret: (f'`now` 是尾节点：让它也指向 `last`，反转完成' if not B.now.next else f'节点 `{B.now.val}` 的 next 改指向前一个，箭头掉头'),
        'last = now': '`last` 前进到 `{last.val}`',
        'now = tmp': '`now` 前进到后继 `{now.val}`',
        'left = head': '`left` 从链表头出发',
        'right = now': '`right` 从尾节点出发（反转后它是后半段的头）',
        'while right': lambda S, B, ret: ('`right` 不为空 → 还有孪生对没算' if B.right else '`right` 走完反转后的后半段 → 结束'),
        'res = max': '`left.val + right.val` = `{B.left.val} + {B.right.val}` = {B.left.val + B.right.val}，`res = max({B.res}, ...)` = =={res}==',
        'left = left.next': '`left` 向中间走',
        'right = right.next': '`right` 沿反转后的指针也向中间走',
        'return res': '最大孪生和 `{res}`',
    },
    cards=dict(
        one_liner='链表不能倒着走，就把后半段反过来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长链表，第 `i` 个节点与倒数第 `i+1` 个是孪生节点',
                 '孪生和 = 两节点值之和，求最大值',
                 '本视频：`[5,4,2,6,1,3]` → `8`（5+3，4+1，2+6）'],
        quote='对于上面从两端往中间扫的做法，当前主要的困难是链表只能单向遍历，那么一个自然的想法就是将链表的后半部分先反转。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素做法：用数组存下来，双指针从两端往中间算，空间 `O(n)`',
              '想省空间：快慢指针找中心 → 反转后半段 → 头尾同时向中心扫',
              '代码三段，正好对应这三步'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用哨兵 `p_head` 起步，快慢指针停在前半段最后一个节点',
                 '反转循环 `while now.next` 退出时，尾节点还没改指向，要补一句 `now.next = last`',
                 '原文就是 Python 3 可运行的写法，无需修改；对比灵神：灵神 `fast` 从 head 起，停在后半段起点'],
    ),
)
