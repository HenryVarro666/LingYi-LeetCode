import string as _st


def _pair(S):
    if 'i' not in S or 'ans' not in S:
        return '先统计每个字符出现的次数，再把「字母 i」和「倒数第 i 个字母」配对'
    i, cnt = S['i'], S['cnt']
    if S['_line'] in (6, 7):
        a, b = _st.ascii_lowercase[i], _st.ascii_lowercase[-1 - i]
    else:
        a, b = _st.digits[i], _st.digits[-1 - i]
    return f"`|cnt['{a}'] − cnt['{b}']|` = `|{cnt.get(a, 0)} − {cnt.get(b, 0)}|` = =={abs(cnt.get(a, 0) - cnt.get(b, 0))}=="


def _hl(S, k):
    if 'i' not in S or 'ans' not in S:
        return False
    i = S['i']
    if S['_line'] in (6, 7):
        return k in (_st.ascii_lowercase[i], _st.ascii_lowercase[-1 - i])
    return k in (_st.digits[i], _st.digits[-1 - i])


CONFIG = dict(
    num=3889, title='镜像频次距离', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='Counter 计数 · 镜像字符配对',
    tags=[],
    code='''
class Solution:
    def mirrorFrequency(self, s: str) -> int:
        cnt = Counter(s)

        ans = 0
        for i in range(13):
            ans += abs(cnt[ascii_lowercase[i]] - cnt[ascii_lowercase[-1 - i]])
        for i in range(5):
            ans += abs(cnt[digits[i]] - cnt[digits[-1 - i]])
        return ans
''',
    setup='from string import ascii_lowercase, digits',
    call="Solution().mirrorFrequency('ab1z9')",
    expect=3,
    views=[
        dict(type='text', h=90, size=30, fn=_pair),
        dict(type='string', var='s', label='s', cell=100, h=190),
        dict(type='map', var='cnt', label='cnt（字符 → 出现次数，没出现的算 0）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter(s)': '先统计每个字符出现的次数：`cnt = {cnt}`',
        'ans = 0': '`ans` 累加所有镜像对的绝对差',
        'for i in range(13)': lambda S, B, r: ('字母 26 个，镜像配成 13 对：`a↔z`、`b↔y`、…、`m↔n`' if 'i' not in B
                                               else (f'`i` → {S.i}，看下一对' if S.get('i') is not None and S.i > B.i else '13 对字母都算完，接着算数字')),
        'for i in range(5)': lambda S, B, r: ('数字 10 个，镜像配成 5 对：`0↔9`、`1↔8`、…、`4↔5`' if B.i == 12
                                              else (f'`i` → {S.i}，看下一对' if S.i > B.i else '5 对数字都算完')),
        'ans += abs(cnt[ascii_lowercase[i]]': lambda S, B, r: (
            f"第 `{S.i}` 对：`{_st.ascii_lowercase[S.i]}` 出现 {S.cnt.get(_st.ascii_lowercase[S.i], 0)} 次，"
            f"`{_st.ascii_lowercase[-1 - S.i]}` 出现 {S.cnt.get(_st.ascii_lowercase[-1 - S.i], 0)} 次 → 差 =={S.ans - B.ans}==，`ans` = {S.ans}"),
        'ans += abs(cnt[digits[i]]': lambda S, B, r: (
            f"第 `{S.i}` 对：`{_st.digits[S.i]}` 出现 {S.cnt.get(_st.digits[S.i], 0)} 次，"
            f"`{_st.digits[-1 - S.i]}` 出现 {S.cnt.get(_st.digits[-1 - S.i], 0)} 次 → 差 =={S.ans - B.ans}==，`ans` = {S.ans}"),
        'return ans': '18 对镜像字符都算完，答案 `{ans}`',
    },
    cards=dict(
        one_liner='先数频次，再枚举镜像对累加绝对差',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['字符串由小写字母和数字组成；`a↔z`、`b↔y`…，`0↔9`、`1↔8`… 互为镜像',
                 '每个镜像对只算一次：`|freq(c) − freq(m)|`，求所有镜像对之和',
                 '本视频：`s = "ab1z9"` → `3`'],
        quote='对于小写英文字母：计算 a 和 z 的出现次数的绝对差。计算 b 和 y 的出现次数的绝对差。……计算 m 和 n 的出现次数的绝对差。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter(s)` 统计每个字符的次数，没出现的字符取值为 0',
              '字母前 13 个与倒数对应的配对：`ascii_lowercase[i]` 对 `ascii_lowercase[-1-i]`',
              '数字前 5 个同理，用 `digits[i]` 对 `digits[-1-i]`，累加所有绝对差'],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '只枚举前一半（字母 13 对、数字 5 对），避免同一对算两次',
                 '`Counter` 里查不到的字符返回 0，不用特判',
                 '`ascii_lowercase`、`digits` 来自 `string` 模块，本视频在 setup 里导入'],
    ),
)
