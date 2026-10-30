import tracer

VALS = [1, 1, 2, 3, 3, 3]


def _alive_cols(S):
    h = S.get('head')
    out = set()
    while h is not None:
        out.add(tracer._origin.get(h._uid, (0, -1))[1])
        h = h.next
    return out


def _cur_col(S):
    c = S.get('cur')
    return tracer._origin.get(c._uid, (0, None))[1] if c is not None else None


def _cap_if(S, B, ret):
    c = B.cur
    if c.next.val == c.val:
        return f'下个节点 `{c.next.val}` 和我 `{c.val}` ==一样== → 删！'
    return f'下个节点 `{c.next.val}` 和我 `{c.val}` 不一样 → 它要保留，我移动过去'


def _cap_while(S, B, ret):
    c = B.cur
    if c.next is not None:
        return f'看看下个节点……`cur.next = {c.next.val}`，还有节点'
    return f'`cur = {c.val}` 已经是最后一个节点，没有下一个了 → 结束'


def _alive(S):
    h = S.get('head')
    out = []
    while h is not None:
        out.append(h.val)
        h = h.next
    return out


CONFIG = dict(
    num=83, title='删除排序链表中的重复元素', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='看下一个，一样就删',
    tags=['热题173'],
    code='''
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        cur = head
        while cur.next:  # 看看下个节点……
            if cur.next.val == cur.val:  # 和我一样，删！
                cur.next = cur.next.next
            else:  # 和我不一样，移动到下个节点
                cur = cur.next
        return head
''',
    call=f'Solution().deleteDuplicates(L({VALS}))',
    result_fn=list_vals,
    expect=[1, 2, 3],
    views=[
        dict(type='text', fn=lambda S: '链表已排序 → ==重复的数一定挨在一起==，只需比较相邻节点', size=26, h=60),
        dict(type='linked', label='链表（蓝 = cur；被删的节点从链上消失）', h=300, pointers={'cur': 'blue', 'head': 'green'}),
        dict(type='array', var=lambda S: VALS, label='原链表的 6 个节点（灰 = 已被删掉，蓝 = cur）', h=170, cell=80,
             dim=lambda S, i, v: 'head' in S and i not in _alive_cols(S),
             color=lambda S, i, v: 'blue' if i == _cur_col(S) else None),
        dict(type='text', fn=lambda S: f"从 head 出发能走到：`{' → '.join(map(str, _alive(S)))}`" if S.get('head') else '', size=26, h=70),
    ],
    watch=[('cur', 'cur', 'blue'), ('cur.next', 'cur.next', 'pink'), ('head', 'head', 'green')],
    captions={
        'if head is None': lambda S, B, r: '链表为空 → 直接返回 None' if B.head is None else '链表非空，开始去重',
        'cur = head': '`cur` 从头节点出发：cur 自己一定是要保留的',
        'while cur.next': _cap_while,
        'if cur.next.val == cur.val': _cap_if,
        'cur.next = cur.next.next': '跳过下个节点：`cur.next` 指向 `{cur.next.val if cur.next else None}`，==cur 先不动==，继续和新的下一个比',
        'cur = cur.next': '`cur` 移动到 `{cur.val}`',
        'return head': '去重完成，头节点没变 → 返回 `head`',
    },
    cards=dict(
        one_liner='看看下个节点：和我一样就删，不一样就走过去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定==已排序==链表的头 `head`，删除所有重复元素，使每个元素==只出现一次==',
                 '返回去重后的（仍有序的）链表',
                 '示例：`[1,1,2,3,3]` → `[1,2,3]`',
                 f'本视频：`{VALS}` → `[1,2,3]`'],
        quote='`while cur.next`：看看下个节点…… 如果 `cur.next.val == cur.val`：和我一样，==删！== 否则：和我不一样，移动到下个节点。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['有序 → 重复元素一定==相邻==，cur 只和 `cur.next` 比',
              '一样：`cur.next = cur.next.next` 删掉下一个，==cur 不动==（后面可能还有一样的）',
              '不一样：`cur = cur.next` 走过去；头节点一定保留，所以不需要哨兵'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：删除后 ==cur 不能前进==，否则连续 3 个相同只能删掉 1 个',
                 '循环条件是 `cur.next`：最后一个节点不用再比较',
                 '进阶：82 题要把重复的数==全部删掉==，头节点可能被删 → 需要哨兵节点'],
    ),
)
