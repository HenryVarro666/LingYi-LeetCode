S0, ML, MIN, MAX = 'aabcaab', 2, 3, 4


def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['minSize'] + 1)


def _info(S):
    if 'char_cnt' not in S:
        return '只看长度恰好 `minSize` 的子串：越短，字母越少、出现越多'
    return f"窗口内不同字母 `{len(S['char_cnt'])}` 种，上限 `maxLetters = {S['maxLetters']}`"


CONFIG = dict(
    num=1297, title='子串的最大出现次数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 只看 minSize',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·贪心与思维', '难度分 1748'],
    code='''
class Solution:
    def maxFreq(self, s: str, maxLetters: int, minSize: int, _) -> int:
        str_cnt = defaultdict(int)
        char_cnt = defaultdict(int)

        for i, ch in enumerate(s):
            # 1. 进入窗口
            char_cnt[ch] += 1

            left = i - minSize + 1
            if left < 0:  # 窗口大小不足 minSize
                continue

            # 2. 更新统计量
            if len(char_cnt) <= maxLetters:
                str_cnt[s[left: i + 1]] += 1

            # 3. 离开窗口，为下一个循环做准备
            out = s[left]
            char_cnt[out] -= 1
            if char_cnt[out] == 0:
                del char_cnt[out]

        return max(str_cnt.values(), default=0)
''',
    call=f'Solution().maxFreq({S0!r}, {ML}, {MIN}, {MAX})',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（框 = 长为 minSize 的窗口）', cell=96, h=190,
             pointers={'i': 'blue'}, window=(_wl, 'i')),
        dict(type='map', var='char_cnt', label='char_cnt（窗口内字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='map', var='str_cnt', label='str_cnt（合法子串出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='text', h=80, size=28, fn=_info),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'cyan'), ('out', 'out', 'pink'), ('max(str_cnt.values(), default=0)', 'max(str_cnt.values(), default=0)', 'green')],
    captions={
        'str_cnt = defaultdict': '`str_cnt` 统计每个==合法子串==出现的次数',
        'char_cnt = defaultdict': '`char_cnt` 统计窗口内每个字母的次数，`len(char_cnt)` 就是不同字母数',
        'for i, ch in enumerate': lambda S, B, ret: (f'`s[{S.i}] = {S.ch!r}` 要进入窗口' if 'i' not in B or S.i != B.i else '遍历结束'),
        'char_cnt[ch] += 1': '`{ch!r}` 进入窗口：`char_cnt[{ch!r}] = {char_cnt[ch]}`',
        'left = i - minSize + 1': '窗口左端点 `left = {i} − {minSize} + 1 = {left}`',
        'if left < 0': lambda S, B, ret: (f'`left = {S.left} < 0`：窗口还不满 {S.minSize} 个，先继续进' if S.left < 0
                                          else f'`left = {S.left} ≥ 0`：窗口刚好 `minSize` 个字符了'),
        'continue': '继续扩大窗口',
        'if len(char_cnt) <= maxLetters': lambda S, B, ret: (
            f'不同字母 `{len(S.char_cnt)} ≤ {S.maxLetters}` → ==合法==，可以统计' if len(S.char_cnt) <= S.maxLetters
            else f'不同字母 `{len(S.char_cnt)} > {S.maxLetters}` → 不合法，跳过'),
        'str_cnt[s[left: i + 1]] += 1': '子串 `{s[left:i+1]!r}` 出现次数 → `{str_cnt[s[left:i+1]]}`',
        'out = s[left]': '窗口最左边的 `{out!r}` 要离开',
        'char_cnt[out] -= 1': '`char_cnt[{out!r}]` 减一 → `{char_cnt[out]}`',
        'if char_cnt[out] == 0': lambda S, B, ret: (f'`{S.out!r}` 的次数变成 0：窗口里已经没有它了 → ==删除==，不同字母数才会减少'
                                                     if S.char_cnt[S.out] == 0 else f'`{S.out!r}` 还剩 {S.char_cnt[S.out]} 个，保留'),
        'del char_cnt[out]': '删掉 `{out!r}`，`len(char_cnt)` 变为 {len(char_cnt)}',
        'return max': '出现最多的合法子串出现 `{max(str_cnt.values(), default=0)}` 次',
    },
    max_steps=90,
    cards=dict(
        one_liner='子串越短越容易合法、出现越多，只看长度 minSize 就够了',
        complexity='时间 `O((n−minSize)·minSize)`，空间同阶',
        problem=['找一个子串：不同字母数 `≤ maxLetters`，长度在 `[minSize, maxSize]` 内',
                 '求它在 `s` 中出现次数的最大值（可重叠）',
                 f'本视频：`s = "{S0}"`，`maxLetters = {ML}`，`minSize = {MIN}` → `2`（`"aab"`）'],
        quote='子串越短，包含的不同字母个数越少，越能满足 ≤ maxLetters 的要求。子串越短，子串在 s 中的出现次数也越多。……只需考虑长度恰好等于 minSize 的子串（maxSize 是多余的）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长串一定包含合法的短串，且短串出现次数不会更少 → ==maxSize 用不上==',
              '定长滑窗：==进入窗口 → 更新统计 → 离开窗口==',
              '`char_cnt` 数字母种数：减到 0 就删键；`str_cnt` 记每个合法子串的次数'],
        summary=['时间 `O((n−minSize)·minSize)`，切片和哈希都要 `O(minSize)`；`minSize ≤ 26` 所以可行',
                 '易错：`char_cnt` 减到 0 必须 `del`，否则 `len` 会多算',
                 '若不保证 `minSize ≤ 26`，要用字典树代替字符串哈希',
                 '第四个参数 `maxSize` 用 `_` 占位，题解里根本没用到'],
    ),
)
