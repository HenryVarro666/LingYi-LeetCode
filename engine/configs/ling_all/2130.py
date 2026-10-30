CONFIG = dict(
    num=2130, title='链表最大孪生和', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='快慢指针 + 反转后半段',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution:
    # 876. 链表的中间结点
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    # 206. 反转链表
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def pairSum(self, head: Optional[ListNode]) -> int:
        mid = self.middleNode(head)
        head2 = self.reverseList(mid)

        ans = 0
        while head2:
            ans = max(ans, head.val + head2.val)
            head = head.next
            head2 = head2.next
        return ans
''',
    call='Solution().pairSum(L([4,2,7,3,1,5]))',
    expect=10,
    views=[
        dict(type='linked', label='链表', pointers={'slow': 'blue', 'fast': 'pink', 'pre': 'purple', 'cur': 'cyan', 'head': 'green', 'head2': 'orange', 'mid': 'yellow'}, h=330),
        dict(type='text', fn=lambda S: f"当前孪生和：`{S['head'].val} + {S['head2'].val}` = =={S['head'].val + S['head2'].val}==" if S.get('head') is not None and S.get('head2') is not None and 'ans' in S else ''),
    ],
    watch=['ans', ('slow', 'slow.val if slow else None', 'blue'), ('fast', 'fast.val if fast else None', 'pink')],
    captions={
        'while fast and fast.next': lambda S, B, ret: ('`fast` 和 `fast.next` 都不为空 → 快指针还能走两步' if B.fast and B.fast.next else '`fast` 走到头 → 慢指针恰好在后半段起点'),
        'slow = slow.next': '`slow` 走一步 → 节点 `{slow.val}`',
        'fast = fast.next.next': '`fast` 走两步：它到头时 `slow` 刚好走了一半',
        'return slow': '链表长度是偶数，`slow` 停在后半段第一个节点 `{slow.val}`',
        'pre, cur = None, head': '反转后半段：`pre` 在前，`cur` 从 `{head.val}` 开始',
        'nxt = cur.next': '先记住 `cur` 的后继 `nxt`，免得断链后找不到',
        'cur.next = pre': '`{cur.val}.next` 改指向前一个节点，箭头掉头',
        'pre = cur': '`pre` 前进到 `{pre.val}`',
        'cur = nxt': '`cur` 前进到后继',
        'while cur':lambda S, B, ret: ('`cur` 不为空 → 还有节点要掉头' if B.cur else '`cur` 为空 → 后半段全部掉头完毕'),
        'return pre': '反转完成，`pre` 是后半段的新头（原来的尾巴）`{pre.val}`',
        'mid = self.middleNode': '先找后半段起点：`mid` = 节点 `{mid.val}`',
        'head2 = self.reverseList': '反转后半段 → `head2` 从原链表尾部出发',
        'ans = max': '`head.val + head2.val` = `{B.head.val} + {B.head2.val}` = {B.head.val + B.head2.val}，`ans = max({B.ans}, ...)` = =={ans}==',
        'head = head.next': '`head` 右移：下一对孪生',
        'head2 = head2.next': '`head2` 沿反转后的链表往原链表中间走',
        'while head2': lambda S, B, ret: ('`head2` 不为空 → 还有孪生对没算' if B.head2 else '`head2` 为空 → 所有孪生对算完'),
        'return ans': '最大孪生和 `{ans}`',
    },
    skip=['ans = 0'],
    cards=dict(
        one_liner='反转后半段，头尾两指针同时往中间走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长链表，第 `i` 个节点与第 `n-1-i` 个互为孪生节点',
                 '孪生和 = 两个节点值之和，返回==最大孪生和==',
                 '示例：`[5,4,2,1]` → `6`；本视频：`[4,2,7,3,1,5]` → `10`'],
        quote='本思路与 234. 回文链表 是一样的……注意题目保证链表长度是偶数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['链表只能向后走，没法从尾巴往前数',
              '找到中点，把后半段反转 → 尾巴变成了新链表的头',
              '两个头同时往后走，每步就是一对孪生节点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '灵神还给了递归写法：递时 `right` 走到末尾，归时 `left` 右移、`right` 左移，空间 `O(n)`',
                 '长度为偶数，`slow` 恰好停在后半段第一个节点；奇数则要多考虑一格',
                 '反转后半段会改变原链表结构（中点前一个节点仍指向 mid）'],
    ),
)
