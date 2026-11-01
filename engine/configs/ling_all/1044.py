def _pair(S):
    s = S['s']
    sa = S.get('sa')
    if not sa:
        return ''
    if 'rk' in S and S["rk"] > 0 and S["_line"] in range(15, 19):
        a, b = sa[S['rk']], sa[S['rk'] - 1]
        return f'排名 {S["rk"]} 的后缀 `{s[a:]}`（起点 {a}）  vs  排名 {S["rk"] - 1} 的后缀 `{s[b:]}`（起点 {b}），已匹配 h = =={S["h"]}=='
    return '后缀数组 sa 把所有后缀按字典序排好：' + ' < '.join(s[p:] for p in sa)


def _ih(S):
    return S['i'] + S['h'] if 'j' in S and 11 < S['_line'] < 19 and S['i'] + S['h'] < S['n'] else None


def _jh(S):
    return S['j'] + S['h'] if 'j' in S and 14 < S['_line'] < 19 and S['j'] + S['h'] < S['n'] else None


def _rk_ptr(S):
    return S['rk'] if 'rk' in S and S['_line'] <= 18 else None


CONFIG = dict(
    num=1044, title='最长重复子串', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='后缀数组 + 高度数组（Go 原文转写）',
    tags=['灵神题单', '字符串', '难度分 2429'],
    setup='''
def suffix_array(s):
    # 对应 Go 里 suffixarray.New 内部的 sa：所有后缀按字典序排序后的起点
    return sorted(range(len(s)), key=lambda i: s[i:])
''',
    code='''
class Solution:
    def longestDupSubstring(self, s: str) -> str:
        # 求出后缀数组和高度数组
        n = len(s)
        sa = suffix_array(s)
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i
        height = [0] * n
        h = 0
        for i, rk in enumerate(rank):
            if h > 0:
                h -= 1
            if rk > 0:
                j = sa[rk - 1]
                while i + h < n and j + h < n and s[i + h] == s[j + h]:
                    h += 1
            height[rk] = h

        # 高度数组中的最大值对应的就是最长的重复子串
        idx = max_h = 0
        for i, h in enumerate(height):
            if h > max_h:
                idx, max_h = i, h
        return s[sa[idx]: sa[idx] + max_h]
''',
    call='Solution().longestDupSubstring("banana")',
    expect='ana',
    views=[
        dict(type='text', fn=_pair, size=24),
        dict(type='string', var='s', label='s（蓝 = 后缀 i 的比较位置，粉 = 排名前一位的后缀的比较位置）', cell=84,
             pointers={_ih: 'blue', _jh: 'pink'}, pointer_labels={_ih: 'i+h', _jh: 'j+h'}),
        dict(type='array', var='sa', label='sa（第 k 小的后缀从哪里开始）', cell=84, h=150,
             pointers={_rk_ptr: 'blue'}, pointer_labels={_rk_ptr: 'rk'}),
        dict(type='array', var='height', label='height（与前一名后缀的最长公共前缀）', cell=84, h=150,
             color=lambda S, k, v: 'green' if 'max_h' in S and k == S.get('idx') and v == S['max_h'] and v > 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('rk', 'rk', 'cyan'), ('j', 'j', 'pink'), ('h', 'h', 'orange'), 'max_h'],
    skip=['n = len(s)', 'rank = [0] * n', 'height = [0] * n'],
    captions={
        'sa = suffix_array': '排好序的后缀：`sa = {sa}`，即 `{[s[p:] for p in sa]}`',
        'rank[sa[i]] = i': '`rank[{sa[i]}] = {i}`：后缀 `s[{sa[i]}:]` 排第 {i}（`sa` 的反函数）',
        10: '`h` 是当前 LCP，下面按 `i` 从小到大算',
        'for i, rk': lambda S, B, ret: ('所有后缀都算完，`height` 就绪' if 'i' in B and B.i == S.i else f'处理后缀 `s[{S.i}:]`，它排第 `rk = {S.rk}`'),
        'h -= 1': '上一个后缀去掉首字母后，LCP ==至少还剩 h-1==，所以只回退 1 → `h = {h}`',
        'if rk > 0': lambda S, B, ret: ('`rk > 0`：有前一名后缀可比较' if S.rk > 0 else '`rk = 0` 排第一，没有前一名，`height` 记 0'),
        'j = sa[rk - 1]': '前一名后缀从 `j = {j}` 开始',
        'while i + h < n': lambda S, B, ret: (f'`s[{S.i + S.h}] = {S.s[S.i + S.h]}` 与 `s[{S.j + S.h}] = {S.s[S.j + S.h]}` 相等 → 再匹配一位' if S.i + S.h < S.n and S.j + S.h < S.n and S.s[S.i + S.h] == S.s[S.j + S.h]
                                              else '不再相等（或到头）→ LCP 就是 `h = {}`'.format(S.h)),
        'h += 1': '`h` → {h}',
        'height[rk] = h': '`height[{rk}] = {h}`：与前一名后缀的公共前缀长 {h}',
        21: '接下来在 `height` 里找最大值',
        'for i, h in enumerate(height)': lambda S, B, ret: ('扫完 `height`，最大值已找到' if B.get('i') == S.i and 'max_h' in B and B.get('h') == S.h else f'看 `height[{S.i}] = {S.h}`'),
        'if h > max_h': lambda S, B, ret: (f'`{S.h} > {S.max_h}` → ==更长的重复子串==' if S.h > S.max_h else f'`{S.h} ≤ {S.max_h}`，不更新'),
        'idx, max_h = i, h': '更新：`idx = {idx}`，`max_h = {max_h}`',
        'return s[': lambda S, B, ret: f'取后缀 `s[{S.sa[S.idx]}:]` 的前 `{S.max_h}` 位 = `"{ret}"`',
    },
    max_steps=110,
    cards=dict(
        one_liner='重复子串 = 相邻后缀的公共前缀，最大的 LCP 就是答案',
        complexity='时间 `O(n)`（库函数用 SA-IS 建 sa），空间 `O(n)`',
        problem=['找出 `s` 中出现 ==至少两次== 的最长子串（可以重叠）',
                 '没有重复子串返回 `""`',
                 '示例：`"banana"` → `"ana"`'],
        quote='高度数组中的最大值对应的就是最长的重复子串',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先求后缀数组 `sa`：所有后缀按字典序排好，再求 `rank`',
              '`height[rk]` = 排名 rk 的后缀与前一名的 LCP，用 `h` 滑动着求：上一步 `h` 只减 1 就能继续',
              '最大 `height` 对应的后缀前缀就是最长重复子串'],
        result='`height` 最大为 3，对应后缀 `ana` → 返回 `"ana"` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；Go 里的 `suffixarray` 取 sa 用了 unsafe，Python 在 setup 里用排序后缀的等价函数 `suffix_array` 代替',
                 '`h` 只回退 1 而不是清零，是 `O(n)` 的关键',
                 '`i` 按原串顺序走，`rk` 按后缀排名查：两套下标别混',
                 '同类题：后缀数组求不同子串、最长公共子串'],
    ),
)
