def _rm(S):
    return S.get('remove_set') or set()


def _top(S):
    if 'l' not in S:
        return ''
    l, r = S['l'], S['r']
    if l >= r:
        return f'二分结束：`l = r = {r}` → 最多能移除 ==`{r}`== 个'
    if 'mid' in S:
        return f'答案范围 `[{l}, {r}]`，试 `mid = {S["mid"]}`：移除前 `{S["mid"]}` 个下标，p 还是子序列吗？'
    return f'答案范围 `[{l}, {r}]`：移除个数越少越容易成立（==单调==）'


def _scol(S, i, v):
    if i in _rm(S):
        return 'red'
    if 'pos' in S and 'index' in S and i == S['index'] and 'char' in S:
        return 'blue'
    return None


CONFIG = dict(
    num=1898, title='可移除字符的最大数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='二分答案 · 记录不可用位置',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·二分算法', '难度分 1913'],
    code='''
class Solution(object):
    def maximumRemovals(self, s, p, removable):

        l = 0
        r = len(removable)
        while l < r:
            mid = (l + r + 1) >> 1
            remove_set = set()
            for index in range(mid):
                remove_set.add(removable[index])
            
            pos = 0
            for index, char in enumerate(s):
                if index not in remove_set and char == p[pos]:
                    pos += 1
                    if pos == len(p):
                        break
            
            if pos == len(p):
                l = mid
            else:
                r = mid - 1

        return r
''',
    call='Solution().maximumRemovals("abcacb", "ab", [3, 1, 0])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（红 = 被移除的位置，蓝 = 正在匹配的 index）', cell=84,
             pointers={'index': 'blue'}, color=_scol, dim=lambda S, i, v: i in _rm(S)),
        dict(type='string', var='p', label='p（pos 指向下一个要匹配的字符）', cell=84, pointers={'pos': 'pink'},
             color=lambda S, i, v: 'green' if 'pos' in S and 'char' in S and i < S['pos'] else None),
        dict(type='array', var='removable', label='removable（红 = 本轮要移除的前 mid 个）', cell=84,
             color=lambda S, i, v: 'red' if 'mid' in S and i < S['mid'] else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('pos', 'pos', 'green')],
    skip=['remove_set = set()', 'remove_set.add'],
    captions={
        'l = 0': '`l` 是答案的下界：什么都不移除一定成立',
        'r = len': '`r = {r}` 是答案的上界：最多把 `removable` 全移除',
        'while l < r': lambda S, B, rt: (f'`l = {S.l} < r = {S.r}`，答案还没确定' if S.l < S.r
                                         else f'`l = r = {S.r}`：范围缩成一个数 → 就是答案'),
        'mid = (l + r + 1)': '取 ==上中位数== `mid = (l + r + 1) >> 1 = {mid}`（因为下面是 `l = mid`，不加 1 会死循环）',
        'for index in range(mid)': lambda S, B, rt: (f'前 `{S.mid}` 个下标都放进 `remove_set` 了：`{sorted(S.remove_set)}`'
                                                     if 'index' in B and B.get('index') == S.index and S.index == S.mid - 1
                                                     else f'把 `removable[{S.index}] = {S.removable[S.index]}` 放进 `remove_set`'),
        'remove_set.add': '`remove_set` = `{sorted(remove_set)}`：匹配时跳过这些位置，不用真的改 s',
        'pos = 0': '`pos` 指向 p 里下一个要匹配的字符',
        'for index, char in enumerate(s)': lambda S, B, rt: (f'扫描 `s[{S.index}] = {S.char!r}`'
                                                             if 'char' not in B or B.get('index') != S.index else 's 扫完了'),
        'if index not in remove_set': lambda S, B, rt: (
            f'`s[{S.index}]` 已被移除 → 跳过' if S.index in S.remove_set
            else (f'`{S.char!r}` == `p[{S.pos}] = {S.p[S.pos]!r}` → ==匹配上了==' if S.char == S.p[S.pos]
                  else f'`{S.char!r}` ≠ `p[{S.pos}] = {S.p[S.pos]!r}` → 不匹配，看下一个')),
        'pos += 1': '`pos` → `{pos}`',
        16: lambda S, B, rt: (f'`pos == len(p) = {S.pos}`：p 全部匹配上了 → 提前 `break`'
                              if S.pos == len(S.p) else f'`pos = {S.pos} < {len(S.p)}`，p 还没匹配完'),
        17: '`break`：p 已经匹配完，不用再扫了',
        19: lambda S, B, rt: (f'`pos = {S.pos} == len(p)`：移除前 `{S.mid}` 个后 p 仍是子序列' if S.pos == len(S.p)
                              else f'`pos = {S.pos} < len(p) = {len(S.p)}`：移除前 `{S.mid}` 个后 p 匹配不完了'),
        'l = mid': '移除前 `{mid}` 个后 p 仍是子序列 → 答案 ≥ `{mid}`，`l` → {l}',
        'r = mid - 1': '移除前 `{mid}` 个后 p 不是子序列了 → 答案 ≤ `{mid - 1}`，`r` → {r}',
        'return r': '`l = r = {r}`，最多可以移除 ==`{r}`== 个',
    },
    cards=dict(
        one_liner='移除个数有单调性：能移 j 个，就一定能移 i<j 个',
        complexity='时间 `O(n log m)`，空间 `O(m)`',
        problem=['`p` 是 `s` 的子序列；按 `removable` 的顺序，移除前若干个下标上的字符',
                 '求最多能移除多少个，使 `p` 仍是 `s` 的子序列',
                 '示例：`s = "abcacb"`，`p = "ab"`，`removable = [3,1,0]` → `2`'],
        quote='若选择移除前j个下标对应的字符后p依然是s的子序列，那么移除前i个下标对应的字符后p必然也是s的子序列，即这里的答案满足二分的性质。',
        quote_src='—— yiduobo 题解原文',
        idea=['i < j 时，前 i 个下标是前 j 个的子集 → 移得少一定更容易成立',
              '所以二分最终答案；检测时把要移除的位置记进 ==`remove_set`==',
              '用双指针扫 s 匹配 p，==遇到被移除的位置直接跳过==，不必真的改 s'],
        result='移除 2 个时成立，移除 3 个时不成立 → 答案 `2` ✓',
        summary=['时间 `O(n log m)`，空间 `O(m)`',
                 '二分写的是「最大的成立值」：`mid = (l + r + 1) >> 1`，成立 `l = mid`，否则 `r = mid - 1`',
                 '代码里 `break` 只跳出匹配循环，`pos == len(p)` 才表示成立',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，其余未改',
                 '对比灵神：灵神用 `sort.Search` 找第一个失败的 k；这里直接找最大成立的 mid'],
    ),
)
