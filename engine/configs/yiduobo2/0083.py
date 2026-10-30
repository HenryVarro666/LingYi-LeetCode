import tracer

VALS = [1, 1, 1, 2, 3, 3]


def _cols(S):
    h = S.get('head')
    out = set()
    while h is not None:
        out.add(tracer._origin.get(h._uid, (0, -1))[1])
        h = h.next
    return out


def _col(x):
    return tracer._origin.get(x._uid, (0, None))[1] if x is not None else None


def _rule(S):
    now = S.get('now')
    if now is None or now.next is None:
        return '对于节点 p：若 `p.val == p.next.val` → 删去 `p.next`'
    nx = now.next
    nn = nx.next.val if nx.next is not None else 'None'
    if nx.val == now.val:
        return f'`now.val == now.next.val`（{now.val} == {nx.val}）→ `now.next` 改指 `now.next.next` = =={nn}=='
    return f'`now.val ≠ now.next.val`（{now.val} ≠ {nx.val}）→ 保留，`now` 往后走'


def _cap_if(S, B, ret):
    p = B.now
    if p.next.val == p.val:
        return f'`now.next.val == now.val`（`{p.val}`）：重复了 → 删去 now.next'
    return f'`{p.next.val} ≠ {p.val}`：不重复 → now 往后走一步'


CONFIG = dict(
    num=83, title='删除排序链表中的重复元素', difficulty='Easy', category='链表',
    author='yiduobo', technique='p.next = p.next.next 删除下一个',
    tags=['热题173'],
    code='''
class Solution(object):
    def deleteDuplicates(self, head):

        if not head:
            return head

        now = head
        while now.next:
            if now.next.val == now.val:
                now.next = now.next.next
            else:
                now = now.next

        return head
''',
    call=f'Solution().deleteDuplicates(L({VALS}))',
    result_fn=list_vals,
    expect=[1, 2, 3],
    views=[
        dict(type='linked', label='链表（青 = now）', h=280, pointers={'now': 'cyan', 'head': 'green'}),
        dict(type='text', fn=_rule, size=26, h=100, lines=2),
        dict(type='array', var=lambda S: VALS, label='输入的 6 个节点（灰 = 已删去）', h=170, cell=80,
             dim=lambda S, i, v: 'head' in S and i not in _cols(S),
             color=lambda S, i, v: 'cyan' if i == _col(S.get('now')) else None),
    ],
    watch=[('now', 'now', 'cyan'), ('now.next', 'now.next', 'pink'), ('head', 'head', 'green')],
    captions={
        'if not head': lambda S, B, r: '空链表直接返回' if not B.head else '链表非空',
        'now = head': '`now` 从头节点开始扫描',
        'while now.next': lambda S, B, r: (f'`now.next = {B.now.next.val}` 存在 → 比较 now 和 now.next' if B.now.next
                                           else f'`now = {B.now.val}` 没有 next 了 → 扫描结束'),
        'if now.next.val == now.val': _cap_if,
        'now.next = now.next.next': lambda S, B, r: (f'经典删除操作：`now.next = now.next.next` → `{S.now.val}` 直接连到 '
                                                     f'`{S.now.next.val if S.now.next else "None"}`；now 不动，继续检查新的 next'),
        'now = now.next': '`now` → `{now.val}`',
        'return head': '每个值只保留了一个 → 返回 `head`',
    },
    cards=dict(
        one_liner='p.val == p.next.val 就删去 p.next：把 p.next 指向 p.next.next',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定==已排序==链表的头 `head`，删除所有重复元素，使每个元素==只出现一次==',
                 '示例：`[1,1,2]` → `[1,2]`；`[1,1,2,3,3]` → `[1,2,3]`',
                 f'本视频：`{VALS}` → `[1,2,3]`（开头连续 3 个 1）'],
        quote='对于一个节点p，若p.val == p.next.val那么需要删去p.next这个节点。链表操作中删除next的经典操作是==将p.next指向p.next.next==。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 82 题一样是链表操作，不过这里重复的数==只保留住一个==',
              '用 `now` 从头扫：`now.next` 和 `now` 相同就删掉 `now.next`',
              '不同才让 `now = now.next`；头节点一定保留，直接返回 `head`'],
        summary=['时间 `O(n)`：每个节点要么被删一次，要么被 now 走过一次',
                 '易错：删完 next 后 now ==不能前进==，开头 3 个 1 就要连删两次',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '和灵神写法几乎一致：灵神用 `is None` 判空，yiduobo 用 `not head`'],
    ),
)
