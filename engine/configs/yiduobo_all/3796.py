
def _phase_vals(S):
    """受限位置 -> (原上限, 当前值)"""
    ln = S.get('_line', 0)
    cur = {i: mv for i, mv in S['restrictions']}
    orig = dict(cur)
    if 'bound' in S and ln >= 12:
        for i, v in S['bound']:
            cur[i] = v
    if 'adj_bound' in S and ln >= 25:
        for i, v in S['adj_bound']:
            cur[i] = v
    return orig, cur


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, diff = S['n'], S['diff']
    ln = S.get('_line', 0)
    orig, cur = _phase_vals(S)
    if ln <= 11:
        title = '受限位置（黄 = 上限）：先按下标排序'
    elif ln <= 22:
        title = '正向：从左到右，算每个受限位置「够得到」的最大值'
    elif ln <= 34:
        title = '反向修正：右边的限制会把左边的值拉低'
    else:
        title = '逐段构造：先涨后降，峰值更新答案'
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    cell = min(86, (x1 - x0 - 50) / n)
    sx = x0 + 25 + ((x1 - x0 - 50) - cell * n) / 2
    ya = y0 + 80
    ch = cell * 0.9
    final = ln >= 35 and 'index' in S
    p = S.get('p') if ln >= 40 else None
    for i in range(n):
        X = sx + i * cell
        if i in cur:
            fill = T['yellow'] if (ln >= 12) else T['orange']
            cv.rect((X + 3, ya, X + cell - 3, ya + ch), fill=fill, r=8, alpha=230)
            cv.text((X + cell / 2, ya + ch * 0.42), cur[i], 30, T['bg'], anchor='mm', bold=True)
            if cur[i] != orig[i]:
                cv.text((X + cell / 2, ya + ch * 0.8), f'≤{orig[i]}', 17, T['bg'], anchor='mm')
            else:
                cv.text((X + cell / 2, ya + ch * 0.8), '上限', 15, T['bg'], anchor='mm')
        else:
            cv.rect((X + 3, ya, X + cell - 3, ya + ch), fill=T['panel2'], r=8, outline=T['border'])
            cv.text((X + cell / 2, ya + ch / 2), '·', 24, T['dim'], anchor='mm')
        cv.text((X + cell / 2, ya + ch + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 6, ya + ch / 2), '值', 18, T['muted'], anchor='rm')
    # diff 行：diff[k] 在位置 k 与 k+1 之间
    yd = ya + ch + 70
    cv.text((sx - 6, yd + ch * 0.3), 'diff', 18, T['muted'], anchor='rm')
    lo = hi = None
    if ln >= 15 and 'pre_index' in S and 'index' in S and ln <= 22:
        lo, hi = S['pre_index'], S['index']
    if 28 <= ln <= 30 and 'index' in S and 'nxt_index' in S:
        lo, hi = S['index'], S['nxt_index']
    if final:
        lo, hi = S['pre_index'], S['index']
    for k, d in enumerate(diff):
        X = sx + (k + 0.5) * cell
        inr = lo is not None and lo <= k < hi
        done = final and p is not None and lo <= k < p
        fill = T['green'] if done else (T['blue'] if inr else T['panel2'])
        cv.rect((X + 3, yd, X + cell - 3, yd + ch * 0.6), fill=fill, r=8, outline=T['border'], alpha=200)
        cv.text((X + cell / 2, yd + ch * 0.3), d, 24, T['bg'] if (inr or done) else T['text'], anchor='mm', bold=True)
    # 指针
    yp = yd + ch * 0.6 + 14
    marks = []
    if 'pre_index' in S and 12 <= ln <= 22:
        marks.append(('pre_index', S['pre_index'], T['blue']))
    if final:
        marks.append(('index', S['index'], T['pink']))
        if p is not None:
            marks.append(('p', p, T['orange']))
    elif 'index' in S and 11 <= ln <= 31:
        marks.append(('index', S['index'], T['pink']))
    used = {}
    for name, idx, c in marks:
        if not (0 <= idx <= n):
            continue
        # 指针指向位置 idx 的左边缘（diff[idx] 起点）
        X = sx + idx * cell + cell / 2
        row = used.get(idx, 0)
        used[idx] = row + 1
        cv.tri_up(X, yp + 6, 9, c)
        cv.text((X, yp + 20 + row * 24), name, 20, c, anchor='mt', bold=True)
    # 状态文字
    ys = yp + 86
    if final:
        parts = [f"pre_v = {S['pre_v']}", f"v = {S['v']}"]
        if 'delta' in S:
            parts.append(f"delta = {S['delta']}")
        parts.append(f"res = {S['res']}")
        cv.text((x0 + 30, ys), '    '.join(parts), 26, T['text'], bold=True)
        cv.text((x0 + 30, ys + 40), '黄格 = 受限位置最终值；蓝 = 当前这段 diff；绿 = 已经「涨」过的 diff', 18, T['muted'])
    elif 'pre_v' in S and 12 <= ln <= 22:
        cv.text((x0 + 30, ys), f"pre_v = {S['pre_v']}" + (f"    delta = {S['delta']}" if 'delta' in S else ''), 26, T['text'], bold=True)


CONFIG = dict(
    num=3796, title='找到带限制序列的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='受限位置 · 正反两遍 + 先升后降',
    tags=['灵神题单', '难度分 1833'],
    code='''
class Solution(object):
    def findMaxVal(self, n, restrictions, diff):
        
        pre_index = 0
        pre_v = 0
        
        restrictions.sort()
        bound = []
        pre_index = 0
        pre_v = 0
        for index, v in restrictions:
            if pre_v > v:
                pre_v = v
            else:
                delta = sum(diff[pre_index: index])
                if pre_v + delta < v:
                    pre_v += delta
                else:
                    pre_v = v
            
            bound.append([index, pre_v])
            pre_index = index
        
        nxt_index, nxt_v = bound[-1]
        adj_bound = [(nxt_index, nxt_v)]
        for index, v in bound[-2::-1]:
            if v > nxt_v:
                delta = sum(diff[index: nxt_index])
                v = min(nxt_v + delta, v)
            adj_bound.append((index, v))
            nxt_index, nxt_v = index, v
        
        print(adj_bound)
        adj_bound.reverse()

        res = 0
        pre_index = 0
        pre_v = 0
        for index, v in adj_bound:
            p = pre_index
            while p < index and pre_v + diff[p] < v:
                pre_v += diff[p]
                p += 1

            delta = sum(diff[p: index])
            while p < index and pre_v + diff[p] - (delta - diff[p]) <= v:
                pre_v += diff[p]
                delta -= diff[p]
                p += 1

            if p < index and pre_v < delta - diff[p] + v:
                pre_v = delta - diff[p] + v
            
            res = max(res, min(pre_v, v + delta))
            pre_index, pre_v = index, v
        
        return max(res, pre_v + sum(diff[pre_index:]))
''',
    call='Solution().findMaxVal(8, [[2,6],[4,1]], [3,3,2,1,2,2,1])',
    expect=6,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['pre_index', 'pre_v', 'index', 'v', ('res', 'res', 'green')],
    skip=[4, 5],
    max_steps=90,
    captions={
        7: '受限位置按下标排序：`{restrictions}`，从左往右一个个处理',
        8: '`bound` 记录每个受限位置「正向」能达到的最大值',
        9: '`pre_index`、`pre_v`：上一个受限位置，起点是下标 `0`',
        10: '起点 `a[0] = 0`：`pre_v = 0`',
        12: lambda S, B, r: (f"上一位置的值 `pre_v = {S['pre_v']}` 比本位置上限 `v = {S['v']}` 大 → 只能降到 `v`" if S['pre_v'] > S['v'] else f"`pre_v = {S['pre_v']} ≤ v = {S['v']}`：还要看能不能涨到 `v`"),
        13: '`pre_v = v` = =={pre_v}==：从上一位置一路递减，位置 `{index}` 最多取 `{v}`',
        15: '两个受限位置之间 `diff[{pre_index}:{index}]` 一共能涨 `delta` = =={delta}==',
        16: lambda S, B, r: (f"`pre_v + delta = {S['pre_v'] + S['delta']}` 涨满也到不了 `v = {S['v']}` → 只能取涨满的值" if S['pre_v'] + S['delta'] < S['v'] else f"`pre_v + delta = {S['pre_v'] + S['delta']} ≥ v = {S['v']}`：够得到上限 → 取 `v`"),
        17: '`pre_v += delta` → =={pre_v}==：涨满',
        19: '`pre_v = v` → =={pre_v}==：涨得到，取上限 `v`',
        21: '`bound` 记下 `[{index}, {pre_v}]`：位置 `{index}` 正向最多到 `{pre_v}`',
        22: '`pre_index` → `{pre_index}`',
        24: '开始反向修正：从最后一个受限位置 `({nxt_index}, {nxt_v})` 往前看',
        25: '`adj_bound` 存修正后的值（先倒着存）',
        27: lambda S, B, r: (f"前一位置的值 `v = {S['v']}` 比后一位置 `nxt_v = {S['nxt_v']}` 大 → 可能降不下去，要修正" if S['v'] > S['nxt_v'] else f"`v = {S['v']} ≤ nxt_v = {S['nxt_v']}`：不用修正"),
        28: '`delta = sum(diff[{index}:{nxt_index}])` = =={delta}==：这段最多降 `{delta}`',
        29: '`v = min(nxt_v + delta, v)` = =={v}==：被右边的限制拉低',
        30: '`adj_bound` 加入 `({index}, {v})`',
        31: '继续往前：`nxt_index, nxt_v = {index}, {v}`',
        33: '每个受限位置最终最大值（倒序）：`{adj_bound}`',
        34: '翻转成从左到右：`{adj_bound}`',
        36: '`res` 记录最大值',
        37: '重新从起点 `(0, 0)` 出发',
        38: '`pre_v = 0`',
        39: lambda S, B, r: ('所有受限位置处理完' if S['index'] == S['pre_index'] else f"处理受限位置 `({S['index']}, {S['v']})`：从 `({S['pre_index']}, {S['pre_v']})` 走过来"),
        40: '`p = {p}`：从下标 `{p}` 开始，沿着 `diff` 往 `{index}` 走',
        41: lambda S, B, r: ('`p` 已走到 `index`' if S['p'] >= S['index'] else (f"`pre_v + diff[p] = {S['pre_v'] + S['diff'][S['p']]} < v = {S['v']}`：还没到 `v` → 必须先涨" if S['pre_v'] + S['diff'][S['p']] < S['v'] else f"`pre_v + diff[p] = {S['pre_v'] + S['diff'][S['p']]} ≥ v = {S['v']}`：已经够高，不必先涨")),
        42: '`pre_v += diff[p]` → {pre_v}：往上涨一步',
        43: '`p` → {p}',
        45: '剩下 `diff[{p}:{index}]` 的总幅度 `delta` = =={delta}==',
        46: lambda S, B, r: ('`p` 已到 `index`，没有可涨的了' if S['p'] >= S['index'] else (f"再涨 `diff[p]` 到 `{S['pre_v'] + S['diff'][S['p']]}`，剩下 `{S['delta'] - S['diff'][S['p']]}` 还能降回 `v = {S['v']}` 吗？" + ('==能==' if S['pre_v'] + S['diff'][S['p']] - (S['delta'] - S['diff'][S['p']]) <= S['v'] else '==不能=='))),
        47: '`pre_v += diff[p]` → {pre_v}：继续涨，还能降回 `v`',
        48: '`delta -= diff[p]` → {delta}',
        49: '`p` → {p}',
        51: lambda S, B, r: ('涨整根 `diff[p]` 不行，但可以涨一部分：`pre_v = delta − diff[p] + v`' if (S['p'] < S['index'] and S['pre_v'] < S['delta'] - S['diff'][S['p']] + S['v']) else '没有可以再涨一部分的空间'),
        52: '涨一部分：`pre_v` = =={pre_v}==',
        54: '这一段的峰值 `min(pre_v, v + delta)` = `min({pre_v}, {v + delta})` → `res` = =={res}==',
        55: '`pre_index, pre_v = {index}, {v}`：移到下一个受限位置',
        57: '最后一个受限位置之后一路涨：`pre_v + sum(diff[pre_index:])` = `{pre_v + sum(diff[pre_index:])}`，与 `res = {res}` 比 → =={ret}==',
    },
    cards=dict(
        one_liner='受限位置的值先正向推、再反向修；两个位置之间先涨后降',
        complexity='时间 `O(n + r·n)`（受限数 `r`），空间 `O(r)`',
        problem=['构造长度 `n` 的序列 `a`：`a[0]=0`、非负、`|a[i]−a[i+1]| ≤ diff[i]`，且 `a[idx] ≤ maxVal`',
                 '求序列里最大值的最大可能值',
                 '本视频：`n=8, restrictions=[[2,6],[4,1]], diff=[3,3,2,1,2,2,1]` → `6`'],
        quote='对于两个受限制位置，期间的元素应该是按照先单调递增再单调递减才能使得最大值最大，当然在这里可能只有单调递增或者单调递减其中一侧。',
        quote_src='—— yiduobo 题解原文',
        idea=['先只管受限位置：从左往右推 `min(前一个 + 幅度, 上限)`，再从右往左修正被后面限制拉低的值',
              '受限位置的值定下后，每两个相邻受限位置之间：先涨、再降回去，峰值就是候选答案',
              '最后一个受限位置之后没有约束，一路涨到底'],
        summary=['时间 `O(n + r·n)`，`r` 为受限位置个数，空间 `O(r)`',
                 '反向修正不能省：后面的限制会通过 `diff` 一路传回前面',
                 '易错：两段之间要把涨和降拆开；涨不满一整格 `diff` 时只涨一部分，峰值是 `v + delta − diff[p]`',
                 '原文本身 Python 3 可运行，未做改动（含一个 `print(adj_bound)` 调试输出）',
                 '对比灵神：灵神两遍线性扫描直接填 `a`，更短；yiduobo 只处理受限位置，再分段计算峰值'],
    ),
)
