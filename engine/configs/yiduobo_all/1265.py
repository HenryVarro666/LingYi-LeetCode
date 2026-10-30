CONFIG = dict(
    num=1265, title='逆序打印不可变链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='递归 · 先递归后输出',
    tags=['灵神题单', '链表树与回溯', 'VIP 题'],
    code='''
class Solution(object):
    def printLinkedListInReverse(self, head):

        next = head.getNext()
        if next:
            self.printLinkedListInReverse(next)
        
        head.printValue()
''',
    setup='''
class ImmutableListNode(ListNode):
    def getNext(self):
        return self.next
    def printValue(self):
        printed.append(self.val)

printed = []
head = L([1, 2, 3, 4])
_x = head
while _x:
    _x.__class__ = ImmutableListNode
    _x = _x.next
''',
    call='''s = Solution()
s.printed = printed
s.printLinkedListInReverse(head)
printed''',
    expect=[4, 3, 2, 1],
    views=[
        dict(type='linked', label='不可变链表（蓝 = 当前 head）', pointers={'head': 'blue'}, h=170),
        dict(type='text', fn=lambda S: f"已输出 `printed = {S.get('self.printed')}`", size=28, h=60),
        dict(type='calls', h=300),
    ],
    watch=[('head', 'head.val', 'blue'), ('next', lambda S: S['_inner'].get('next') and S['_inner']['next'].val), ('printed', 'self.printed', 'green')],
    captions={
        'next = head.getNext()': '只能用 `getNext()` 往后走，不能存节点：拿到下一个节点 `{next.val if next else None}`',
        'if next:': lambda S, B, r: (f'后面还有节点 `{S.next.val}` → ==先把后面的处理完==' if S.next else '`next` 为空：当前是最后一个节点，不用再递归'),
        'self.printLinkedListInReverse(next)': '进入下一个节点 `{next.val}` 的那一层，等它们都输出完才轮到我',
        'head.printValue()': '后面的都输完了 → 输出当前 `{head.val}`，已输出 `{self.printed}`',
    },
    cards=dict(
        one_liner='先递归处理后面的节点，再输出自己',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给你一个不可变链表的头节点 `head`，只能调用接口：',
                 '`getNext()` 返回下一个节点，`printValue()` 输出当前节点的值',
                 '要求==从后往前==输出所有节点；不能修改链表，也不能直接访问节点值',
                 '本视频：`1 → 2 → 3 → 4`，输出 `4 3 2 1`'],
        quote='题目无法记录链表中的节点，因此只能按照类似树的后续遍历的处理方法，从链表头开始，先递归处理后续节点，然后再输出当前节点的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['不能把节点存进数组再倒着输出，只能靠==递归栈==记住路径',
              '就像树的后序遍历：先处理「后面」，最后才输出自己',
              '最后一个节点没有 `next`，第一个输出的就是它'],
        summary=['时间 `O(n)`，空间 `O(n)`：递归深度等于链表长度',
                 '顺序别写反：`printValue()` 放在递归调用==之后==才是逆序，放前面就是正序',
                 '`next` 是接口返回值，判空用 `if next`',
                 '题目的接口 `ImmutableListNode` 由视频里的 setup 模拟：打印改为追加进 `printed` 列表'],
    ),
)
