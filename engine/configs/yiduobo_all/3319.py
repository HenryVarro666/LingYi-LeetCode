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


def _rec(fn, record=False):
    def cap(S, B, ret):
        n = S.get('now')
        if record and n is not None:
            DONE[n._uid] = ret[0]
        for m in _walk(S.get('self.tree')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


import re as _re


def _fmt(t):
    def f(S, B, r):
        env = {'B': B, 'ret': r, 'sorted': sorted, 'len': len, 'max': max, 'min': min}
        return _re.sub(r'\{([^{}]+)\}', lambda m: str(eval(m.group(1), env, S)), t)
    return f


def _wrap(d):
    return {k: _rec(v if callable(v) else _fmt(v)) for k, v in d.items()}


def _st(n):
    d = getattr(n, '_d', None)
    return None if d is None else ('green' if d else 'red')


def _clear(S, B, r):
    DONE.clear()
    return '`heap` 是小根堆，最多留 `k` 个高度：==堆顶就是第 k 大==；`dfs` 返回 `(是否完美, 高度)`'


def _cap_l(S, B, ret):
    return f'节点 `{B.now.val}` 有左儿子 → 先递归求左子树的 `(是否完美, 高度)`'


def _cap_r(S, B, ret):
    return f'节点 `{B.now.val}` 有右儿子 → 同样递归求右子树'


def _cap_if(S, B, ret):
    n = S.now
    ok = S.left_prefect and S.right_prefect and S.left_height == S.right_height
    if ok:
        return f'节点 `{n.val}`：左右都完美且高度同为 `{S.left_height}` → ==当前子树完美=='
    return f'节点 `{n.val}`：左 `({S.left_prefect}, {S.left_height})`，右 `({S.right_prefect}, {S.right_height})` → ==不完美=='


def _info(S):
    h = S.get('heap')
    return f"小根堆 `heap = {sorted(h) if h is not None else []}`，只保留最大的 `k = {S.get('k')}` 个高度"


CONFIG = dict(
    num=3319, title='第 K 大的完美二叉子树的大小', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS + 大小为 k 的小根堆',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1603'],
    code='''
class Solution(object):
    def kthLargestPerfectSubtree(self, root, k):
        
        heap = []
        def dfs(now):
            left_prefect, left_height = True, 0 
            if now.left:
                left_prefect, left_height = dfs(now.left)
            
            right_prefect, right_height = True, 0
            if now.right:
                right_prefect, right_height = dfs(now.right)
            
            height = max(left_height, right_height) + 1
            if left_prefect and right_prefect and left_height == right_height:
                prefect = True
                heapq.heappush(heap, height)
                if len(heap) > k:
                    heapq.heappop(heap)
            else:
                prefect = False

            return prefect, height
        
        dfs(root)
        if len(heap) < k:
            return -1
        
        return (1 << (heap[0])) - 1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,6,7,8,9])
s.kthLargestPerfectSubtree(s.tree, 2)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 完美子树，红 = 不完美）', pointers={'now': 'blue'}, h=320, color=lambda S, n: _st(n)),
        dict(type='heap', var='heap', label='heap（只留最大的 k 个高度）', cell=64, h=200, fmt=lambda x: str(x)),
        dict(type='calls', h=210, hide=('heap',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('左(完美, 高)', lambda S: (S['_inner'].get('left_prefect'), S['_inner'].get('left_height'))),
           ('右(完美, 高)', lambda S: (S['_inner'].get('right_prefect'), S['_inner'].get('right_height'))),
           ('k', 'k', 'yellow')],
    captions=_wrap({
        'heap = []': _clear,
        'left_prefect, left_height = True, 0': '默认左边是「空」：==空子树算完美，高度 0==',
        'if now.left': lambda S, B, r: f'节点 `{S.now.val}` 有左儿子 → 去求左子树' if S.now.left else f'节点 `{S.now.val}` 没有左儿子 → 保持默认 `(True, 0)`',
        'left_prefect, left_height = dfs': _cap_l,
        'right_prefect, right_height = True, 0': '右边同理，先默认 `(True, 0)`',
        'if now.right': lambda S, B, r: f'节点 `{S.now.val}` 有右儿子 → 去求右子树' if S.now.right else f'节点 `{S.now.val}` 没有右儿子 → 保持默认 `(True, 0)`',
        'right_prefect, right_height = dfs': _cap_r,
        'height = max': '当前子树高度 = 较高一边 + 1 = `{height}`',
        'if left_prefect': _cap_if,
        'prefect = True': '完美：标记 `prefect = True`',
        'heapq.heappush': '高度 `{height}` 入堆 → `{sorted(heap)}`',
        'if len(heap) > k': lambda S, B, r: f'堆里 `{len(S.heap)}` 个 > `k = {S.k}`？' + ('==是，弹出最小的==' if len(S.heap) > S.k else '否，先留着'),
        'heapq.heappop': '弹掉堆顶（最小高度）：==堆里始终是最大的 k 个==，现在 `{sorted(heap)}`',
        'prefect = False': '左右不都完美或高度不同 → ==不完美==，==祖先也不可能完美==',
        'return prefect, height': _rec(lambda S, B, r: f'返回 `{r}` 给父节点', True),
        'if len(heap) < k': lambda S, B, r: f'堆里只有 `{len(S.heap)}` 个，`k = {S.k}`：' + ('不够 k 个 → 返回 `-1`' if len(S.heap) < S.k else '够 k 个 → 堆顶就是第 k 大'),
        'return (1 << (heap[0])) - 1': '堆顶高度 `{heap[0]}` → 节点数 `2^{heap[0]} - 1` = =={ret}==',
    }),
    skip=['dfs(root)', 'left_prefect, left_height = True, 0', 'right_prefect, right_height = True, 0', 'if now.left', 'if now.right', 'prefect = True'],
    max_steps=90,
    cards=dict(
        one_liner='完美子树只看高度：用大小为 k 的小根堆留住最大的 k 个高度',
        complexity='时间 `O(n log k)`，空间 `O(n + k)`',
        problem=['给你二叉树 `root` 和整数 `k`，求第 `k` 大的==完美二叉子树==的节点数',
                 '完美二叉树：所有叶子在同一层，且每个父节点恰有两个孩子',
                 '不存在则返回 `-1`',
                 '本视频：`root = [1,2,3,4,5,6,7,8,9]`，`k = 2` → `3`'],
        quote='对于完美二叉树，只有以下两种构成：1、单独的叶子节点 2、左右子树都为完美二叉树，且左右子树的高度也相同。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs` 返回 `(是否完美, 高度)`：左右都完美且高度相同，当前子树才完美',
              '高度为 `h` 的完美二叉树共 `2^h - 1` 个节点，所以只需找==高度第 k 大==',
              '用大小为 `k` 的小根堆装高度，超了就弹堆顶，最后堆顶即答案'],
        result='堆里剩 `[2, 2]`，堆顶 `2` → 返回 `2^2 - 1 = 3`',
        summary=['时间 `O(n log k)`，空间 `O(n + k)`（递归栈 + 堆）',
                 '对比灵神：他用数组计数；这里用小根堆，不需要知道高度上限',
                 '易错：空孩子要当成 `(True, 0)`，否则叶子判断会出错；不足 `k` 个时返回 `-1`',
                 '原文为 Python 2 写法，本身无需改动（变量名 `prefect` 是原文拼写）'],
    ),
)
