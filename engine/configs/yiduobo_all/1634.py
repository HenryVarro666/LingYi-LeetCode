SETUP = '''
import tracer


class PolyNode(tracer.ListNode):
    def __init__(self, x=0, y=0, next=None):
        self.coefficient = x
        self.power = y
        self.next = next
        self._uid = tracer.next_uid()

    @property
    def val(self):
        return f'{self.coefficient}x^{self.power}'

    def __repr__(self):
        return f'PolyNode({self.coefficient}x^{self.power})'


def build_poly(pairs, row):
    nodes = [PolyNode(c, p) for c, p in pairs]
    for i, nd in enumerate(nodes):
        tracer._origin[nd._uid] = (row, i)
        if i + 1 < len(nodes):
            nd.next = nodes[i + 1]
    return nodes[0]


poly1 = build_poly([(2, 3), (4, 2), (3, 0)], 0)
poly2 = build_poly([(1, 3), (-4, 2), (5, 1)], 1)
'''

CONFIG = dict(
    num=1634, title='求两个多项式链表的和', difficulty='Medium', category='链表',
    author='yiduobo', technique='二路归并 + 假头',
    tags=['链表树与回溯'],
    code='''
class Solution:
    def addPoly(self, poly1, poly2):

        p1 = poly1
        p2 = poly2

        p_head = PolyNode()
        p = p_head

        while p1 and p2:
            if p1.power == p2.power:
                node = PolyNode(p1.coefficient + p2.coefficient, p1.power)
                p1 = p1.next
                p2 = p2.next
            elif p1.power > p2.power:
                node = PolyNode(p1.coefficient, p1.power)
                p1 = p1.next
            else:
                node = PolyNode(p2.coefficient, p2.power)
                p2 = p2.next
            
            if node.coefficient != 0:
                p.next = node
                p = node
        
        while p1:
            node = PolyNode(p1.coefficient, p1.power)
            p.next = node
            p = node
            p1 = p1.next
        
        while p2:
            node = PolyNode(p2.coefficient, p2.power)
            p.next = node
            p = node
            p2 = p2.next

        return p_head.next
''',
    setup=SETUP,
    call='Solution().addPoly(poly1, poly2)',
    expect=['3x^3', '5x^1', '3x^0'],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='多项式链表（节点 = 系数 x^次数，次数从大到小）；第三行是结果链表',
             pointers={'p1': 'blue', 'p2': 'pink', 'p': 'green'}, h=480),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('p（结果尾）', 'p', 'green')],
    captions={
        'p_head = PolyNode()': '建假头 `p_head`：结果可能为空，有假头就不用特判',
        'p = p_head': '`p` 是结果链表的尾指针',
        'while p1 and p2': lambda S, B, ret: ('两条链都还有节点 → 继续归并' if (B.p1 and B.p2) else '有一条链走完了 → 归并结束，处理剩余部分'),
        'if p1.power == p2.power': lambda S, B, ret: (
            f'次数相同（`{B.p1.power}` = `{B.p2.power}`）→ 系数相加' if B.p1.power == B.p2.power
            else f'次数不同（`{B.p1.power}` ≠ `{B.p2.power}`）→ 照抄次数较大的那个'),
        'node = PolyNode(p1.coefficient + p2.coefficient': '合并同类项：`{B.p1.coefficient}` + `{B.p2.coefficient}` = =={node.coefficient}==，次数 `{node.power}`',
        'elif p1.power > p2.power': lambda S, B, ret: (
            f'`{B.p1.power}` > `{B.p2.power}` → 次数大的先出，抄 `p1`' if B.p1.power > B.p2.power
            else f'`{B.p1.power}` < `{B.p2.power}` → 抄 `p2`'),
        16: '`p1` 次数更大，原样抄成新节点 `{node.val}`',
        19: '抄 `p2` 的节点 `{node.val}`',
        26: lambda S, B, ret: ('`p1` 还有剩余节点 → 剩下的次数都更小，原样抄过来' if B.p1 else '`p1` 已空，没有剩余'),
        27: '抄 `p1` 剩余的节点 `{node.val}`',
        32: lambda S, B, ret: ('`p2` 还有剩余节点 → 原样抄过来' if B.p2 else '`p2` 也已空，两条链都处理完了'),
        34: '抄 `p2` 剩余的节点 `{node.val}`',
        'p1 = p1.next': '`p1` 后移',
        'p2 = p2.next': '`p2` 后移',
        'if node.coefficient != 0': lambda S, B, ret: (
            f'系数 `{B.node.coefficient}` ≠ 0 → 保留，接到结果尾部' if B.node.coefficient != 0
            else '系数为 ==0== → 这一项消掉了，不加入答案'),
        'p.next = node': '新节点接在结果尾部',
        'p = node': '尾指针 `p` 后移到新节点',
        'return p_head.next': '返回 `p_head.next`：即使结果为空也安全',
    },
    cards=dict(
        one_liner='次数有序，就像归并两个有序链表',
        complexity='时间 `O(m+n)`，空间 `O(1)`（不计结果）',
        problem=['多项式用链表表示，节点含系数 `coefficient` 和次数 `power`',
                 '次数从大到小排列，返回两个多项式的和',
                 '系数为 0 的项不能出现在结果里',
                 '示例：`2x^3+4x^2+3` 加 `x^3-4x^2+5x` → `3x^3+5x+3`'],
        quote='由于power字段是有序的，因此本题可以参照二路归并的思路，使用两个指针p1和p2分别从两个链表头部开始向后移动。',
        quote_src='—— yiduobo 题解',
        idea=['`p1`、`p2` 各指一条链：次数相同 → 系数相加，同时后移',
              '次数不同 → 照抄次数大的那个，只移动对应的指针',
              '新节点系数为 0 就丢掉；最后把剩下的一条链接上'],
        summary=['时间 `O(m+n)`，空间 `O(1)`（不计结果）',
                 '易错点：系数相加为 0 时不能加入答案，结果可能为空',
                 '加假头 `p_head`，处理空结果和第一个节点都不用特判',
                 '同类题：21 合并两个有序链表、2 两数相加'],
    ),
)
