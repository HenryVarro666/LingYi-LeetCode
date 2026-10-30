# queue.Queue 内含线程锁，不能 deepcopy；setup 里用 copyreg 注册一个按内容重建的方法，追踪器才能拍下队列快照
SETUP = '''
import copyreg, queue
def _rebuild(items, maxsize):
    q = queue.Queue(maxsize)
    q.queue.extend(items)
    return q
copyreg.pickle(queue.Queue, lambda q: (_rebuild, (list(q.queue), q.maxsize)))
'''

DONE = set()   # 值已配对相等的节点
GETS = [0]     # 到目前为止 q.get() 的次数（决定队首元素属于第几对）


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def track(fn, get=False, mark=False):
    def cap(S, B, ret):
        if get:
            GETS[0] += 1
        if mark and S.node1.val == S.node2.val:
            DONE.update([S.node1._uid, S.node2._uid])
        if S.get('q') is not None:
            S.q._gets = GETS[0]
        for n in _walk(S.get('root')):
            n._d = n._uid in DONE
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def nv(x):
    return '空' if x is None else str(x.val)


def draw_queue(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'q（队首 → 队尾，每两个一对；紫 = 下一对）', 24, T['muted'], bold=True)
    q = S.get('q')
    if q is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    items = list(q.queue)
    g = getattr(q, '_gets', 0)
    if not items:
        cv.text((x0 + 18, y0 + 66), '空', 26, T['dim'], anchor='lm')
    w, gap, pair_gap = 64, 6, 22
    x, y = x0 + 22, y0 + 44
    for k, it in enumerate(items):
        idx = g + k            # 绝对序号：偶数位是一对的第一个
        if idx % 2 == 0 and k > 0:
            x += pair_gap
        if x + w > x1 - 20:
            cv.text((x, y + 24), '…', 26, T['muted'], anchor='lm')
            break
        front = k < 2 - (g % 2)
        fill = T['purple'] if front else T['panel2']
        cv.rect((x, y, x + w, y + 48), fill=fill, outline=T['border'], width=1, r=10)
        cv.text((x + w / 2, y + 24), nv(it), 24, T['bg'] if front else T['text'], anchor='mm', bold=True, mono=True)
        if idx % 2 == 1 and k > 0:  # 画一对的括号
            cv.line([(x - w - gap + 4, y + 58), (x + w - 4, y + 58)], T['cyan'] if not front else T['purple'], 3)
        x += w + gap


PAIRS = set()


def cap_get2(S, B, ret):
    n1, n2 = S.node1, S.node2
    if n1 is not None and n2 is not None and n1 is not n2:
        dup = (n2._uid, n1._uid) in PAIRS
        PAIRS.add((n1._uid, n2._uid))
        if dup:
            return f'再取 `node2 = {n2.val}`：这一对是前面某一对==反过来==（根入队两次，每对会查两遍）'
    return f'再取一个 `node2 = {nv(n2)}`：它应该和 `node1` ==互为镜像=='


def cap_while(S, B, ret):
    n = len(B.q.queue)
    if n:
        return f'队列非空（还有 {n} 个，即 {n // 2} 对）→ 取出下一对'
    return '队列空了 → 所有镜像对都检查完毕，跳出循环'


def cap_val(S, B, ret):
    if S.node1.val != S.node2.val:
        return f'`{S.node1.val} != {S.node2.val}` → ==值不相等=='
    return f'`{S.node1.val} == {S.node2.val}` ✓ 值相等 → 把它们的孩子按镜像关系入队'


CONFIG = dict(
    num=101, title='对称二叉树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='迭代 · 队列成对比较',
    code='''
class Solution(object):
    def isSymmetric(self, root):
        import queue

        q = queue.Queue()

        q.put(root)
        q.put(root)

        while not q.empty():
            node1 = q.get()
            node2 = q.get()
            if node1 is None:
                if node2 is None:
                    continue
                else:
                    return False
            else:
                if node2 is None:
                    return False
                else:
                    if node1.val != node2.val:
                        return False
                    else:
                        q.put(node1.left)
                        q.put(node2.right)
                        q.put(node1.right)
                        q.put(node2.left)

        return True
''',
    setup=SETUP,
    call='Solution().isSymmetric(Tr([1,2,2,None,3,4]))',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（绿 = 已配对且值相等）', pointers={'node1': 'blue', 'node2': 'pink'}, h=370, path=False,
             color=lambda S, n: 'green' if getattr(n, '_d', False) else None),
        dict(type='custom', draw=draw_queue, h=130),
        dict(type='text', h=60, fn=lambda S: (f"正在比较：`node1 = {nv(S['node1'])}`  vs  `node2 = {nv(S['node2'])}`"
                                               if 'node2' in S else '')),
    ],
    watch=[('node1', 'node1', 'blue'), ('node2', 'node2', 'pink')],
    captions={
        'import queue': track('原文是 Python 2 的 `import Queue`；Python 3 里这个模块叫 `queue`'),
        'q = queue.Queue()': track('建一个先进先出的队列 `q`，==里面的元素两个一组=='),
        7: track('根节点入队……'),
        8: track('……再入队一次：第一对就是「整棵树」和「它自己」，==互为镜像才对称=='),
        'while not q.empty()': track(cap_while),
        'node1 = q.get()': track(lambda S, B, ret: f'取出队首 `node1 = {nv(S.node1)}`', get=True),
        'node2 = q.get()': track(cap_get2, get=True),
        'if node1 is None': track(lambda S, B, ret: '`node1` 是空 → 看 `node2`' if S.node1 is None
                                  else f'`node1 = {S.node1.val}` 不为空 → 走 `else`'),
        14: track(lambda S, B, ret: '`node2` 也是空 → 空对空，镜像成立' if S.node2 is None
                  else f'`node2 = {S.node2.val}` 不为空 → 一空一不空'),
        'continue': track('这一对没问题，`continue` 检查下一对'),
        17: track('一空一不空 → ==不对称==，返回 `False`'),
        19: track(lambda S, B, ret: f'`node2` 是空，`node1 = {S.node1.val}` 不是' if S.node2 is None
                  else f'`node2 = {S.node2.val}` 也不为空 → 比较值'),
        20: track('一空一不空 → ==不对称==，返回 `False`'),
        'if node1.val != node2.val': track(cap_val, mark=True),
        23: track(lambda S, B, ret: f'镜像位置的值 `{S.node1.val}` 和 `{S.node2.val}` 不同 → ==不对称==，返回 `False`'),
        'q.put(node1.left)': track(lambda S, B, ret: f'外侧一对：先放 `node1.left`（{nv(S.node1.left)}）'),
        'q.put(node2.right)': track(lambda S, B, ret: f'再放 `node2.right`（{nv(S.node2.right)}），和上一个凑成==外侧==一对'),
        'q.put(node1.right)': track(lambda S, B, ret: f'内侧一对：先放 `node1.right`（{nv(S.node1.right)}）'),
        'q.put(node2.left)': track(lambda S, B, ret: f'再放 `node2.left`（{nv(S.node2.left)}），凑成==内侧==一对'),
        'return True': track('队列取空也没发现问题 → 对称，返回 `True`'),
    },
    cards=dict(
        one_liner='把递归改成队列：每次取出两个，判断它们是否互为镜像',
        complexity='时间 `O(n)`，空间 `O(n)`（队列）',
        problem=['给你二叉树的根 `root`，检查它是否==轴对称==',
                 '示例 1：`[1,2,2,3,4,4,3]` → `true`',
                 '本视频：`[1,2,2,null,3,4]` → `false`（`3` 和 `4` 在镜像位置）'],
        quote='将递归的做法改成队列，即依次将 ==a.left，b.right，a.right，b.left== 入队，然后每次取队首前两位判断 val 是否相等。',
        quote_src='—— yiduobo 题解（迭代做法）',
        idea=['递归版：值相等，且外侧、内侧两对子树分别对称',
              '迭代版：队列里==两个一组==，每组就是一次递归调用的参数',
              '一空一不空、值不同 → 立即 `False`；两个都空 → `continue`'],
        result='运行结束，返回 `False`：内侧那一对是 `3` 和 `4`，值不同',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '根入队两次，相当于从 `(root, root)` 开始：每对会被检查两遍，但不影响正确性',
                 'yiduobo 还提到：逐层层序遍历，看每层是否回文，也能判断',
                 '原文为 Python 2：`Queue` 模块已改为 Python 3 的 `queue`；删去 docstring'],
    ),
)
