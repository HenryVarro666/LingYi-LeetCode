def _layout(c, node, depth, acc, nxt):
    """acc[node] = (x_leaf_unit, depth); x of internal node = mean of children"""
    kids = [ch for ch in c[node] if ch is not None]
    if not kids:
        acc[node] = (nxt[0], depth)
        nxt[0] += 1
        return
    for ch in kids:
        _layout(c, ch, depth + 1, acc, nxt)
    xs = [acc[ch][0] for ch in kids]
    acc[node] = (sum(xs) / len(xs), depth)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    c, w = S.get('c'), S.get('weight')
    cv.text((x0 + 18, y0 + 4), 'trie：每条边是二进制的一位（0 / 1），节点里是经过它的前缀个数 weight', 22, T['muted'], bold=True)
    if not c or not w:
        return
    L = S.get('length')
    acc, nxt = {}, [0]
    _layout(c, 0, 0, acc, nxt)
    leaves = max(nxt[0], 1)
    maxd = max(d for _, d in acc.values())
    top, bot = y0 + 90, y1 - 70
    dy = (bot - top) / max(maxd, 1) if maxd else 0
    left, right = x0 + 150, x1 - 90
    ux = (right - left) / max(leaves - 1, 1) if leaves > 1 else 0
    pos = {n: ((left + right) / 2 if leaves == 1 else left + acc[n][0] * ux, top + acc[n][1] * dy) for n in acc}
    now = S.get('now')
    idx = S.get('index')
    for n, (px, py) in pos.items():
        for b_, ch in enumerate(c[n]):
            if ch is not None and ch in pos:
                qx, qy = pos[ch]
                cv.line([(px, py), (qx, qy)], T['border'] if b_ == 0 else T['dim'], 4)
                cv.text(((px + qx) / 2 + (-16 if b_ == 0 else 16), (py + qy) / 2), b_, 24, T['cyan'] if b_ == 0 else T['orange'], anchor='mm', bold=True, mono=True)
    for n, (px, py) in pos.items():
        cur = (n == now)
        cv.rect((px - 30, py - 24, px + 30, py + 24), fill=T['yellow'] if cur else T['panel2'], outline=T['border'], r=24)
        cv.text((px, py), w[n], 28, T['bg'] if cur else T['text'], anchor='mm', bold=True)
    if L:
        for dep in range(L + 1):
            yy = top + dep * ((bot - top) / max(L, 1))
            lab = '根' if dep == 0 else f'第 {L - dep} 位'
            hot = idx is not None and dep >= 1 and L - dep == idx
            cv.text((x0 + 18, yy), lab, 22, T['yellow'] if hot else T['dim'], anchor='lm', bold=hot)


def _bits(S):
    if 'digits_k' not in S or 'length' not in S:
        return '先看一眼：子数组异或 = 两个前缀异或再异或，`xor ^ 旧前缀 >= k` 就算一个'
    L = S['length']
    kb = ''.join(map(str, S['digits_k'][::-1]))
    xb = format(S['xor'], f'0{L}b') if 'res' in S else '?' * L
    return f'前缀 `xor = {xb}`（{S.get("xor", 0)}）　`k = {kb}`　`res = {S.get("res", 0)}`'


CONFIG = dict(
    num=3632, title='子数组异或至少为K的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀异或 + 01 Trie 计数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countXorSubarrays(self, nums, k):
        
        c = [[None, None]]
        weight = [0]

        ma = max(max(nums), k)
        length = len(bin(ma)) - 2
        p2 = [1]
        while len(p2) < length:
            p2.append(p2[-1] + p2[-1])

        now = 0
        for index in range(length - 1, -1, -1):
            c[now][0] = len(weight)
            c.append([None, None])
            weight.append(1)
            now = c[now][0]

        digits_k = [0] * length
        p = 0
        while k:
            digits_k[p] = k % 2
            k //= 2
            p += 1

        xor = 0
        res = 0
        for v in nums:
            xor ^= v
            now = 0
            for index in range(length - 1, -1, -1):
                if xor & p2[index]:
                    d = 1
                else:
                    d = 0

                if digits_k[index] == 1:
                    now = c[now][1 - d]
                else:
                    if c[now][1 - d] is not None:
                        res += weight[c[now][1 - d]]
                    now = c[now][d]
                
                if now is None:
                    break

            if now is not None:
                res += weight[now]
        
            now = 0
            for index in range(length - 1, -1, -1):
                if xor & p2[index]:
                    d = 1
                else:
                    d = 0
                
                if c[now][d] is None:
                    c[now][d] = len(weight)
                    c.append([None, None])
                    weight.append(0)
                
                now = c[now][d]
                weight[now] += 1

        return res
''',
    call='Solution().countXorSubarrays([3, 1], 2)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', h=90, size=28, fn=_bits),
    ],
    max_steps=140,
    skip=['d = 1', 'd = 0', 'else:', 'c.append(', 'p2.append', 'while len(p2)', 'p = 0', 'k //= 2', 'p += 1', 'while k', 'weight.append(0)', 'weight.append(1)', 63, 'p2 = [1]', 'ma = ', 'c = [[', 'weight = [0]'],
    watch=['now', 'index', 'd', ('res', 'res', 'green')],
    captions={
        'length = len': '最大数 `{ma}` 的二进制有 `length = {length}` 位，所有数都按这个位数处理',
        'now = 0': lambda S, B, r: ('从根出发' if S._line == 13 else ('从根出发查询：数有多少个旧前缀 `p` 满足 `xor ^ p >= k`' if S._line == 31 else '从根出发，把当前 xor 插入 trie')),
        'for index in range(length - 1, -1, -1)': lambda S, B, r: (
            f'处理第 `{S.index}` 位' if 'index' in S and B.get('index') != S.index else '这一轮的所有位都处理完了'),
        'c[now][0] = len(weight)': '先把空前缀（xor = 0）插入：沿 0 边建一条链，新节点 `{c[now][0]}` 挂在 `{now}` 的 0 边上',
        'weight.append(1)': '新节点 `{len(weight)-1}` 的 weight = 1（经过它的前缀只有 0）',
        'now = c[now][0]': '走进新节点 `now = {now}`',
        'digits_k = [0]': '`digits_k` 存 k 的每一位（下标 0 是最低位）',
        'digits_k[p]': '`k` 的第 `{p}` 位是 `{digits_k[p]}`',
        'xor = 0': '`xor` 是前缀异或，`res` 是答案',
        'for v in nums': lambda S, B, r: (f'取 `v = {S.v}`' if B.get('v') != S.get('v') or S.v is None else '所有数处理完了'),
        'xor ^= v': '前缀异或：`xor = {B.xor} ^ {v} = {xor}`，`xor ^ 旧前缀` 就是以 v 结尾的子数组的异或',
        'if xor & p2[index]': lambda S, B, r: f'`xor` 的第 `{S.index}` 位是 `d = {1 if S.xor & S.p2[S.index] else 0}`',
        'if digits_k[index] == 1': lambda S, B, r: (
            f'`k` 的第 {S.index} 位是 ==1==：异或结果这一位必须是 1 → 只能走 `1 - d` 那边' if S.digits_k[S.index] == 1 else
            f'`k` 的第 {S.index} 位是 ==0==：异或结果这位只要是 1 就一定大于 k'),
        'now = c[now][1 - d]': '`k` 位为 1：只能往 `1 - d` 走，下一个节点 `now = {now}`（None 表示没有这样的前缀）',
        'if c[now][1 - d] is not None': lambda S, B, r: ('`1 - d` 那一侧存在 → 那里所有前缀异或后这一位是 1，全部合法' if B.c[B.now][1 - B.d] is not None else '`1 - d` 那一侧没有前缀，不加'),
        'res += weight[c[now][1 - d]]': '`1 - d` 侧整棵子树都满足：加上它的 weight → `res = {res}`',
        43: '`k` 位为 0 时，还要沿着 `d` 这一侧继续比低位：`now = {now}`（None 表示没有）',
        'if now is None': lambda S, B, r: ('走不下去了（没有这样的前缀）→ 退出' if S.now is None else '这一位走通了，继续看低一位'),
        'if now is not None': lambda S, B, r: ('走到了最底层：异或结果恰好等于 `k`' if S.now is not None else '中途断路，没有恰好等于 k 的前缀'),
        'res += weight[now]': '恰好等于 `k` 也算（至少为 k）：加上 weight → `res = {res}`',
        'if c[now][d] is None': lambda S, B, r: ('这条边还没有 → 新建节点' if B.c[B.now][B.d] is None else '这条边已有，直接走'),
        'c[now][d] = len(weight)': '新建节点 `{c[now][d]}` 挂在第 `{index}` 位的 `{d}` 边上（weight 先记 0）',
        'weight.append(0)': '新节点 weight 先记 0，下面统一加 1',
        63: '走到第 `{index}` 位的 `{d}` 边下的节点 `{now}`',
        'weight[now] += 1': '走到节点 `{now}`，经过它的前缀多了一个：`weight[{now}] = {weight[now]}`',
        'break': '`now` 是 None，后面的位不用看了',
        'res = 0': '`res` 是答案',
        'return res': '一共 `{res}` 个子数组的异或 >= k',
    },
    cards=dict(
        one_liner='子数组异或 = 前缀异或再异或；用 trie 一次数完所有合法前缀',
        complexity='时间 `O(n log C)`，空间 `O(n log C)`',
        problem=['给 `nums` 和非负整数 `k`，统计异或值 `>= k` 的子数组个数',
                 '`n <= 10^5`，元素和 `k` 不超过 `10^9`，暴力不行',
                 '本视频：`nums = [3,1]`，`k = 2` → `2`'],
        quote='对同一个元素异或两次相当于无事发生……子数组异或值可以转化为两个前缀数组的异或结果再进行异或。',
        quote_src='—— yiduobo 题解原文',
        idea=['异或没有单调性，滑窗不行：改成「当前前缀 xor」配「旧前缀」，看 `xor ^ 旧前缀 >= k`',
              '把前缀拉成定长 01 串放进 trie，每个节点记 `weight` = 经过它的前缀个数',
              '逐位比较：`k` 这位是 1 就只能走 `1 - d`；是 0 时，`1 - d` 侧整棵子树都更大，直接加 weight，再沿 `d` 继续'],
        summary=['时间 `O(n log C)`，空间 `O(n log C)`，C 是数值上界',
                 '起初先插入空前缀 0（代码开头沿 0 边建的那条链）',
                 '`k` 位为 0 时：`1 - d` 侧整棵子树计入，再沿 `d` 走；位为 1 时只能走 `1 - d`',
                 '走到最底层（异或结果恰好等于 k）也要加 `weight[now]`；先查询、后插入当前前缀'],
    ),
)
