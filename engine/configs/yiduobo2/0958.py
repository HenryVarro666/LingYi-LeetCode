import views as V


def _level_ids(S):
    q, l, r = S.get('q'), S.get('l'), S.get('r')
    if q is None or not isinstance(l, int):
        return set()
    return {n._uid for n in q[l:r] if n is not None}


def _tree_color(S, n):
    if n._uid in _level_ids(S):
        return 'cyan'
    q = S.get('q') or []
    l = S.get('l', 0)
    if any(x._uid == n._uid for x in q[:l]):
        return 'purple'
    return None


def tree_view(**spec):
    """迭代写法：不画递归路径黄圈"""
    def draw(cv, S, B, box, T):
        V.v_tree(cv, dict(spec, path=False), {'_S': S, '_B': B, '_frames': []}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 300))


def _which(S):
    root = S.get('root')
    if root is None:
        return ''
    ex2 = root.right is not None and root.right.right is not None
    return '示例 2：`[1,2,3,4,5,null,7]`' if ex2 else '示例 1：`[1,2,3,4,5,6]`'


def _text(S):
    if 'leaf_flag' not in S:
        return '第 `k` 层是满的 ⟺ 有 `2^k` 个节点'
    full = S['full_len'] if S.get('_line') == LEAF_LINE else S['full_len'] // 2
    s = f"本层 `r - l = {S['r'] - S['l']}` 个节点，满层应有 `{full}` 个"
    flags = []
    if S['leaf_flag']:
        flags.append('==leaf_flag==：最下层，不能有孩子')
    if S.get('stop_flag'):
        flags.append('==stop_flag==：右边不能再有孩子')
    return s + ('；' + '，'.join(flags) if flags else '')


def _leaf_cap(S, B, ret):
    cnt, full = B.r - B.l, B.full_len
    if S.leaf_flag:
        return f'本层 `{cnt}` 个 ≠ 满层的 `{full}` 个 → `leaf_flag = True`：==这是最下层==，它的节点都不能有孩子'
    return f'本层 `{cnt}` 个 = 满层的 `{full}` 个 → `leaf_flag = False`；下一层满的话应有 `{full * 2}` 个'


def _child_cap(side, word):
    def f(S, B, ret):
        nd = S.now
        ch = getattr(nd, side)
        if ch is not None:
            return f'`{nd.val}` 有{word}孩子 `{ch.val}`'
        return f'`{nd.val}` 没有{word}孩子'
    return f


def _flag_cap(S, B, ret):
    if S.stop_flag:
        return '`stop_flag` 为真：左边已经缺过孩子，这里却有孩子 → ==不是完全二叉树=='
    if S.leaf_flag:
        return '`leaf_flag` 为真：最下层的节点却有孩子 → ==不是完全二叉树=='
    return '两个标记都为假 → 可以有这个孩子，入队'


CODE = '''
class Solution(object):
    def isCompleteTree(self, root):
        q = [root]
        l = 0
        r = 1
        full_len = 1
        while l < r:
            leaf_flag = (r - l) != full_len
            full_len += full_len
            stop_flag = False
            for now in q[l : r]:
                if now.left:
                    if stop_flag or leaf_flag:
                        return False
                    q.append(now.left)
                else:
                    stop_flag = True

                if now.right:
                    if stop_flag or leaf_flag:
                        return False
                    q.append(now.right)
                else:
                    stop_flag = True

            l, r = r, len(q)

        return True
'''
_LINES = CODE.strip('\n').split('\n')
LEAF_LINE = next(i + 1 for i, l in enumerate(_LINES) if 'leaf_flag = (' in l)

CONFIG = dict(
    num=958, title='二叉树的完全性检验', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='层序遍历 + leaf_flag / stop_flag',
    tags=['热题173'],
    code=CODE,
    call='''a = Solution().isCompleteTree(Tr([1, 2, 3, 4, 5, 6]))
b = Solution().isCompleteTree(Tr([1, 2, 3, 4, 5, None, 7]))
(a, b)''',
    expect=(True, False),
    views=[
        dict(type='text', fn=_which, size=26, h=56),
        tree_view(var='root', label='二叉树（青 = 当前层，紫 = 已遍历的层）', h=300,
                  pointers={'now': 'blue'}, color=_tree_color),
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else None,
             label='q（层序队列，框 = 当前层 [l, r)）', cell=80, window=('l', 'r - 1'), h=165, index=True),
        dict(type='text', fn=_text, size=25, h=90, lines=2),
    ],
    watch=[('l', 'l'), ('r', 'r'), ('full_len', 'full_len'), ('leaf_flag', 'leaf_flag', 'orange'),
           ('stop_flag', 'stop_flag', 'red')],
    skip=['full_len += full_len', 'for now in q[l : r]', 'q.append(now.left)',
          'q.append(now.right)', 'l = 0', 'r = 1'],
    captions={
        'q = [root]': '层序遍历：数组 `q` 当队列，`[l, r)` 圈出当前层',
        'full_len = 1': '`full_len`：这一层如果是满的应有几个节点（第 0 层 1 个，之后每层翻倍）',
        'while l < r': lambda S, B, ret: ('队列里还有下一层' if B.l < B.r else '整棵树遍历完了'),
        'leaf_flag = (': _leaf_cap,
        'stop_flag = False': '每层开头 `stop_flag = False`：本层还没有节点缺孩子',
        'if now.left': _child_cap('left', '左'),
        'if now.right': _child_cap('right', '右'),
        'if stop_flag or leaf_flag': _flag_cap,
        'stop_flag = True': lambda S, B, ret: ('仍然缺孩子，`stop_flag` 保持 True' if B.stop_flag else
                                               '缺了孩子 → `stop_flag = True`（最下层本来也不能有孩子）' if S.leaf_flag else
                                               '缺了孩子 → `stop_flag = True`：==同一层右侧的节点都不能再有孩子=='),
        'return False': '返回 ==False==',
        'l, r = r, len(q)': '进入下一层：`q[{l}:{r}]`',
        'return True': '没有发现矛盾 → 是完全二叉树，返回 ==True==',
    },
    max_steps=60,
    cards=dict(
        one_liner='层序遍历：不满的层是最下层；某个节点缺了孩子，右边的都不能再有孩子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断一棵二叉树是不是==完全二叉树==',
                 '完全二叉树：除最后一层外每层都是满的，最后一层的节点==全部靠左==',
                 '示例：`[1,2,3,4,5,6]` → `true`；`[1,2,3,4,5,null,7]` → `false`'],
        quote='可以设置两个标记leaf_flag以及stop_flag，==分别表示当前层是否为最后一层，以及当前层后续的节点是否能继续有孩子节点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['前面的层都是满的 → 第 `k` 层应有 `2^k` 个节点；不等就是最下层',
              '最下层的节点不能再有孩子（`leaf_flag`）',
              '某个节点缺了左或右孩子 → 同层右侧都不能再有孩子（`stop_flag`）'],
        summary=['时间 `O(n)`，空间 `O(n)`（队列）',
                 '`leaf_flag` 用 `r - l != full_len` 判断，`full_len` 每层翻倍',
                 '`stop_flag` 每层开头重置为 False；缺左孩子时右孩子也不能有',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
