CONFIG = dict(
    num=2074, title='反转偶数长度组的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='栈辅助：先遍历一组，再决定是否反转',
    tags=['灵神题单', '链表、二叉树与回溯'],
    code='''
class Solution(object):
    def reverseEvenLengthGroups(self, head):

        stack = []
        p_head = ListNode()
        p_head.next = head

        now = p_head
        l = 0
        while now.next:
            l += 1
            last = now
            for index in range(l):
                if now.next:
                    stack.append(now.next)
                    now = now.next
                       
            if len(stack) % 2 == 0:
                stack[0].next = now.next
                while stack:
                    last.next = stack[-1]
                    last = last.next
                    stack.pop()

                now = last

            else:
                stack = []
        
        return p_head.next
''',
    call='Solution().reverseEvenLengthGroups(head)',
    setup='head = L([5,2,6,3,9,1,7,3,8,4])',
    expect=[5, 6, 2, 3, 9, 1, 4, 8, 3, 7],
    result_fn=list_vals, max_steps=90,
    views=[
        dict(type='linked', label='链表（粉 = last 组前一个，蓝 = now 已读到的位置）', pointers={'last': 'pink', 'now': 'blue', 'p_head': 'purple'}, h=300),
        dict(type='stack', var='stack', fmt=lambda x: str(x.val), label='stack：当前组的节点（栈底在左）', h=200),
    ],
    watch=['l', ('len(stack)', 'len(stack)', 'cyan')],
    captions={
        4: '`stack` 用来存当前这一组的节点',
        'p_head = ListNode()': '加一个哨兵 `p_head`，头节点被反转时也不用特判',
        'p_head.next = head': '哨兵接到原链表前面',
        'now = p_head': '`now` 指向哨兵，表示「已经读完的最后一个节点」',
        'l = 0': '`l` 是当前组应有的长度',
        'while now.next': lambda S, B, ret: ('`now` 后面还有节点 → 开始新的一组' if S.now.next else '`now` 后面没有节点了 → 全部分完'),
        'l += 1': '新的一组，目标长度 `l` = {l}',
        'last = now': '`last` 记下这一组的前一个节点，反转后要从它接回去',
        'for index in range(l)': '尝试读 `l` = {l} 个节点：第 {index + 1} 个',
        'if now.next': lambda S, B, ret: ('后面还有节点，可以读' if S.now.next else '链表到头了，最后一组不满，就按实际读到的个数算'),
        'stack.append': '节点 `{now.next.val}` 入栈，当前组已有 `{len(stack)}` 个',
        'now = now.next': '`now` 前进到节点 `{now.val}`',
        'if len(stack) % 2': lambda S, B, ret: (f'栈里有 `{len(S.stack)}` 个节点，==偶数== → 要反转' if len(S.stack) % 2 == 0 else f'栈里有 `{len(S.stack)}` 个节点，奇数 → 不反转'),
        'stack[0].next': '栈底是这一组原来的第一个节点，反转后它排最后 → 先让它指向后面的 `now.next`',
        'while stack': lambda S, B, ret: ('栈不空，继续弹出' if S.stack else '栈空了，这一组反转完'),
        'last.next = stack[-1]': '把栈顶（原来这组的最后一个）接到 `last` 后面：节点 `{stack[-1].val}`',
        'last = last.next': '`last` 前进一格',
        'stack.pop()': '弹出栈顶，栈里剩 `{len(stack)}` 个',
        'now = last': '`now` 对齐到这一组的新末尾，准备读下一组',
        28: '奇数组不反转：清空栈，继续往后',
        'return p_head.next': '返回哨兵后面的节点，才是真正的头',
    },
    cards=dict(
        one_liner='先把一组节点压进栈，数完个数再决定反不反',
        complexity='时间 `O(n)`，空间 `O(√n)`',
        problem=['链表按 `1, 2, 3, …` 的长度分组，把长度为偶数的组反转',
                 '示例：`[5,2,6,3,9,1,7,3,8,4]` → `[5,6,2,3,9,1,4,8,3,7]`'],
        quote='由于必须要先执行遍历，所以我才用了栈辅助的做法，在遍历过程中使用栈储存当前这一组的节点，然后通过栈的长度判断当前组是否需要翻转。',
        quote_src='—— yiduobo 题解原文',
        idea=['最后一组可能不满，只有读完才知道实际长度，所以先遍历再决定',
              '偶数：从栈顶依次弹出，接到 `last` 后面，顺序正好反过来',
              '奇数：清空栈即可，链表保持原样'],
        summary=['时间 `O(n)`，空间 `O(√n)`（栈最多存一组）',
                 '反转时别忘了 `stack[0].next = now.next`，否则会断链',
                 '反转后要 `now = last`，让下一组从新的末尾开始',
                 '对比灵神：灵神只交换节点的值，这里真正改 `next` 指针'],
    ),
)
