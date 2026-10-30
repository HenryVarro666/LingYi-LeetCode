def _top(S):
    if 'now' not in S:
        return ''
    s, r, n, l = S['s'], S['res'], S['now'], S['l']
    a = s[r:r + l]
    return f"候选后缀 `s[{r}:] = \"{s[r:]}\"`，对手 `s[{n}:] = \"{s[n:]}\"`，已相同的前缀长度 `l = {l}`"


def _cmp(S, B, ret):
    s, r, n, l = S.s, S.res, S.now, S.l
    x, y = s[r + l], s[n + l]
    if x == y:
        return f"`s[{r}+{l}] = '{x}'` == `s[{n}+{l}] = '{y}'` → 看不出大小，继续比下一位"
    return f"`s[{r}+{l}] = '{x}'` ≠ `s[{n}+{l}] = '{y}'` → 这一位能分出大小"


CONFIG = dict(
    num=1163, title='按字典序排在最后的子串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='双指针比较后缀（最大后缀）',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def lastSubstring(self, s):

        res = 0
        now = 1
        l = 0
        while now + l < len(s):
            if s[res + l] == s[now + l]:
                l += 1
            elif s[res] < s[now + l]:
                res = now + l
                now = res + 1
                l = 0
            elif s[res + l] < s[now + l]:
                res = now
                now += 1
                l = 0
            else:
                now += l + 1
                l = 0

        return s[res:]
''',
    call='Solution().lastSubstring("cacacb")',
    expect='cb',
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（粉 = res 候选起点，蓝 = now 对手起点）', pointers={'res': 'pink', 'now': 'blue'},
             color=lambda S, i, v: (None if 'l' not in S else
                                    'green' if (S['res'] <= i < S['res'] + S['l']) else
                                    'cyan' if (S['now'] <= i < S['now'] + S['l']) else None),
             h=330),
        dict(type='text', fn=lambda S: f"当前候选答案：`\"{S['s'][S['res']:]}\"`" if 'res' in S else '', size=28, h=80),
    ],
    watch=[('res', 'res', 'pink'), ('now', 'now', 'blue'), ('l', 'l', 'yellow')],
    captions={
        'res = 0': '`res`：当前最大后缀的起点（备选答案），先假设是 0',
        'now = 1': '`now`：用来挑战 res 的另一个后缀起点；`l` 记录两者已相同的前缀长度',
        'l = 0': '`l`：两个后缀已经比较过、相同的长度',
        'while now + l': lambda S, B, r: (f'`now + l = {S.now + S.l} < {len(S.s)}`，还能继续比' if S.now + S.l < len(S.s)
                                           else f'`now + l = {S.now + S.l}` 到头了 → 没有更大的后缀，`res = {S.res}` 就是答案'),
        'if s[res + l] == s[now + l]': _cmp,
        'l += 1': '前 `{l}` 位都相同，`l` → {l}，继续往后比',
        'elif s[res] < s[now + l]': lambda S, B, r: (
            f"`s[res] = '{S.s[S.res]}' < s[now+l] = '{S.s[S.now+S.l]}'` → ==成立==：res 的首字母比这位还小" if S.s[S.res] < S.s[S.now + S.l]
            else f"`s[res] = '{S.s[S.res]}'` 不小于 `s[now+l] = '{S.s[S.now+S.l]}'`，看下一种情况"),
        'res = now + l': '`res` 直接跳到 `now + l = {res}`：中间的位置不可能更大（原文证明），全部跳过',
        'now = res + 1': '`now` 重置为 `res + 1 = {now}`',
        'elif s[res + l] < s[now + l]': lambda S, B, r: (
            f"`'{S.s[S.res+S.l]}' < '{S.s[S.now+S.l]}'` → ==成立==：now 开头的后缀更大" if S.s[S.res + S.l] < S.s[S.now + S.l]
            else f"`'{S.s[S.res+S.l]}' < '{S.s[S.now+S.l]}'` 不成立 → res 的后缀更大"),
        'res = now': 'now 的后缀更大 → `res = now = {res}`',
        'now += 1': '`now` → {now}，挑战下一个起点',
        'now += l + 1': 'res 的后缀更大：now 到 `now+l` 之间都不可能赢，直接跳到 `{now}`',
        'return': '返回 `s[{res}:]` = `"{s[res:]}"`，最大子串一定是某个后缀',
    },
    skip=['l = 0'],
    max_steps=80,
    cards=dict(
        one_liner='最大子串一定是后缀；双指针比后缀，输的一方整段跳过',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给字符串 `s`，返回它所有子串中==字典序最大==的那个',
                 '示例：`"abab"` → `"bab"`；`"leetcode"` → `"tcode"`',
                 '本视频：`"cacacb"` → `"cb"`'],
        quote='字典序最大的子串必然是一个后缀字符串……直接枚举答案后缀字符串的起始字符位置res，然后从now = res + 1开始对比s[res:]与s[now:]的字典序大小。',
        quote_src='—— yiduobo 题解原文',
        idea=['证明：最大子串若不是后缀，往后补字符会更大，矛盾 → 只比较后缀',
              '`res` 是候选，`now` 是挑战者，`l` 是已相同的前缀长度',
              '相等就 `l+1`；挑战者大：`res` 跳到 `now`（或 `now+l`）；挑战者小：`now` 跳过 `l+1` 位'],
        summary=['时间 `O(n)`，空间 `O(1)`（相当于最大后缀的 Duval 式双指针）',
                 '跳过的正确性来自原文的证明：被跳过的位置开头的后缀不可能更大',
                 '易错：循环条件是 `now + l < len(s)`，访问的是 `s[now + l]`',
                 '另一种做法：后缀数组排序取最后一个，但更重',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
