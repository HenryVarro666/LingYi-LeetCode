def _phase(S):
    if 'left' in S and 'right' in S and isinstance(S.get('right'), int):
        return 3
    if 'suffix' in S and 'prefix' in S and S.get('suffix') is not None and 'left' not in S and S['_line'] >= 13:
        return 2
    return 1


def _p_ptr(S):
    p = S.get('p')
    if _phase(S) == 3:
        return None
    return p if isinstance(p, int) and 0 <= p < len(S['s']) else None


def _s_color(S, k, v):
    ph = _phase(S)
    if ph == 3:
        pp, sp = S.get('pre_pos'), S.get('suf_pos')
        if 'pre_len' not in S or S['_line'] < 30:
            return None
        if pp is not None and k <= pp and S['_line'] >= 37:
            return 'green'
        if sp is not None and k >= sp and S['_line'] >= 43:
            return 'orange'
        return None
    if ph == 1:
        return 'green' if k in (S.get('prefix') or []) and k < len(S['s']) else None
    return 'orange' if k in (S.get('suffix') or []) and k >= 0 else None


def _t_color(S, k, v):
    if 'pre_len' in S and 'mid' in S and _phase(S) == 3 and 'suf_len' in S:
        if k < S['pre_len']:
            return 'green'
        if k < S['pre_len'] + S['mid']:
            return 'red'
        return 'orange'
    cur = S.get('char')
    return None


def _top(S):
    ph = _phase(S)
    if ph == 1:
        return '第一步：正向，prefix[i] = 匹配 t[:i+1] 所需的 s 最短前缀的终点'
    if ph == 2:
        return '第二步：反向，suffix[i] = 匹配 t[i:] 所需的 s 最短后缀的起点'
    if 'mid' not in S:
        return f'二分答案：删掉的子串长度在 `[{S["left"]}, {S["right"]}]`'
    t = S['t']
    out = f'二分删除长度：`left={S["left"]}`，`right={S["right"]}`，试 `mid = {S["mid"]}`'
    if 'pre_len' in S and 'suf_len' in S:
        out = f'`mid = {S["mid"]}`：留前缀 `t[:{S["pre_len"]}]`，删中间 {S["mid"]} 个，留后缀 {S["suf_len"]} 个'
    return out


CONFIG = dict(
    num=2565, title='最少得分子序列', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='二分删除长度 + 前后缀数组',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 2432'],
    code='''
class Solution(object):
    def minimumScore(self, s, t):

        prefix = []
        p = 0
        for char in t:
            while p < len(s) and s[p] != char:
                p += 1
            prefix.append(p)
            if p < len(s):
                p += 1
        
        suffix = []
        p = len(s) - 1
        for char in t[::-1]:
            while p >= 0 and s[p] != char:
                p -= 1
            suffix.append(p)
            if p >= 0:
                p -= 1
        
        suffix.reverse()
        
        if prefix[-1] < len(s):
            return 0
        

        left = 1
        right = len(t)
        while left < right:
            mid = (left + right) >> 1
            flag = False
            for pre_len in range(len(t) - mid + 1):
                suf_len = len(t) - mid - pre_len
                if pre_len == 0:
                    pre_pos = -1
                else:
                    pre_pos = prefix[pre_len - 1]

                if suf_len == 0:
                    suf_pos = len(s)
                else:
                    suf_pos = suffix[len(t) - suf_len]

                if pre_pos < suf_pos:
                    flag = True
                    break
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call="Solution().minimumScore('abcb', 'bzc')",
    expect=1,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='s', label='s（绿 = 前缀匹配用到的位置，橙 = 后缀匹配用到的位置）', cell=84, h=170,
             pointers={_p_ptr: 'pink'}, pointer_labels={_p_ptr: 'p'}, color=_s_color),
        dict(type='string', var='t', label='t（二分阶段：绿 = 留下的前缀，红 = 删掉的子串，橙 = 留下的后缀）', cell=84, h=170, color=_t_color),
        dict(type='array', var='prefix', label='prefix[i]（等于 len(s)=7 表示匹配不上）', cell=84, h=130, min_slots=3),
        dict(type='array', var='suffix', label='suffix[i]（-1 表示匹配不上）', cell=84, h=130, min_slots=3),
    ],
    watch=[('p', 'p', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('pre_pos', 'pre_pos', 'green'), ('suf_pos', 'suf_pos', 'orange')],
    captions={
        'prefix = []': '`prefix[i]`：让 `t[:i+1]` 成为 s 子序列所需的 ==s 最短前缀== 的最后一个下标',
        'p = 0': '`p` 在 s 上从左往右走，`p = 0`',
        'for char in t:': lambda S, B, r: ('prefix 算完了' if len(S.prefix) == len(S.t) else f"匹配 t 的下一个字母 `char = '{S.char}'`"),
        'while p < len(s) and s[p] != char': lambda S, B, r: (
            f"`s[{S.p}] = '{S.s[S.p]}'` ≠ `'{S.char}'` → `p` 继续往右" if S.p < len(S.s) and S.s[S.p] != S.char
            else (f"`s[{S.p}] = '{S.s[S.p]}'` == `'{S.char}'` → 找到了" if S.p < len(S.s) else f'`p = {S.p}` 走出 s：匹配不上了')),
        'prefix.append(p)': '`prefix` 追加 `{p}`：`t[:{len(prefix)}]` 最早在 `s[{p}]` 处匹配完（`{len(s)}` 表示失败）',
        'if p < len(s):': '`p` 没越界就后移一位，下一个字母从它右边找',
        'suffix = []': '`suffix[i]`：让 `t[i:]` 成为 s 子序列所需的 ==s 最短后缀== 的起点，倒着算',
        'p = len(s) - 1': '`p` 从 s 的末尾往左走：`p = {p}`',
        'for char in t[::-1]': lambda S, B, r: ('suffix 算完了' if len(S.suffix) == len(S.t) else f"倒着取 t 的字母 `char = '{S.char}'`"),
        'while p >= 0 and s[p] != char': lambda S, B, r: (
            f"`s[{S.p}] = '{S.s[S.p]}'` ≠ `'{S.char}'` → `p` 继续往左" if S.p >= 0 and S.s[S.p] != S.char
            else (f"`s[{S.p}] = '{S.s[S.p]}'` == `'{S.char}'` → 找到了" if S.p >= 0 else '`p < 0`：走出 s 左边，匹配不上了')),
        'suffix.append(p)': '`suffix` 追加 `{p}`（`-1` 表示匹配不上）',
        'suffix.reverse()': '`suffix` 是倒着追加的，翻转后下标和 t 对齐：`{suffix}`',
        'if prefix[-1] < len(s)': lambda S, B, r: (f'`prefix[-1] = {S.prefix[-1]} < {len(S.s)}`：整个 t 都能匹配 → 不用删，得分 0' if S.prefix[-1] < len(S.s)
                                                 else f'`prefix[-1] = {S.prefix[-1]}` = len(s)：t 不是 s 的子序列，要删'),
        'left = 1': '删除长度至少 `1`（不删的情况上面已处理）：`left = 1`',
        'right = len(t)': '最多把 t 全删光，长度 `{right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续二分' if S.left < S.right else f'`left = right = {S.left}` → 结束'),
        'mid = (left + right) >> 1': '二分删除长度：试 `mid = {mid}`。删得越多越容易成立，所以==单调==',
        'flag = False': '`flag` 记录：存在某个起点，删掉 `t[p:p+mid]` 后前后缀能被 s 容纳',
        'for pre_len in range': lambda S, B, r: (f'枚举保留的前缀长度 `pre_len = {S.pre_len}`' if S.get('pre_len') != B.get('pre_len') or 'pre_len' not in B else '枚举完了，没有可行的起点'),
        'suf_len = ': '保留前缀 `{pre_len}` 个、删 `{mid}` 个 → 后缀保留 `suf_len = {suf_len}` 个',
        'pre_pos = -1': '前缀为空 → 不占 s 的任何位置：`pre_pos = -1`',
        'pre_pos = prefix[': '前缀 `t[:{pre_len}]` 在 s 里最早匹配到 `{pre_pos}`',
        'suf_pos = len(s)': '后缀为空 → `suf_pos = len(s) = {suf_pos}`',
        'suf_pos = suffix[': '后缀 `t[{len(t) - suf_len}:]` 在 s 里最晚从 `{suf_pos}` 开始匹配',
        'if pre_pos < suf_pos': lambda S, B, r: (f'`pre_pos = {S.pre_pos} < suf_pos = {S.suf_pos}`：前缀后缀在 s 里不重叠 → ==可行=='
                                                  if S.pre_pos < S.suf_pos else f'`pre_pos = {S.pre_pos} ≥ suf_pos = {S.suf_pos}`：重叠了 → 这个起点不行'),
        'flag = True': '找到可行的删法，`flag = True`',
        'break': '不用再试别的起点了',
        'if flag': lambda S, B, r: (f'删 `{S.mid}` 个可行 → 试试更短的' if S.flag else f'删 `{S.mid}` 个都不行 → 必须删更多'),
        'right = mid': '`right = mid = {right}`：答案 ≤ mid',
        'left = mid + 1': '`left = mid + 1 = {left}`：答案 > mid',
        'return left': '最少要删的子串长度 `{left}`，即最小得分',
    },
    max_steps=110,
    skip=['flag = False', 'p += 1', 'p -= 1', 'if p < len(s):', 'if p >= 0:'],
    cards=dict(
        one_liner='删中间一段子串最划算；二分删多长，前后缀数组秒判',
        complexity='时间 `O(n + m log m)`，空间 `O(m)`',
        problem=['从 `t` 删任意字符，使 `t` 成为 `s` 的子序列；得分 = 删掉字符的 `最大下标 − 最小下标 + 1`',
                 '示例：`s = "abacaba"`，`t = "bzaa"` → `1`',
                 '本视频：`s = "abcb"`，`t = "bzc"` → `1`'],
        quote='对于a的某个子序列b，从b中删去若干字符得到的子序列c依然是a的子序列。……问题就变成了从t中删去一个最短的子串，使得新的t为s的一个子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间里的字符全删也不影响得分 → 只考虑删==子串==；删得越长越容易成立 → ==二分长度==',
              '`prefix[i]`、`suffix[i]` 预处理好：留 `t[:p]` 和 `t[p+mid:]` 时，查表得到它们在 s 里的位置',
              '`pre_pos < suf_pos` 说明两段在 s 里不重叠，这个删法可行'],
        summary=['时间 `O(n + m log m)`，空间 `O(m)`',
                 '`prefix` 里等于 `len(s)`、`suffix` 里等于 `-1` 表示匹配失败，比较时自然判不可行',
                 '空前缀用 `pre_pos = -1`，空后缀用 `suf_pos = len(s)`',
                 '先判断 `prefix[-1] < len(s)`：t 本来就是子序列 → 返回 0',
                 '对比灵神：灵神一次线性双指针，不用二分；yiduobo 二分长度，多一个 log'],
    ),
)
