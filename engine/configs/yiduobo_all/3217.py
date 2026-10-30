CONFIG = dict(
    num=3217, title='从链表中移除在数组中存在的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='集合判重 · 假头 · 删 next',
    tags=[],
    code='''
class Solution(object):
    def modifiedList(self, nums, head):

        p_head = ListNode()
        p_head.next = head
        nums_set = set(nums)
        p = p_head
        while p.next:
            if p.next.val in nums_set:
                p.next = p.next.next
            else:
                p = p.next
        
        return p_head.next
''',
    setup='head = L([1,2,3,4,2,5])',
    call='Solution().modifiedList([1,2,3], head)',
    expect=[4, 5],
    result_fn=list_vals,
    views=[
        dict(type='set', var='nums_set', label='nums_set', h=110),
        dict(type='linked', label='链表（p 的下一个节点是待判断的）', pointers={'p': 'blue', 'p_head': 'purple'}, h=380),
    ],
    watch=[('p', 'p.val', 'blue'), ('p.next', 'p.next.val if p.next else None', 'pink')],
    captions={
        'p_head = ListNode()': '新建一个==假头节点== `p_head`：头节点也可能被删，有它就不用特判',
        'p_head.next = head': '`p_head.next` 指向真正的头节点',
        'nums_set = set(nums)': '把 `nums` 变成集合：判断“值是否出现过”从 `O(m)` 降到 `O(1)`',
        'p = p_head': '`p` 从假头出发，==永远看 p.next 要不要删==',
        'while p.next': lambda S, B, r: ('`p.next` 不为空 → 还有节点要判断' if S.p.next else '`p.next` 为空 → 链表走完'),
        'if p.next.val in nums_set': lambda S, B, r: (f'`{S.p.next.val}` 在集合里 → ==要删=='
                                                       if S.p.next.val in S.nums_set else f'`{S.p.next.val}` 不在集合里 → 保留'),
        'p.next = p.next.next': '删 `p.next`：让 `p.next` 直接指向再下一个。==无需记录上一个节点==，`p` 不动（新的 next 还没判断）',
        'p = p.next': '`p.next` 要保留 → `p` 前进一步，现在是 `{p.val}`',
        'return p_head.next': '返回 `p_head.next`：新的头节点',
    },
    cards=dict(
        one_liner='删 p 的 next 而不是 p 自己，配一个假头节点',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和链表头 `head`',
                 '移除链表中所有值在 `nums` 里出现过的节点，返回新链表头',
                 '示例：`nums=[1,2,3]`，`head=[1,2,3,4,5]` → `[4,5]`',
                 '本视频：`nums=[1,2,3]`，`head=[1,2,3,4,2,5]` → `[4,5]`'],
        quote='对于链表中移除节点的操作，一般是通过移除当前节点now的next而不是now自身，理由是移除now后需要将now的上一个节点的next指向当前now.next，需要额外记录上一个节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `nums` 变成集合，判断是否出现过是 `O(1)`',
              '删当前节点要知道前驱；删 `p.next` 就不需要',
              '头节点可能被删 → 加假头 `p_head`'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '删除后 `p` ==不要前进==：新的 `p.next` 还没判断，可能连续要删',
                 '返回 `p_head.next` 而不是 `head`',
                 '原文为 Python 2 风格类声明，代码无需改动'],
    ),
)
