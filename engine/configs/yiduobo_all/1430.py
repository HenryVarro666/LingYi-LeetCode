def _nv(x):
    return '空' if x is None else str(x.val)


def _info(S):
    lv = S['_inner'].get('level')
    arr = S.get('arr')
    if lv is None or arr is None:
        return '搜索回溯：每层按 `arr[level]` 选一个值相同的孩子往下走'
    if lv >= len(arr):
        return f'`level = {lv}` == `len(arr)`：`arr` 已用完，看当前节点是不是==叶子=='
    return f'`level = {lv}`：要在孩子里找值为 `arr[{lv}] = {arr[lv]}` 的节点'


def cap_leaf(S, B, ret):
    n = S.now
    if not n.left and not n.right:
        return f'`{n.val}` 没有左右孩子 → 是==叶子== → 序列刚好走到叶子，返回 True'
    return f'`{n.val}` 还有孩子 → 序列到这里就结束了，不是到叶子的路径 → 返回 False'


def cap_child(side, word):
    def f(S, B, ret):
        n = B.now
        ch = getattr(n, side)
        lv = B.level
        if ch is None:
            return f'`{n.val}` 没有{word}孩子 → 这边走不通，跳过'
        if ch.val == B.arr[lv]:
            return f'{word}孩子 `{ch.val}` == `arr[{lv}] = {B.arr[lv]}` → 值相同，==试着往{word}走=='
        return f'{word}孩子 `{ch.val}` != `arr[{lv}] = {B.arr[lv]}` → 不匹配，跳过'
    return f


CONFIG = dict(
    num=1430, title='判断给定的序列是否是二叉树从根到叶的路径', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='搜索回溯 · DFS',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def isValidSequence(self, root, arr):

        def dfs(level, now):
            if level == len(arr):
                if not now.left and not now.right:
                    return True
                else:
                    return False
            
            if now.left and now.left.val == arr[level]:
                if dfs(level + 1, now.left):
                    return True
            
            if now.right and now.right.val == arr[level]:
                if dfs(level + 1, now.right):
                    return True
            
            return False
        
        if arr[0] != root.val:
            return False

        return dfs(1, root)
''',
    call='''s = Solution()
s.tree = Tr([0,1,1,2,None,3])
s.isValidSequence(s.tree, [0,1,3])''',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=50),
        dict(type='array', var='arr', label='arr（蓝 = 下一个要匹配的位置 level）', pointers={'level': 'blue'}, cell=72, h=140),
        dict(type='tree', label='二叉树（蓝 = now；黄圈 = 当前搜索路径）', pointers={'now': 'blue'}, h=230),
        dict(type='calls', h=190),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'),
           ('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'yellow')],
    captions={
        'if arr[0] != root.val': lambda S, B, r: (f'先看根：`arr[0] = {B.arr[0]}`，`root.val = {B.root.val}` → ' + ('不等，直接 False' if B.arr[0] != B.root.val else '相等，根这一步匹配，从 `level = 1` 开始往下搜')),
        'return dfs(1, root)': '从根出发开始搜：`level = 1` 表示下一个要匹配 `arr[1]`',
        'if level == len(arr)': '`level = {level}`，`len(arr) = {len(arr)}` → ' + '{"arr 已用完，该检查叶子" if level == len(arr) else "arr 还没用完，继续往下找"}',
        'if not now.left and not now.right': cap_leaf,
        'return True': lambda S, B, r: '找到一条完整路径 → 返回 ==True==，一路传回去',
        'return False': lambda S, B, r: ('不是叶子 → 这条路径不合法 → 返回 False' if S.get('level') == len(S.get('arr', [])) else '左右都试过了，没有走通 → ==回溯==：返回 False，回到上一层试别的孩子'),
        'if now.left and now.left.val': cap_child('left', '左'),
        'if now.right and now.right.val': cap_child('right', '右'),
        'if dfs(level + 1, now.left)': lambda S, B, r: f'进入左孩子 `{_nv(B.now.left)}`，下一个匹配 `arr[{B.level + 1}]`',
        'if dfs(level + 1, now.right)': lambda S, B, r: f'进入右孩子 `{_nv(B.now.right)}`，下一个匹配 `arr[{B.level + 1}]`',
    },
    cards=dict(
        one_liner='按 arr 一位一位往下搜，值相同才进，走不通就回溯',
        complexity='时间 最坏 `O(n)`（每个节点至多进一次），空间 `O(h)`',
        problem=['给你二叉树的根 `root` 和一个整数数组 `arr`',
                 '判断 `arr` 是否是==从根到叶子==的一条路径上的节点值序列',
                 '本视频：`root = [0,1,1,2,null,3]`，`arr = [0,1,3]` → `true`'],
        quote='搜索回溯的题目。从根节点开始向下进行搜索回溯，每一轮都根据当前arr中对应的值以及当前节点左右孩子的值决定往哪个节点继续向下搜索回溯。需要注意的是，题目中左右节点的值可能相同。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(level, now)`：`now` 已匹配 `arr[level-1]`，现在看孩子能否匹配 `arr[level]`',
              '`arr` 用完（`level == len(arr)`）时，`now` 必须是叶子才算数',
              '左右孩子值可能相同，所以左边走不通要==回溯==去试右边'],
        result='返回 `True`：先走左边 `0→1→?` 走不通，回溯后走右边 `0→1→3`',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：`arr` 用完时当前节点必须是叶子，否则只是路径的前缀',
                 '易错：左右孩子值可能相同，不能只选一边，要左边失败后再试右边',
                 '先单独检查 `arr[0] == root.val`，`dfs` 从 `level = 1` 起'],
    ),
)
