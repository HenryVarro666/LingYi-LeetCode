import math
def _fit(cv, s, size, maxw, bold=True):
    while size > 13 and cv.tlen(s, size, bold) > maxw:
        size -= 1
    return size


def _seg(cv, T, box, n, lab, kids, cur=(), chg=(), nums=None, num_hl=(), title='', root=1, bound=None):
    """线段树示意图：上排 = 数组（可选），下面每个节点 = 一段区间；黄色 = 当前节点，黄边 = 这一步刚改过，虚框 = 还没算出"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 60) / max(n, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 36
    if nums is not None:
        for i in range(n):
            X = sx + i * cell
            hl = i in num_hl
            cv.rect((X + 2, top, X + cell - 2, top + 40), fill=T['yellow'] if hl else T['panel2'], r=6)
            cv.text((X + cell / 2, top + 20), nums[i] if i < len(nums) else '', 24, T['bg'] if hl else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + 44), i, 16, T['dim'], anchor='mt', mono=True)
        top += 72
    nodes = {}
    def walk(nd, l, r, d):
        nodes[nd] = (l, r, d)
        if l < r:
            m = (l + r) // 2
            a, b = kids(nd)
            walk(a, l, m, d + 1)
            walk(b, m + 1, r, d + 1)
    walk(root, 0, n - 1, 0)
    depth = max(d for _, _, d in nodes.values()) + 1
    rowh = min(112, (y1 - top - 6) / depth)
    bh = min(54, rowh - 30)
    pos = {}
    for nd, (l, r, d) in nodes.items():
        cx = sx + (l + r + 1) / 2 * cell
        pos[nd] = (cx, top + d * rowh)
    for nd, (l, r, d) in nodes.items():
        if l < r:
            for c in kids(nd):
                cv.line([(pos[nd][0], pos[nd][1] + bh + 20), (pos[c][0], pos[c][1])], T['border'], 2)
    for nd, (l, r, d) in nodes.items():
        cx, cy = pos[nd]
        w = min(max(cell * (r - l + 1) - 8, 40), 190 if r > l else 130)
        s = lab(nd)
        is_cur = nd in cur
        changed = nd in chg
        if s is None:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['dim'], width=1, r=8)
            s = ''
        else:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), fill=T['yellow'] if is_cur else T['panel2'],
                    outline=T['yellow'] if changed else T['border'], width=4 if changed else 1, r=8)
        if is_cur and s == '':
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['yellow'], width=4, r=8)
        sz = _fit(cv, s, 24, w - 10)
        cv.text((cx, cy + bh / 2), s, sz, T['bg'] if is_cur and s else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + bh + 3), f'#{nd} [{l},{r}]', 15, T['dim'], anchor='mt', mono=True)



def _draw(cv, S, B, box, T):
    f = S.get('f')
    if f is None or 'n' not in S:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    fb = B.get('f')
    chg = set()
    if fb is not None and len(fb) == len(f):
        chg = {i for i in range(len(f)) if fb[i] != f[i]}
    cur = S['_inner'].get('x')
    if S.get('_line') == 55:
        cur = B.get('x', cur)
    _seg(cv, T, box, S['n'], lambda nd: '∅' if f[nd] is None else str(f[nd]), lambda nd: (nd * 2 + 1, nd * 2 + 2),
         cur=(cur,) if cur is not None else (), chg=chg, root=0,
         title="线段树 f：节点 = 区间内（倍数 ÷ p）的 GCD，∅ = 没有倍数")


def _info(S):
    f = S.get('f')
    if f is None:
        return f"`n = {S['n']}`" + ('，`n ≤ 6` 走暴力枚举' if S['n'] <= 6 else '，`n > 6`：只靠线段树根节点判断')
    return f"根 `f[0]` = ==" + ('∅' if f[0] is None else str(f[0])) + "==：存在好子序列 ⇔ `f[0] == 1`"


def _upd(S, B, ret):
    return f"叶子 `{S.index}`：新值 `{S.v}`，存入 `f[{S.x}]`" + ('（不是倍数 → ∅）' if S.v is None else '')


CONFIG = dict(
    num=3901, title='好子序列查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（倍数除以 p 后求 GCD）+ n ≤ 6 暴力',
    tags=['灵神题单·常用数据结构', '灵神题单·数学算法', '难度分 2545'],
    code='''
class Solution(object):
    def countGoodSubseq(self, nums, p, queries):
        
        n = len(nums)
        res = 0

        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        if n <= 6:
            for index, v in queries:
                nums[index] = v
                flag = False
                for state in range(1, (1 << n) - 1):
                    g = None
                    for idx in range(n):
                        if (state & (1 << idx)) == (1 << idx) and nums[idx] % p == 0:
                            if g is None:
                                g = nums[idx]
                            else:
                                g = gcd(g, nums[idx])

                    if g == p:
                        flag = True
                        break

                if flag:
                    res += 1

            return res

        f = [None] * (n * 4)

        def update(x, left, right, index, v):
            if left == right:
                f[x] = v
                return

            mid = (left + right) // 2
            if index <= mid:
                update(x + x + 1, left, mid, index, v)
            else:
                update(x + x + 2, mid + 1, right, index, v)
            
            if f[x + x + 1] is None:
                if f[x + x + 2] is None:
                    f[x] = None
                else:
                    f[x] = f[x + x + 2]
            elif f[x + x + 2] is None:
                f[x] = f[x + x + 1]
            else:
                f[x] = gcd(f[x + x + 1], f[x + x + 2])
        
        tot = 0
        cnt = {}

        for index, v in enumerate(nums):
            if v % p == 0:
                v //= p
            else:
                v = None
            update(0, 0, n - 1, index, v)
        
        for index, v in queries:
            if v % p == 0:
                v //= p
            else:
                v = None
            update(0, 0, n - 1, index, v)

            if f[0] == 1:
                res += 1
        
        return res
''',
    call='Solution().countGoodSubseq([4, 6, 3, 8, 5, 10, 12], 2, [[1, 4], [5, 12]])',
    expect=1,
    max_steps=70,
    skip=['res = 0', 60, 61, 62, 64, 68, 69, 71, 8, 9, 10, 'n = len(nums)', 'mid = (left + right)', 'f = [None]', 'tot = 0', 'cnt = {}', 'if left == right', 'if index <= mid', 'update(x + x + 1', 'update(x + x + 2', 'is None', 'return', 'while y != 0'],
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=110),
    ],
    watch=['p', 'n', ('res', 'res', 'green')],
    captions={
        5: '`res` 统计答案；下面先按 `n` 的大小分两条路',
        12: '`n = {n}` > 6：不暴力枚举（`n ≤ 6` 才枚举所有长度小于 n 的子序列），改用线段树',
        60: lambda S, B, r: ('7 个数都写进线段树了，建树完成' if B.get('index') == S.index else f"把第 `{S.index}` 个数 `{S.nums[S.index]}` 放进线段树"),
        65: lambda S, B, r: (f"第 `{S.index}` 个数 `{S.nums[S.index]}` 是 `{S.p}` 的倍数 → 除以 `p` 得 `{S.v}`，写入线段树" if S.v is not None
                             else f"第 `{S.index}` 个数 `{S.nums[S.index]}` 不是 `{S.p}` 的倍数 → 记为 ∅（当作不存在）"),
        38: _upd,
        49: '左右儿子都是 ∅ → 节点 `{x}` 也是 ==∅==',
        51: '左儿子是 ∅，只有右儿子有值 → 节点 `{x}` 直接取右儿子 `{f[x]}`',
        53: '右儿子是 ∅，只有左儿子有值 → 节点 `{x}` 直接取左儿子 `{f[x]}`',
        55: lambda S, B, r: f"两个儿子都有值 → 取最大公约数：`gcd({B.f[B.x+B.x+1]}, {B.f[B.x+B.x+2]})` = =={math.gcd(B.f[B.x+B.x+1], B.f[B.x+B.x+2])}==（节点 `{B.x}`）",
        72: lambda S, B, r: (f"查询 `nums[{S.index}] = {S.v if S.v is None else S.v * S.p}`" + (f" → 除以 `p` 得 `{S.v}`，更新线段树" if S.v is not None else " 不是倍数 → 记为 ∅，更新线段树"))
                            if 'v' in S else '',
        74: lambda S, B, r: (f'根节点 `f[0]` = `{S.f[0]}` ' + ('= 1：所有倍数除以 `p` 后互质 → 存在好子序列' if S.f[0] == 1 else ('≠ 1：GCD 大于 `p`，选更少的数也不行 → 没有好子序列' if S.f[0] is not None else '是 ∅：没有 `p` 的倍数'))),
        75: '这次查询有好子序列：`res` → =={res}==',
        67: lambda S, B, r: ('查询处理完毕' if B.get('index') == S.index else '处理下一个查询：只改一个位置，`O(log n)` 更新'),
        170: '一共 `{res}` 次查询后存在好子序列',
    },
    cards=dict(
        one_liner='倍数除以 p 之后 GCD 为 1，且 n ≤ 6 时暴力枚举',
        complexity='时间 `O(n + q log n log U)`（`n ≤ 6` 时暴力），空间 `O(n)`',
        problem=['数组 `nums`、整数 `p`；子序列长度要 `< n` 且 GCD 恰好等于 `p` 才是好子序列',
                 '每次单点修改后，问是否存在好子序列，统计「存在」的查询数',
                 '示例：`nums=[4,5,7,8], p=3, queries=[[0,6],[1,9],[2,3]]` → `2`',
                 '本视频：`[4,6,3,8,5,10,12]`，`p=2`，修改 2 次 → `1`'],
        quote='若数组中所有元素都是p的倍数且最大公约数为p的话，且不存在好子序列的话，任取一个长度为n - 1的子序列，这些子序列的最大公约数都不为p',
        quote_src='—— yiduobo 题解',
        idea=['先不管长度限制：元素都是 `p` 的倍数，==除以 `p` 后 GCD 恰为 1==；用线段树做单点修改 + 区间 GCD',
              '非倍数的叶子存 `None`：一侧为 `None` 就取另一侧，两侧都有值才取 GCD',
              '长度 `n-1` 的 n 个子序列 GCD 要两两不同，每个数至多 6 个质因子 → 只有 ==`n ≤ 6`== 才要特判，直接暴力枚举'],
        summary=['`n > 6` 时每次查询 `O(log n · log U)`；`n ≤ 6` 时枚举 `2^n` 个子集，常数很小',
                 '叶子用 `None` 表示「不是倍数」：不能用 `0`，因为这份代码按「是否 None」来合并',
                 '易错：倍数要先 `v //= p` 再进线段树，根为 `1` 才表示存在好子序列',
                 '原文本身可直接在 Python 3 运行，没有做任何修改；`n > 6` 分支里没有同步更新 `nums`，因为线段树已存下所有信息'],
    ),
)
