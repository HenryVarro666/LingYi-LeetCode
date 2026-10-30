CONFIG = dict(
    num=3263, title='将双链表转换为数组 I', difficulty='Easy', category='链表',
    author='yiduobo', technique='从头遍历',
    tags=['灵神题单', '链表树与回溯'],
    setup='''
# 双向链表节点（val / prev / next）；用引擎的 L() 建出 next，再补上 prev
_h = L([1, 2, 3, 4, 5])
_x = _h
while _x.next:
    _x.next.prev = _x
    _x = _x.next
_h.prev = None
head = _h
''',
    code='''
class Solution:
    def toArray(self, head):

        res = []
        while head:
            res.append(head.val)
            head = head.next
        
        return res
''',
    call='Solution().toArray(head)',
    expect=[1, 2, 3, 4, 5],
    views=[
        dict(type='linked', pointers={'head': 'blue'}, h=230),
        dict(type='array', var='res', h=170, label='res'),
    ],
    watch=[('head', 'head.val if head else None', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = []': '准备一个空数组 `res` 装答案',
        'while head': '`head` 不为空？→ {"是，继续" if head else "否，走到链表尾了"}',
        'res.append': '把当前节点的值 `{head.val}` 放进 `res`：{res}',
        'head = head.next': '沿 `next` 往后走一个节点',
        'return res': '走完整条链表，按顺序返回 `{res}`',
    },
    cards=dict(
        one_liner='给的是头结点，沿着 next 一路走到底',
        complexity='时间 `O(n)`，空间 `O(1)`（不含答案）',
        problem=['给你一个双向链表的 ==头结点== `head`，每个节点有 `val`、`prev`、`next`',
                 '按链表顺序把所有值放进数组并返回',
                 '示例：`1⇄2⇄3⇄4⇄5` → `[1,2,3,4,5]`'],
        quote='对于3263题，只需从头结点开始不断向后迭代，若当前head非空，那么就将其对于的元素加入到答案数组中。',
        quote_src='—— yiduobo 题解',
        idea=['拿到的就是头，用不到 `prev`',
              '`head` 非空就记录值并后移，空了说明走完'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '直接复用参数 `head` 当游标，不需要新变量',
                 '下一题 3294 给的是任意节点，需要先退回到头'],
    ),
)
