TREE = [5, 10, 4, 3, 7, 9]
LEVEL_START = [0, 1, 3, 6]


def _level(S):
    l = S.get('l')
    if l is None:
        return 0
    return LEVEL_START.index(l) if l in LEVEL_START else 0


def _qpos(S, n):
    for k, x in enumerate(S.get('q') or []):
        if x._uid == n._uid:
            return k
    return None


def _checked(S):
    """已经通过检查的节点个数（按 q 的下标）"""
    line = S.get('_line')
    if line == 29:
        return len(S['q'])
    if 'index' not in S or line in (9, 10, 25, 26, 27):
        return S.get('l', 0)
    idx = S['index']
    return idx + 1 if line in (14, 17, 18, 21, 22) else idx


def _tree_color(S, n):
    k = _qpos(S, n)
    if k is None:
        return None
    if k < _checked(S):
        return 'green'
    if 'r' in S and S['r'] <= k:
        return 'cyan'
    return None


def _rule(S):
    if 'multi' not in S or 'l' not in S:
        return ''
    lv = _level(S)
    want = '奇数' if S['rest'] == 1 else '偶数'
    mono = '递增' if S['multi'] == 1 else '递减'
    return f"第 {lv} 层（{'偶' if lv % 2 == 0 else '奇'}数下标）：值必须是=={want}==，从左到右严格=={mono}=="


def _cap_par(S, B, ret):
    v = S.q[S.index].val
    want = '奇数' if S.rest == 1 else '偶数'
    if v % 2 != S.rest:
        return f'`{v} % 2 = {v % 2} ≠ rest = {S.rest}` → 不是{want}，返回 False'
    return f'`{v} % 2 = {v % 2}`，等于 `rest = {S.rest}` → 是{want}'


def _cap_mono(S, B, ret):
    i, l = S.index, S.l
    v = S.q[i].val
    if i == l:
        return f'`{v}` 是本层第一个，不用比较单调性'
    p = S.q[i - 1].val
    prod = (v - p) * S.multi
    mono = '递增' if S.multi == 1 else '递减'
    if prod <= 0:
        return f'`({v} − {p}) × {S.multi} = {prod} ≤ 0` → 不是严格{mono}，返回 False'
    return f'`({v} − {p}) × {S.multi} = {prod} > 0` → 严格{mono}'


def _cap_kid(side):
    def f(S, B, ret):
        nd = S.q[S.index]
        kid = getattr(nd, side)
        word = '左' if side == 'left' else '右'
        if kid:
            return f'`{nd.val}` 有{word}孩子 `{kid.val}`'
        return f'`{nd.val}` 没有{word}孩子'
    return f


def _cap_app(side):
    def f(S, B, ret):
        kid = S.q[-1]
        word = '左' if side == 'left' else '右'
        return f'{word}孩子 `{kid.val}` 追加到 `q` 末尾，属于下一层'
    return f


CONFIG = dict(
    num=1609, title='奇偶树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='层序遍历 · 数组 + 下标区间',
    tags=['字节30天'],
    code='''
class Solution(object):
    def isEvenOddTree(self, root):
        q = [root]
        rest = 1
        multi = 1

        l = 0
        r = 1
        while l < r:
            new_r = r
            for index in range(l, r):
                if q[index].val % 2 != rest:
                    return False
                if index > l and (q[index].val - q[index - 1].val) * multi <= 0:
                    return False

                if q[index].left:
                    q.append(q[index].left)
                    new_r += 1

                if q[index].right:
                    q.append(q[index].right)
                    new_r += 1

            l, r = r, new_r
            rest = 1 - rest
            multi = -multi

        return True
''',
    call=f'Solution().isEvenOddTree(Tr({TREE}))',
    expect=True,
    skip=['for index in range', 'new_r += 1'],
    max_steps=70,
    views=[
        dict(type='text', fn=_rule, h=56),
        dict(type='tree', label='二叉树（绿 = 已检查，青 = 已入队的下一层）', pointers={'q[index]': 'blue'},
             pointer_labels={'q[index]': 'q[index]'}, color=_tree_color, path=False, h=300),
        dict(type='array', var=lambda S: [x.val for x in S['q']] if 'q' in S else None,
             label='q（框 = 当前层 [l, r)，青 = 下一层）', cell=96,
             window=('l', 'r - 1'), pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if i < _checked(S) else ('cyan' if 'r' in S and i >= S['r'] else None), h=200),
    ],
    watch=[('l', 'l'), ('r', 'r'), ('new_r', 'new_r', 'cyan'), ('rest', 'rest', 'yellow'), ('multi', 'multi', 'yellow')],
    captions={
        'q = [root]': '用数组 `q` 做层序遍历：节点只追加不出队，`q[l:r]` 就是当前层',
        4: '`rest`：当前层要求的奇偶性；第 0 层是偶数层，值要是==奇数==（`% 2 == 1`）',
        'multi = 1': '`multi = 1` 要求递增、`-1` 要求递减：统一判断 `(后 − 前) × multi > 0`',
        'l = 0': '`[l, r)` 是当前层在 `q` 中的下标范围',
        'r = 1': '第 0 层只有根：`[0, 1)`',
        'while l < r': lambda S, B, r: (f'`[l, r) = [{S.l}, {S.r})` 非空 → 处理第 {_level(S)} 层' if S.l < S.r
                                        else f'`l = r = {S.r}`：没有下一层了'),
        'new_r = r': '`new_r` 记录下一层的结束位置：孩子会追加到 `q` 末尾',
        'if q[index].val % 2 != rest': _cap_par,
        'if index > l and': _cap_mono,
        'if q[index].left': _cap_kid('left'),
        'q.append(q[index].left)': _cap_app('left'),
        'if q[index].right': _cap_kid('right'),
        'q.append(q[index].right)': _cap_app('right'),
        'l, r = r, new_r': '本层检查完，下一层是 `[l, r) = [{l}, {r})`',
        26: lambda S, B, r: f'奇偶层交替：`rest = {S.rest}`（下一层的值要是{"奇" if S.rest else "偶"}数）',
        'multi = -multi': lambda S, B, r: f'单调方向翻转：`multi = {S.multi}`（下一层要严格{"递增" if S.multi == 1 else "递减"}）',
        'return True': '每一层都满足条件 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='层序遍历，逐层检查奇偶性和严格单调性；rest、multi 随层翻转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['根在下标 0 层，孩子在下一层。满足下面条件的树叫==奇偶树==：',
                 '偶数下标层：所有值都是==奇数==，从左到右==严格递增==',
                 '奇数下标层：所有值都是==偶数==，从左到右==严格递减==',
                 f'本视频：`{TREE}` → `true`'],
        quote='既然是按层来进行判断，那么很自然想到使用==层序遍历==来解决。直接对树进行层序遍历，然后对于每一层的节点判断奇偶性以及单调性即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['用数组 `q` 存所有节点，`[l, r)` 是当前层，孩子追加到末尾就是下一层',
              '`rest`：当前层要求的奇偶（偶数层为 1 → 奇数值，奇数层为 0 → 偶数值）',
              '`multi = ±1`：`(当前 − 前一个) × multi <= 0` 就违反了严格单调'],
        result='三层都满足条件：返回 `True`',
        summary=['时间 `O(n)`：每个节点检查一次；空间 `O(n)`：`q` 保存全部节点',
                 '用下标区间 `[l, r)` 代替 `deque`：不出队，区间往后滑',
                 '易错：要求==严格==单调，相等也不行，所以判断 `<= 0`',
                 '`rest = 1 - rest`、`multi = -multi`：一行完成层间切换',
                 '原文为 Python 2 风格，只删去了 TreeNode 定义注释和类型说明文档字符串'],
    ),
)
