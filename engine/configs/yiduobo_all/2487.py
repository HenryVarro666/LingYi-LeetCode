CONFIG = dict(
    num=2487, title='从链表中移除节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='单调栈 · 边弹边连',
    tags=[],
    code='''
class Solution(object):
    def removeNodes(self, head):

        stack = []

        now = head
        while now:
            while stack and now.val > stack[-1].val:
                stack.pop()
            
            if stack:
                stack[-1].next = now
            stack.append(now)
            now = now.next
        
        return stack[0]
''',
    setup='head = L([5,2,13,3,8])',
    call='Solution().removeNodes(head)',
    expect=[13, 8],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表', pointers={'now': 'blue'}, h=300),
        dict(type='stack', var='stack', fmt=lambda x: str(x.val), label='栈（存节点，栈底到栈顶递减）', h=260),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('栈顶', 'stack[-1].val if stack else None', 'green')],
    captions={
        'stack = []': '用一个栈存“目前还没被淘汰的节点”',
        'now = head': '`now` 从头开始处理',
        'while now': lambda S, B, r: (f'`now` = 节点 {S.now.val} → 要处理它' if S.now else '`now` 为空 → 全部处理完'),
        'while stack and now.val > stack[-1].val': lambda S, B, r: (
            '栈空 → 没有节点能压住 `now`' if not S.stack else
            (f'栈顶 `{S.stack[-1].val}` < `now` = `{S.now.val}` → 栈顶右边有更大的，==要被移除==' if S.now.val > S.stack[-1].val
             else f'栈顶 `{S.stack[-1].val}` ≥ `now` = `{S.now.val}` → 栈顶保留，停止弹出')),
        'stack.pop()': '弹出栈顶：这个节点被 `{now.val}` 压住，从答案里删去',
        'if stack': lambda S, B, r: ('栈不空 → 栈顶是 `now` 的前一个保留节点' if S.stack else '栈空 → `now` 暂时是链表最前面的保留节点'),
        'stack[-1].next = now': '栈顶的 `next` 直接指向 `now`：==跳过中间被弹出的节点==',
        'stack.append(now)': '`now` 入栈，成为新的栈顶',
        'now = now.next': '处理下一个节点',
        'return stack[0]': '栈底是值最大的节点，也就是答案的头：`{stack[0].val}`',
    },
    cards=dict(
        one_liner='用栈存保留的节点，来个更大的就把小的弹掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给单链表头 `head`，移除每个右侧有更大值的节点',
                 '示例：`[5,2,13,3,8]` → `[13,8]`'],
        quote='根据题目删除节点的顺序，很容易想到使用一个栈来储存当前链表中剩余的节点，那么对于接下来遍历到的节点now，若当前栈不为空，且栈顶节点值小于now.val，那么就将栈顶节点从栈中弹出。',
        quote_src='—— yiduobo 题解原文',
        idea=['单链表删掉节点后找不到前驱 → 用栈保存还活着的节点',
              '新节点 `now` 比栈顶大 → 栈顶右边有更大的 → 弹出',
              '入栈前把栈顶的 `next` 指向 `now`，最后栈底就是头'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '严格大于才弹：相等的节点保留',
                 '这里边弹边连 `stack[-1].next = now`，所以直接返回 `stack[0]`',
                 '原文为 Python 2 风格类声明，代码无需改动'],
    ),
)
