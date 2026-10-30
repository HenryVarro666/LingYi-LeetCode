def _k(t):
    if t is None:
        return '∅'
    return f'({t[0]},{_k(t[1])},{_k(t[2])})'


def _nv(n):
    return '空' if n is None else str(n.val)


def _info(S):
    r = S.get('self.res')
    r = [n.val for n in r] if r else []
    return f'已找到的重复子树根 `res = {r}`'


def _cap_key(S, B, ret):
    return (f'节点 `{S.now.val}` 的“指纹” = `(值, 左指纹, 右指纹)` = `{_k(S.tree_key)}`')


def _cap_cnt(S, B, ret):
    return f'节点 `{S.now.val}` 的指纹 `{_k(S.tree_key)}` 已出现 =={S.tree_dict[S.tree_key]}== 次'


def _cap_two(S, B, ret):
    if S.tree_dict[S.tree_key] == 2:
        return f'指纹 `{_k(S.tree_key)}` ==恰好第二次出现== → 记下根 `{S.now.val}`（第三次起不重复记）'
    return f'次数是 `{S.tree_dict[S.tree_key]}`，不是 2 → 不记（第 1 次还不算重复，第 3 次以后已记过）'


CONFIG = dict(
    num=652, title='寻找重复的子树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='子树序列化 + 哈希表',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findDuplicateSubtrees(self, root):

        tree_dict = {}
        self.res = []
        self.dfs(root, tree_dict)
        return self.res

    def dfs(self, now, tree_dict):
        if now:
            tree_key = (now.val, self.dfs(now.left, tree_dict), self.dfs(now.right, tree_dict))
            tree_dict[tree_key] = tree_dict.get(tree_key, 0) + 1
            if tree_dict[tree_key] == 2:
                self.res.append(now)
            return tree_key
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,None,2,4,None,None,4])
s.findDuplicateSubtrees(s.tree)''',
    result_fn=lambda r: [n.val for n in r],
    expect=[4, 2],
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=330),
        dict(type='text', fn=_info, size=26, h=56),
        dict(type='map', var='tree_dict', label='tree_dict：子树指纹 → 出现次数（∅ = 空子树）',
             fmt=lambda k, v: f'{_k(k)} : {v}', font=22, h=260),
        dict(type='calls', h=200, hide=('tree_dict',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('tree_key', lambda S: _k(S['_inner'].get('tree_key')) if S['_inner'].get('tree_key') else None, 'yellow')],
    captions={
        'tree_dict = {}': '`tree_dict`：把每棵子树做成一个键，统计它出现几次',
        'self.res = []': '`res` 收集重复子树的根（每种只收一个）',
        'self.dfs(root': '从根出发做 dfs，==后序==：先拿到左右子树的指纹，再造自己的',
        'if now:': lambda S, B, r: (f'节点 `{S.now.val}` 非空 → 继续' if S.now else '空节点 → 不返回指纹（`None`），代表空子树'),
        'tree_key = (': '要造指纹 `(值, 左指纹, 右指纹)`：先递归拿到左、右子树的指纹',
        'tree_dict[tree_key] = tree_dict.get': _cap_cnt,
        'if tree_dict[tree_key] == 2': _cap_two,
        'self.res.append': lambda S, B, r: f'把 `{S.now.val}` 作为重复子树的根加入 `res` → `{[n.val for n in S["self.res"]]}`',
        'return tree_key': lambda S, B, r: f'把指纹 `{_k(r)}` 交给父节点，用来拼父亲的指纹',
        'return self.res': lambda S, B, r: f'重复子树的根：`{[n.val for n in r]}`',
    },
    cards=dict(
        one_liner='把每棵子树变成 (值, 左指纹, 右指纹) 丢进哈希表，数到第 2 次就记下',
        complexity='时间 `O(n^2)`（指纹嵌套，哈希要遍历整棵子树），空间 `O(n^2)`',
        problem=['给你二叉树的根 `root`，返回所有==重复的子树==',
                 '同一种重复子树只需返回其中任意一棵的根；两棵子树结构相同且节点值相同才算重复',
                 '示例：`[1,2,3,4,null,2,4,null,null,4]`',
                 '重复的是 `[2,4]` 和 `[4]`'],
        quote='将每颗子树做成某种数据结构，然后将其放入哈希表。若某棵树在哈希表里面出现大于等于两次，那么就将这棵树的根节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['子树要保存三样信息：根的值、左子树、右子树',
              '左右子树靠递归得到，并且==顺序固定==（值, 左, 右），才能区分左右',
              '空子树返回 `None`，嵌套起来就是一个可哈希的元组',
              '计数恰好等于 2 时才记录，避免同一种子树被重复收集'],
        summary=['时间/空间最坏 `O(n^2)`：元组嵌套，哈希要比较整棵子树',
                 '易错：==必须区分左右==，只放一堆值会把镜像树误判成相同',
                 '易错：用 `== 2` 而不是 `>= 2`，否则第三次出现会再收集一次',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串；`dfs` 不返回时（空节点）值为 `None`'],
    ),
)
