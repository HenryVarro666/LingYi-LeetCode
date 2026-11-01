CONFIG = dict(
    num=2074, title='反转偶数长度组的节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='攒够一组存进数组，偶数组直接交换值（Go 原文转写）',
    tags=['灵神题单', '链表、二叉树与回溯'],
    code='''
class Solution:
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        nodes = []
        node, size = head, 1
        while node:
            nodes.append(node)
            if len(nodes) == size or node.next is None:  # 统计到 size 个节点，或到达链表末尾
                n = len(nodes)
                if n % 2 == 0:  # 有偶数个节点
                    for i in range(n // 2):
                        nodes[i].val, nodes[n - 1 - i].val = nodes[n - 1 - i].val, nodes[i].val  # 直接交换元素值
                nodes = []
                size += 1
            node = node.next
        return head
''',
    call='Solution().reverseEvenLengthGroups(head)',
    setup='head = L([5,2,6,3,9,1,7,3,8,4])',
    expect=[5, 6, 2, 3, 9, 1, 4, 8, 3, 7],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（蓝 = node，当前正在统计的位置）', pointers={'node': 'blue'}, h=250),
        dict(type='array', var=lambda S: [x.val for x in S['nodes']], label='nodes：当前这一组攒到的节点值', cell=70, h=170),
        dict(type='text', fn=lambda S: f"当前组需要 `size = {S['size']}` 个节点，已攒 `{len(S['nodes'])}` 个" if 'size' in S and 'nodes' in S else '', size=30),
    ],
    watch=['size', ('len(nodes)', 'len(nodes)', 'cyan')],
    captions={
        3: '`nodes` 用来攒当前这一组的节点',
        'node, size = head': '从头节点开始，第一组需要 `size = 1` 个节点',
        'while node': lambda S, B, ret: ('还有节点没处理，继续' if S.node else '链表走完了'),
        'nodes.append(node)': '把节点 `{node.val}` 放进当前组，已攒 `{len(nodes)}` 个',
        'if len(nodes) == size': lambda S, B, ret: (f'已攒 `{len(S.nodes)}` 个，目标 `size = {S.size}`' + ('；==到齐了==，这一组结束' if len(S.nodes) == S.size else '') + ('；`node.next` 为空，==到链表末尾==，最后一组可能不满' if S.node.next is None and len(S.nodes) != S.size else '')),
        'n = len(nodes)': '这一组实际有 `n = {n}` 个节点（最后一组可能不足 `size`）',
        'if n % 2': lambda S, B, ret: (f'`n = {S.n}` 是偶数 → ==要反转==这一组' if S.n % 2 == 0 else f'`n = {S.n}` 是奇数 → 不用反转'),
        'for i in range': '首尾配对交换：共 `{n // 2}` 对',
        'nodes[i].val': '不改指针，直接交换值：`nodes[{i}]` 与 `nodes[{n - 1 - i}]` 互换，值变成 `{nodes[i].val}` 和 `{nodes[n - 1 - i].val}`',
        12: '这一组处理完，清空 `nodes`',
        'size += 1': '下一组要多一个节点：`size` = {size}',
        'node = node.next': '`node` 走向下一个节点',
        'return head': '头节点没变，返回 `head`：值已原地改好',
    },
    cards=dict(
        one_liner='攒够一组再决定反不反，反转只交换值',
        complexity='时间 `O(n)`，空间 `O(√n)`',
        problem=['链表按 `1, 2, 3, …` 的长度分组，把长度为偶数的组反转',
                 '示例：`[5,2,6,3,9,1,7,3,8,4]` → `[5,6,2,3,9,1,4,8,3,7]`'],
        quote='统计到 size 个节点，或到达链表末尾',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['用数组 `nodes` 攒当前组的节点；攒满 `size` 个或到末尾就结算',
              '偶数个才反转：首尾节点互换 `val`，不用改任何指针',
              '结算后清空数组，`size` 加一，继续下一组'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(√n)`（一组最多约 √(2n) 个节点）',
                 '易错：最后一组不满 `size`，要看实际个数 `n` 的奇偶',
                 '换值省去了处理指针的麻烦，头节点也不会变'],
    ),
)
