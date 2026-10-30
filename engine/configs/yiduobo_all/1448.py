DONE = {}


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


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.get('now') is not None:
            DONE[S.now._uid] = S.now.val >= S.max_num
        for n in _walk(S.get('root')):
            n._g = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _txt(S):
    now, mx = S.get('now'), S.get('max_num')
    if now is None or mx is None:
        return '`q` 里每项是 `[节点, 根到它父亲的路径最大值]`'
    ok = now.val >= mx
    return f'节点 `{now.val}`，路径最大值 `{mx}`：`{now.val} >= {mx}` ' + ('==成立，好节点==' if ok else '不成立')


CONFIG = dict(
    num=1448, title='统计二叉树中好节点的数目', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BFS · 队列里带着路径最大值',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1360'],
    code='''
class Solution(object):
    def goodNodes(self, root):

        q = [[root, root.val]]
        l = 0
        r = 1
        res = 0
        while l < r:
            now, max_num = q[l]
            l += 1
            if now.val >= max_num:
                max_num = now.val
                res += 1
            if now.left:
                q.append([now.left, max_num])
                r += 1
            if now.right:
                q.append([now.right, max_num])
                r += 1
        
        return res
''',
    call='Solution().goodNodes(Tr([3,1,4,3,None,1,5]))',
    expect=4,
    skip=['l += 1', 'r += 1', 'l = 0', 'r = 1', 'res = 0'],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='tree', label='二叉树（绿 = 好节点，粉 = 不是好节点，蓝 = 正在处理）', pointers={'now': 'blue'}, path=False, h=330,
             color=lambda S, n: 'green' if getattr(n, '_g', None) is True else ('pink' if getattr(n, '_g', None) is False else None)),
        dict(type='queue', var=lambda S: S.get('q'), label='q（队列，下标 l 起是待处理的）', fmt=lambda e: f'{e[0].val}|{e[1]}', h=160),
        dict(type='text', fn=lambda S: (f"已找到好节点 `res = {S['res']}`；队列指针 `l = {S['l']}`，`r = {S['r']}`" if 'res' in S else ''), size=26, h=60),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'), ('max_num', 'max_num', 'orange'), ('res', 'res', 'green'), ('l', 'l'), ('r', 'r')],
    captions={
        'q = [[root': '从根出发：根一定是好节点，队列里放 `[根, 根的值]`',
        'while l < r': lambda S, B, r: (f'队列里还有 `{S.r - S.l}` 个节点没处理 → 继续' if S.l < S.r else '队列处理完了'),
        'now, max_num = q[l]': track(lambda S, B, r: f'取出节点 `{S.now.val}`，它父亲那条路径上的最大值是 `{S.max_num}`'),
        'if now.val >= max_num': track(lambda S, B, r: (f'`{S.now.val} >= {S.max_num}`：路径上没有比它更大的 → ==好节点==' if S.now.val >= S.max_num
                                                       else f'`{S.now.val} < {S.max_num}`：路径上有更大的值 → 不是好节点，`max_num` 保持 `{S.max_num}`'), record=True),
        'max_num = now.val': track(lambda S, B, r: f'好节点的值成为新的路径最大值 `max_num = {S.max_num}`，孩子们会带着它'),
        'res += 1': track(lambda S, B, r: f'好节点数 `res = {S.res}`'),
        'if now.left': lambda S, B, r: (f'有左孩子 `{S.now.left.val}` → 入队，带上 `max_num = {S.max_num}`' if S.now.left else '没有左孩子'),
        'if now.right': lambda S, B, r: (f'有右孩子 `{S.now.right.val}` → 入队，带上 `max_num = {S.max_num}`' if S.now.right else '没有右孩子'),
        'q.append([now.left': track(lambda S, B, r: f'左孩子 `{S.now.left.val}` 入队：`[{S.now.left.val}, {S.max_num}]`'),
        'q.append([now.right': track(lambda S, B, r: f'右孩子 `{S.now.right.val}` 入队：`[{S.now.right.val}, {S.max_num}]`'),
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='BFS 一层层走，队列里每个节点带着「根到它父亲」的最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树里「好节点」X：从根到 X 的路径上，没有任何节点的值大于 X',
                 '统计好节点的个数，根节点一定是好节点',
                 '示例：`[3,1,4,3,null,1,5]` → `4`'],
        quote='对于f\\[now\\]而言，则可以通过f\\[father\\[now\\]\\]与now.val的得来……一个自然的想法是从根节点开始进行bfs，在bfs的过程同步更新f值以及答案即可。'.replace('\\', ''),
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now]` = 根到 `now` 路径上的最大值，等于 `max(f[父亲], now.val)`',
              '所以必须==先处理父亲、再处理孩子== → 从根开始 BFS',
              '队列里存 `[节点, 父亲传来的最大值]`：`now.val >= max_num` 就是好节点，并更新最大值再传给孩子'],
        result='运行结束，返回 `4`：好节点是 `3`、`4`、`3`、`5`',
        summary=['时间 `O(n)`，空间 `O(n)`（队列）',
                 '易错：比较用 `>=`，相等也算好节点；孩子拿到的是更新后的 `max_num`',
                 '队列用 `l`、`r` 两个下标模拟，`q` 不删除元素，只是 `l` 往后移',
                 '原文已是 Python 3 可运行写法，未改动',
                 '对比灵神：他用 DFS 递归，把 `mx` 当参数往下传，写法只有 5 行']),
)
