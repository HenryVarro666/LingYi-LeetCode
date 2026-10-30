S_IN = 'abcabc'


def _st(S):
    # 第 31–32 行时 r 已是“起点 l+1”的最小右边界
    if 'l' not in S or 'r' not in S:
        return None
    return S['l'] + 1 if S.get('_line') in (31, 32) else S['l']


def _idx(S):
    return None if 'l' in S else S.get('index')


def _top(S):
    if 'l' not in S:
        if 'index' in S:
            return '从后往前扫：`next_pos` 记下每个位置==下一个同字母==的下标'
        return '对每个起点 l，找最小右边界 r：以 l 开头的合法子串有 `n − r` 个'
    if 'r' not in S:
        return '起点 `l = 0`'
    l, r, n = _st(S), S['r'], S['n']
    if l < n:
        return f"起点 `{l}` 的最小右边界 `r = {r}`：`s[{l}..{r}..{n - 1}]` 都合法 → `n − r = {n - r}` 个"
    return '所有起点处理完毕'


def _color(S, i, v):
    if 'l' in S and S['l'] < S['n'] and i >= S['r'] and S.get('_line') in (27, 32):
        return 'green'
    return None


def _nxt(S, B, ret):
    l = S.l
    if S.next_pos[l] is None:
        return f'`s[{l}] = {S.s[l]!r}` 后面再也没有 {S.s[l]!r} → 起点再右移就凑不齐三种，==结束=='
    return f'`s[{l}] = {S.s[l]!r}` 要移出窗口，它的下一次出现在 `{S.next_pos[l]}`'


CONFIG = dict(
    num=1358, title='包含所有三种字符的子字符串数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左端点 · 预处理下一次出现位置',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1646'],
    code='''
class Solution(object):
    def numberOfSubstrings(self, s):

        last_a = None
        last_b = None
        last_c = None
        next_pos = []
        n = len(s)
        for index in range(n - 1, -1, -1):
            if s[index] == 'a':
                next_pos.append(last_a)
                last_a = index
            elif s[index] == 'b':
                next_pos.append(last_b)
                last_b = index
            else:
                next_pos.append(last_c)
                last_c = index
        
        next_pos.reverse()

        if last_a is None or last_b is None or last_c is None:
            return 0
        
        l = 0
        r = max(last_a, last_b, last_c)
        res = n - r
        while l < n:
            if next_pos[l] is None:
                break
            r = max(r, next_pos[l])
            res += n - r
            l += 1

        return res
''',
    call=f'Solution().numberOfSubstrings({S_IN!r})',
    expect=10,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = [起点, r]，绿 = 合法右端点 r..n−1）',
             pointers={_idx: 'orange', _st: 'blue', 'r': 'pink'}, pointer_labels={_idx: 'index', _st: '起点'}, window=(_st, 'r'), color=_color, cell=110, h=290),
        dict(type='array', var='next_pos', label='next_pos（下一个同字母的位置，• = 没有；倒序构造，最后翻转）',
             fmt=lambda x: '–' if x is None else str(x), cell=110, h=200,
             pointers={'l': 'blue'}, pointer_labels={'l': 'l'}),
    ],
    watch=[('last_a', 'last_a', 'cyan'), ('last_b', 'last_b', 'cyan'), ('last_c', 'last_c', 'cyan'),
           ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    skip=['last_b = None', 'last_c = None', 'next_pos = []'],
    captions={
        'last_a = None': '`last_a/b/c`：从后往前扫时，三种字母==最近一次==出现的位置',
        'n = len(s)': '`n = {n}`',
        'for index in range': lambda S, B, r: ('预处理结束' if 'index' in B and B.index == 0 else f'倒着看 `s[{S.index}] = {S.s[S.index]!r}`'),
        "if s[index] == 'a'": lambda S, B, r: f"`s[{S.index}]` {'是' if S.s[S.index] == 'a' else '不是'} 'a'",
        "elif s[index] == 'b'": lambda S, B, r: f"`s[{S.index}]` {'是' if S.s[S.index] == 'b' else '不是'} 'b'",
        'next_pos.append(last_a)': lambda S, B, r: ('它后面==没有== a 了 → 记 None' if S.last_a is None else f'它后面下一个 a 在 `{S.last_a}` → 记入 next_pos'),
        'next_pos.append(last_b)': lambda S, B, r: ('它后面==没有== b 了 → 记 None' if S.last_b is None else f'它后面下一个 b 在 `{S.last_b}` → 记入 next_pos'),
        'next_pos.append(last_c)': lambda S, B, r: ('它后面==没有== c 了 → 记 None' if S.last_c is None else f'它后面下一个 c 在 `{S.last_c}` → 记入 next_pos'),
        'last_a = index': '`last_a` 更新为 {last_a}',
        'last_b = index': '`last_b` 更新为 {last_b}',
        'last_c = index': '`last_c` 更新为 {last_c}',
        'next_pos.reverse()': '倒序追加的，翻转后 `next_pos[i]` 就对应位置 i',
        'if last_a is None': '三种字母都出现过，否则直接返回 0',
        'l = 0': '起点 `l = 0`',
        'r = max(last_a': '此时 `last_*` 是每种字母==第一次==出现的位置 → 最小右边界 `r = max = {r}`',
        'res = n - r': '以 0 开头、右端点在 `{r}..{n - 1}` 的都合法：`res = {n} − {r}` = =={res}==',
        'while l < n': lambda S, B, r: ('`l < n`，继续' if S.l < S.n else '起点枚举完'),
        'if next_pos[l] is None': _nxt,
        'r = max(r, next_pos[l])': lambda S, B, ret: (f'下一个 {S.s[S.l]!r} 在 `{S.next_pos[S.l]}` > `r` → 右边界推到 =={S.r}=='
                                                     if S.r != B.r else f'下一个 {S.s[S.l]!r} 在 `{S.next_pos[S.l]}` ≤ `r = {S.r}`：窗口里仍有三种，==r 不动=='),
        'res += n - r': '以 `{l + 1}` 开头的合法子串有 `{n} − {r} = {n - r}` 个 → `res` = =={res}==',
        'l += 1': '起点右移 → `l = {l}`',
        'break': '跳出循环',
        'return res': '一共 =={ret}== 个',
    },
    max_steps=75,
    cards=dict(
        one_liner='枚举起点，找最小右边界 r：以它开头的合法串有 n − r 个',
        complexity='时间 `O(n)`，空间 `O(n)`（next_pos）',
        problem=['字符串 `s` 只含 a、b、c',
                 '求 ==a、b、c 都至少出现一次== 的子串个数',
                 '示例：`"abcabc"` → `10`；`"aaacb"` → `3`'],
        quote='对于起点为l的字符串，我们找出其满足条件的最小右边界r，那么以l开头，符合条件的字符串就一共有n - r个。',
        quote_src='—— yiduobo 题解原文',
        idea=['起点右移时 `s[l]` 离开窗口，只需看下一个 `s[l]` 在哪',
              '下一个位置 `next ≤ r`：仍有三种，r 不动；否则 ==r 推到 next==',
              '先==从后往前==扫一趟，预处理每个位置的 next'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '枚举的是==左端点==，所以加 `n − r`；灵神枚举右端点，加 `left`',
                 '`next_pos[l]` 为 None 时，后面的起点都凑不齐，直接结束',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
