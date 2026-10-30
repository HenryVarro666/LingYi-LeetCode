CONFIG = dict(
    num=1171, title='从链表中删去总和值为零的连续节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='前缀和 + 哈希表记最后位置',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def removeZeroSumSublists(self, head):

        p_head = ListNode(0)
        p_head.next = head
        now = p_head
        s = 0
        pos_dict = {}
        while now:
            s += now.val
            pos_dict[s] = now
            now = now.next
        
        now = p_head
        s = 0
        while now:
            s += now.val
            now.next = pos_dict[s].next
            now = now.next

        return p_head.next
''',
    setup='''
import tracer, itertools
head = L([1, 2, -3, 3, 1])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().removeZeroSumSublists(head)',
    expect=[3, 1],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（最左边是假头 p_head，值为 0）', pointers={'now': 'blue', 'p_head': 'purple'}, h=300),
        dict(type='map', var='pos_dict', label='pos_dict：前缀和 → 最后一次出现的节点', fmt=lambda k, v: f'{k}: 节点{v.val}', h=200),
    ],
    watch=[('s（前缀和）', 's', 'yellow'), ('now', 'now', 'blue')],
    captions={
        'p_head = ListNode(0)': '建假头 `p_head`（值 0）：因为原来的头节点也可能被删掉',
        'p_head.next = head': '假头指向原链表',
        'now = p_head': lambda S, B, ret: ('第一趟：从假头开始，记录每个前缀和最后出现的位置' if 's' not in B
                                          else '第二趟：从假头重新开始，用 `pos_dict` 跳过和为零的一段'),
        's = 0': '前缀和清零，重新累加',
        'now.val': '前缀和 `s` 加上 `{now.val}` → =={s}==',
        'pos_dict[s] = now': '记下前缀和 `{s}` 对应节点 `{now.val}`；相同的 `s` 会==覆盖==成更靠后的节点',
        'now = now.next': '`now` 后移一个节点',
        'now.next = pos_dict[s].next': lambda S, B, ret: (
            f'前缀和 `{S.s}` 最后出现在节点 `{B.pos_dict[S.s].val}`：中间这一段和为 0，==整段跳过==，`now.next` 直接接到它后面'
            if B.pos_dict[S.s] is not B.now else f'前缀和 `{S.s}` 的最后位置就是自己，没有要删的段，`next` 不变'),
        'return p_head.next': '返回 `p_head.next`：头节点被删了也没关系',
    },
    cards=dict(
        one_liner='前缀和相同的两个位置之间，节点和为零',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['删去链表中和为 0 的连续节点，直到不存在这样的节点',
                 '返回最终链表，答案可能不唯一',
                 '示例：`1→2→-3→3→1` → `3→1`（`1→2→1` 也对）'],
        quote='找到s最后一次出现时对应的节点q，那么p + 1到q之间所有的节点之和恰好为0，我们可以将这些节点全部删去。',
        quote_src='—— yiduobo 题解',
        idea=['子段和 → 前缀和：两处前缀和相等，中间段和为 0',
              '第一趟：用 dict 记下每个前缀和==最后一次==出现的节点',
              '第二趟：每到一个节点，把 `next` 接到该前缀和最后节点的后面'],
        summary=['时间 `O(n)`，空间 `O(n)`；两趟遍历',
                 '易错点：必须加假头（值 0），否则开头的零和段删不掉',
                 '哈希表要记==最后一次==，这样一次跳过最长的段',
                 '同类题：560 和为 K 的子数组（前缀和 + 哈希表）'],
    ),
)
