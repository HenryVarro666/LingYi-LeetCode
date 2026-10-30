def _heap(S, root, sign):
    """把左偏树里的有效值（val + 沿路 delta）收集成排好序的列表；sign=-1 为大顶堆（负斜率），1 为小顶堆"""
    try:
        val, lc, rc, dl = S['val'], S['left'], S['right'], S['delta']
    except KeyError:
        return []
    out = []

    def go(x, acc):
        if not x:
            return
        acc += dl[x]
        out.append(val[x] + acc)
        go(lc[x], acc)
        go(rc[x], acc)
    go(root, 0)
    return sorted(out, reverse=(sign < 0))


def _show(names):
    def fn(S):
        parts = []
        for label, nn, pn in names:
            if label != '合并后' and S.get('_line', 0) > 60:
                parts.append(f'{label}　（已并入下方的堆）')
            elif nn in S and pn in S:
                parts.append(f'{label}　负斜率堆 `{_heap(S, S[nn], -1)}`　正斜率堆 `{_heap(S, S[pn], 1)}`')
        return '\n'.join(parts) if parts else '（还没有堆）'
    return fn


def _eff(S, node):
    return S['val'][node] + S['delta'][node]


def _res(S):
    """res 是 global 变量，不在栈帧里；本例只有根节点换位一次，用 ori_neg/ori_pos 还原，dfs 结束后取最终答案"""
    if 'ori_neg' in S and 'ori_pos' in S and S.get('_line') not in range(73, 86):
        return S['val'][S['ori_neg']] - S['val'][S['ori_pos']]
    if 'now' not in S:
        return 3
    return 0


def _merged(S, a, b, sign):
    return sorted(_heap(S, a, sign) + _heap(S, b, sign), reverse=(sign < 0))


CONFIG = dict(
    num=4082, title='使得二叉树稳定的最小操作数', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='斜率技巧 · 左偏树 · 对顶堆',
    code='''
class Solution(object):
    def stabilizeBinaryTree(self, root):
        
        left = [0]
        right = [0]
        dist = [0]
        val = [0]
        delta = [0]
        global res
        res = 0

        def new_ist(v):
            left.append(0)
            right.append(0)
            dist.append(1)
            val.append(v)
            delta.append(0)
            return len(left) - 1

        def merge(x, y, sign):
            if not x or not y:
                return x | y
            
            if delta[x]:
                val[x] += delta[x]
                delta[left[x]] += delta[x]
                delta[right[x]] += delta[x]
                delta[x] = 0
            
            if delta[y]:
                val[y] += delta[y]
                delta[left[y]] += delta[y]
                delta[right[y]] += delta[y]
                delta[y] = 0
            
            if val[x] * sign > val[y] * sign:
                x, y = y, x
            
            right[x] = merge(right[x], y, sign)
            if dist[left[x]] < dist[right[x]]:
                left[x], right[x] = right[x], left[x]
            
            dist[x] = dist[right[x]] + 1
            return x

        def dfs(now):
            if now.left:
                left_neg, left_pos = dfs(now.left)
                delta[left_neg] -= 1
                delta[left_pos] += 1
            else:
                left_neg, left_pos = 0, 0
            
            if now.right:
                right_neg, right_pos = dfs(now.right)
                delta[right_neg] -= 1
                delta[right_pos] += 1
            else:
                right_neg, right_pos = 0, 0
            
            neg = merge(left_neg, right_neg, -1)
            pos = merge(left_pos, right_pos, 1)
            

            root_neg = new_ist(now.val)
            root_pos = new_ist(now.val)

            neg = merge(neg, root_neg, -1)
            pos = merge(pos, root_pos, 1)

            global res
            while neg and pos and val[neg] + delta[neg] > val[pos] + delta[pos]:
                ori_neg = neg
                neg = merge(left[neg], right[neg], -1)
                left[ori_neg] = 0
                right[ori_neg] = 0

                ori_pos = pos
                pos = merge(left[pos], right[pos], 1)
                left[ori_pos] = 0
                right[ori_pos] = 0

            
                neg = merge(neg, ori_pos, -1)
                pos = merge(pos, ori_neg, 1)
                res += val[ori_neg] - val[ori_pos]

            return neg, pos

        dfs(root)
        return res
''',
    call='''s = Solution()
s.tree = Tr([5,8,3])
s.stabilizeBinaryTree(s.tree)''',
    expect=3,
    skip=['left = [0]', 'right = [0]', 'dist = [0]', 'val = [0]', 'delta = [0]', 'global res', 'def ',
          # new_ist 与 merge 内部：只看 dfs 里每次 merge 的结果
          'left.append', 'right.append', 'dist.append', 'val.append', 'delta.append', 'return len(left)',
          'if not x or not y', 'return x | y', 'if delta[x]', 'if delta[y]', 'val[x] += delta[x]', 'val[y] += delta[y]',
          'delta[left[x]]', 'delta[right[x]]', 'delta[left[y]]', 'delta[right[y]]', 'delta[x] = 0', 'delta[y] = 0',
          'if val[x] * sign', 'x, y = y, x', 'right[x] = merge', 'if dist[left[x]]', 'left[x], right[x] = right[x]',
          'dist[x] = dist[right[x]]', 'return x', 'left[ori_neg] = 0', 'right[ori_neg] = 0',
          'left[ori_pos] = 0', 'right[ori_pos] = 0', 'else:', 'left_neg, left_pos = 0, 0', 'right_neg, right_pos = 0, 0',
          'root_neg = new_ist', 'root_pos = new_ist'],
    views=[
        dict(type='tree', var='s.tree', label='二叉树（黄圈 = 当前递归到的节点）', h=260),
        dict(type='text', h=70, size=28, fn=_show([('左子树', 'left_neg', 'left_pos')])),
        dict(type='text', h=70, size=28, fn=_show([('右子树', 'right_neg', 'right_pos')])),
        dict(type='text', h=70, size=28, fn=_show([('合并后', 'neg', 'pos')])),
        dict(type='calls', h=130),
    ],
    watch=[('res', _res, 'green')],
    captions={
        'res = 0': '`res` 累计代价：每次对顶堆换位，答案加上两个堆顶之差',
        'if now.left': lambda S, B, r: ('有左孩子 → 先递归处理左子树' if S.now.left else '没有左孩子 → 左边是空堆'),
        'if now.right': lambda S, B, r: ('有右孩子 → 再递归处理右子树' if S.now.right else '没有右孩子 → 右边是空堆'),
        'left_neg, left_pos = dfs(now.left)': '左子树返回两个堆：负斜率堆（大顶）和正斜率堆（小顶）',
        'delta[left_neg] -= 1': '对父节点来说有 1 的容错：负斜率堆整体 ==减 1==（懒标记，分割点向左外扩）',
        'delta[left_pos] += 1': '正斜率堆整体 ==加 1==（分割点向右外扩）→ 左子树函数的最低点变成一段区间',
        'right_neg, right_pos = dfs(now.right)': '右子树同样返回两个堆',
        'delta[right_neg] -= 1': '右子树负斜率堆整体减 1（懒标记）',
        'delta[right_pos] += 1': '右子树正斜率堆整体加 1，同样外扩',
        'neg = merge(left_neg, right_neg, -1)': lambda S, B, r: f'左右两个负斜率堆合并（大顶堆）→ `{_merged(S, S.left_neg, S.right_neg, -1)}`',
        'pos = merge(left_pos, right_pos, 1)': lambda S, B, r: f'左右两个正斜率堆合并（小顶堆）→ `{_merged(S, S.left_pos, S.right_pos, 1)}`',
        'neg = merge(neg, root_neg, -1)': lambda S, B, r: f'把自身 `|x - {S.now.val}|` 的分割点 `{S.now.val}` 并入负斜率堆 → `{sorted(_heap(S, S.neg, -1) + [S.now.val], reverse=True)}`',
        'pos = merge(pos, root_pos, 1)': lambda S, B, r: f'同样并入正斜率堆 → `{sorted(_heap(S, S.pos, 1) + [S.now.val])}`',
        'while neg and pos': lambda S, B, r: (
            (lambda n, p: f'负堆顶 `{n}` > 正堆顶 `{p}`：==逆序==，斜率抵消、最小值被抬高 → 要纠正' if n > p
             else f'负堆顶 `{n}` ≤ 正堆顶 `{p}`：没有逆序，合并完成')
            (_eff(S, S.neg), _eff(S, S.pos)) if S.neg and S.pos
            else '有一个堆为空：没有逆序，合并完成'),
        'ori_neg = neg': lambda S, B, r: f'取出负堆顶 `ori_neg`（值 `{_eff(S, S.ori_neg)}`）',
        'neg = merge(left[neg], right[neg], -1)': lambda S, B, r: f'弹出负堆顶，合并它的左右孩子 → 负堆 `{_heap(S, B.neg, -1)[1:]}`',
        'ori_pos = pos': lambda S, B, r: f'取出正堆顶 `ori_pos`（值 `{_eff(S, S.ori_pos)}`）',
        'pos = merge(left[pos], right[pos], 1)': lambda S, B, r: f'弹出正堆顶，合并它的左右孩子 → 正堆 `{_heap(S, B.pos, 1)[1:]}`',
        'neg = merge(neg, ori_pos, -1)': lambda S, B, r: f'==交换==：正堆顶 `{_eff(S, S.ori_pos)}` 放进负堆 → `{sorted(_heap(S, S.neg, -1) + [_eff(S, S.ori_pos)], reverse=True)}`',
        'pos = merge(pos, ori_neg, 1)': lambda S, B, r: f'负堆顶 `{_eff(S, S.ori_neg)}` 放进正堆 → `{sorted(_heap(S, S.pos, 1) + [_eff(S, S.ori_neg)])}`',
        'res += val[ori_neg] - val[ori_pos]': lambda S, B, r: f'交换代价 `{S.val[S.ori_neg]} − {S.val[S.ori_pos]}` = =={S.val[S.ori_neg] - S.val[S.ori_pos]}==，累加进 `res`（这就是答案的来源）',
        'return neg, pos': lambda S, B, r: f'返回 负堆 `{_heap(S, B.neg, -1)}`、正堆 `{_heap(S, B.pos, 1)}`（所有分割点）',
        'dfs(root)': '自底向上处理整棵树',
        'return res': '答案 `3`：根取 5 时总代价最小',
    },
    cards=dict(
        one_liner='把每棵子树的代价函数拆成分割点，用两个堆维护，换位一次就是答案加一份',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['二叉树每个节点有权重 `val`；若所有父子之差都 `≤ 1` 则稳定',
                 '每次操作可把一个节点的值 `+1` 或 `-1`，求使树稳定的最少操作数',
                 '节点数 ≤ 50000，权重在 `[-10^5, 10^5]`',
                 '本视频：根 5，左孩子 8，右孩子 3 → `3`'],
        quote='自底向上，不断将左右孩子的分段函数分割点向外扩展1，合并后再与自身的绝对值函数合并的过程。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f(x)` 表示根取 `x` 时子树的最小代价，是一串斜率递增的折线',
              '只记斜率为负、正的分割点：两个堆（大顶 / 小顶）',
              '父子容错 1：负堆整体 `-1`、正堆整体 `+1`（懒标记）',
              '负堆顶 > 正堆顶就逆序：交换二者，答案加上差值'],
        after=[dict(heading='和 LCP 59 同一类', lines=[
            '「斜率技巧」：折线函数的分割点按斜率排序存进堆',
            '合并子树 = 合并堆，用左偏树做到 `O(log n)`',
            '对顶堆纠正逆序：弹出两堆顶互换，代价累加',
        ])],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '整体平移用懒标记，只改堆根，合并时再下放',
                 '易错：`while` 里要弹出两个堆顶并交换，答案累加 `ori_neg − ori_pos`',
                 '用 `global res` 在嵌套函数里累计答案，原文为 Python 2 风格，代码未改'],
    ),
)
