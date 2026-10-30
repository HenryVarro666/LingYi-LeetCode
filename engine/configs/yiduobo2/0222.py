VALS = [1, 2, 3, 4, 5, 6]
H = 3  # 树高


def _heap_index(root):
    """节点 uid -> 堆编号（根为 1）"""
    out, q = {}, [(root, 1)]
    while q:
        n, k = q.pop()
        if n is None:
            continue
        out[n._uid] = k
        q += [(n.left, 2 * k), (n.right, 2 * k + 1)]
    return out


def draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '完全二叉树（虚线 = 最后一层可能的位置，下方数字 = 去掉上层后的编号）', 24, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    idx = _heap_index(root)
    vals = {}
    st = [root]
    while st:
        n = st.pop()
        if n is None:
            continue
        vals[idx[n._uid]] = n.val
        st += [n.left, n.right]
    W = x1 - x0 - 80
    dy, rad = 100, 28

    def P(k):
        d = k.bit_length() - 1
        p = k - (1 << d)
        return x0 + 40 + (p + 0.5) * W / (1 << d), y0 + 105 + d * dy

    l, r, mid = S.get('l'), S.get('r'), S.get('mid')
    base = 1 << (H - 1)
    for k in range(2, 1 << H):
        (X, Y), (X2, Y2) = P(k // 2), P(k)
        if k in vals:
            cv.line([(X, Y), (X2, Y2)], T['border'], 4)
        else:
            cv.dashed((X, Y + rad), (X2, Y2 - rad), T['dim'], 2, 8, 8)
    now = S.get('now')
    now_k = idx.get(now._uid) if isinstance(now, TreeNode) else None
    tgt = base + mid if isinstance(mid, int) else None
    for k in range(1, 1 << H):
        X, Y = P(k)
        last = k >= base
        j = k - base
        known_yes = last and isinstance(l, int) and j < l
        known_no = last and isinstance(r, int) and j > r and 'mid' in S
        if k in vals:
            fill = T['green'] if known_yes else T['panel2']
            outline = T['blue'] if k == now_k else (T['yellow'] if k == tgt else T['border'])
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline,
                         width=5 if (k == now_k or k == tgt) else 2)
            cv.text((X, Y), str(vals[k]), 26, T['bg'] if known_yes else T['text'], anchor='mm', bold=True)
        else:
            c = T['yellow'] if k == tgt else (T['red'] if known_no else T['dim'])
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), outline=c, width=3 if k == tgt else 2)
            cv.text((X, Y), '空', 20, c, anchor='mm')
        if k == now_k:
            cv.text((X, Y - rad - 4), 'now', 21, T['blue'], anchor='mb', bold=True)
        if last:
            cv.text((X, Y + rad + 8), str(j), 22, T['yellow'] if k == tgt else T['muted'], anchor='mt', mono=True, bold=True)
    if 'now' in S and now is None and tgt is not None:
        X, Y = P(tgt)
        cv.text((X, Y - rad - 4), 'now = None', 21, T['blue'], anchor='mb', bold=True)


def _bits(S):
    if not isinstance(S.get('mid'), int) or 'pow_list' not in S:
        return ''
    mid, pl = S['mid'], S['pow_list']
    parts, t = [], mid
    for i in range(len(pl) - 2, -1, -1):
        if t >= pl[i]:
            parts.append(f'{t}≥{pl[i]} 右')
            t -= pl[i]
        else:
            parts.append(f'{t}<{pl[i]} 左')
    return f'找编号 `mid = {mid}`：' + ' → '.join(f'`{p}`' for p in parts)


def _cap_if(S, B, ret):
    t, p = B.tmp, S.pow_list[S.index]
    if t >= p:
        return f'`tmp = {t} ≥ pow_list[{S.index}] = {p}`：在==右子树==，往右走，编号减去左子树的 {p} 个'
    return f'`tmp = {t} < pow_list[{S.index}] = {p}`：在==左子树==，往左走'


CONFIG = dict(
    num=222, title='完全二叉树的节点个数', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='算树高 + 二分最后一层的节点数',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def countNodes(self, root):
        if not root:
            return 0

        pow_list = [1]
        now = root
        while now.left:
            now = now.left
            pow_list.append(pow_list[-1] + pow_list[-1])

        level_cnt = pow_list[-1]

        res = 0
        l = 0
        r = level_cnt - 1
        while l <= r:
            mid = (l + r) // 2
            tmp = mid
            now = root
            for index in range(len(pow_list) - 2, -1, -1):
                if tmp >= pow_list[index]:
                    now = now.right
                    tmp -= pow_list[index]
                else:
                    now = now.left

            if now:
                res = mid
                l = mid + 1
            else:
                r = mid - 1

        return res + level_cnt
''',
    call='Solution().countNodes(Tr([1, 2, 3, 4, 5, 6]))',
    expect=6,
    views=[
        dict(type='custom', draw=draw_tree, h=400),
        dict(type='text', fn=_bits, size=26),
        dict(type='array', var='pow_list', label='pow_list（2 的幂；最后一个 = 最后一层最多的节点数）', cell=72, h=130),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), 'tmp', ('res', 'res', 'green')],
    skip=['for index in range'],
    captions={
        'if not root': '`root` 不为空 → 继续',
        'pow_list = [1]': '`pow_list` 记录每一层的节点数：第一层 1 个',
        'now = root': lambda S, B, ret: ('`now` 从根开始，一直往左走，统计树高' if 'mid' not in S
                                         else f'从根出发，按编号 `{S.mid}` 一路往下找'),
        'while now.left': lambda S, B, ret: (f'`{B.now.val}` 有左孩子 → 下面还有一层' if B.now.left
                                             else f'`{B.now.val}` 没有左孩子 → 树高 `h = {len(S.pow_list)}`'),
        'now = now.left': lambda S, B, ret: (f'往左走到 `{S.now.val}`' if 'mid' not in S else
                                             (f'往左走 → `{S.now.val}`' if S.now else '往左走 → ==空==')),
        'pow_list.append': '这一层的节点数翻倍：`pow_list` 末尾加入 `{pow_list[-1]}`',
        'level_cnt = pow_list[-1]': '最后一层最多 `level_cnt = {level_cnt}` 个；上面各层共 `{level_cnt} - 1` 个',
        'res = 0': '`res`：最后一层能找到的最大编号',
        'l = 0': '二分最后一层的编号：从 `0` 到 `level_cnt - 1`',
        'r = level_cnt - 1': '`r = {r}`',
        'while l <= r': lambda S, B, ret: (f'`l = {S.l} ≤ r = {S.r}` → 继续二分' if S.l <= S.r
                                           else f'`l = {S.l} > r = {S.r}` → 二分结束，最大存在编号是 `{S.res}`'),
        'mid = (l + r)': lambda S, B, ret: (f'`mid = ({S.l} + {S.r}) // 2 = {S.mid}`'
                                            + ('（原文 `/` 是 Python 2 整除，已改为 `//`）' if B.get('mid') is None else '')),
        'tmp = mid': '`tmp = {tmp}`：要在当前子树里找的编号',
        'if tmp >= pow_list': _cap_if,
        'now = now.right': lambda S, B, ret: f'往右走 → `{S.now.val}`' if S.now else '往右走 → ==空==',
        'tmp -= pow_list': '`tmp` 减去 `{pow_list[index]}` → `{tmp}`（略过左孩子的编号）',
        'if now:': lambda S, B, ret: (f'编号 `{S.mid}` 的节点==存在==（{S.now.val}）→ 答案在 `[mid, r]`' if S.now
                                      else f'编号 `{S.mid}` 的节点==不存在== → 答案在 `[l, mid - 1]`'),
        'res = mid': '`res = {res}`',
        'l = mid + 1': '`l = {l}`',
        'r = mid - 1': '`r = {r}`',
        'return res + level_cnt': '最后一层编号 `0..{res}` 共 `{res + 1}` 个，上面 `{level_cnt - 1}` 个 → 共 =={ret}== 个',
    },
    cards=dict(
        one_liner='上面各层是满的：先算树高，再二分最后一层有几个节点',
        complexity='时间 `O(log²n)`，空间 `O(log n)`（pow_list）',
        problem=['给你一棵==完全二叉树==的根节点 `root`，求出该树的节点个数',
                 '完全二叉树：除最后一层外每层都是满的，最后一层的节点==集中在左边==',
                 '示例：`[1,2,3,4,5,6]` → `6`'],
        quote='除了最底下那一层的所有节点个数为 2^h - 1……那么只需要想办法得到最后一层有多少个节点就行了。一个经典的做法就是==二分答案==。',
        quote_src='—— yiduobo 题解',
        idea=['一直往左走得到树高 `h`，上面 `h-1` 层共 `2^(h-1) - 1` 个节点',
              '最后一层编号 `0..2^(h-1)-1`，存在的节点是一段前缀 → 可以二分',
              '找编号 `mid`：逐层与 `2^k` 比较，`≥` 就往右并减去 `2^k`，否则往左'],
        result='运行结束：返回 `6` ✓',
        summary=['二分 `O(log n)` 次，每次从根走到底 `O(log n)` → `O(log²n)`',
                 '原文写的是 `O(loglogn·logn)`；但二分范围有 `2^(h-1)` 个数，要二分约 `h` 次',
                 '编号判断本质是看 `mid` 的二进制位：1 往右，0 往左',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去 docstring',
                 '朴素做法：直接遍历计数 `O(n)`'],
    ),
)
