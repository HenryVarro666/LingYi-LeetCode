S1, N1, S2, N2 = 'baba', 11, 'baab', 1


def _s2pos(S):
    p = S.get('pos')
    return p if isinstance(p, int) and p < len(S['s2']) else None


def _s1pos(S):
    if S.get('char') is None or 's1' not in S:
        return None
    return S.get('_s1i')


def _txt(S):
    if 'cnt1' not in S:
        return '用 s1 去贪心匹配 s2：`s2[pos]` 是下一个要匹配的字符'
    return f"已用 `{S['cnt1']}` 个 s1，完整匹配了 `{S['cnt2']}` 个 s2，下一个要匹配 `s2[{S['pos']}]`"


CONFIG = dict(
    num=466, title='统计重复个数', difficulty='Hard', category='字符串',
    author='yiduobo', technique='贪心匹配 + 找循环节',
    tags=['图论算法'],
    code='''
class Solution(object):
    def getMaxRepetitions(self, s1, n1, s2, n2):

        if not n1:
            return 0

        cnt1 = cnt2 = 0
        pos_dict = {}
        pos = 0
        while True:
            cnt1 += 1
            for char in s1:
                if char == s2[pos]:
                    pos += 1
                    if pos == len(s2):
                        cnt2 += 1
                        pos = 0

            if cnt1 == n1:
                return cnt2 // n2

            if pos in pos_dict:
                unloop1, unloop2 = pos_dict[pos]
                loop1 = cnt1 - unloop1
                loop2 = cnt2 - unloop2

                res = unloop2 + (n1 - unloop1) // loop1 * loop2
                for index in range((n1 - unloop1) % loop1):
                    for char in s1:
                        if char == s2[pos]:
                            pos += 1
                            if pos == len(s2):
                                res += 1
                                pos = 0
                
                return res // n2

            else:
                pos_dict[pos] = [cnt1, cnt2]
''',
    call=f'Solution().getMaxRepetitions({S1!r}, {N1}, {S2!r}, {N2})',
    expect=7,
    views=[
        dict(type='string', var='s1', label='s1（每个 s1 从头到尾扫一遍，当前字符见下方 char）', cell=90, h=140),
        dict(type='string', var='s2', label='s2（pos = 下一个要匹配的位置）', cell=90, h=170,
             pointers={_s2pos: 'pink'}, pointer_labels={_s2pos: 'pos'}),
        dict(type='map', var='pos_dict', label='pos_dict：pos → [cnt1, cnt2]', fmt=lambda k, v: f'pos={k}: 用了 {v[0]} 个 s1，匹配 {v[1]} 个 s2', h=230, font=28),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=['cnt1', 'cnt2', 'pos', ('char', 'char', 'cyan'), ('res', 'res', 'green')],
    skip=['while True', 'for char in s1', 'pos += 1', 'pos = 0', 'if not n1', 'pos_dict = {}', 'loop1 = cnt1', 'loop2 = cnt2'],
    max_steps=120,
    captions={
        'cnt1 = cnt2 = 0': '`cnt1` = 已经用掉几个 s1，`cnt2` = 已经完整匹配几个 s2；`pos` = 下一个要匹配 `s2[pos]`；`pos_dict` 记“每个 pos 第一次出现时的 (cnt1, cnt2)”',
        'cnt1 += 1': '拿出第 `{cnt1}` 个 s1，从头到尾贪心匹配 s2',
        'if char == s2[pos]': lambda S, B, r: (f'`{S.char}` == `s2[{S.pos}]`：匹配上了 → `pos` 前进到 {S.pos + 1}' if S.char == S.s2[S.pos]
                                               else f'`{S.char}` ≠ `s2[{S.pos}] = {S.s2[S.pos]}`：这个字符用不上，跳过（贪心：能匹配就匹配）'),
        'if pos == len(s2)': lambda S, B, r: (f'`pos = {S.pos}`，`len(s2) = {len(S.s2)}`：' + ('s2 匹配完一整个 → 下一步 `cnt2` +1，`pos` 回到 0' if S.pos == len(S.s2) else 's2 还没匹配完')),
        'cnt2 += 1': 's2 完整匹配了一个：`cnt2 = {cnt2}`，`pos` 回到 0',
        'if cnt1 == n1': lambda S, B, r: (f'`cnt1 = {S.cnt1}`，`n1 = {S.n1}`：' + ('s1 用完了 → 直接返回 `cnt2 // n2`' if S.cnt1 == S.n1 else '还没用完')),
        'if pos in pos_dict': lambda S, B, r: (f'一个 s1 匹配完后停在 `pos = {S.pos}`：' + ('以前出现过！从那次到现在就是一个循环节' if S.pos in S.pos_dict else '第一次出现，先记下来')),
        'pos_dict[pos] = [cnt1, cnt2]': '记录：`pos = {pos}` 第一次出现时，用了 `{cnt1}` 个 s1、匹配了 `{cnt2}` 个 s2',
        'unloop1, unloop2 = pos_dict': '进入循环前用了 `unloop1 = {unloop1}` 个 s1，匹配了 `unloop2 = {unloop2}` 个 s2；循环节：`loop1 = {cnt1 - unloop1}` 个 s1 匹配 `loop2 = {cnt2 - unloop2}` 个 s2，之后每轮都一样',
        'res = unloop2': '剩下 `n1 - unloop1 = {n1 - unloop1}` 个 s1，整循环 `{(n1 - unloop1) // (cnt1 - unloop1)}` 轮：`res = unloop2 + 轮数 × loop2 = {res}`',
        'for index in range': '整循环之后还剩 `(n1 - unloop1) % loop1 = {(n1 - unloop1) % (cnt1 - unloop1)}` 个 s1，从当前 `pos` 接着手动匹配',
        'res += 1': '又匹配完一个 s2：`res = {res}`',
        'return res // n2': '`res = {res}` 个 s2，每 `n2 = {n2}` 个凑成一个 str2 → ==返回 {res // n2}==',
        'return cnt2 // n2': '`cnt2 // n2` = =={cnt2 // n2}==',
    },
    cards=dict(
        one_liner='用 s1 贪心匹配 s2，像找循环小数一样找循环节',
        complexity='时间 `O(|s1|·|s2|)`，空间 `O(|s2|)`',
        problem=['`str = [s, n]` 表示 `s` 重复 `n` 次；`str1 = [s1, n1]`，`str2 = [s2, n2]`',
                 '求最大整数 `M`，使 `[str2, M]` 能从 `str1` 里删去若干字符得到',
                 '示例：`s1="acb", n1=4, s2="ab", n2=2` → `2`',
                 f'本视频：`s1={S1!r}, n1={N1}, s2={S2!r}, n2={N2}` → `7`'],
        quote='首先需要明确的一点是，在匹配时应该采用贪心法，尽可能地使用s1中靠前的字符去匹配s2中的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['这题像小数找循环节：要先找到“进入循环的长度”和“循环长度”',
              '每用完一个 s1，记下停在 s2 的哪个 `pos`；同一个 `pos` 再出现，说明恰好整数个 s1 匹配了整数个 s2',
              '用乘除法算出整循环能匹配多少，剩下不够一轮的 s1 再从 `pos` 手动匹配'],
        summary=['时间 `O(|s1|·|s2|)`：`pos` 只有 `|s2|` 种，最多扫这么多个 s1 就会出现循环',
                 '最后要 `// n2`：数的是 s2 的个数，不是 str2 的个数',
                 '原文为 Python 2 写法，其中的 `/` 是整数除法，已改为 `//`（共 3 处）',
                 '没有循环（`cnt1 == n1` 先到）时直接返回 `cnt2 // n2`'],
    ),
)
