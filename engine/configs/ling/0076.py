def _cover(S):
    if 'ge_cnt' not in S or 'kinds' not in S:
        return ''
    g, kd = S['ge_cnt'], S['kinds']
    tail = '==涵盖 t==' if g == kd else '还没涵盖'
    return f'`ge_cnt = {g}`，`kinds = {kd}` → {tail}'


def _ans_color(S, i, v):
    a, b = S.get('ans_left', -1), S.get('ans_right')
    if a is not None and a >= 0 and a <= i <= b:
        return 'green'
    return None


def _diff_fmt(c, v):
    return f'{c}: {v:+d}' if v else f'{c}: 0 ✓'


CONFIG = dict(
    num=76, title='最小覆盖子串', difficulty='Hard', category='子串',
    author='灵茶山艾府', technique='不定长滑动窗口（越长越合法）',
    code='''
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # 注：defaultdict 比 Counter 快
        diff = defaultdict(int)  # 窗口每种字母个数 - t 每种字母个数
        for c in t:
            diff[c] -= 1
        kinds = len(diff)  # t 中有 kinds 种不同的字母

        ans_left, ans_right = -1, len(s)
        ge_cnt = 0  # 窗口内有 ge_cnt 种字母的出现次数 >= t 中相应字母的出现次数
        left = 0

        for right, c in enumerate(s):  # 移动子串右端点
            diff[c] += 1  # 右端点字母移入子串
            if diff[c] == 0:  # 原来窗口内 c 的出现次数比 t 的少，现在一样多
                ge_cnt += 1  # 从 < 变成 >=

            while ge_cnt == kinds:  # 涵盖：所有字母的出现次数都是 >=
                if right - left < ans_right - ans_left:  # 找到更短的子串
                    ans_left, ans_right = left, right  # 记录此时的左右端点

                x = s[left]  # 左端点字母
                if diff[x] == 0:
                    # x 移出窗口之前，检查出现次数，
                    # 如果窗口内 x 的出现次数和 t 一样，
                    # 那么 x 移出窗口后，窗口内 x 的出现次数比 t 的少
                    ge_cnt -= 1  # 从 >= 变成 <
                diff[x] -= 1  # 左端点字母移出子串
                left += 1

        return "" if ans_left < 0 else s[ans_left: ans_right + 1]
''',
    call='Solution().minWindow("ABBCA", "ABC")',
    expect='BCA',
    views=[
        dict(type='text', fn=_cover),
        dict(type='string', var='s', label='s',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_ans_color, cell=100),
        dict(type='string', var='t', label='t　　　（上面 s 中：框 = 窗口 [left, right]，绿 = 目前最短的答案）', cell=80, index=False),
        dict(type='map', var='diff', label='diff = 窗口字母数 − t 字母数（0 ✓ = 刚好够；≥ 0 的种数就是 ge_cnt）', fmt=_diff_fmt, font=28, h=130),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'c', ('ge_cnt', 'ge_cnt', 'orange'), 'kinds',
           ('ans', 's[ans_left:ans_right + 1] if ans_left >= 0 else "-"', 'green')],
    captions={
        'diff = defaultdict': '把 `cnt_s` 和 `cnt_t` 合并成一个 `diff[x] = cnt_s[x] − cnt_t[x]`',
        'for c in t:': lambda S, B, ret: (f'统计 `t` 的字母：`c = {S.c!r}`' if -sum(S.diff.values()) < len(S.t) else '`t` 统计完毕'),
        'diff[c] -= 1': '窗口还是空的，`diff[{c!r}] = {diff[c]}`：还差 {-diff[c]} 个',
        'kinds = len(diff)': '`t` 有 `kinds = {kinds}` 种字母：等到 `ge_cnt == kinds` 时==窗口就涵盖了 t==',
        'ans_left, ans_right = -1': '答案端点先设成 `-1` 和 `len(s) = {ans_right}`（比任何窗口都长）',
        'ge_cnt = 0': '`ge_cnt`：窗口里有几种字母的个数 ≥ `t` 里的个数，先是 0',
        'left = 0': '左端点 `left = 0`',
        'for right, c in enumerate(s)': lambda S, B, ret: (f'枚举右端点 `right = {S.right}`，字母 `{S.c}` 进入窗口'
                                                           if 'right' not in B or S.right != B.right else '右端点枚举完了'),
        'diff[c] += 1': '`diff[{c!r}]`：`{B.diff[c]}` → `{diff[c]}`',
        'if diff[c] == 0': lambda S, B, ret: (f'`diff[{S.c!r}]` 恰好变成 0：`{S.c}` 从「不够」变成「够了」'
                                              if S.diff[S.c] == 0 else
                                              (f'`diff[{S.c!r}] = {S.diff[S.c]}` > 0：之前就够了，==不能重复计数=='
                                               if S.diff[S.c] > 0 else f'`diff[{S.c!r}] = {S.diff[S.c]}` < 0：`{S.c}` 还不够')),
        'ge_cnt += 1': '`ge_cnt = {ge_cnt}`：又有一种字母够了',
        'while ge_cnt == kinds': lambda S, B, ret: (f'`ge_cnt = kinds = {S.kinds}`：窗口 `{S.s[S.left:S.right + 1]}` ==涵盖 t== → 尝试缩短'
                                                    if S.ge_cnt == S.kinds else
                                                    f'`ge_cnt = {S.ge_cnt} < {S.kinds}`：没涵盖，继续右移 `right`'),
        'if right - left < ans_right': lambda S, B, ret: (
            '第一次涵盖（答案还是初始值），直接记录' if S.ans_left < 0 else
            f'窗口长 `{S.right - S.left + 1}`，比答案 `{S.ans_right - S.ans_left + 1}` 短 → 更新'
            if S.right - S.left < S.ans_right - S.ans_left else
            f'窗口长 `{S.right - S.left + 1}`，不比答案 `{S.ans_right - S.ans_left + 1}` 短，不更新'),
        'ans_left, ans_right = left, right': '记录答案 `s[{ans_left}..{ans_right}] = {s[ans_left:ans_right + 1]!r}`',
        'x = s[left]': '准备把左端点字母 `x = {x!r}` 移出窗口',
        'if diff[x] == 0': lambda S, B, ret: (f'`diff[{S.x!r}] = 0`：刚好够，移出后就==不够了==' if S.diff[S.x] == 0 else
                                              f'`diff[{S.x!r}] = {S.diff[S.x]}`：移出后仍然够（或本来就不需要），`ge_cnt` 不变'),
        'ge_cnt -= 1': '`ge_cnt = {ge_cnt}`：`{x}` 从 ≥ 变成 <，窗口不再涵盖 t',
        'diff[x] -= 1': '`diff[{x!r}]`：`{B.diff[x]}` → `{diff[x]}`',
        'left += 1': '左端点右移：`left = {left}`',
        'return': '返回最短涵盖子串 `{ret!r}`',
    },
    cards=dict(
        one_liner='右端点不断扩张，一旦涵盖 t 就收缩左端点，边缩边记最短',
        complexity='时间 `O(m + n)`，空间 `O(|Σ|)`',
        problem=['返回 `s` 中==涵盖 t 所有字符==（含重复）的最短子串，没有就返回 `""`',
                 '涵盖：子串里每个字母的出现次数 ≥ 它在 `t` 里的出现次数',
                 '示例：`s = "ADOBECODEBANC", t = "ABC"` → `"BANC"`',
                 '演示用 `s = "ABBCA", t = "ABC"` → `"BCA"`'],
        quote='用一个变量 `geCnt` 维护目前子串（窗口）中有 `geCnt` 种字母的出现次数大于等于 `t` 中相应字母的出现次数。',
        quote_src='—— 灵茶山艾府题解「优化」一节',
        idea=['和 209 题一样「越长越合法」：枚举右端点，涵盖时不断右移左端点',
              '每次都比较 52 个字母太慢 → 用 `ge_cnt` 计数，`ge_cnt == kinds` ==就是涵盖==',
              '`x` 进窗口后 `diff[x]` ==恰好变成 0== 才加一；离开前 `diff[x]` 为 0 才减一'],
        summary=['时间 `O(m + n)`：`left`、`right` 都只增不减',
                 '==不能在 diff[x] ≥ 0 时就加一==：同一字母会被重复统计（看演示里的第二个 B）',
                 '先更新答案，再移出左端点字母：缩到不涵盖为止',
                 '答案初始化成 `-1, len(s)`，最后 `ans_left < 0` 就返回空串',
                 '优化前写法：直接比较 `cnt_s >= cnt_t`，每次 `O(52)`，总 `O(52m + n)`'],
    ),
)
