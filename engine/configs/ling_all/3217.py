CONFIG = dict(
    num=3217, title='从链表中移除在数组中存在的节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='哈希集合 + 哨兵节点',
    tags=[],
    code='''
class Solution:
    def modifiedList(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        st = set(nums)
        cur = dummy = ListNode(next=head)
        while cur.next:
            nxt = cur.next
            if nxt.val in st:
                cur.next = nxt.next  # 从链表中删除 nxt 节点
            else:
                cur = nxt  # 不删除 nxt，继续向后遍历链表
        return dummy.next
''',
    setup='head = L([1,2,3,4,2,5])',
    call='Solution().modifiedList([1,2,3], head)',
    expect=[4, 5],
    result_fn=list_vals,
    views=[
        dict(type='set', var='st', label='哈希集合 st', h=110),
        dict(type='linked', label='链表（cur 之后的 nxt 是待判断节点）', pointers={'cur': 'blue', 'nxt': 'pink', 'dummy': 'purple'}, h=380),
    ],
    watch=[('cur', 'cur.val', 'blue'), ('nxt', 'nxt.val if "nxt" in S else None', 'pink')],
    captions={
        'st = set(nums)': '`nums` 放进哈希集合：判断节点值在不在 `nums` 中，从 `O(n)` 降到 ==`O(1)`==',
        'cur = dummy': '头节点可能被删 → 前面插==哨兵== `dummy`；`cur` 和 `dummy` 是同一个节点的引用',
        'while cur.next': lambda S, B, r: ('`cur.next` 不为空 → 还有节点要检查' if S.cur.next else '`cur.next` 为空 → 遍历结束'),
        'nxt = cur.next': '`nxt` 是 `cur` 的下一个节点（值 `{nxt.val}`）：这就是要判断的节点',
        'if nxt.val in st': lambda S, B, r: (f'`{S.nxt.val}` 在 `st` 中 → ==需要删除==' if S.nxt.val in S.st else f'`{S.nxt.val}` 不在 `st` 中 → 保留'),
        'cur.next = nxt.next': '`cur.next` 跳过 `nxt` → 节点 {nxt.val} 被删除；`cur` ==不动==，因为新的 next 还没判断',
        'cur = nxt': '不删 → `cur` 前进到节点 `{cur.val}`，继续向后',
        'return dummy.next': '`dummy.next` 才是新的头节点（原头可能已被删）',
    },
    cards=dict(
        one_liner='哈希集合 O(1) 判断，哨兵节点让删头不用特判',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和链表头 `head`',
                 '移除链表中所有值在 `nums` 里的节点，返回修改后的头节点',
                 '示例：`nums=[1,2,3]`，`head=[1,2,3,4,5]` → `[4,5]`',
                 '本视频：`head=[1,2,3,4,2,5]` → `[4,5]`'],
        quote='由于头节点可能会被删除，在头节点前面插入一个哨兵节点 dummy，以简化代码逻辑。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接在 `nums` 里找要 `O(n)`；先存进哈希集合，查询变 `O(1)`',
              '`cur` 站在待删节点的前一个：删 `nxt` 就是 `cur.next = nxt.next`',
              '删了 `cur` 不动，没删才前进'],
        summary=['时间 `O(n + m)`，空间 `O(n)`（集合）',
                 '易错：删除后不要移动 `cur`，否则会漏掉连续的待删节点',
                 '返回 `dummy.next`，不是 `head`',
                 '同类：83 删除排序链表重复元素、203 移除链表元素（灵神链表题单 §1.2）'],
    ),
)
