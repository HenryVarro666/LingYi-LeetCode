DONE = {}   # 节点 _uid -> (最大深度, path_flag)


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


def _rec(fn):
    def cap(S, B, ret):
        n = S.get('now')
        if n is not None and isinstance(ret, tuple):
            DONE[n._uid] = ret
        for m in _walk(S.get('root')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _color(S, n):
    d = getattr(n, '_d', None)
    if n.val == 3:
        return 'yellow'
    if d is not None and d[1]:
        return 'orange'
    if d is not None:
        return 'green'
    return None


def _info(S):
    sd = S.get('self.start_depth')
    return f"`start_depth = {sd}`　`res = {S.get('self.res', 0)}`" if sd is not None else f"还没找到 start　`res = {S.get('self.res', 0)}`"


def _cap_final(S, B, ret):
    n = S.now
    md = S._inner['max_depth']
    if S.now.val == S.start:
        return f'`{n.val}` 就是 start，记下它的深度 `{S.depth}`；情形 1：start 往下的最大深度 `{md}` 就是候选答案'
    return ''


def _cap_left(S, B, ret):
    n = S.now
    return (f'左子树含 start：先走到 `{n.val}`（深度 `{S.depth}`），再往右子树一路走到底 `{S.right_max_depth}` 步'
            f'，总长 `{S.self.start_depth} - {S.depth} + {S.right_max_depth}` = =={S.self.start_depth - S.depth + S.right_max_depth}==')


def _cap_right(S, B, ret):
    n = S.now
    return (f'右子树含 start：从 start 上到 `{n.val}`，再往左子树走到底 `{S.left_max_depth}` 步'
            f'，总长 `{S.self.start_depth} - {S.depth} + {S.left_max_depth}` = =={S.self.start_depth - S.depth + S.left_max_depth}==')


CONFIG = dict(
    num=2385, title='感染二叉树需要的总时间', difficulty='Medium',
    category='链表、二叉树与回溯',
    author='yiduobo', technique='一次 DFS · 记录 start 深度 + path_flag',
    tags=['动态规划', '链表树与回溯', '难度分 1711'],
    code='''
class Solution(object):
    def amountOfTime(self, root, start):

        self.res = 0
        self.start_depth = None

        def dfs(now, depth):
            if now.left:
                left_max_depth, left_path_flag = dfs(now.left, depth + 1)
            else:
                left_max_depth = 0
                left_path_flag = False

            if now.right:
                right_max_depth, right_path_flag = dfs(now.right, depth + 1)
            else:
                right_max_depth = 0
                right_path_flag = False
            
            max_depth = max(left_max_depth, right_max_depth)
            path_flag = False

            if now.val == start:
                self.start_depth = depth
                self.res = max_depth
                path_flag = True
            elif left_path_flag:
                self.res = max(self.res, self.start_depth - depth + right_max_depth)
                path_flag = True
            elif right_path_flag:
                self.res = max(self.res, self.start_depth - depth + left_max_depth)
                path_flag = True

            return max_depth + 1, path_flag
        
        dfs(root, 0)
        return self.res
''',
    call='Solution().amountOfTime(Tr([1,5,3,None,4,10,6,9,2]), 3)',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（黄 = start，橙 = path_flag 为真，绿 = 为假）', pointers={'now': 'blue'}, h=330, color=_color),
        dict(type='text', fn=_info, size=26, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('depth', lambda S: S['_inner'].get('depth')),
           ('max_depth', lambda S: S['_inner'].get('max_depth')),
           ('path_flag', lambda S: S['_inner'].get('path_flag'), 'orange'),
           ('res', 'self.res', 'green')],
    captions={
        'self.res = 0': '`res` 存答案，`start_depth` 存 start 的深度（还没找到）',
        'if now.left:': lambda S, B, r: (f'`{S.now.val}` 有左儿子 → 递归下去，深度 +1' if S.now.left else f'`{S.now.val}` 没有左儿子'),
        'left_max_depth = 0': '没有左儿子：最大深度 `0`，path_flag 为假',
        'if now.right:': lambda S, B, r: (f'`{S.now.val}` 有右儿子 → 递归下去，深度 +1' if S.now.right else f'`{S.now.val}` 没有右儿子'),
        'right_max_depth = 0': '没有右儿子：最大深度 `0`，path_flag 为假',
        'max_depth = max': '两边子树的较大深度 `{max_depth}`：以 `now` 为根往下最远能走多远',
        'path_flag = False': '先假设 start 不在这棵子树里',
        'if now.val == start': lambda S, B, r: (f'`{S.now.val} == {S.start}` → ==找到 start==' if S.now.val == S.start else f'`{S.now.val}` 不是 start'),
        'self.start_depth = depth': '记下 start 的深度 `{depth}`，后面祖先要用它算「向上走几步」',
        'self.res = max_depth': '情形 1：答案至少是 start 往下的最大深度 `{max_depth}`',
        'path_flag = True': '标记「start 在这棵子树里」，让祖先知道要走情形 2',
        'elif left_path_flag': lambda S, B, r: (f'左子树含 start → 走情形 2：start 先向上到 `{S.now.val}`，再往右走到底' if S.left_path_flag else f'左子树不含 start，看右边'),
        'elif right_path_flag': lambda S, B, r: (f'右子树含 start → 走情形 2：start 先向上到 `{S.now.val}`，再往左走到底' if S.right_path_flag else f'左右都没有 start，不更新答案'),
        'self.res = max(self.res, self.start_depth - depth + right': _cap_left,
        'self.res = max(self.res, self.start_depth - depth + left': _cap_right,
        'return max_depth + 1': _rec(lambda S, B, r: f'`{S.now.val}` 返回（最大深度 `{r[0]}`，path_flag `{r[1]}`）：深度 +1 把自己算进去'),
        'dfs(root, 0)': '从根节点（深度 `0`）出发，只遍历一遍',
        'return self.res': '`res` 就是感染整棵树的分钟数',
    },
    skip=['dfs(root, 0)', 'left_max_depth = 0', 'left_path_flag = False', 'right_max_depth = 0', 'right_path_flag = False', 'path_flag = False', 'max_depth = max'],
    max_steps=110,
    cards=dict(
        one_liner='一次 DFS：start 往下走，或先向上到祖先再往另一侧走到底',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树节点值互不相同，第 `0` 分钟从 `start` 开始感染',
                 '每分钟感染与已感染节点相邻的节点',
                 '示例：`root = [1,5,3,null,4,10,6,9,2]`，`start = 3` → `4`'],
        quote='最终答案有两种可能：1、从start到以start为根的子树中某个节点的距离；2、从start向上走若干步到达某个祖先节点p，然后从p出发向不是start所在的子树一侧一直走到底',
        quote_src='—— yiduobo 知乎题解',
        idea=['问题就是「离 start 最远的节点有多远」，不必真的 BFS 模拟感染',
              '递归返回 `(最大深度, path_flag)`，`path_flag` 表示 start 是否在这棵子树里',
              '到达祖先 `now` 时：`start_depth - depth` 是向上走的步数，加上另一侧子树的最大深度'],
        result='运行结束，返回 `4`：从 `3` 上到 `1`，再沿 `5 → 4 → 9` 走到底',
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈）',
                 '易错：祖先处要用 ==另一侧== 子树的深度，而不是 start 所在一侧',
                 '`start_depth` 必须在遇到 start 时才赋值：start 一定先于它的祖先结束递归，所以祖先处已可用',
                 '对比灵神：灵神把链长在返回值里传递；yiduobo 用全局深度差 `start_depth - depth` 计算',
                 '原文先说 BFS 做法（先记父亲再 BFS），代码用的是一次 DFS，无需 Python 2 改动'],
    ),
)
