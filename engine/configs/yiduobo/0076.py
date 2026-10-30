S_IN, T_IN = 'ABECBA', 'ABC'


def _chosen(S):
    """当前被选中的位置集合：pos_dict[c] 中 now_choose_pos[c]-count+1 .. now_choose_pos[c]"""
    pd, nc, cd = S.get('pos_dict'), S.get('now_choose_pos'), S.get('count_dict')
    out = set()
    if not pd or not nc or not cd:
        return out
    for c, k in nc.items():
        if c in pd and c in cd:
            out.update(pd[c][k - cd[c] + 1:k + 1])
    return out


def _s_color(S, i, v):
    return 'purple' if i in _chosen(S) else None


def _win_ok(S):
    return isinstance(S.get('l'), int) and isinstance(S.get('r'), int) and 'res' in S


def _res_text(S):
    res = S.get('res')
    if not res:
        return ''
    return f'当前最短 `res = {res}` → `{S_IN[res[1]:res[2] + 1]!r}`　　紫色 = 每个字母当前选用的位置'


def _pos_fmt(c, v):
    return f'{c}: {v}'


CONFIG = dict(
    num=76, title='最小覆盖子串', difficulty='Hard', category='子串',
    author='yiduobo', technique='位置表 + 左边界推进',
    code='''
class Solution(object):
    def minWindow(self, s, t):
        if not s or not t:
            return ''

        pos_dict = {}
        count_dict = {}
        now_choose_pos = {}
        for char in t:
            pos_dict[char] = []
            count_dict[char] = count_dict.get(char, 0) + 1

        for index, char in enumerate(s):
            if char in pos_dict:
                pos_dict[char].append(index)

        l = len(s)
        r = 0
        for char in pos_dict:
            if len(pos_dict[char]) < count_dict[char]:
                return ''
            l = min(l, pos_dict[char][0])
            r = max(r, pos_dict[char][count_dict[char] - 1])
            now_choose_pos[char] = count_dict[char] - 1

        res = [r - l + 1, l, r]

        while l < r:
            if r - l + 1 == len(t):
                return s[l : r + 1]
            char = s[l]
            if char in pos_dict:
                if now_choose_pos[char] == len(pos_dict[char]) - 1:
                    break
                else:
                    now_choose_pos[char] += 1
                    next_pos = pos_dict[char][now_choose_pos[char]]
                    if next_pos > r:
                        r = next_pos
            l += 1
            if r - l + 1 < res[0]:
                res = [r - l + 1, l, r]

        return s[res[1] : res[2] + 1]
''',
    call=f'Solution().minWindow({S_IN!r}, {T_IN!r})',
    expect='CBA',
    views=[
        dict(type='text', fn=_res_text),
        dict(type='string', var='s', pointers={'l': 'blue', 'r': 'pink'},
             window=(lambda S: S['l'] if _win_ok(S) else None, lambda S: S['r'] if _win_ok(S) else None),
             color=_s_color, cell=96),
        dict(type='map', var='pos_dict', label='pos_dict：t 中每个字母在 s 中的所有位置', fmt=_pos_fmt, font=26, h=120),
        dict(type='map', var='now_choose_pos', label='now_choose_pos：每个字母当前用到 pos_dict 的第几个', font=26, h=110),
    ],
    skip=['if not s or not t', 'count_dict = {}', 'now_choose_pos = {}', 'for char in t:', 'pos_dict[char] = []',
          'count_dict[char] = ', 'for index, char in enumerate(s)', 'pos_dict[char].append',
          'if len(pos_dict[char]) < count_dict[char]'],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'char', 'next_pos', ('res', 'res', 'green')],
    captions={
        'if not s or not t': '`s`、`t` 非空，继续',
        'pos_dict = {}': '三张表：`pos_dict[c]` 是 `c` 在 `s` 中的==所有位置==；`count_dict[c]` 是 `c` 在 `t` 中的次数；`now_choose_pos[c]` 是用到第几个',
        'count_dict = {}': '`count_dict[c]`：字母 `c` 在 `t` 中出现几次',
        'now_choose_pos = {}': '`now_choose_pos[c]`：字母 `c` 当前用到了 `pos_dict[c]` 的第几个',
        'for char in t:': lambda S, B, ret: (f'统计 `t`：`char = {S.char!r}`' if sum(S.count_dict.values()) < len(S.t) else '`t` 统计完毕'),
        'pos_dict[char] = []': '`pos_dict[{char!r}]` 先置空',
        'count_dict[char] = ': '`count_dict[{char!r}] = {count_dict[char]}`',
        'if char in pos_dict:': lambda S, B, ret: (
            (f'`s[{S.index}] = {S.char!r}` 在 `t` 中 → 记下位置 `{S.index}`' if S.char in S.pos_dict
             else f'`s[{S.index}] = {S.char!r}` 不在 `t` 中，跳过') if 'res' not in S else
            (f'`s[l] = {S.char!r}` 在 `t` 中：移走它，需要从后面补一个 `{S.char}`' if S.char in S.pos_dict
             else f'`s[l] = {S.char!r}` 不在 `t` 中，==无事发生==')),
        'l = len(s)': '位置表建好了（每个字母在 `t` 中都只出现 1 次）。左边界先设成 `len(s) = {l}`',
        'r = 0': '右边界 `r` 先设成 0，下面对每个字母取最左的几个位置',
        'for char in pos_dict:': lambda S, B, ret: (f'处理字母 `{S.char!r}`：位置 `{S.pos_dict[S.char]}`，需要 {S.count_dict[S.char]} 个'
                                                    if 'char' not in B or S.char != B.char or B.char not in B.now_choose_pos
                                                    else '每个字母都取了最左的几个位置（`s` 里不够的话会直接返回空串）'),
        'if len(pos_dict[char]) < count_dict[char]': lambda S, B, ret: (
            f'`s` 里的 `{S.char}` 不够 → 返回空串' if len(S.pos_dict[S.char]) < S.count_dict[S.char]
            else f'`s` 里有 {len(S.pos_dict[S.char])} 个 `{S.char}` ≥ 需要的 {S.count_dict[S.char]} 个，够用'),
        'l = min(l, pos_dict[char][0])': '左边界 = 各字母第一个位置的最小值：`l = {l}`',
        'r = max(r, pos_dict[char][count_dict': '右边界 = 各字母第 k 个位置的最大值：`r = {r}`',
        'now_choose_pos[char] = count_dict': '`{char}` 先用前 {count_dict[char]} 个位置：`now_choose_pos[{char!r}] = {now_choose_pos[char]}`',
        '                res = [r - l + 1': '`res = {res}`：目前最短是 `{s[l:r + 1]!r}`',
        'res = [r - l + 1, l, r]': '==最左侧的一个可行解==：`s[{l}..{r}] = {s[l:r + 1]!r}`，记 `res = {res}`',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：继续把 `l` 往右推' if S.l < S.r else '`l` 追上 `r`，结束'),
        'if r - l + 1 == len(t)': lambda S, B, ret: (
            f'长度 `{S.r - S.l + 1}` 恰好等于 `len(t)`：==不可能更短了==，直接返回' if S.r - S.l + 1 == len(S.t)
            else f'长度 `{S.r - S.l + 1}` > `len(t) = {len(S.t)}`，还可能更短'),
        'return s[l : r + 1]': '返回 `{ret!r}`',
        'char = s[l]': '看左边界字母 `s[{l}] = {char!r}`',
        'if now_choose_pos[char] == len': lambda S, B, ret: (
            f'`{S.char}` 后面没有了 → s 中的 `{S.char}` 不够，`break`' if S.now_choose_pos[S.char] == len(S.pos_dict[S.char]) - 1
            else f'`{S.char}` 后面还有备用位置 `{S.pos_dict[S.char][S.now_choose_pos[S.char] + 1:]}`'),
        'now_choose_pos[char] += 1': '`now_choose_pos[{char!r}] = {now_choose_pos[char]}`：换用下一个 `{char}`',
        'next_pos = ': '下一个 `{char}` 在位置 `next_pos = {next_pos}`',
        'if next_pos > r': lambda S, B, ret: (f'`next_pos = {S.next_pos}` > `r = {S.r}`：超出右边界，要扩右边界' if S.next_pos > S.r
                                              else f'`next_pos = {S.next_pos}` ≤ `r = {S.r}`：已经在窗口里，==右边界无需移动=='),
        '                        r = next_pos': '右边界扩到 `r = {r}`：窗口变成 `{s[l:r + 1]!r}`',
        'l += 1': '`l` 右移到 {l}：窗口 `s[{l}..{r}] = {s[l:r + 1]!r}`，仍然涵盖 `t`',
        'if r - l + 1 < res[0]': lambda S, B, ret: (f'长度 `{S.r - S.l + 1}` < `res[0] = {S.res[0]}`：更短，更新' if S.r - S.l + 1 < S.res[0]
                                                    else f'长度 `{S.r - S.l + 1}` 不比 `{S.res[0]}` 短'),
        'return s[res[1]': '返回 `{ret!r}`',
    },
    cards=dict(
        one_liner='先找最左侧的可行解，再把左边界一格格往右推，缺谁就从后面补谁',
        complexity='时间 `O(m + n)`，空间 `O(m)`',
        problem=['返回 `s` 中==涵盖 t 所有字符==（含重复）的最短子串，没有就返回 `""`',
                 '示例：`s = "ADOBECODEBANC", t = "ABC"` → `"BANC"`',
                 '演示用 `s = "ABECBA", t = "ABC"` → `"CBA"`'],
        quote='接下来，我们将l往右推动。若当前s[l]是t中的字符，那么说明需要将pos_dict[s[l]]的下一个字符补充进来，用来替代当前的s[l]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos_dict` 记下 `t` 中每个字母在 `s` 里的所有位置；每个字母取最左的几个 → ==最左侧的可行解==',
              '`l` 右移：移走的不是 `t` 的字母就无事发生；是的话换用它的下一个位置，必要时扩 `r`',
              '某字母后面没有备用位置了 → `break`；长度恰好 `len(t)` → 一定最优，直接返回'],
        summary=['一趟扫描：`l` 只往右走，`now_choose_pos` 也只增不减，时间 `O(m + n)`',
                 '每次推进后的 `s[l..r]` 都是合法解，边走边记最短',
                 '小优化：`r − l + 1 == len(t)` 时一定最优，提前返回',
                 '对比灵神：灵神是枚举右端点 + 收缩左端点；yiduobo 是枚举左端点 + 用位置表补右边',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
