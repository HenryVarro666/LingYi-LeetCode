from math import gcd

NUMS = [2, 4, 9, 6]
MAXC = 1


def _bounds():
    n = len(NUMS)
    out = []
    for i in range(n):
        j = i
        g = 0
        while j < n and gcd(g, NUMS[j]) > 1:
            g = gcd(g, NUMS[j])
            j += 1
        out.append(j - 1)
    return out


BL = _bounds()


def _mods(mid):
    """复现二分里 check 的贪心：返回 (要改的位置列表, 是否超出 maxC)"""
    n, p, out = len(NUMS), 0, []
    while p + mid < n:
        while p + mid < n and p + mid > BL[p]:
            p += 1
        if p + mid == n:
            break
        out.append(p + mid)
        if len(out) > MAXC:
            return out, True
        p += mid + 1
    return out, False


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    line = S.get('_line', 0)
    cell = min(100, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 96
    binary = line >= 58 and 'mid' in S and 'need' in S and line >= 62
    bl = S.get('bound_list', []) if 'bound_list' in S else []
    scan = 37 <= line <= 56 and 'index' in S and 'bound_list' in S
    cv.text((x0 + 18, y0 + 4), 'nums（下方横条 = 以 index 为左端点、GCD > 1 的最远范围）' if not binary else
            f"nums（试 mid = {S['mid']}：每个长 {S['mid'] + 1} 的窗口里至少改一个，红 = 改成 1）", 24, T['muted'], bold=True)
    mods, over = _mods(S['mid']) if binary else ([], False)
    shown = mods[:S['need']] if binary else []
    for idx, v in enumerate(NUMS):
        X = sx + idx * cell
        modded = idx in shown
        cv.rect((X + 4, top, X + cell - 4, top + cell * 0.68), fill=T['red'] if modded else (60, 68, 80), r=8)
        cv.text((X + cell / 2, top + cell * 0.34), 1 if modded else v, 34, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, top + cell * 0.68 + 4), idx, 18, T['dim'], anchor='mt', mono=True)
    yb = top + cell * 0.68 + 36
    for k, b in enumerate(bl):
        if b < k:
            continue
        if scan and k == S['index'] and line < 56:
            continue
        yy = yb + k * 44
        cv.rect((sx + k * cell + 8, yy, sx + (b + 1) * cell - 8, yy + 14), fill=T['cyan'], r=6, alpha=220)
        cv.text((sx + (k + b + 1) * cell / 2, yy + 18), f'bound_list[{k}] = {b}', 19, T['muted'], anchor='mt', mono=True)
    if scan:
        for name, val, c, row in (('index', S['index'], T['blue'], 0), ('p', S.get('p'), T['pink'], 1)):
            if val is not None and 0 <= val < n:
                X = sx + val * cell + cell / 2
                cv.tri_down(X, top - 6, 9, c)
                cv.text((X + (12 if row else -12), top - 34), name, 20, c, anchor='lm' if row else 'rm', bold=True)
    if binary:
        p = S['p']
        for name, val, c in (('p', p, T['blue']), ('p+mid', p + S['mid'], T['yellow'])):
            if 0 <= val < n:
                X = sx + val * cell + cell / 2
                cv.tri_down(X, top - 6, 9, c)
                cv.text((X, top - 34), name, 20, c, anchor='mb', bold=True)
        cv.text((x0 + 30, y1 - 36), f"需要修改 need = {S['need']}，限额 maxC = {MAXC}", 24, T['red'] if S['need'] > MAXC else T['green'], bold=True)


def _tree(S):
    if 'f' not in S or S.get('_line', 0) >= 58:
        return ''
    f = S['f'][:2 * len(NUMS) - 1]
    return '线段树 `f` = ' + ', '.join(str(v) for v in f) + '　（节点 0 = 整段，1、2 = 左右半，3–6 = 叶子）'


def _top(S):
    line = S.get('_line', 0)
    if line >= 62 and 'mid' in S and 'need' in S:
        return f"试 `mid = {S['mid']}`：窗口长 `mid + 1 = {S['mid'] + 1}`，全是 GCD > 1 就必须改一个"
    if 'bound_list' in S and 35 <= line <= 56:
        return '双指针算 `bound_list`：右端点 `p` 只前进；左端点右移时，GCD 要重新查线段树'
    if 'bound_list' not in S:
        return '先建线段树，用来 `O(log n)` 查任意区间的 GCD'
    return '二分稳定性因子 `mid`：贪心看每个长 `mid + 1` 的窗口'


def _ret_mid(S, B, ret):
    return f'`left = right = {S.left}` → 最小稳定性因子 =={ret}=='



CONFIG = dict(
    num=3605, title='数组的最小稳定性因子', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 线段树查 GCD',
    tags=['灵神题单·二分算法', '灵神题单·位运算', '难度分 2410'],
    code='''
class Solution(object):
    def minStable(self, nums, maxC):

        n = len(nums)
        f = [0] * (n * 4)
        
        def gcd(x, y):
            while x % y != 0:
                x, y = y, x % y
            return y

        def build(now, left, right, f):
            if left == right:
                f[now] = nums[left]
            else:
                mid = (left + right) // 2
                build(now + now + 1, left, mid, f)
                build(now + now + 2, mid + 1, right, f)
                f[now] = gcd(f[now + now + 1], f[now + now + 2])
        
        def get(now, left, right, start, end, f):
            if left == start and right == end:
                return f[now]
            
            mid = (left + right) // 2
            if end <= mid:
                return get(now + now + 1, left, mid, start, end, f)
            elif start > mid:
                return get(now + now + 2, mid + 1, right, start, end, f)
            else:
                return gcd(get(now + now + 1, left, mid, start, mid, f), get(now + now + 2, mid + 1, right, mid + 1, end, f))

        build(0, 0, n - 1, f)

        bound_list = []
        p = 0
        for index in range(n):
            if p <= index:
                if nums[index] == 1:
                    bound_list.append(index - 1)
                    continue
                    
                p = index + 1
                g = nums[index]
            else:           
                g = get(0, 0, n - 1, index, p - 1, f)

            while p < n:
                new_g = gcd(g, nums[p])
                if new_g > 1:
                    g = new_g
                    p += 1
                else:
                    break
            
            bound_list.append(p - 1)

        left = 0
        right = n
        while left < right:
            mid = (left + right) // 2
            p = 0
            need = 0
            while p + mid < n:
                while p + mid < n and p + mid > bound_list[p]:
                    p += 1
                if p + mid == n:
                    break
                need += 1
                if need > maxC:
                    break
                p += mid + 1
            
            if need <= maxC:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call=f'Solution().minStable({NUMS}, {MAXC})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=25, h=80),
        dict(type='text', fn=_tree, size=24, h=60),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'), ('p', 'p', 'pink'),
           ('need', 'need', 'red')],
    skip=['while x % y != 0', 'x, y = y, x % y', 'return y', 'f[now] = nums[left]', 13, 16, 17, 18, 22, 25, 26, 27, 28, 29, 39, 44, 49, 51, 54, 35, 36, 58, 59, 63, 64, 68, 71],
    max_steps=90,
    captions={
        4: '`n = {n}`',
        5: '`f`：线段树数组，每个节点存一段区间的 GCD（开 `4n` 个格子）',
        7: '先定义 `gcd`（辗转相除）',
        12: '`build` 递归建线段树：节点 `now` 管 `[left, right]`',
        13: lambda S, B, r: (f'`left == right = {S.left}`：叶子，直接存 `nums[{S.left}]`' if S.left == S.right
                             else f'区间 `[{S.left}, {S.right}]` 还可以再分 → 取中点递归'),
        16: '`mid = ({left} + {right}) // 2 = {mid}`：左半 `[{left}, {mid}]`，右半 `[{mid + 1}, {right}]`',
        19: lambda S, B, r: f'节点 `{S.now}` = 左右孩子的 GCD：`gcd({S.f[S.now + S.now + 1]}, {S.f[S.now + S.now + 2]}) = {gcd(S.f[S.now + S.now + 1], S.f[S.now + S.now + 2])}`',
        21: '`get` 查询 `[start, end]` 的 GCD：区间完全落在一边就进那一边，跨中点就拆成两段再 gcd',
        22: lambda S, B, r: ('查询区间正好是这个节点 → 直接用 `f[now]`' if S.left == S.start and S.right == S.end
                             else '查询区间比节点小 → 要往下走'),
        23: '命中节点 `{now}`：`f[{now}] = {f[now]}`',
        33: '递归建线段树：叶子存 `nums[i]`，节点 = 两个孩子的 GCD',
        35: '`bound_list[i]`：以 `i` 为左端点，GCD > 1 的子数组最远能到哪',
        36: '`p`：右端点（下一个还没并进来的位置），只会向右走',
        37: lambda S, B, r: (f'`index` 遍历完 → `bound_list` = {S.bound_list}' if B.get('index') == S.index and S.index == len(NUMS) - 1 and len(S.bound_list) == len(NUMS)
                             else (f'处理左端点 `index = {S.index}`（`bound_list[i]`：从 `i` 出发 GCD > 1 最远到哪；`p` 是只右移的右端点）' if S.index == 0 else f'处理左端点 `index = {S.index}`')),
        38: lambda S, B, r: (f'`p = {S.p} <= index = {S.index}`：窗口是空的，从 `index` 重新开始' if S.p <= S.index
                             else f'`p = {S.p} > index = {S.index}`：窗口 `[{S.index}, {S.p - 1}]` 还在，但左端点移动了'),
        39: lambda S, B, r: ('`nums[index] == 1`：GCD 一定是 1 → 范围为空' if S.nums[S.index] == 1 else f'`nums[{S.index}] = {S.nums[S.index]} != 1`'),
        43: '窗口先放 `nums[{index}] = {nums[index]}`，`p = {p}`',
        44: '`g = nums[{index}] = {g}`：当前窗口的 GCD',
        46: lambda S, B, r: f'左端点右移，GCD ==可能变大==，要查线段树：`[{S.index}, {S.p - 1}]` 的 GCD = =={__import__("functools").reduce(gcd, S.nums[S.index:S.p])}==',
        48: lambda S, B, r: (f'`p = {S.p} < n`：试着把 `nums[{S.p}]` 并进窗口' if S.p < len(NUMS) else f'`p = {S.p} == n` → 右边没有了'),
        49: lambda S, B, r: f'`gcd({S.g}, nums[{S.p}] = {S.nums[S.p]}) = {gcd(S.g, S.nums[S.p])}`：把 `nums[{S.p}]` 并进窗口后的 GCD',
        50: lambda S, B, r: (f'`gcd({S.g}, nums[{S.p}] = {S.nums[S.p]}) = {gcd(S.g, S.nums[S.p])}` > 1 → 可以并进来，`g` 更新，`p` 右移' if gcd(S.g, S.nums[S.p]) > 1 else f'`gcd({S.g}, nums[{S.p}] = {S.nums[S.p]}) = 1` → ==不能并==，窗口到头了'),
        51: '窗口 GCD 更新为 `g = {g}`',
        52: '`g` 更新为新的 GCD，`p` → {p}：右端点右移',
        54: 'GCD 变成 1，窗口到头了',
        56: '`bound_list[{index}] = p - 1 = {p - 1}`：从 `{index}` 出发，GCD > 1 最远到 `{p - 1}`',
        58: '`left = 0`：稳定性因子下界',
        59: '`right = n = {right}`：不改也满足',
        60: lambda S, B, r: (f'`left = {S.left}`、`right = {S.right}`：答案区间，继续二分' if S.left < S.right else f'`left == right = {S.left}` → 结束'),
        61: '`mid = ({left} + {right}) // 2 = {mid}`：试==稳定性因子不超过 mid==',
        62: '`p = 0`、`need = 0`：扫描每个长 `mid + 1` 的窗口',
        64: lambda S, B, r: (f'`p + mid = {S.p + S.mid} < n`：还有完整的窗口' if S.p + S.mid < len(NUMS) else f'`p + mid = {S.p + S.mid} >= n`：没有完整窗口了'),
        65: lambda S, B, r: (f'窗口 `[{S.p}, {S.p + S.mid}]`：`{S.p + S.mid} > bound_list[{S.p}] = {S.bound_list[S.p]}` → GCD 已是 1，没问题'
                             if S.p + S.mid < len(NUMS) and S.p + S.mid > S.bound_list[S.p]
                             else (f'窗口 `[{S.p}, {S.p + S.mid}]`：`bound_list[{S.p}] = {S.bound_list[S.p]}` 够得到末尾 → ==GCD > 1，必须改==' if S.p + S.mid < len(NUMS)
                                   else '窗口已经出界')),
        66: '`p` → {p}：窗口左端点右移一格',
        67: lambda S, B, r: ('`p + mid == n`：后面凑不成完整窗口 → 不用再改' if S.p + S.mid == len(NUMS) else '找到一个必须改的窗口'),
        69: '改最后一个 `nums[{p + mid}]` 为 1 → `need = {need}`',
        70: lambda S, B, r: (f'`need = {S.need} > maxC = {S.maxC}` → 次数不够，`mid` 不行' if S.need > S.maxC else f'`need = {S.need} <= maxC = {S.maxC}` → 还够用'),
        72: '1 挡住了前面的窗口 → `p += mid + 1` = {p}',
        74: lambda S, B, r: (f'`need = {S.need} <= maxC = {S.maxC}` → `mid = {S.mid}` 可行，答案 ==不超过 mid=='
                             if S.need <= S.maxC else f'`need = {S.need} > maxC = {S.maxC}` → `mid = {S.mid}` 不可行，答案 ==大于 mid=='),
        75: '`right = {right}`',
        77: '`left = mid + 1 = {left}`',
        79: _ret_mid,
    },
    cards=dict(
        one_liner='二分稳定性因子 mid；每个长 mid+1 的窗口若 GCD>1 就改末尾为 1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组 GCD ≥ 2 称为==稳定==；稳定性因子 = 最长稳定子数组的长度',
                 '最多修改 `maxC` 个元素为任意整数，使稳定性因子最小',
                 '示例：`[2,4,9,6], maxC = 1` → `2`'],
        quote='每次修改都应该将数组中一个大于1的元素修改成1，这样一来包含这个元素的任意子数组的最大公约数都为1，换言之这个1截断了整个数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['改成 1 把数组截断；固定左端点，右端点越远 GCD 越小 → 可二分答案',
              '判 `mid`：从左往右，窗口 `[p, p+mid]` 的 GCD > 1 就改最后一个元素，`p` 跳到 `p+mid+1`',
              '窗口 GCD 用线段树查；预处理 `bound_list`：每个左端点 GCD > 1 的最远右端点'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '左端点右移后 GCD 可能变大（`[2,3,6]` → `[3,6]`），不能只用滑窗，要查线段树；对比灵神的 LogTrick',
                 '`bound_list[p] >= p + mid` 等价于窗口 `[p, p+mid]` 的 GCD > 1',
                 '原文已是 Python 3 可运行，没有改动']
    ),
)
