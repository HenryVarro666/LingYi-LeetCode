def _hv(S):
    h = S.get('h')
    if h is None:
        return '把 k 条链表的当前头节点放进最小堆，每次取最小的接到答案后面'
    return '堆里始终是 =={}== 个「候选」：每条还没取完的链表，各出一个当前头节点'.format(len(h))


def cap_pop(S, B, ret):
    rest = ' '.join(str(n.val) for n in S.h)
    return f'弹出堆中最小的节点 `{S.node.val}`；堆里剩 `[{rest}]`' if rest else f'弹出最后一个节点 `{S.node.val}`，堆空了'


CONFIG = dict(
    num='LCR 078', title='合并 K 个升序链表', difficulty='Hard', category='链表',
    author='灵茶山艾府', technique='最小堆 + 哨兵节点',
    code='''
ListNode.__lt__ = lambda a, b: a.val < b.val  # 让堆可以比较节点大小

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点，作为合并后链表头节点的前一个节点
        h = [head for head in lists if head]  # 初始把所有链表的头节点入堆
        heapify(h)  # 堆化
        while h:  # 循环直到堆为空
            node = heappop(h)  # 剩余节点中的最小节点
            if node.next:  # 下一个节点不为空
                heappush(h, node.next)  # 下一个节点有可能是最小节点，入堆
            cur.next = node  # 合并到新链表中
            cur = cur.next  # 准备合并下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是新链表的头节点
''',
    setup='lists = [L([1, 4]), L([2, 3]), L([1, 5])]',
    call='Solution().mergeKLists(lists)',
    expect=[1, 1, 2, 3, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', h=60, size=26, fn=_hv),
        dict(type='linked', label='链表（dummy 开头的是合并结果）', pointers={'cur': 'blue', 'node': 'pink', 'dummy': 'purple'}, h=380),
        dict(type='heap', var='h', fmt=lambda n: str(n.val), label='h 最小堆（节点的 val）', top_color='pink', h=130),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') is not None else None, 'pink'),
           ('cur', lambda S: S['cur'].val if S.get('cur') is not None else None, 'blue'),
           ('len(h)', lambda S: len(S['h']) if 'h' in S else None)],
    captions={
        'ListNode.__lt__': 'Python 的堆要比较元素：给 `ListNode` 定义 `<`，按 `val` 比大小',
        'cur = dummy': '哨兵 `dummy` 作为结果链表的「前一个节点」，`cur` 指向结果的末尾',
        'h = [head': lambda S, B, r: f'每条链表的==头节点==都可能是全局最小：先把 {len(S.h)} 个头节点收进 `h`',
        'heapify(h)': '堆化：堆顶就是最小的头节点 `{h[0].val}`',
        'while h': lambda S, B, r: ('堆里还有节点 → 继续取最小的' if S.h else '堆空了 → 所有节点都已合并'),
        'node = heappop': cap_pop,
        'if node.next': lambda S, B, r: (f'`{S.node.val}` 后面还有节点 `{S.node.next.val}` → 它成为这条链表新的头，可能是下一个最小'
                                         if S.node.next else f'`{S.node.val}` 已是所在链表的末尾 → 这条链表取完了，不用补'),
        'heappush(h, node.next)': '`{node.next.val}` 入堆：==每次取走一个，就补上同一条链表的下一个==',
        'cur.next = node': '把最小节点 `{node.val}` 接到结果末尾',
        'cur = cur.next': '`cur` 前进到 `{cur.val}`，准备接下一个',
        'return dummy.next': '返回 `dummy.next`：哨兵后面就是合并后的头节点',
    },
    max_steps=80,
    cards=dict(
        one_liner='堆里放每条链表的当前头：弹出最小，补上它的下一个',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['`k` 条升序链表，合并成一条升序链表',
                 '示例：`[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`',
                 '本视频：`[1,4]`、`[2,3]`、`[1,5]` → `[1,1,2,3,4,5]`'],
        quote='每当我们找到一个节点值最小的节点 x，就把节点 x.next 加入「可能是最小节点」的集合中。',
        quote_src='—— 灵茶山艾府题解「方法一：最小堆」',
        idea=['合并后的第一个节点，一定是某条链表的==头节点==',
              '取走最小的 `x` 后，下一个最小的只可能是别的头，或 `x.next`',
              '需要「找最小 + 删最小 + 插入」→ 最小堆；哨兵节点省去头节点的特判'],
        summary=['时间 `O(n log k)`（`n` 为总节点数），空间 `O(k)`',
                 '易错：Python 里节点不能直接比大小，要给 `ListNode` 加 `__lt__`',
                 '易错：只把非空链表的头节点入堆；`node.next` 为空就不要入堆',
                 '另一种写法：分治，把 `lists` 一分为二递归合并，再套用「合并两个有序链表」，同样 `O(n log k)`、空间 `O(log k)`'],
    ),
)
