def _digits(x, k):
    d = []
    while x:
        d.append(x % k)
        x //= k
    return ''.join(map(str, d[::-1])) or '0'


def _t_x(S):
    I = S.get('_inner', {})
    if 'rev' in I:
        x0 = S.get('x', I['x'])
        return f"`x = {x0}` 的 {I['k']} 进制是 `{_digits(x0, I['k'])}`：边除边把低位倒进 `rev`，和剩下的高位比较"
    if 'x' in I and 'k' in I:
        return f"十进制回文数 `{I['x']}`，检查它的 `{I['k']}` 进制 `{_digits(I['x'], I['k'])}` 是不是回文"
    if 'x' in S:
        return f"当前十进制回文数 `x = {S['x']}`"
    return '枚举回文数左半边 → 拼成十进制回文数 → 检查 2~9 进制'



MAXN = 2


def _isk(x, k):
    t = []
    y = x
    while y:
        t.append(y % k)
        y //= k
    return t == t[::-1]


def _pals(limit, include):
    out = []
    base = 1
    while True:
        for i in range(base, base * 10):
            si = str(i)
            out.append(int(si + si[::-1][1:]))
        for i in range(base, base * 10):
            si = str(i)
            out.append(int(si + si[::-1]))
        base *= 10
        if out[-1] > limit + 1000:
            break
    return [v for v in out if v < limit or (include and v == limit)]


def _state(S, kk):
    """ans[kk] as the video has built it so far (reconstructed from the visible variables)"""
    if 'x' not in S:
        return []
    line = S['_line']
    x = S['x']
    in_do = 'done' in S
    if line >= 24:
        pass
    k_cur = S.get('k', 0)
    if in_do:
        full = False
        upto = x
        cur_done = kk < k_cur or (kk == k_cur and line >= 18)
        lst = [v for v in _pals(upto, False) if _isk(v, kk)]
        if cur_done and _isk(x, kk):
            lst.append(x)
    else:
        lst = [v for v in _pals(x, line <= 32 or line > 34) if _isk(v, kk)]
    lst = lst[:MAXN]
    return lst


def _row(kk):
    def fn(S):
        if S['_line'] >= 44 or ('x' not in S and 'n' in S):
            a = [v for v in _pals(10**4, False) if _isk(v, kk)][:MAXN]
            tot = [sum(a[:j + 1]) for j in range(len(a))]
            return f'`ans[{kk}]`（{kk} 进制）= `{tot}` 前缀和'
        a = _state(S, kk)
        mark = ' ==凑满==' if len(a) >= MAXN else ''
        return f'`ans[{kk}]`（{kk} 进制）= `{a}`{mark}'
    return fn


CONFIG = dict(
    num=2081, title='k 镜像数字的和', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举回文数左半边 + 预处理',
    tags=['灵神题单·数学算法', '难度分 2210'],
    code='''
MAX_N = 2
ans = [[] for _ in range(10)]

# 力扣 9. 回文数
def is_k_palindrome(x: int, k: int) -> bool:
    if x % k == 0:
        return False
    rev = 0
    while rev < x // k:
        rev = rev * k + x % k
        x //= k
    return rev == x or rev == x // k

def do_palindrome(x: int) -> bool:
    done = True
    for k in range(2, 10):
        if len(ans[k]) < MAX_N and is_k_palindrome(x, k):
            ans[k].append(x)
        if len(ans[k]) < MAX_N:
            done = False
    if not done:
        return False
    for k in range(2, 10):
        ans[k] = list(accumulate(ans[k]))
    return True

def init() -> None:
    base = 1
    while True:
        # 生成奇数长度回文数，例如 base = 10，生成的范围是 101 ~ 999
        for i in range(base, base * 10):
            s = str(i)
            x = int(s + s[::-1][1:])
            if do_palindrome(x):
                return
        # 生成偶数长度回文数，例如 base = 10，生成的范围是 1001 ~ 9999
        for i in range(base, base * 10):
            s = str(i)
            x = int(s + s[::-1])
            if do_palindrome(x):
                return
        base *= 10

class Solution:
    def kMirror(self, k: int, n: int) -> int:
        return ans[k][n - 1]
''',
    call='init()\nSolution().kMirror(3, 2)',
    expect=3,
    views=[
        dict(type='text', fn=_t_x, size=28, h=90),
        *[dict(type='text', fn=_row(kk), size=26, h=48) for kk in range(2, 10)],
    ],
    watch=['base', 'i', 'x', 'k', 'done'],
    skip=['done = True', 'done = False', 's = str(i)', 'rev = 0', 'for k in range', 'base = 1', 'while True', 'return False', 'if len(ans[k]) < MAX_N:', 35],
    max_steps=40,
    captions={
        'x = int(s + s[::-1][1:])': '奇数长度：左半边 `{s}` 去掉末位后反转拼上去 → 回文数 `x = {x}`',
        'x = int(s + s[::-1])': '偶数长度：整个左半边反转拼上去 → 回文数 `x = {x}`',
        'if do_palindrome': '把这个十进制回文数交给 `do_palindrome`，看它在 2~9 进制里是不是回文',
        'if len(ans[k]) < MAX_N and': '只有 `ans[{k}]` 还没凑满 `MAX_N` 个，才需要检查 `{x}` 在 {k} 进制下是否回文',
        'if x % k == 0': '`{x} % {k} = {x % k}`：{"k 进制末位是 0，反过来就有前导 0 → 不可能是回文" if x % k == 0 else "末位不是 0，继续检查"}',
        'while rev < x // k': '`rev = {rev}` vs 高位 `x // k = {x // k}`：{"`rev` 还没超过高位，继续倒" if rev < x // k else "`rev` 已不小于高位，反转到一半了，停"}（只反转后半段）',
        'rev = rev * k': '把 `x` 的末位倒进 `rev`：`rev = {rev}`',
        'return rev == x': '`rev = {rev}`，剩下的高位 `x = {x}`：`rev == x`（偶数位）或 `rev == x // k`（奇数位，丢掉中间位）→ 回文？=={ret}==',
        'ans[k].append(x)': '`{x}` 在 {k} 进制也是回文 → 记入 `ans[{k}]`',
                'if not done': '`done = {done}`：{"还有某个进制没凑满，继续生成下一个回文数" if not done else "所有 k 都凑满了 → 进入前缀和"}',
        'ans[k] = list(accumulate': '`ans[{k}]` 变成前缀和，`ans[k][n-1]` 就是前 n 小之和',
        'return True': '所有进制都凑满，预处理结束',
        'return ans[k][n - 1]': '查表：前 `{n}` 个 {k} 镜像数字之和 `ans[{k}][{n}-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='把十进制回文数一个个造出来，逐个检查 k 进制',
        complexity='预处理后查表 `O(1)`',
        problem=['十进制和 k 进制都是回文的正整数叫 k 镜像数字', '求最小的 n 个 k 镜像数字之和', '示例：`k=3, n=7` → `499`'],
        quote='枚举回文数的左半边。……将除了末尾数位的其余部分反转，拼到原数字末尾，这样可以生成奇数长度回文数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数据范围小：`k` 在 2~9，`n` ≤ 30，直接打表', '回文数由左半边决定，从小到大枚举 `base`、奇偶长度各一次', '每个回文数检查 2~9 进制，凑满 30 个就停，再做前缀和'],
        summary=['原题 `MAX_N = 20`；视频里为了演示改成 `MAX_N = 2`，示例 `kMirror(3, 2) = 7`', '引擎里 `init()` 放到了调用里一起演示（题解是模块加载时执行）', '`x % k == 0` 直接排除（末位 0 说明有前导零问题）', '最后一个回文数 `64454545446` 超过 32 位整数'],
    ),
)
