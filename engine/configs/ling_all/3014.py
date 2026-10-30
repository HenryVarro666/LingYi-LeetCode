def _tier(S, i, v):
    return ['blue', 'green', 'orange', 'pink'][min(i // 8, 3)]


def _txt(S):
    if 'k' not in S:
        return '8 个按键，字母均匀分配：前 8 个字母按 1 次，接着 8 个按 2 次……'
    k, rem = S['k'], S['rem']
    s = f"`k = {k}`：每个按键先分 {k} 个字母，共 `4k(k+1) = {4*k*(k+1)}` 次"
    return s + f"；余下 `{rem}` 个字母各按 `{k+1}` 次"


CONFIG = dict(
    num=3014, title='输入单词需要的最少按键次数 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='均匀分配 · 公式',
    code='''
class Solution:
    def minimumPushes(self, word: str) -> int:
        k, rem = divmod(len(word), 8)
        return (k * 4 + rem) * (k + 1)
''',
    call="Solution().minimumPushes('abcdefghijklmnopqrstu')",
    expect=39,
    views=[
        dict(type='string', var='word', label='word（蓝=按1次 绿=按2次 橙=按3次）', cell=60, h=240, color=_tier),
        dict(type='text', fn=_txt, h=120, size=30),
    ],
    watch=['k', 'rem'],
    captions={
        'divmod': '`len(word) = {len(word)}`，除以 8 个按键：每键分 `k = {k}` 个，余 `rem = {rem}` 个',
        'return': '`({k}×4 + {rem}) × ({k}+1)` = =={ret}==：先算整轮，再算余下字母多按的一档',
    },
    cards=dict(
        one_liner='字母互不相同，均匀塞进 8 个按键，次数最少',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`word` 由互不相同的小写字母组成，可以任意重映射按键 2~9',
                 '一个键上第 `j` 个字母要按 `j` 次，求输入 `word` 的最少按键数',
                 '示例：`"xycdefghij"` → `12`；本视频：21 个字母 → `39`'],
        quote='由于 word 中的所有字母互不相同，所以只需均匀分配字母到这 8 个按键中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个字母出现一次，位置越靠前越省：每键各放 `k` 个，按 `1+2+…+k` 次',
              '共 8 个键：`8·(1+…+k) = 4k(k+1)`',
              '剩下 `n mod 8` 个字母放在第 `k+1` 档，每个按 `k+1` 次'],
        summary=['时间、空间都是 `O(1)`，答案 `(4k + n mod 8)(k + 1)`',
                 '易错：键数是 8（2~9），不是 9 或 10',
                 '`divmod(len(word), 8)` 一次得到商和余数',
                 '进阶：第 3016 题字母可重复，需先按频率从大到小分配'],
        after=[dict(heading='验算本例', lines=['`n = 21`，`k = 2`，`rem = 5`',
                                              '整轮：`4×2×3 = 24`；余下 5 个字母各按 3 次 = 15',
                                              '合计 `24 + 15 = 39`，与代码一致'])],
    ),
)
