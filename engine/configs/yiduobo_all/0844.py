S0, T0 = 'axb##c', 'ad#c'


def _states(s, p):
    """从后往前扫描，下标 > p 的字符各是什么命运：'hash' 退格、'del' 被删、'keep' 保留并已比较"""
    res, cnt = {}, 0
    for idx in range(len(s) - 1, p, -1):
        if s[idx] == '#':
            cnt += 1
            res[idx] = 'hash'
        elif cnt > 0:
            cnt -= 1
            res[idx] = 'del'
        else:
            res[idx] = 'keep'
    return res


def _col(sv, pv, cur):
    def f(S, k, v):
        if sv not in S or pv not in S:
            return None
        p = S[pv]
        if k == p:
            return cur
        return {'hash': 'orange', 'keep': 'green'}.get(_states(S[sv], p).get(k))
    return f


def _dim(sv, pv):
    def f(S, k, v):
        if sv not in S or pv not in S:
            return False
        return _states(S[sv], S[pv]).get(k) == 'del'
    return f


def _text(S):
    if 'cnt_s' not in S:
        return '两个字符串都==从后往前==扫，`#` 是退格'
    ln = S['_line']
    if ln <= 5:
        return '`i`、`j` 分别指向两个串的末尾；`cnt` 记录还欠着几个退格'
    if ln <= 14:
        return f"S 这边：找下一个==不会被删掉==的字符（欠着 `{S['cnt_s']}` 个退格）"
    if ln <= 22:
        return f"T 这边：找下一个==不会被删掉==的字符（欠着 `{S['cnt_t']}` 个退格）"
    return '两边各找到一个有效字符：比较它们'


def _cap_hash(sv, iv, cv_):
    def f(S, B, r):
        i = S[iv]
        c = S[sv][i]
        if c == '#':
            return f'`{sv}[{i}] = "#"`：退格，它会删掉前面的一个字符'
        return f'`{sv}[{i}] = "{c}"`：普通字符，要看前面是不是欠着退格'
    return f


def _cap_cnt(sv, iv, cv_):
    def f(S, B, r):
        i, n = S[iv], S[cv_]
        c = S[sv][i]
        if n == 0:
            return f'`{cv_} = 0`：没有退格欠着 → `"{c}"` ==会留下==，停在这里去比较'
        return f'`{cv_} = {n} > 0`：还欠着退格 → `"{c}"` 要被删掉'
    return f


def _cap_while(sv, iv):
    def f(S, B, r):
        i = S[iv]
        if i >= 0:
            return f'`{iv} = {i} >= 0`：{sv} 还没扫完，继续往前找'
        return f'`{iv} = {i} < 0`：{sv} 已经扫到头了'
    return f


def _cap_main(S, B, r):
    i, j = S.i, S.j
    if i >= 0 or j >= 0:
        return f'`i = {i}`、`j = {j}` 至少有一个 >= 0：还有字符没处理 → 继续'
    return '`i`、`j` 都扫到头了：两个串的有效字符全部对上 → 循环结束'


def _cap_cmp(S, B, r):
    a, b = S.S[S.i], S.T[S.j]
    if a != b:
        return f'`S[{S.i}] = "{a}"` ≠ `T[{S.j}] = "{b}"`：最终字符串在这一位不同 → ==返回 False=='
    return f'`S[{S.i}] = T[{S.j}] = "{a}"`：这一位相同 ✓ 两边各往前一格'


CONFIG = dict(
    num=844, title='比较含退格的字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='从后往前双指针 · 累计退格',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def backspaceCompare(self, S, T):
        i = len(S) - 1
        j = len(T) - 1
        cnt_s = cnt_t = 0
        while i >= 0 or j >= 0:
            while i >= 0:
                if S[i] == '#':
                    cnt_s += 1
                elif cnt_s == 0:
                    break
                else:
                    cnt_s -= 1
                i -= 1
            while j >= 0:
                if T[j] == '#':
                    cnt_t += 1
                elif cnt_t == 0:
                    break
                else:
                    cnt_t -= 1
                j -= 1
            if i < 0:
                if j < 0:
                    return True
                else:
                    return False
            elif j < 0:
                return False
            elif S[i] != T[j]:
                return False
            else:
                i -= 1
                j -= 1

        return True
''',
    call=f'Solution().backspaceCompare({S0!r}, {T0!r})',
    expect=True,
    views=[
        dict(type='text', fn=_text, size=26, h=60),
        dict(type='string', var='S', label='S（蓝 = i，橙 = 退格，暗 = 被删掉，绿 = 已比较过）', cell=90,
             pointers={'i if i >= 0 else None': 'blue'}, pointer_labels={'i if i >= 0 else None': 'i'},
             color=_col('S', 'i', 'blue'), dim=_dim('S', 'i'), h=200),
        dict(type='string', var='T', label='T（粉 = j）', cell=90,
             pointers={'j if j >= 0 else None': 'pink'}, pointer_labels={'j if j >= 0 else None': 'j'},
             color=_col('T', 'j', 'pink'), dim=_dim('T', 'j'), h=200),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cnt_s', 'cnt_s', 'orange'), ('cnt_t', 'cnt_t', 'orange')],
    captions={
        'i = len(S) - 1': '`i = {i}`：指向 S 的最后一个字符，==从后往前==扫',
        'j = len(T) - 1': '`j = {j}`：指向 T 的最后一个字符',
        'cnt_s = cnt_t = 0': '`cnt_s`、`cnt_t`：S、T 当前累计的退格数，还没有被抵消',
        'while i >= 0 or j >= 0': _cap_main,
        'while i >= 0:': _cap_while('S', 'i'),
        "if S[i] == '#'": _cap_hash('S', 'i', 'cnt_s'),
        'cnt_s += 1': '退格累计：`cnt_s` → {cnt_s}，前面还要删 `{cnt_s}` 个字符',
        'elif cnt_s == 0': _cap_cnt('S', 'i', 'cnt_s'),
        'cnt_s -= 1': '这个字符被退格删掉：`cnt_s` → {cnt_s}',
        'while j >= 0:': _cap_while('T', 'j'),
        "if T[j] == '#'": _cap_hash('T', 'j', 'cnt_t'),
        'cnt_t += 1': '退格累计：`cnt_t` → {cnt_t}，前面还要删 `{cnt_t}` 个字符',
        'elif cnt_t == 0': _cap_cnt('T', 'j', 'cnt_t'),
        'cnt_t -= 1': '这个字符被退格删掉：`cnt_t` → {cnt_t}',
        11: '`i = {i}`：S 停在这个==保留下来==的字符 `S[i]`，它就是 S 最终文本里的下一个字符',
        19: '`j = {j}`：T 停在这个保留下来的字符 `T[j]`，它就是 T 最终文本里的下一个字符',
        14: '`i` 往前走一格 → {i}',
        22: '`j` 往前走一格 → {j}',
        23: lambda S, B, r: ('S 已经没有有效字符了（`i < 0`）' if S.i < 0 else f'`i = {S.i} >= 0`：S 还有有效字符，接着看 T'),
        24: '`i < 0`：S 扫完了，看 T：`j = {j}`，T 也扫完了吗？',
        25: 'S、T 同时扫完，每一位有效字符都相同 → `True`',
        27: 'S 扫完了但 T 还有有效字符 → 最终长度不同 → `False`',
        28: lambda S, B, r: (f'`j = {S.j} < 0`：T 扫完了，但 S 还有有效字符 `S[{S.i}]`' if S.j < 0
                             else f'`j = {S.j}`：T 也还有有效字符，两边都能比较'),
        29: 'T 扫完了但 S 还有有效字符 → 最终长度不同 → `False`',
        36: '循环结束没有发现不同的位置 → 最终文本相同，返回 `True`',
        'elif S[i] != T[j]': _cap_cmp,
        33: '两个有效字符相同：`i` → {i}',
        34: '`j` → {j}，继续比较前面的字符',
    },
    cards=dict(
        one_liner='从后往前扫：遇到退格就累计，遇到字符先抵消，剩下的才是有效字符',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['`S` 和 `T` 是两个含 `#` 的字符串，`#` 代表退格键，对空文本退格仍为空',
                 '判断两个字符串敲进空文本编辑器后，得到的最终文本是否相等',
                 '示例：`"ab#c"` 和 `"ad#c"` 都变成 `"ac"` → `true`',
                 '本视频：`"axb##c"` 和 `"ad#c"` → `true`'],
        quote='乍一看感觉可以从前往后扫描，用栈来解决。但是可以转换思路，如果从后往前来看，将每个碰到的退格键累计起来……',
        quote_src='—— yiduobo 题解原文',
        idea=['退格只影响它==前面==的字符，所以从后往前扫，遇到 `#` 就知道要删几个',
              '碰到正常字符：`cnt > 0` 就跳过并 `cnt -= 1`；`cnt == 0` 才是有效字符',
              '两个串各找到一个有效字符后比较；不同直接 `False`，相同一起前进'],
        summary=['时间 `O(n+m)`，空间 `O(1)`：不需要栈，也不需要重建字符串',
                 '易错：一个串先扫完时（`i < 0` 或 `j < 0`），要看另一个串是否也同时扫完',
                 '易错：外层 `while i >= 0 or j >= 0`，用 `or`，因为两边可能以 `#` 结尾而长度不同',
                 '原文在 Python 3 下可直接运行，代码未做修改',
                 '另一种写法：用栈分别还原两个字符串再比较，空间 `O(n)`'],
    ),
)
