CONFIG = dict(
    num=817, title='链表组件', difficulty='Medium', category='链表',
    author='yiduobo', technique='遍历 + 连续段标记',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def numComponents(self, head, G):

        num_set = set(G)
        now = head
        flag = False
        res = 0
        while now:
            if now.val in num_set:
                flag = True
            else:
                if flag:
                    res += 1
                flag = False
            now = now.next
        
        if flag:
            res += 1
            
        return res
''',
    call='Solution().numComponents(L([0,1,2,3,4,5,6]), [0,1,3,5,6])',
    expect=3,
    views=[
        dict(type='linked', pointers={'now': 'blue'}, h=250),
        dict(type='set', var='num_set', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=lambda S: ('`flag` = ==True==：前面正处在一个组件里' if S.get('flag') else '`flag` = False：前面不在组件里') if 'flag' in S else ''),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('flag', 'flag', 'yellow'), ('res', 'res', 'green')],
    captions={
        6: '`flag = False`：一开始不在任何组件里',
        'num_set = set(G)': '把 `G` 放进集合，判断节点在不在 `G` 里只要 `O(1)`',
        'if now.val in num_set': '节点值 `{now.val}` 在 `G` 里吗？→ {"在" if now.val in num_set else "不在"}',
        10: '值在 `G` 里：组件继续（或开始），`flag = True`',
        13: '遇到不在 `G` 的节点，而 `flag` 为真：前面那一串连续节点刚好成一个组件，==组件数 +1== = {res}',
        14: '断开了，`flag` 复位为 False，等下一个组件',
        'now = now.next': '看下一个节点',
        17: '循环结束，`flag` 为 {flag}：{"链表以组件结尾，还要再数一个" if flag else "最后没有未结算的组件"}',
        18: '补上结尾的组件：==组件数 +1== = {res}',
        'return res': '共 =={res}== 个组件',
    },
    cards=dict(
        one_liner='用一个 flag 标记“正在一个组件里”，断开时数一个',
        complexity='时间 `O(n + |G|)`，空间 `O(|G|)`',
        problem=['链表元素互不相同；`G` 是链表值的子集',
                 '组件：链表里 ==连续== 且都在 `G` 中的一段',
                 '示例：链表 `0→1→2→3→4→5→6`，`G=[0,1,3,5,6]` → 组件 `0-1`、`3`、`5-6`，共 `3`'],
        quote='使用一个标记flag来表示之前是否有节点在G当中……若当前flag为true，说明当前节点之前存在若干个连续节点在G当中，因此组件数加一，同时置flag为false。',
        quote_src='—— yiduobo 题解',
        idea=['在 `G` 中的节点只负责把 `flag` 置 True',
              '一旦碰到不在 `G` 的节点，且 `flag` 是 True，就说明刚刚结束了一个组件',
              '循环结束后要再检查一次 `flag`，因为链表可能以组件结尾'],
        summary=['最容易漏的是循环后的 `if flag: res += 1`（组件在链表尾部）',
                 '用集合而不是列表判断成员，避免 `O(n·|G|)`',
                 '时间 `O(n + |G|)`，空间 `O(|G|)`'],
    ),
)
