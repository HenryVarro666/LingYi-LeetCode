A_ = [0, 1, 0, 0, 1, 1, 0]
S_ = 2


def _color(E, i, v):
    if 'l' not in E or 'last_pos' not in E:
        return None
    l, lp = E['l'], E['last_pos']
    r = E.get('r')
    nx = E.get('next_pos')
    if r is not None and i in (l, r) and v == 1 and l < len(A_):
        return 'green'
    if lp < i < l and v == 0 and r is not None:
        return 'cyan'
    if r is not None and nx is not None and r < i < nx:
        return 'purple'
    return None


def _text(E):
    if 'next_pos' not in E or 'r' not in E:
        return '合法子数组 = ==前缀若干个 0== + `1 XX…X 1`（恰好 S 个 1）+ ==后缀若干个 0=='
    l, lp, r, nx = E['l'], E['last_pos'], E['r'], E['next_pos']
    if E.get('_line') in (43, 55):
        return (f'前缀 0 可取 0～{l - lp - 1} 个：`{l - lp}` 种；后缀 0 可取 0～{nx - r - 1} 个：`{nx - r}` 种'
                f' → =={(l - lp) * (nx - r)}== 个')
    return f'窗口 `[{l}, {r}]`；左边可用的 0：`({lp}, {l})`，右边可用的 0：`({r}, {nx})`'


def _cap_find_l(E, B, ret):
    l = B.l
    if l < len(B.A) and B.A[l] != 1:
        return f'`A[{l}] = 0` → 继续往右找第一个 1'
    return f'`A[{l}] = 1`：找到第一个 1，窗口左边界 `l = {l}`'


def _cap_grow(E, B, ret):
    if B.r + 1 < len(B.A) and B.now < B.S:
        return f'窗口里只有 `now = {B.now}` 个 1，`< S = {B.S}` → `r` 右移'
    return f'`now = {B.now} = S`：窗口 `[{B.l}, {B.r}]` 就是 `1 XX…X 1`'


def _cap_next(E, B, ret):
    p = B.next_pos
    if p < len(B.A) and B.A[p] == 0:
        return f'`A[{p}] = 0`：是窗口右边的后缀 0 → 继续'
    if p >= len(B.A):
        return f'`next_pos = {p}` 走到数组末尾：后缀 0 数完了'
    return f'`A[{p}] = 1`：这就是 `r` 右边==下一个 1==，`next_pos = {p}`'


def _cap_slide(E, B, ret):
    if B.next_pos < len(B.A):
        return f'`next_pos = {B.next_pos}` 还在数组里 → 窗口==整体滑到下一个 1=='
    return '右边没有下一个 1 了 → 结束'


def _cap_l0(E, B, ret):
    l = B.l
    if l < len(B.A) and B.A[l] == 0:
        return f'`A[{l}] = 0` → 继续右移'
    return f'`A[{l}] = 1`：新的左边界 `l = {l}`'


def _cap_res(E, B, ret):
    a, b = E.l - E.last_pos, E.next_pos - E.r
    return f'`({E.l} − ({E.last_pos})) × ({E.next_pos} − {E.r}) = {a} × {b} = {a * b}` → `res = {E.res}`'


CONFIG = dict(
    num=930, title='和相同的二元子数组', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='窗口跳 1：前缀 0 × 后缀 0 计数',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numSubarraysWithSum(self, A, S):
        res = 0

        if S == 0:
            start_pos = None
            for index, num in enumerate(A):
                if num == 1:
                    if start_pos is None:
                        continue
                    l = index - start_pos
                    res += l * (l + 1) // 2
                    start_pos = None
                else:
                    if start_pos is None:
                        start_pos = index

            if start_pos is not None:
                l = len(A) - start_pos
                res += l * (l + 1) // 2
            return res

        last_pos = -1
        l = 0
        while l < len(A) and A[l] != 1:
            l += 1
        if l == len(A):
            return 0

        r = l
        now = 1
        while r + 1 < len(A) and now < S:
            r += 1
            now += A[r]

        if now < S:
            return 0

        next_pos = r + 1
        while next_pos < len(A) and A[next_pos] == 0:
            next_pos += 1

        res = (l - last_pos) * (next_pos - r)
        while next_pos < len(A):
            last_pos = l
            l += 1
            while l < len(A) and A[l] == 0:
                l += 1

            r = next_pos
            next_pos += 1
            while next_pos < len(A) and A[next_pos] == 0:
                next_pos += 1

            res += (l - last_pos) * (next_pos - r)

        return res
''',
    call=f'Solution().numSubarraysWithSum({A_}, {S_})',
    expect=8,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='A', label='A（绿 = 窗口两端的 1，青 = 可选的前缀 0，紫 = 可选的后缀 0）', cell=110,
             pointers={'last_pos': 'cyan', 'l': 'green', 'r': 'pink', 'next_pos': 'orange'},
             window=('l', 'r'), color=_color, h=330),
    ],
    watch=[('last_pos', 'last_pos', 'cyan'), ('l', 'l', 'green'), ('r', 'r', 'pink'), ('next_pos', 'next_pos', 'orange'),
           ('now', 'now'), ('res', 'res', 'yellow')],
    skip=[51],
    captions={
        'res = 0': '`res` 统计答案',
        'if S == 0': '`S = {S} > 0`，走一般情况（`S = 0` 的特殊情况见后面卡片）',
        'last_pos = -1': '`last_pos`：==上一个窗口左端 1== 的位置，开始时是 `-1`',
        24: '`l` 去找第一个 1',
        25: _cap_find_l,
        26: '`l` → {l}',
        'if l == len(A)': 'A 中有 1，继续',
        'r = l': '`r` 从 `l` 出发，往右凑够 S 个 1',
        'now = 1': '`now`：窗口里 1 的个数',
        32: _cap_grow,
        'r += 1': '`r` → {r}',
        'now += A[r]': '`A[{r}] = {A[r]}` → `now = {now}`',
        'if now < S': '1 的总数够 `S` 个',
        'next_pos = r + 1': '`next_pos`：从 `r + 1` 开始找下一个 1',
        40: _cap_next,
        41: '`next_pos` → {next_pos}',
        43: _cap_res,
        44: _cap_slide,
        'last_pos = l': '记下旧的左端：`last_pos = {last_pos}`',
        46: '`l` 右移',
        47: _cap_l0,
        48: '`l` → {l}',
        'r = next_pos': '右边界跳到下一个 1：`r = {r}`',
        52: _cap_next,
        53: '`next_pos` → {next_pos}',
        55: _cap_res,
        'return res': '一共 =={ret}== 个子数组',
    },
    cards=dict(
        one_liner='恰好含 S 个 1 的窗口，前缀 0 和后缀 0 的选法相乘',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二元数组 `A`（只有 0 和 1），统计和为 `S` 的==非空子数组==个数',
                 '示例：`A = [1,0,1,0,1]`，`S = 2` → `4`',
                 '演示：`A = [0,1,0,0,1,1,0]`，`S = 2` → `8`'],
        quote='合法答案必然是形如 ==00...000 1 XX...XXX 1 00.000== 的子数组……前缀和后缀分别有l和r个0……因此一共可以产生 ==(l + 1) * (r + 1)== 种合法的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`1 XX…X 1` 这段必须要；前缀 0 可取 `0～l` 个，后缀 0 可取 `0～r` 个',
              '滑动窗口：右边界跳到 `r` 右侧下一个 1，左边界也跳到下一个 1',
              '左边界滑动的距离 = 前缀选法数，右边界滑动的距离 = 后缀选法数'],
        after=[dict(heading='特殊情况：S = 0', lines=[
            '子数组里不能有 1：只能取在==连续的 0== 里面',
            '一段长为 `l` 的全 0 区间，能产生 `l * (l + 1) / 2` 个子数组',
            '从头扫一遍找出所有连续 0 段，累加即可（代码前半部分）',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`last_pos` 初始为 `-1`：第一个窗口的前缀 0 从下标 0 开始数',
                 '1 的总数不足 `S` 时直接返回 0',
                 '原文为 Python 2 写法，`l * (l + 1) / 2` 已改为 `//`，并删去类型说明文档字符串',
                 '对比灵神：灵神用「≥ goal 减 > goal」两个计数滑窗，S = 0 也不用特判'],
    ),
)
