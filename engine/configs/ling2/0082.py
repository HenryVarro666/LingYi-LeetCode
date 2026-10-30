def _nv(x):
    return 'None' if x is None else str(x.val)


def _while_out(S, B, ret):
    cur = B['cur']
    a, b = cur.next, cur.next.next if cur.next else None
    if a and b:
        return f'`cur` 后面还有两个节点 `{a.val}`、`{b.val}` → 可能有重复，继续检查'
    if a:
        return f'`cur` 后面只剩一个节点 `{a.val}` → ==单独一个不可能重复==，结束'
    return '`cur` 后面没有节点了 → 结束'


def _if_cap(S, B, ret):
    nxt = S.cur.next.next
    if nxt.val == S.val:
        return f'后两个节点都是 `{S.val}` → ==值为 {S.val} 的节点一个不留=='
    return f'后两个节点 `{S.val}` ≠ `{nxt.val}` → `{S.val}` 没有重复，保留'


def _inner_while(S, B, ret):
    nx = B['cur'].next
    if nx and nx.val == S.val:
        return f'`cur.next` 的值还是 `{S.val}` → 继续删'
    return f'`cur.next` 是 `{_nv(nx)}`，不再等于 `{S.val}` → 删完了，`cur` ==原地不动=='


CONFIG = dict(
    num=82, title='删除排序链表中的重复元素 II', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='哨兵节点 · 看后两个节点',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode(next=head)
        while cur.next and cur.next.next:
            val = cur.next.val
            if cur.next.next.val == val:  # 后两个节点值相同
                # 值等于 val 的节点全部删除
                while cur.next and cur.next.val == val:
                    cur.next = cur.next.next
            else:
                cur = cur.next
        return dummy.next
''',
    # setup 只做布局：运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([1,2,3,3,4,4,5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().deleteDuplicates(head)',
    expect=[1, 2, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f'当前要检查的值 `val = {S["val"]}`' if 'val' in S else '`cur` 从哨兵出发，盯住它==后面的两个节点==')),
        dict(type='linked', label='链表（最左边是哨兵 dummy）', pointers={'cur': 'blue', 'dummy': 'purple', 'head': 'green'}, h=440),
    ],
    watch=[('cur', 'cur', 'blue'), ('cur.next', lambda S: S['cur'].next if S.get('cur') else None, 'cyan'), ('val', 'val', 'orange')],
    captions={
        'cur = dummy': '头节点也可能被删 → 加一个哨兵 `dummy`，`cur` 从它出发',
        'while cur.next and cur.next.next': _while_out,
        'val = cur.next.val': '记下 `cur` 后面第一个节点的值 `val = {val}`',
        'if cur.next.next.val == val': _if_cap,
        'while cur.next and cur.next.val == val': _inner_while,
        'cur.next = cur.next.next': lambda S, B, ret: f'删掉值为 `{S.val}` 的节点：`cur.next` 直接跳过它，指向 `{_nv(S.cur.next)}`',
        'cur = cur.next': '`{cur.val}` 保留下来 → `cur` 前进到它',
        'return dummy.next': '返回 `dummy.next`：原来的头节点可能已经被删了',
    },
    cards=dict(
        one_liner='站在要删节点的前面看后两个：值相同就把这个值全删光',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个==已排序==链表，把==出现重复的数字全部删除==，只留下没重复过的',
                 '示例：`[1,2,3,3,4,4,5]` → `[1,2,5]`',
                 '示例：`[1,1,1,2,3]` → `[2,3]`'],
        quote='`if cur.next.next.val == val:  # 后两个节点值相同` → ==值等于 val 的节点全部删除==：`while cur.next and cur.next.val == val`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['删节点要站在它的==前一个==：`cur` 永远停在“确定保留”的节点上',
              '看 `cur` 后两个节点：值相同 → 内层 while 把值为 `val` 的节点==一个不留==',
              '值不同 → `cur.next` 必然保留，`cur` 前进一步'],
        summary=['时间 `O(n)`：每个节点要么被删，要么被 `cur` 经过一次',
                 '易错：删完后 `cur` ==不能前进==，新的 `cur.next` 可能又是一组重复',
                 '头节点可能被删 → 哨兵 `dummy`，最后返回 `dummy.next`',
                 '对比 83 题（重复的保留一个）：那里 `cur.next = cur.next.next` 只删一个'],
    ),
)
