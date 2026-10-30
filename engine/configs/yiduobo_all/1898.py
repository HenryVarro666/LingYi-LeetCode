def _rm(S):
    return S.get('remove_set') if 'remove_set' in S and 'mid' in S else None


def _s_color(S, k, v):
    rs = S.get('remove_set')
    if rs is None:
        return None
    if k in rs:
        return 'red'
    if 'index' in S and S['index'] == k and S['_line'] in (13, 14, 15, 16):
        return 'blue'
    return None


def _s_dim(S, k, v):
    rs = S.get('remove_set')
    return rs is not None and k in rs


def _p_color(S, k, v):
    pos = S.get('pos')
    if pos is None or 'remove_set' not in S:
        return None
    return 'green' if k < pos else None


def _pos_ptr(S):
    pos = S.get('pos')
    return pos if isinstance(pos, int) and pos < len(S['p']) and 'remove_set' in S else None


def _idx_ptr(S):
    i = S.get('index')
    return i if isinstance(i, int) and i < len(S['s']) and 'pos' in S else None


def _r_color(S, k, v):
    mid = S.get('mid')
    if mid is not None and 'remove_set' in S and k < mid:
        return 'red'
    return None


def _top(S):
    if 'l' not in S:
        return ''
    l, r = S['l'], S['r']
    if l >= r:
        return f'`l = {l}`、`r = {r}` 相遇 → 答案 =={r}=='
    if 'mid' in S and S['_line'] >= 7:
        return f'二分答案：`l={l}`，`r={r}`，试 `mid = {S["mid"]}`（移除前 {S["mid"]} 个下标）'
    return f'二分答案：`k` 的范围是 `[{l}, {r}]`'


CONFIG = dict(
    num=1898, title='可移除字符的最大数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='二分答案 + 子序列检测',
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
    call="Solution().maximumRemovals('abcacb', 'ab', [3, 1, 0])",
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（灰 = 被移除，蓝箭头 = 当前检查的位置）', cell=84, h=200,
             pointers={_idx_ptr: 'blue'}, pointer_labels={_idx_ptr: 'index'}, color=_s_color, dim=_s_dim),
        dict(type='string', var='p', label='p（绿 = 已匹配，粉箭头 = pos）', cell=84, h=200,
             pointers={_pos_ptr: 'pink'}, pointer_labels={_pos_ptr: 'pos'}, color=_p_color),
        dict(type='array', var='removable', label='removable（红 = 本轮要移除的前 mid 个）', cell=84, h=140, color=_r_color),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('pos', 'pos', 'green'), ('remove_set', 'remove_set', 'red')],
    captions={
        'l = 0': '`k` 的最小可能是 `0`（一个都不移除），`l = 0`',
        'r = len(removable)': '`k` 最大是 `{r}`（全部移除），`r = {r}`；答案 `k` 一定在 `[l, r]`',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，区间里还有候选，继续二分' if S.l < S.r else f'`l = {S.l} == r = {S.r}`：区间只剩一个值，结束'),
        'mid = (l + r + 1) >> 1': '取 `mid = {mid}`：==向上取整==，因为下面成立时 `l = mid`，向下取整会死循环',
        'remove_set = set()': '每轮重新准备要移除的下标集合（不真的改 s，只记下哪些位置不可用）',
        'for index in range(mid)': lambda S, B, r_: (f'把 `removable` 前 `{S.mid}` 个下标放进集合' if S.index != B.get('index') or 'index' not in B else '集合准备好了'),
        'remove_set.add': '`remove_set` 加入 `{removable[index]}`：`s[{removable[index]}]` 视为被移除',
        'pos = 0': '`pos` 指向 `p` 里下一个要匹配的字符，从 `0` 开始',
        'for index, char in enumerate(s)': lambda S, B, r_: (f"扫描 `s[{S.index}] = '{S.char}'`" if S.get('char') != B.get('char') or S.index != B.get('index') else 's 扫描完了'),
        'if index not in remove_set and char == p[pos]': lambda S, B, r_: (
            f"`s[{S.index}]` 被移除了，直接跳过" if S.index in S.remove_set else
            (f"`'{S.char}'` == `p[{S.pos}] = '{S.p[S.pos]}'` → 匹配" if S.char == S.p[S.pos] else f"`'{S.char}'` ≠ `p[{S.pos}] = '{S.p[S.pos]}'` → 不匹配，看下一个")),
        'pos += 1': '匹配成功，`pos` → `{pos}`：接着找 `p` 的下一个字符',
        'if pos == len(p)': lambda S, B, r_: (f'`pos = {S.pos} == len(p)`：p 全部匹配 → ==提前结束==' if S.pos == len(S.p) else f'`pos = {S.pos} < len(p) = {len(S.p)}`，还没匹配完'),
        'break': 'p 已经是子序列，不用再扫了',
        'if pos == len(p):': lambda S, B, r_: (f'`pos = {S.pos} == {len(S.p)}`：移除前 `{S.mid}` 个后 p ==仍是子序列== → 答案 ≥ mid' if S.pos == len(S.p)
                                               else f'`pos = {S.pos} < {len(S.p)}`：p 不再是子序列 → 移除 `{S.mid}` 个太多了'),
        'l = mid': '可行：`l = mid = {l}`，试试移除更多',
        'r = mid - 1': '不可行：`r = mid - 1 = {r}`，`{mid}` 个及以上都不行',
        'return r': '`l == r`，答案 `k = {r}`',
    },
    cards=dict(
        one_liner='移除得越少越容易成立：对 k 二分，每次 O(n) 检验',
        complexity='时间 `O(n log m)`，空间 `O(m)`',
        problem=['`p` 是 `s` 的子序列，按 `removable` 的顺序从 `s` 里移除前 `k` 个下标',
                 '求最大的 `k`，使得移除后 `p` 仍是 `s` 的子序列',
                 '示例：`s = "abcacb"`，`p = "ab"`，`removable = [3,1,0]` → `2`'],
        quote='若选择移除前j个下标对应的字符后p依然是s的子序列，那么移除前i个下标对应的字符后p必然也是s的子序列，即这里的答案满足二分的性质。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 越大，被移除的字符越多（前 `i` 个是前 `j` 个的子集），越难保持子序列',
              '所以能成立的 `k` 是一段前缀 → 二分最大的 `k`',
              '检验时不真的改 `s`：用集合记下被移除的下标，匹配时跳过'],
        summary=['时间 `O(n log m)`，空间 `O(m)`',
                 '`mid = (l + r + 1) >> 1` 向上取整，配合 `l = mid` / `r = mid - 1`',
                 '检验里 `pos == len(p)` 要提前 `break`，否则 `p[pos]` 越界',
                 '本题 `p` 一定是 `s` 的子序列，所以 `k = 0` 一定成立',
                 '原文是 Python 2 风格，但语法在 Python 3 里直接可运行，未做修改'],
    ),
)
