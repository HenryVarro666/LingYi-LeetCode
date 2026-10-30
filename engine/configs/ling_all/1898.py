def _chk(S):
    return 'del_' in S and S.get('_line') is not None and 'j' in S


def _del_set(S):
    if 'del_' in S:
        return {i for i, d in enumerate(S['del_']) if d}
    return set()


def _top(S):
    if 'lo' not in S:
        return ''
    lo, hi = S['lo'], S['hi']
    if lo >= hi:
        return f'二分结束：`lo = hi = {lo}` → 第一个删了就失败的 k 是 `{lo}`，最多可删 ==`{lo}`== 个'
    if 'k' in S and 'del_' in S:
        return f'二分区间 `[{lo}, {hi})`，检查 `k = {S["k"]}`：删前 `{S["k"] + 1}` 个下标后 p 还是子序列吗？'
    return f'二分区间 `[{lo}, {hi})`：==返回 True 表示删多了，p 不再是子序列=='


def _scol(S, i, v):
    d = _del_set(S)
    if i in d:
        return 'red'
    if 'j' in S and 'i' in S and S.get('_line') is not None and 'del_' in S:
        if i == S['i']:
            return 'blue'
    return None


def _idcol(S, i, v):
    if 'k' in S and 'del_' in S and i <= S['k']:
        return 'red'
    return None


CONFIG = dict(
    num=1898, title='可移除字符的最大数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='二分答案 + 判断子序列（Go 原文转写）',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·二分算法', '难度分 1913'],
    code='''
class Solution:
    def maximumRemovals(self, s: str, p: str, id: List[int]) -> int:
        def check(k: int) -> bool:
            del_ = [False] * len(s)
            for i in id[:k + 1]:
                del_[i] = True
            j = 0
            for i in range(len(s)):
                if not del_[i] and s[i] == p[j]:
                    j += 1
                    if j == len(p):
                        return False
            return True

        # sort.Search(len(id), check)：找最小的 k，使 check(k) 为 True
        lo, hi = 0, len(id)
        while lo < hi:
            h = (lo + hi) >> 1
            if not check(h):
                lo = h + 1
            else:
                hi = h
        return lo
''',
    call='Solution().maximumRemovals("abcacb", "ab", [3, 1, 0])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（红 = 被删除，蓝 = 当前扫描的 i）', cell=84, pointers={'i': 'blue'},
             color=_scol, dim=lambda S, i, v: i in _del_set(S)),
        dict(type='string', var='p', label='p（j 指向下一个要匹配的字符）', cell=84, pointers={'j': 'pink'},
             color=lambda S, i, v: 'green' if 'j' in S and 'del_' in S and i < S['j'] else None),
        dict(type='array', var='id', label='removable（红 = 本次检查要删的前 k+1 个）', cell=84,
             color=_idcol),
    ],
    watch=[('lo', 'lo', 'blue'), ('hi', 'hi', 'pink'), ('k', 'k', 'yellow'), ('i', 'i'), ('j', 'j', 'green')],
    skip=['del_ = [False]', 'del_[i] = True'],
    captions={
        'lo, hi = 0, len(id)': '二分答案：最多删 `{hi}` 个，区间 `[{lo}, {hi})`，==sort.Search 的写法==',
        'while lo < hi': lambda S, B, r: (f'`lo = {S.lo} < hi = {S.hi}`，区间还没缩完' if S.lo < S.hi
                                          else f'`lo = hi = {S.lo}`：区间缩成一点 → 答案就是它'),
        'h = (lo + hi) >> 1': '取中点 `h = {h}`，检查删掉前 `{h + 1}` 个下标后 p 还是不是子序列',
        'for i in id[:k + 1]': lambda S, B, r: (f'`removable` 的前 `{S.k + 1}` 个下标都标记完了：`{S.id[:S.k + 1]}`'
                                                if 'i' in B and B.i == S.i else f'标记下标 `{S.i}` 为已删除（`del_[{S.i}] = True`）'),
        'j = 0': '`j` 指向 p 中下一个要匹配的字符；用「跳过已删位置」代替真的改 s',
        'for i in range(len(s))': lambda S, B, r: ('s 扫完了' if 'i' in B and B.i == S.i and S.i == len(S.s) - 1
                                                   else f'双序列双指针：枚举 `s[{S.i}] = {S.s[S.i]!r}`'),
        'if not del_[i]': lambda S, B, r: (
            f'`s[{S.i}]` 已被删除 → 跳过' if S.del_[S.i]
            else (f'`s[{S.i}] = {S.s[S.i]!r}` == `p[{S.j}] = {S.p[S.j]!r}` → ==匹配上了==' if S.s[S.i] == S.p[S.j]
                  else f'`s[{S.i}] = {S.s[S.i]!r}` ≠ `p[{S.j}] = {S.p[S.j]!r}` → 不匹配，继续往后找')),
        'j += 1': '`j` → `{j}`，去匹配 p 的下一个字符',
        'if j == len(p)': lambda S, B, r: (f'`j == len(p) = {S.j}`：p 全部匹配完 → 删了这些 p 还是子序列'
                                           if S.j == len(S.p) else f'`j = {S.j} < {len(S.p)}`，p 还没匹配完'),
        'return False': '删了前 `{k + 1}` 个后 p 仍是子序列 → ==还能再多删==，`check({k})` 为 False',
        'return True': '扫完 s，p 没匹配完 → 删了前 `{k + 1}` 个就==太多了==，`check({k})` 为 True',
        'if not check(h)': '调用 `check({h})`：删掉前 `{h + 1}` 个下标，p 还是 s 的子序列吗？',
        'lo = h + 1': '删 `{h + 1}` 个还行，答案 ≥ `{h + 1}`，`lo` → {lo}',
        'hi = h': '删 `{h + 1}` 个不行，答案 ≤ `{h}`，`hi` → {hi}',
        'return lo': '第一个「删了就不行」的 k 是 `{lo}`，所以最多删 `{lo}` 个 → ==返回 {lo}==',
    },
    cards=dict(
        one_liner='二分「删前 k 个」，扫一遍 s 判断 p 还是不是子序列',
        complexity='时间 `O(n log m)`，空间 `O(n)`',
        problem=['`p` 是 `s` 的子序列；按 `removable` 的顺序，删掉前 `k` 个下标上的字符',
                 '求最大的 `k`，使删完后 `p` 仍是 `s` 的子序列',
                 '示例：`s = "abcacb"`，`p = "ab"`，`removable = [3,1,0]` → `2`'],
        quote='sort.Search(len(id), func(k int) bool { ... }) —— 删除前 k+1 个下标后，p 不再是 s 的子序列则返回 true。',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['删得越多，p 越难匹配：==有单调性==，可以二分答案 `k`',
              '`sort.Search` 找的是第一个 `check(k)` 为 true（删 k+1 个就失败）的 `k`，它恰好等于最多能删的个数',
              '`check` 里不真的改 s：用 `del_` 标记删除位置，双指针扫 s 去匹配 p'],
        result='`k = 0, 1` 时 p 仍是子序列，`k = 2` 时不是 → 最多删 `2` 个 ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Search` 展开成等价的二分循环）',
                 '时间 `O(n log m)`，空间 `O(n)`，`n = len(s)`，`m = len(removable)`',
                 '`check(k)` 删的是前 `k+1` 个，所以答案就是 `sort.Search` 返回的 `k`，不用再加一',
                 '全删光也能匹配时 `sort.Search` 返回 `len(id)`',
                 '同类题：392 判断子序列（本题的 check）'],
    ),
)
