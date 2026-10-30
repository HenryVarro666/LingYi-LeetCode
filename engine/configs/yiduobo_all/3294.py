CONFIG = dict(
    num=3294, title='将双链表转换为数组 II', difficulty='Medium', category='链表',
    author='yiduobo', technique='先退回头结点，再遍历',
    tags=['灵神题单', '链表树与回溯'],
    setup='''
# 双向链表节点（val / prev / next）；用引擎的 L() 建出 next，再补上 prev
_h = L([1, 2, 3, 4, 5])
_x = _h
while _x.next:
    _x.next.prev = _x
    _x = _x.next
_h.prev = None
node = _h.next.next
''',
    code='''
class Solution:
    def toArray(self, node):

        now = node
        while now.prev:
            now = now.prev
        
        res = []
        while now:
            res.append(now.val)
            now = now.next
        
        return res
''',
    call='Solution().toArray(node)',
    expect=[1, 2, 3, 4, 5],
    views=[
        dict(type='linked', pointers={'now': 'blue'}, h=230),
        dict(type='array', var='res', h=170, label='res'),
    ],
    watch=[('node', 'node.val', 'pink'), ('now', 'now.val if now else None', 'blue'), ('res', 'res', 'green')],
    captions={
        'now = node': '给的是中间的节点 `{node.val}`，用 `now` 当游标从它出发',
        'while now.prev': '前面还有节点吗？→ {"有，继续往前退" if now.prev else "没有，已在头结点"}',
        'now = now.prev': '`now` 沿 `prev` 往前退一步，到 `{now.val}`',
        'res = []': '已经在头结点 `{now.val}`，准备空数组装答案',
        'while now:': '`now` 不为空？→ {"是，继续" if now else "否，走到链表尾了"}',
        'res.append': '放入当前值 `{now.val}`：{res}',
        'now = now.next': '沿 `next` 往后走一个节点',
        'return res': '按链表顺序返回 `{res}`',
    },
    cards=dict(
        one_liner='先沿 prev 退到头，再按 3263 的办法走',
        complexity='时间 `O(n)`，空间 `O(1)`（不含答案）',
        problem=['给你双向链表中的 ==任意一个节点== `node`',
                 '按链表顺序（从头到尾）返回所有节点的值',
                 '示例：给的是值为 3 的节点，链表 `1⇄2⇄3⇄4⇄5` → `[1,2,3,4,5]`'],
        quote='对于3294题，则只需要先将node往前迭代到链表的头节点，然后再按3263题的方法处理就行了。',
        quote_src='—— yiduobo 题解',
        idea=['头结点的特征：`prev` 为空，所以不断 `now = now.prev` 直到 `now.prev` 为空',
              '到头以后就是 3263 的写法：边走边收集'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '第一个循环判断的是 `now.prev`，不是 `now`，否则会退到 `None`',
                 '收集阶段不能漏掉前半段，所以一定要先回到头'],
    ),
)
