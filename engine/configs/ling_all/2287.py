CONFIG = dict(
    num=2287, title='重排字符形成目标字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='计数 + 取最小商',
    tags=[],
    code='''
class Solution:
    def rearrangeCharacters(self, s: str, target: str) -> int:
        cnt_s = Counter(s)
        cnt_t = Counter(target)
        return min(cnt_s[ch] // cnt for ch, cnt in cnt_t.items())
''',
    call="Solution().rearrangeCharacters('aabbbcc', 'abb')",
    expect=1,
    views=[
        dict(type='string', var='s', label='s（原料）', cell=90, h=150),
        dict(type='string', var='target', label='target（一份要用的字符）', cell=90, h=150),
        dict(type='map', var='cnt_s', label='cnt_s（s 里每个字母有几个）', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
        dict(type='map', var='cnt_t', label='cnt_t（一份 target 要几个）', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
        dict(type='text', h=110, size=30,
             fn=lambda S: ('各字母够凑几份：' + '，'.join(f"`{c}`: `{S['cnt_s'][c]} // {k}` = =={S['cnt_s'][c] // k}==" for c, k in S['cnt_t'].items())
                           if 'cnt_t' in S and 'cnt_s' in S and S['_line'] == 5 else '')),
    ],
    watch=[('len(s)', 'len(s)'), ('len(target)', 'len(target)')],
    captions={
        'cnt_s = Counter': '统计 `s` 每个字母的个数：`{dict(cnt_s)}`',
        'cnt_t = Counter': '统计 `target` 每个字母的个数：`{dict(cnt_t)}`',
        'return min': lambda S, B, ret: f'每种字母能凑出 `cnt_s[ch] // cnt` 份，==取最小值== `{ret}`：最缺的字母决定份数',
    },
    cards=dict(
        after=[dict(heading='为什么取最小值', lines=['本视频：`a` 够 `2 // 1 = 2` 份，`b` 够 `3 // 2 = 1` 份',
                                                    '拼第 2 份时 `b` 已不够（只剩 1 个，要 2 个）',
                                                    '所以瓶颈是 `b`，答案 `min(2, 1)` = ==1==',
                                                    '`c` 不在 target 里，不参与比较'])],
        one_liner='最缺的那种字母，决定能拼几份',
        complexity='时间 `O(n+m)`，空间 `O(|Σ|)`',
        problem=['从 `s` 里取字符并重排，最多能拼出几份 `target`',
                 '示例：`s = "abcba", target = "abc"` → `1`',
                 '本视频：`s = "aabbbcc", target = "abb"` → `1`'],
        quote='枚举 cntT[i]>0 的字母 i，计算 ⌊cntS[i]/cntT[i]⌋ 的最小值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字符可以随便重排，所以只看每个字母够不够',
              's 有 7 个 a、一份要 2 个 a，那 a 最多撑 `7 // 2 = 3` 份',
              '每种字母各算一个商，==取最小==就是答案'],
        summary=['时间 `O(n+m)`，空间 `O(|Σ|)`，|Σ| = 26',
                 '`Counter` 对不存在的键返回 0，所以 `cnt_s[ch]` 不会报错',
                 '易错：用整除 `//`，别用普通除法；与 1189 题“气球”相同'],
    ),
)
