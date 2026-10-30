CONFIG = dict(
    num=1669, title='合并两个链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='找 a-1 与 b 节点 · 拼接 list2',
    tags=[],
    code='''
class Solution(object):
    def mergeInBetween(self, list1, a, b, list2):

        cnt = 0
        now = list1
        while cnt < a - 1:
            now = now.next
            cnt += 1
        
        pre_a = now
        while cnt < b:
            now = now.next
            cnt += 1
        
        pre_a.next = list2
        while pre_a.next:
            pre_a = pre_a.next
        
        pre_a.next = now.next
        return list1
''',
    setup='list1 = L([10,1,13,6,9,5]); list2 = L([100,101,102])',
    call='Solution().mergeInBetween(list1, 3, 4, list2)',
    expect=[10, 1, 13, 100, 101, 102, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f"删除下标 `a={S['a']}` 到 `b={S['b']}` 的节点，换成 list2" + (f"　　cnt = ==%d==" % S['cnt'] if 'cnt' in S else '')),
        dict(type='linked', label='list1（第 1 行）与 list2（第 2 行）', pointers={'now': 'blue', 'pre_a': 'pink'}, h=430),
    ],
    watch=[('cnt', 'cnt', 'yellow'), ('now', 'now.val if now else None', 'blue'), ('pre_a', 'pre_a.val', 'pink')],
    captions={
        'cnt = 0': '`cnt` 记录 `now` 当前的下标',
        'now = list1': '`now` 从 list1 头部出发',
        'while cnt < a - 1': lambda S, B, r: (f'`cnt = {S.cnt} < a - 1 = {S.a - 1}` → 还没到第 `a-1` 个节点，继续走' if S.cnt < S.a - 1
                                              else f'`cnt = {S.cnt}`：已经到第 `a-1` 个节点，停'),
        'now = now.next': '`now` 后移一格',
        'cnt += 1': '`cnt` → {cnt}',
        'pre_a = now': '`pre_a` 记住第 `a-1` 个节点（值 `{pre_a.val}`）：它之后就要接上 list2',
        'while cnt < b': lambda S, B, r: (f'`cnt = {S.cnt} < b = {S.b}` → 继续走向第 `b` 个节点' if S.cnt < S.b
                                          else f'`cnt = {S.cnt} = b`：`now` 停在第 `b` 个节点（值 `{S.now.val}`），它的 next 是要保留的后半段'),
        'pre_a.next = list2': '`pre_a.next = list2`：==a 到 b 之间的节点从链上脱落==，list2 接在后面',
        'while pre_a.next': lambda S, B, r: ('`pre_a.next` 不为空 → 沿 list2 往后找尾巴' if S.pre_a.next else '`pre_a.next` 为空 → ==走到 list2 的尾部=='),
        'pre_a = pre_a.next': '`pre_a` → 节点 `{pre_a.val}`',
        'pre_a.next = now.next': '尾巴接上 `now.next`（值 `{now.next.val}`）：==后半段重新连回来==',
        'return list1': '头节点没变，返回 `list1`',
    },
    cards=dict(
        one_liner='先找 a-1 和 b 两个位置，再把 list2 嵌进去',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['给两个链表 `list1`、`list2` 和下标 `a`、`b`',
                 '删除 `list1` 中下标 `a` 到 `b` 的节点，换成整个 `list2`',
                 '本视频：`list1=[10,1,13,6,9,5]`，`a=3`，`b=4`，`list2=[100,101,102]` → `[10,1,13,100,101,102,5]`'],
        quote='首先从list1开始向后遍历，找到第a - 1个节点，记为pre_a。接下来从pre_a向后继续走走到第b个节点，记为b。',
        quote_src='—— yiduobo 题解原文',
        idea=['一次遍历，`cnt` 数下标：先停在 `a-1`，记为 `pre_a`',
              '继续走到第 `b` 个节点 `now`：它的 `next` 是要保留的后半段',
              '`pre_a.next = list2`，走到 list2 尾部再接 `now.next`'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '`pre_a` 是第 `a-1` 个，不是第 `a` 个；`now` 是第 `b` 个，要接的是 `now.next`',
                 '题目保证 `a ≤ b` 且都不是头尾，所以不用哨兵',
                 '原文为 Python 2 风格类声明，代码无需改动'],
    ),
)
