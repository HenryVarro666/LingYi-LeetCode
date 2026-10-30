import tracer
import views as V


def ll_view(label, ptrs, drop=60):
    """内置 linked 视图，但整体下移 drop 像素：给“尾→头”的弧线留出空间，不压住标题"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        V.label(cv, box, label)
        V.v_linked(cv, dict(label='', pointers=ptrs), {'_S': S, '_B': B}, (x0, y0 + drop, x1, y1), 0,
                   {'ll_pos': dict(tracer._origin)})
    return draw


def _v(x):
    return '∅' if x is None else str(x.val)


def _chain(node, limit=8):
    vals, seen = [], set()
    while node is not None and node._uid not in seen and len(vals) < limit:
        seen.add(node._uid)
        vals.append(str(node.val))
        node = node.next
    s = ' → '.join(vals) if vals else '空'
    if node is not None:
        s += ' → …（回到开头，成环）'
    return s


def _is_ring(S):
    return S['_line'] >= 15 and not ('new_head' in S and S['new_tail'].next is None)


def _info(S):
    if 'tail' not in S:
        return '把链表每个节点==向右移动 k 个位置==：原链表的倒数第 k 个节点会成为新头'
    if 'new_head' in S and S['new_tail'].next is None:
        return f"断开后：从 new_head 出发 = =={_chain(S['new_head'])}=="
    if _is_ring(S):
        return f"成环后：新头是==倒数第 {S['k']} 个==，新尾是倒数第 {S['k'] + 1} 个（正数第 {S['length'] - S['k']} 个）"
    return f"第 1 步：数长度、找尾巴。目前 `length = {S.get('length')}`"


def _while(S, B, ret):
    t = B.tail
    if t.next is not None:
        return f'`tail = {t.val}` 后面还有节点 → 继续往后走'
    return f'`tail = {t.val}` 后面没有了 → 它就是==尾节点==，链表长度 `n = {S.length}`'


def _loop(S, B, ret):
    steps = S.length - S.k - 1
    if '_' in S and S.get('_') != B.get('_'):
        return f'`new_tail` 第 `{S["_"] + 1}` 步（共 `n - k - 1 = {steps}` 步）'
    return f'走完 `{steps}` 步：`new_tail = {S.new_tail.val}` 是正数第 `n - k = {S.length - S.k}` 个 = ==倒数第 k+1 个=='


CONFIG = dict(
    num=61, title='旋转链表', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='首尾相连再断开',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return None

        # 1. 计算链表长度，并找到尾节点
        length = 1
        tail = head
        while tail.next:
            length += 1
            tail = tail.next
        k %= length

        # 2. 首尾相连
        tail.next = head

        # 3. 找倒数第 k+1 个节点，作为新链表的尾节点
        new_tail = head
        for _ in range(length - k - 1):
            new_tail = new_tail.next

        # 4. 断开倒数第 k+1 个节点（new_tail）和倒数第 k 个节点（new_head）
        new_head = new_tail.next
        new_tail.next = None
        return new_head
''',
    call='Solution().rotateRight(L([1, 2, 3, 4, 5]), 7)',
    expect=[4, 5, 1, 2, 3],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='custom', h=330, draw=ll_view('链表（上方弧线 = 尾巴连回头部）',
                                                  {'head': 'green', 'tail': 'pink', 'new_tail': 'purple', 'new_head': 'orange'})),
        dict(type='array', var=lambda S: [1, 2, 3, 4, 5], label='原链表位置（橙 = 最后 k 个，会被转到前面）', cell=84, h=150,
             color=lambda S, i, v: ('orange' if i >= 5 - S['k'] else None) if S['_line'] >= 12 else None),
    ],
    watch=[('k', 'k', 'yellow'), ('length', 'length', 'cyan'), ('tail', 'tail.val', 'pink'),
           ('new_tail', 'new_tail.val', 'purple'), ('new_head', 'new_head.val', 'orange')],
    captions={
        'if head is None': '链表非空，开始旋转（空链表直接返回 None）',
        'length = 1': '`length` 从 1 开始：`tail` 先站在头节点上，它本身算 1 个',
        8: '`tail` 从 `head = {head.val}` 出发，往后找尾节点',
        'while tail.next': _while,
        'tail = tail.next': '`tail` 走到 `{tail.val}`，`length = {length}`',
        'k %= length': '转 `n` 次等于没转：`k = {B.k} % {length} = =={k}==（k 很大也不怕）',
        'tail.next = head': '首尾相连：`{tail.val}.next` 指向 `{head.val}`，链表变成一个==环==',
        'new_tail = head': '从头出发走 `n - k - 1 = {length - k - 1}` 步，找==倒数第 k+1 个==节点（新尾巴）',
        'for _ in range(length - k - 1)': _loop,
        'new_tail = new_tail.next': '`new_tail` 走到 `{new_tail.val}`',
        'new_head = new_tail.next': '新尾巴的下一个就是==倒数第 k 个==：`new_head = {new_head.val}`',
        'new_tail.next = None': '断开 `{new_tail.val} → {new_head.val}`：环在这里剪开，又变回一条链',
        'return new_head': lambda S, B, r: f'返回 `new_head` → =={_chain(r)}==',
    },
    skip=['length += 1'],
    cards=dict(
        one_liner='先把尾巴接回头部连成环，再在倒数第 k+1 个节点后面剪开',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你链表头节点 `head`，把链表每个节点==向右移动 `k` 个位置==',
                 '示例：`head = [1,2,3,4,5], k = 2` → `[4,5,1,2,3]`',
                 '`k` 最大可达 `2×10^9`；本视频用 `k = 7`（等价于 `k = 2`）'],
        quote='旋转后，原链表的==倒数第 k 个节点，成为新链表的头节点==。……旋转 k 次等价于旋转 k mod n 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['① 遍历一遍：求长度 `n`、找到尾节点，`k %= n`',
              '② 首尾相连：`tail.next = head`，链表变成环',
              '③ 从头走 `n-k-1` 步到==倒数第 k+1 个==（新尾），断开它和倒数第 k 个（新头）'],
        result='返回 `[4,5,1,2,3]` ✓ 与示例答案一致',
        summary=['时间 `O(n)`（最多两趟），空间 `O(1)`',
                 '易错：一定先 `k %= n`，否则 `k = 2×10^9` 会走到天荒地老',
                 '倒数第 `k+1` 个 = 正数第 `n-k` 个，从 head 出发只走 `n-k-1` 步',
                 '`k % n == 0` 时走 `n-1` 步到原尾巴，断开后链表不变，无需特判'],
    ),
)
