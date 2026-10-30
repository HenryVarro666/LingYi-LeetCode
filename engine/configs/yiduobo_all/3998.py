def _kind(S):
    if 't' not in S or 'index' not in S:
        return ''
    ix = S['index']
    a, b = S['s'][ix], S['t'][ix]
    if a == b:
        return f"位置 {ix}：`s{a}t{b}` 相同 → 不用参与操作"
    names = {('1', '0'): '要把 1 换走、0 换来：需要右边有 0 来配',
             ('1', '?'): '灵活：可当 1 的搭档，也可自己消化',
             ('0', '?'): '灵活：可和左边的 s1t0 配对，也可自行消化',
             ('0', '1'): '必须由左边的 1 来换：需要左边有 s1t0 或 s1t?'}
    return f"位置 {ix}：`s{a}t{b}` {names[(a, b)]}"


def _cur(S, idx, v, col):
    return col if 'index' in S and idx == S['index'] and S.get('_line', 0) >= 11 and S.get('_line', 0) <= 28 else None


CONFIG = dict(
    num=3998, title='使用子序列排序转换二进制字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='计数配对 · 一遍扫描',
    tags=['灵神题单', '难度分 1862'],
    code='''
class Solution(object):
    def transformStr(self, s, strs):
        
        res = []
        for t in strs:
            one_q = 0
            zero_q = 0
            one_zero = 0

            flag = True
            for index in range(len(s)):
                if s[index] == t[index]:
                    continue
                if s[index] == '1' and t[index] == '0':
                    one_zero += 1
                elif s[index] == '1' and t[index] == '?':
                    one_q += 1
                elif s[index] == '0' and t[index] == '?':
                    zero_q += 1
                    zero_q = min(zero_q, one_zero)
                elif one_zero > 0:
                    one_zero -= 1
                    zero_q = min(zero_q, one_zero)
                elif one_q > 0:
                    one_q -= 1
                else:
                    flag = False
                    break
            
            if flag and one_zero <= zero_q:
                res.append(True)
            else:
                res.append(False)
        
        return res
''',
    call='Solution().transformStr("101", ["0?1", "110"])',
    expect=[True, False],
    views=[
        dict(type='text', fn=lambda S: _kind(S) or ('每个 `t` 单独检查：`s` 能否经过「0 移到 1 左边」变成 `t`' if 't' not in S else ''), size=24),
        dict(type='string', var='s', label='s', pointers={'index': 'blue'}, h=170, pointer_labels={'index': 'index'},
             color=lambda S, idx, v: _cur(S, idx, v, 'blue')),
        dict(type='string', var='t', label='t', h=170, index=False,
             color=lambda S, idx, v: _cur(S, idx, v, 'pink')),
    ],
    watch=[('one_zero (s1t0)', 'one_zero', 'orange'), ('one_q (s1t?)', 'one_q', 'cyan'), ('zero_q (s0t?)', 'zero_q', 'purple'), ('flag', 'flag', 'green')],
    skip=['one_q = 0', 'zero_q = 0', 'one_zero = 0'],
    captions={
        'res = []': '`res` 保存每个 `t` 的答案',
        'for t in strs': lambda S, B, r: (f"逐个检查：当前 `t = {S.t}`（各个 `t` 之间没有关联，只能一个个来）" if B.get('t') != S.t or B.get('t') is None else '所有 `t` 都检查完了'),
        'flag = True': '三个计数器清零：`one_zero`=落单的 s1t0，`one_q`=落单的 s1t?，`zero_q`=可用的 s0t?；`flag` 记录有没有失败',
        'for index in range': lambda S, B, r: ('这个 `t` 扫完了，看最后的计数' if B.get('index') == S.get('index') and B.get('index') is not None else f"看第 `{S.index}` 位：`s = {S.s[S.index]}`，`t = {S.t[S.index]}`"),
        'if s[index] == t[index]': lambda S, B, r: (f"`s` 与 `t` 相同 → 这一位不必加入子序列，跳过" if S.s[S.index] == S.t[S.index] else f"`s[{S.index}] = {S.s[S.index]}` ≠ `t[{S.index}] = {S.t[S.index]}` → 要分情况"),
        "t[index] == '0'": lambda S, B, r: ("是 s1t0：1 要被换走，需要右边有 0 来配" if S.s[S.index] == '1' and S.t[S.index] == '0' else f"不是 s1t0（`s{S.s[S.index]}t{S.t[S.index]}`），看下一类"),
        'one_zero += 1': '落单的 s1t0：`one_zero` → {one_zero}，等右边的 0 来换',
        "t[index] == '?'": lambda S, B, r: (("是 s1t?：灵活位，当「1」来用" if S.s[S.index] == '1' and S.t[S.index] == '?' else f"不是 s1t?（`s{S.s[S.index]}t{S.t[S.index]}`），看下一类") if S._line == 16 else
                                              ("是 s0t?：灵活位，可以接左边的 s1t0" if S.s[S.index] == '0' and S.t[S.index] == '?' else f"不是 s0t?（`s{S.s[S.index]}t{S.t[S.index]}`），只剩 s0t1")),
        'one_q += 1': '`s1t?` 可当「左边的 1」来配 s0t1：`one_q` → {one_q}',
        'zero_q += 1': '`s0t?` 可以和==左边==的 s1t0 配对（10 → 01）：`zero_q` → {zero_q}',
        'zero_q = min': '`zero_q` 不能超过当前落单的 `one_zero`（只能配左边的）：取 min → {zero_q}',
        'elif one_zero > 0': lambda S, B, r: (f"s0t1：左边有落单的 s1t0（`one_zero = {S.one_zero}`）→ 可以 10→01 配对" if S.one_zero > 0 else "s0t1：左边没有落单的 s1t0，再看 s1t?"),
        'one_zero -= 1': '配对成功：`one_zero` → {one_zero}（优先用 s1t0，因为 s1t? 自己能消化）',
        'elif one_q > 0': lambda S, B, r: (f"没有 s1t0，但有 s1t?（`one_q = {S.one_q}`）→ 把它当 1 来配" if S.one_q > 0 else "既没有 s1t0，也没有 s1t?"),
        'one_q -= 1': '用掉一个 `s1t?`：`one_q` → {one_q}',
        'flag = False': '这个 s0t1 左边没有任何 1 能换给它：s 的 0 只能往左，永远到不了这里 → ==False==',
        'break': '已经确定不行，不用再扫',
        'if flag and one_zero': lambda S, B, r: (f"`flag = {S.flag}`，`one_zero = {S.one_zero} <= zero_q = {S.zero_q}`：落单的 s1t0 都能被右边的 s0t? 消化 → ==True==" if S.flag and S.one_zero <= S.zero_q else (f"扫描中已失败（`flag = False`）→ ==False==" if not S.flag else f"`one_zero = {S.one_zero} > zero_q = {S.zero_q}`：还有 s1t0 右边没有 0 可换 → ==False==")),
        'res.append(True)': '这个 `t` 可行：`res` = {res}',
        'res.append(False)': '这个 `t` 不可行：`res` = {res}',
        'return res': '每个 `t` 的答案：`{res}`',
    },
    cards=dict(
        one_liner='只看 s 与 t 不同的位置：1→0 的要往右找 0 来换',
        complexity='时间 `O(nm)`，空间 `O(1)`（返回值除外）',
        problem=['对 `s` 的任意子序列「0 放到 1 左边」排序，可做任意多次',
                 '`strs[i]` 里的 `?` 可以换成 `0` 或 `1`',
                 '判断每个 `strs[i]` 能否由 `s` 变出来',
                 '本视频：`s = 101`，`strs = ["0?1", "110"]`'],
        quote='若当前有一个靠前的下标位置满足s0t1，同时其左侧既没有落单的s1t0的位置，也没有落单的s1t？的位置，那么这个位置就不可能变为相同',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 与 `t` 相同的位置不必操作；不同的只有 s1t0、s0t1、s0t?、s1t? 四种',
              's0t1 必须有左边的 1 来换；s1t0 则需要右边有 0 来配',
              '用三个计数 `one_zero`、`one_q`、`zero_q` 一遍扫描配对'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '`zero_q` 只能配左边的 s1t0，所以每次都和 `one_zero` 取 min',
                 's0t1 优先用 s1t0，再用 s1t?（s1t? 自己也能消化）',
                 '最后要求 `one_zero <= zero_q`：落单的 s1t0 都得被右边的 s0t? 接走',
                 '对比灵神：灵神把 `?` 左 0 右 1 补好，再比 0 的下标；yiduobo 按位置分四类配对计数'],
    ),
)
