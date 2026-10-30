def _vals(x):
    out = []
    while x is not None and len(out) < 8:
        out.append(str(x.val))
        x = x.next
    return '→'.join(out) or '∅'


def _chains(S):
    parts = []
    names = ('list1', 'list2', 'dummy') if 'dummy' in S else ('head', 'head2')
    for name in names:
        v = S.get(name)
        if v is None or not hasattr(v, 'next'):
            continue
        out, x = [], (v.next if name == 'dummy' else v)
        while x is not None and len(out) < 8:
            out.append(str(x.val))
            x = x.next
        parts.append(f'`{"dummy.next" if name == "dummy" else name}` = ' + ('→'.join(out) or '∅'))
    return '　'.join(parts)


CONFIG = dict(
    num=148, title='排序链表', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='归并排序（分治）',
    code='''
class Solution:
    # 876. 链表的中间结点（快慢指针）
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            pre = slow  # 记录 slow 的前一个节点
            slow = slow.next
            fast = fast.next.next
        pre.next = None  # 断开 slow 的前一个节点和 slow 的连接
        return slow

    # 21. 合并两个有序链表（双指针）
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 用哨兵节点简化代码逻辑
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1  # 把 list1 加到新链表中
                list1 = list1.next
            else:  # 注：相等的情况加哪个节点都是可以的
                cur.next = list2  # 把 list2 加到新链表中
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2  # 拼接剩余链表
        return dummy.next

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 如果链表为空或者只有一个节点，无需排序
        if head is None or head.next is None:
            return head
        # 找到中间节点 head2，并断开 head2 与其前一个节点的连接
        # 比如 head=[4,2,1,3]，那么 middleNode 调用结束后 head=[4,2] head2=[1,3]
        head2 = self.middleNode(head)
        # 分治
        head = self.sortList(head)
        head2 = self.sortList(head2)
        # 合并
        return self.mergeTwoLists(head, head2)
''',
    call='Solution().sortList(L([4,2,1,3]))',
    expect=[1, 2, 3, 4],
    result_fn=list_vals,
    max_steps=75,
    views=[
        dict(type='text', fn=_chains, size=26),
        dict(type='linked', label='链表（位置按输入固定；下排是合并用的哨兵）',
             pointers={'head': 'purple', 'head2': 'pink', 'slow': 'blue', 'fast': 'green', 'pre': 'cyan',
                       'list1': 'blue', 'list2': 'pink', 'cur': 'orange'}, h=330),
        dict(type='calls', h=170),
    ],
    watch=[('head', 'head', 'purple'), ('head2', 'head2', 'pink')],
    skip=['pre = slow', 'slow = slow.next', 'list1 = list1.next', 'list2 = list2.next', 'return head'],
    captions={
        'if head is None or head.next is None': lambda S, B, ret: (
            '只剩 `{}` 一个节点 → 本身有序，==直接返回=='.format(B.head.val) if B.head is not None and B.head.next is None else
            '`head` = {}，至少两个节点 → 需要拆开排序'.format(_vals(B.head))),
        'head2 = self.middleNode(head)': '先找中点（876 题）：快慢指针，顺便把链表断成两半',
        'slow = fast = head': '`slow`、`fast` 都从 `head`（{head.val}）出发',
        'while fast and fast.next': lambda S, B, ret: ('`fast` 还能走两步 → 继续' if B.fast and B.fast.next else
                                                       '`fast` 走到头了 → `slow`（{}）就是中点'.format(B.slow.val)),
        'fast = fast.next.next': lambda S, B, ret: '`pre` 记住 {}，`slow` 走一步到 {}，`fast` 走两步到 {}'.format(
            S.pre.val, S.slow.val, S.fast.val if S.fast else 'None'),
        'pre.next = None': lambda S, B, ret: '==断开== `pre.next`：前一半 `{}`，后一半 `{}`'.format(_vals(S.head), _vals(S.slow)),
        'return slow': '返回中点 `{ret.val}`，它就是后一半的头 `head2`',
        'head = self.sortList(head)': lambda S, B, ret: '分治：递归排序前一半 `{}`'.format(_vals(S.head)),
        'head2 = self.sortList(head2)': lambda S, B, ret: '分治：递归排序后一半 `{}`'.format(_vals(S.head)),
        'return self.mergeTwoLists(head, head2)': lambda S, B, ret: '两半都有序了：合并 `{}` 和 `{}`（21 题）'.format(
            _vals(S.list1), _vals(S.list2)),
        'cur = dummy = ListNode()': '哨兵 `dummy` 当新链表的“头前一个”，`cur` 指向新链表末尾',
        'while list1 and list2': lambda S, B, ret: ('两条都没取完 → 比较两个头' if B.list1 and B.list2 else
                                                    '有一条取完了 → 退出循环'),
        'if list1.val < list2.val': lambda S, B, ret: ('`{} < {}` → 取 `list1` 的头'.format(B.list1.val, B.list2.val)
                                                       if B.list1.val < B.list2.val else
                                                       '`{} ≥ {}` → 取 `list2` 的头'.format(B.list1.val, B.list2.val)),
        'cur.next = list1  #': '把 `{cur.next.val}` 接到新链表末尾（下一行 `list1` 随即后移）',
        'cur.next = list2  #': '把 `{cur.next.val}` 接到新链表末尾（下一行 `list2` 随即后移）',
        'cur = cur.next': '`cur` 移到新链表末尾 `{cur.val}`',
        'cur.next = list1 if list1 else list2': lambda S, B, ret: '剩下的 `{}` 本来就有序，==整段接上=='.format(
            _vals(B.list1 or B.list2)),
        'return dummy.next': lambda S, B, ret: '返回合并结果 `{}`'.format(_vals(ret)),
    },
    cards=dict(
        one_liner='找中点断开 → 两半分别排序 → 合并两个有序链表',
        complexity='时间 `O(n log n)`，空间 `O(log n)`（递归栈）',
        problem=['给链表头 `head`，按==升序==排序后返回',
                 '示例：`[4,2,1,3]` → `[1,2,3,4]`',
                 '进阶：`O(n log n)` 时间、常数空间'],
        quote='找到链表的中间结点 head2 的前一个节点，并断开 head2 与其前一个节点的连接……分治，递归调用 sortList……合并两个有序链表',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['模块化：876 找中点 + 21 合并两个有序链表，拼成归并排序',
              '快慢指针找中点时用 `pre` 记住 `slow` 的前一个，`pre.next = None` ==把链表切成两半==',
              '每层合并总长 `O(n)`，递归深度 `O(log n)` ⇒ `O(n log n)`'],
        summary=['时间 `O(n log n)`，空间 `O(log n)`',
                 '易错：一定要断开 `pre.next`，否则递归永远处理同一条长链',
                 '递归边界：空或只有一个节点，直接返回',
                 '方法二自底向上迭代归并（`step` = 1,2,4…），空间 `O(1)`'],
    ),
)
