EXPECT = [[], [[0, 0, 0, None, None, 0, 0], [0, 0, 0, 0, 0]],
          [[0, 0, 0, None, None, 0, 0, None, None, 0, 0], [0, 0, 0, None, None, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, None, None, None, None, 0, 0], [0, 0, 0, 0, 0, None, None, 0, 0]]]


def _ino(n, d, out):
    """中序展开；子树被多处共享时按路径重复展开，所以返回 (深度, 左, 右) 的下标结构"""
    if n is None:
        return None
    li = _ino(n.left, d + 1, out)
    out.append([d, None, None, n.left is None and n.right is None])
    me = len(out) - 1
    ri = _ino(n.right, d + 1, out)
    out[me][1], out[me][2] = li, ri
    return me


def _mini(cv, T, root, x, y, sp, dy, color):
    """画一棵小树，左上角 (x, y)，返回占用宽度"""
    out = []
    _ino(root, 0, out)
    pos = [(x + i * sp + sp / 2, y + o[0] * dy + 9) for i, o in enumerate(out)]
    for i, o in enumerate(out):
        for c in (o[1], o[2]):
            if c is not None:
                cv.line([pos[i], pos[c]], T['border'], 2)
    for i, o in enumerate(out):
        px, py = pos[i]
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=T['green'] if o[3] else color, r=8)
    return len(out) * sp


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('self.f')
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), 'f[i]：i 个叶子的所有真二叉树（绿 = 叶子，蓝 = 有两个儿子的节点）', 22, T['muted'], bold=True)
    if not f:
        return
    ks = [1, 2, 3, 4]
    use = (n + 1) // 2 if n is not None and n % 2 else None

    def gw(k, sp):
        return max(150, sum((2 * k - 1) * sp for _ in f[k]) + 20 * (len(f[k]) - 1))

    sp = 26
    while sp > 8 and sum(gw(k, sp) + 40 for k in ks) > (x1 - x0) - 40:
        sp -= 1
    x = x0 + 30
    y = y0 + 110
    for k in ks:
        w_group = gw(k, sp)
        hit = use == k
        if hit:
            cv.rect((x - 12, y - 52, x + w_group + 12, y + 190), outline=T['yellow'], width=4, r=12)
        cv.text((x, y - 44), f'f[{k}]（{len(f[k])} 棵）', 22, T['yellow'] if hit else T['text'], bold=True)
        xx = x
        for t in f[k]:
            xx += _mini(cv, T, t, xx, y, sp, 40, T['blue']) + 20
        x += w_group + 40
    if n is not None:
        if use is None:
            cv.text((x0 + 18, y0 + 400), f'n = {n} 是偶数：没有对应的 f，返回 []', 30, T['red'], bold=True)
        else:
            cv.text((x0 + 18, y0 + 400), f'n = {n} → 叶子数 (n+1)/2 = {use} → 返回 f[{use}]，共 {len(f[use])} 棵', 30, T['yellow'], bold=True)


def _cap(S, B, ret):
    n = S.n
    if n % 2 == 0:
        return f'`n = {n}` 是偶数：每次加节点至少加 2 个，节点数必为奇数 → ==返回 `[]`=='
    k = (n + 1) // 2
    return f'`n = {n}` 是奇数：叶子数 `({n}+1)//2 = {k}` → 直接取预处理好的 `f[{k}]`，共 `{len(S["self.f"][k])}` 棵'


CONFIG = dict(
    num=894, title='所有可能的真二叉树', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='按叶子数递推预处理 f[i]',
    tags=[],
    code='''
MX = 11
f = [[] for _ in range(MX)]
f[1] = [TreeNode()]
for i in range(2, MX):  # 计算 f[i]
    f[i] = [TreeNode(0, left, right)
            for j in range(1, i)  # 枚举左子树叶子数
            for left in f[j]  #  枚举左子树
            for right in f[i - j]]  # 枚举右子树

class Solution:
    def allPossibleFBT(self, n: int) -> List[Optional[TreeNode]]:
        return f[(n + 1) // 2] if n % 2 else []
''',
    call='''s = Solution()
s.f = f[:5]
[s.allPossibleFBT(n) for n in (4, 5, 7)]''',
    result_fn=lambda r: [[tree_list(t) for t in x] for x in r],
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=['n', ('叶子数', lambda S: (S['n'] + 1) // 2 if S['n'] % 2 else '无')],
    captions={'return f[': _cap},
    cards=dict(
        one_liner='节点数换成叶子数，左右子树的叶子数加起来就行',
        complexity='预处理 `O(4^N / N^1.5)`（卡特兰数），查询 `O(1)`',
        problem=['返回所有含 `n` 个节点的==真二叉树==：每个节点恰有 `0` 或 `2` 个子节点，节点值都是 `0`',
                 '示例：`n = 3` → `[[0,0,0]]`；`n = 7` → 5 棵',
                 '本视频一次问三个：`n = 4`、`5`、`7`'],
        quote='由于每增加 2 个节点，真二叉树就会多 1 个叶子，所以一棵有 n 个节点的真二叉树恰好有 (n+1)/2 个叶子。',
        quote_src='—— 灵茶山艾府题解「性质」',
        idea=['每次最少添加 `2` 个节点 → 整棵树和每棵子树的节点数都是==奇数==',
              '定义 `f[i]` 为有 `i` 个==叶子==的所有真二叉树',
              '枚举左子树叶子数 `j`，右子树 `i-j` 个，左右各选一棵接到新根下'],
        before=[dict(heading='预处理：f[1] → f[2] → f[3]', lines=[
            '`f[1]` 只有一个节点：`[TreeNode()]`',
            '`f[2]`：`j = 1`，左 `f[1]`、右 `f[1]` → ==1 棵==（根 + 两个叶子）',
            '`f[3]`：`j = 1` 左 1 右 2，`j = 2` 左 2 右 1 → ==2 棵==',
            '`f[4]`：`j = 1,2,3` → `1×2 + 1×1 + 2×1`，共 ==5 棵==（卡特兰数）',
            '这段预处理在 `Solution` 之外只做一次，下面只看查询']),
        ],
        summary=['`n` 为偶数返回 `[]`；`n` 为奇数返回 `f[(n+1)//2]`',
                 '易错：`f` 按==叶子数==而不是节点数定义，下标是 `(n+1)//2`',
                 '各树共享子树节点：`f[i]` 里的树会复用 `f[j]` 里的节点，不用复制',
                 '相似题：96 不同的二叉搜索树、95 不同的二叉搜索树 II'],
    ),
)
