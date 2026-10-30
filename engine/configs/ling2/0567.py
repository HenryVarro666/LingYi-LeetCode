S1, S2 = 'abb', 'eabcbba'


def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['m'] + 1)


def _less_txt(S):
    if 'less' not in S:
        return '`cnt[x]` = s1 中 x 的次数 − 窗口中 x 的次数；`> 0` 表示窗口里 x ==还不够=='
    pos = [k for k, v in S['cnt'].items() if v > 0]
    show = '、'.join(pos) if pos else '无'
    return f'`less = {S["less"]}`：窗口中次数==不足==的字母有 {show}'


CONFIG = dict(
    num=567, title='字符串的排列', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='定长滑动窗口 · less 计数 O(n)',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m = len(s1)
        if m > len(s2):
            return False

        cnt = Counter(s1)
        less = len(cnt)
        for i, c in enumerate(s2):
            # 1. 进入窗口
            cnt[c] -= 1
            if cnt[c] == 0:
                less -= 1

            if i < m - 1:  # 窗口大小不足 m
                continue

            # 2. 判断子串 t 的每种字母的出现次数是否均与 s1 的相同
            if less == 0:
                return True

            # 3. 离开窗口，为下一个循环做准备
            out = s2[i - m + 1]
            if cnt[out] == 0:
                less += 1
            cnt[out] += 1
        return False
''',
    call=f'Solution().checkInclusion({S1!r}, {S2!r})',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1（要找它的排列）', cell=96, h=150),
        dict(type='string', var='s2', label='s2（框 = 长为 m 的窗口 t）', cell=110, h=210,
             pointers={'i': 'blue'}, window=(_wl, 'i')),
        dict(type='map', var='cnt', label='cnt（s1 次数 − 窗口次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', h=100, size=30, fn=_less_txt),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c'), ('less', 'less', 'orange'), ('out', 'out', 'pink')],
    captions={
        'm = len(s1)': '窗口长度固定为 `m = {m}`',
        'if m > len(s2)': '`s1` 不比 `s2` 长，可以继续',
        'cnt = Counter(s1)': '`cnt` 先统计 `s1` 每种字母的次数：`{dict(cnt)}`',
        'less = len(cnt)': '`less`：窗口中次数==小于== s1 的字母种数，一开始 = `{less}`',
        'for i, c in enumerate(s2)': lambda S, B, ret: (f'`s2[{S.i}] = {S.c!r}` 进入窗口' if 'i' not in B or S.i != B.i
                                                        else '遍历结束'),
        'cnt[c] -= 1': '`cnt[{c!r}]` 减一 → `{cnt[c]}`',
        'if cnt[c] == 0': lambda S, B, ret: (f'`cnt[{S.c!r}]` 变成 0：窗口里 {S.c!r} 的次数==刚好够了==' if S.cnt[S.c] == 0
                                             else (f'`cnt[{S.c!r}] = {S.cnt[S.c]}`，还不够' if S.cnt[S.c] > 0
                                                   else f'`cnt[{S.c!r}] = {S.cnt[S.c]}`，less 不变')),
        'less -= 1': '少了一种“不足”的字母 → `less = {less}`',
        'if i < m - 1': lambda S, B, ret: (f'`i = {S.i} < m − 1`：窗口还不满 {S.m} 个，先不判断' if S.i < S.m - 1
                                           else f'窗口 `{S.s2[S.i - S.m + 1:S.i + 1]!r}` 长度为 {S.m}，可以判断'),
        'continue': '继续往右扩',
        'if less == 0': lambda S, B, ret: ('`less == 0`：没有不足的字母，长度又相同 → ==也不会有多余的==，找到了！' if S.less == 0
                                           else f'`less = {S.less} ≠ 0`：还有字母不够，不是 s1 的排列'),
        'return True': '返回 `True`：子串 `{s2[i - m + 1:i + 1]!r}` 是 `{s1!r}` 的排列',
        'out = s2[i - m + 1]': '窗口最左边的 `{out!r}` 准备离开',
        'if cnt[out] == 0': lambda S, B, ret: (f'`cnt[{S.out!r}]` 本来是 0（刚好够），移出后就==不够了==' if S.cnt[S.out] == 0
                                               else f'`cnt[{S.out!r}] = {S.cnt[S.out]} ≠ 0`，移出后 less 不变'),
        'less += 1': '多了一种不足的字母 → `less = {less}`',
        'cnt[out] += 1': '`cnt[{out!r}]` 加一 → `{cnt[out]}`',
        'return False': '没有找到，返回 `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='定长滑窗 + less：只关心“不足”的字母有几种',
        complexity='时间 `O(n)`（n = len(s2)），空间 `O(|Σ|)`',
        problem=['判断 `s2` 是否包含 `s1` 的某个==排列==（作为连续子串）',
                 '示例：`s1 = "ab", s2 = "eidbaooo"` → `true`（含 `"ba"`）',
                 '本视频：`s1 = "abb", s2 = "eabcbba"` → `true`（含 `"bba"`）'],
        quote='用一个变量 less 维护 t 中有 less 种字母的出现次数小于 s1 中字母的出现次数。……如果 less=0，说明 t 中每种字母的出现次数一定都恰好等于 s1 的。',
        quote_src='—— 灵茶山艾府题解（优化写法）',
        idea=['长为 m 的子串 t 每种字母次数都和 s1 相同 ⇔ t 是 s1 的排列',
              '定长滑窗三步：==进入窗口 → 判断 → 离开窗口==',
              '`cnt` 从 s1 的次数往下减；变成 0 时 `less -= 1`，从 0 变正时 `less += 1`'],
        summary=['时间 `O(n)`，比直接比较两个 Counter 的 `O(26n)` 更快',
                 '为什么 less = 0 就够了？长度相同，没有“不足”就不可能“多余”',
                 '易错：离开窗口时要==先判断== `cnt[out] == 0` 再加一',
                 '主写法用 `del cnt[c]` + `len(cnt) == 0`，思路相同；本视频选 less 写法',
                 '定长滑窗模板同 1456 题：入 → 更新/判断 → 出'],
    ),
)
