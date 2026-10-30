S0, T0, K0 = 'abcdabab', 'ababcdab', 4
L0 = len(S0) // K0
PAL = ['blue', 'pink', 'green', 'purple']


def _blk(S, i, v):
    return PAL[(i // L0) % 4]


def _parts(S):
    if 'n' not in S:
        return f'`s = "{S0}"`，`t = "{T0}"`，`k = {K0}`：每块长 `{len(S0)} // {K0} = {L0}`'
    ps = [S0[i:i + L0] for i in range(0, len(S0), L0)]
    pt = [T0[i:i + L0] for i in range(0, len(T0), L0)]
    return f's 切成 `{" | ".join(ps)}`　　t 切成 `{" | ".join(pt)}`'


CONFIG = dict(
    num=3365, title='重排子字符串以形成目标字符串', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='子串当元素 · 哈希表计数',
    tags=['灵神题单', '难度分 1514'],
    code='''
class Solution:
    def isPossibleToRearrange(self, s: str, t: str, k: int) -> bool:
        n = len(s)
        k = n // k
        cnt_s = Counter(s[i: i + k] for i in range(0, n, k))
        cnt_t = Counter(t[i: i + k] for i in range(0, n, k))
        return cnt_s == cnt_t
''',
    call=f'Solution().isPossibleToRearrange("{S0}", "{T0}", {K0})',
    expect=True,
    views=[
        dict(type='text', fn=_parts, size=28),
        dict(type='string', var='s', label='s（同色 = 同一块）', color=_blk, cell=70),
        dict(type='string', var='t', label='t', color=_blk, cell=70),
        dict(type='map', var='cnt_s', label='cnt_s：s 的每块出现次数', fmt=lambda k, v: f'"{k}" × {v}'),
        dict(type='map', var='cnt_t', label='cnt_t：t 的每块出现次数', fmt=lambda k, v: f'"{k}" × {v}'),
    ],
    watch=['n', ('每块长 k', 'k', 'blue')],
    captions={
        'n = len(s)': '`n = {n}`',
        'k = n // k': '重新定义：每块长度 `k = n // k = {k}`（分成几块是固定的）',
        'cnt_s = Counter': '把 s 每 `{k}` 个字符切一块，统计每块出现几次：`{dict(cnt_s)}`',
        'cnt_t = Counter': '对 t 同样切块计数：`{dict(cnt_t)}`',
        'return cnt_s': '子串可随意重排 ⇔ 两边的块==多重集相同== → `cnt_s == cnt_t` 为 `{ret}`',
    },
    cards=dict(
        one_liner='交换 s 的两块，等于交换 t 的两块：块可随意重排',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `s` 切成 `k` 个等长子串，任意重排后拼接，能否得到 `t`（`s`、`t` 互为字母异位词）',
                 '示例：`s = "abcd"`，`t = "cdab"`，`k = 2` → `true`',
                 '本视频：`s = "abcdabab"`，`t = "ababcdab"`，`k = 4` → `true`'],
        quote='最终只需要关心 s 是否等于 t，那么交换 s 中的两个子串，等同于交换 t 中的两个子串。所以可以视作 s 和 t 中的子串可以随意重排。',
        quote_src='—— 灵茶山艾府题解',
        idea=['块长固定为 `n // k`，切法唯一',
              '块可以随意重排 → 只看每种块出现几次',
              '思路和 242 题判断字母异位词一样，只是元素从字符变成了子串'],
        result='两边都是 `"ab" × 3`、`"cd" × 1` → True ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`k` 是块数，块长是 `n // k`，代码里把 `k` 覆盖成了块长',
                 '题解还给了排序写法：两边块排序后比较，`O(n log k)`',
                 '同类题：242 有效的字母异位词'],
    ),
)
