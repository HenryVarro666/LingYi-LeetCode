CONFIG = dict(
    num=2074, title='反转偶数长度组的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='栈辅助 · 分组反转',
    tags=['灵神题单', '反转链表'],
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
    call='Solution().reverseEvenLengthGroups(L([5, 2, 6, 3, 9, 1, 7, 3, 8, 4]))',
    expect=[5, 6, 2, 3, 9, 1, 4, 8, 3, 7],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f'第 `l` = =={S["l"]}== 组，目标长度 {S["l"]}，已入栈 {len(S["stack"])} 个' if 'l' in S and 'stack' in S and S['l'] > 0 else '')),
        dict(type='linked', label='链表（最左边是假头 p_head）', pointers={'last': 'pink', 'now': 'blue', 'p_head': 'purple'}, h=330),
        dict(type='stack', var='stack', fmt=lambda x: str(x.val), label='stack（当前组的节点）', h=230),
    ],
    watch=[('l', 'l', 'cyan'), ('len(stack)', 'len(stack)', 'yellow'), ('last', 'last.val', 'pink'), ('now', 'now.val', 'blue')],
    captions={
        'stack = []': '`stack` 用来暂存==当前这一组==的节点',
        'p_head = ListNode()': '建==假头== `p_head`：第一组也有前驱',
        'p_head.next = head': '假头接到表头前面',
        'now = p_head': '`now` 站在假头，表示“已处理部分的末尾”',
        'l = 0': '`l` 是当前组的目标长度，依次 1、2、3……',
        'while now.next': lambda S, B, r: ('`now.next` 不为空，还有节点没分组' if B.now.next else '`now.next` 为空 → 全部分完'),
        'l += 1': '开始第 `{l}` 组，目标长度 `{l}`',
        'last = now': '`last` 记住这一组的==前驱==，反转后要从它接起',
        'for index in range(l)': lambda S, B, r: (f'这组最多取 `{S.l}` 个节点，第 {S.index + 1} 次' if 'index' in S else ''),
        'if now.next': lambda S, B, r: ('后面还有节点，入栈' if B.now.next else '==链表提前结束==：最后一组不足 `l` 个'),
        'stack.append': '节点 `{stack[-1].val}` 入栈，栈里共 `{len(stack)}` 个',
        'now = now.next': '`now` 前进到 {now.val}',
        'if len(stack) % 2 == 0': '栈长度 `{len(stack)}` 是{"==偶数==，这组要反转" if len(stack) % 2 == 0 else "奇数，保持原样"}（实际长度，不是目标长度）',
        'stack[0].next = now.next': '栈底（组内第一个）反转后变成组尾：先让它指向==后面的链表==',
        'while stack': lambda S, B, r: (f'栈不为空：从栈顶弹出，倒序接回' if B.stack else '栈空了，这组反转完毕'),
        'last.next = stack[-1]': '`last.next` 指向栈顶节点 `{stack[-1].val}`：==后入栈的先接==，就是反转',
        'last = last.next': '`last` 前进到 {last.val}',
        'stack.pop()': '弹出栈顶',
        'now = last': '`now` 回到反转后这组的末尾 `{last.val}`，下一组从这里开始',
        'stack = []': '奇数长度不反转，清空栈，继续下一组',
        'return p_head.next': '返回 `p_head.next`',
    },
    cards=dict(
        one_liner='用栈装下一组节点，长度是偶数就倒着接回去',
        complexity='时间 `O(n)`，空间 `O(√n)`（栈最多装一组）',
        problem=['链表按 1、2、3、4…的长度分组，把==长度为偶数==的组反转',
                 '最后一组可能不足，按==实际长度==判断奇偶',
                 '示例：`[5,2,6,3,9,1,7,3,8,4]` → `[5,6,2,3,9,1,4,8,3,7]`'],
        quote='最后一组的长度可能达不到预期，且在遍历完整个链表前是无从得知其长度的，因此还是需要先遍历，再决定是否反转。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历：把这一组的节点压进栈，数出实际长度',
              '偶数 → 从栈顶依次弹出，重新接 `next`，天然就是反转',
              '奇数 → 清空栈继续；用 `p_head` 假头避免第一组特判'],
        summary=['时间 `O(n)`，空间 `O(√n)`：栈只存一组',
                 '易错：判断用 `len(stack)`（实际长度），不是 `l`',
                 '反转后要 `stack[0].next = now.next` 先接好后面，再 `now = last` 继续',
                 '原文就是 Python 3 可运行的写法，未做改动'],
    ),
)
