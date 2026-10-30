S0, ML, MIN, MAX = 'aabcaab', 2, 3, 4


def _wl(S):
    if 'now' not in S:
        return None
    i = S.get('index')
    return 0 if i is None else i - S['minSize'] + (1 if S['_line'] >= 18 else 0)


def _wr(S):
    if 'now' not in S:
        return None
    i = S.get('index')
    return S['minSize'] - 1 if i is None else (i if S['_line'] >= 18 else i - 1)


CONFIG = dict(
    num=1297, title='子串的最大出现次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗 · dict 计数',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·贪心与思维', '难度分 1748'],
    code='''
class Solution(object):
    def maxFreq(self, s, maxLetters, minSize, maxSize):

        s_dict = {}
        now = s[:minSize]
        cnt_dict = {}
        for char in now:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1

        if len(cnt_dict) <= maxLetters:
            s_dict[now] = 1

        for index in range(minSize, len(s)):
            cnt_dict[now[0]] -= 1
            cnt_dict[s[index]] = cnt_dict.get(s[index], 0) + 1
            if cnt_dict[now[0]] == 0:
                cnt_dict.pop(now[0])
            now = now[1:] + s[index]
            if len(cnt_dict) <= maxLetters:
                s_dict[now] = s_dict.get(now, 0) + 1

        if len(s_dict) == 0:
            return 0
        return max(s_dict.values())
''',
    call=f'Solution().maxFreq({S0!r}, {ML}, {MIN}, {MAX})',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（框 = 当前子串 now，长度 minSize）', cell=96, h=190,
             window=(_wl, _wr)),
        dict(type='map', var='cnt_dict', label='cnt_dict（now 内字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='map', var='s_dict', label='s_dict（合法子串出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='text', h=80, size=28,
             fn=lambda S: f"`now = {S['now']!r}`，不同字母 `{len(S['cnt_dict'])}` 种（上限 {S['maxLetters']}）" if 'now' in S and 'cnt_dict' in S else '只检测长度为 minSize 的子串'),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('len(cnt_dict)', 'len(cnt_dict)', 'orange')],
    captions={
        's_dict = {}': '`s_dict` 记录每个合法子串出现的次数',
        'now = s[:minSize]': '`now`：第一个长度为 `minSize` 的子串 `{now!r}`',
        'cnt_dict = {}': '`cnt_dict` 记录 `now` 里每个字母的个数',
        'for char in now': lambda S, B, ret: (f'统计字母 `{S.char!r}`' if 'char' in S and sum(S.cnt_dict.values()) < len(S.now) else '统计完毕'),
        'cnt_dict[char] =': '`cnt_dict[{char!r}]` → {cnt_dict[char]}',
        'if len(cnt_dict) <= maxLetters:': lambda S, B, ret: (
            f'`{len(S.cnt_dict)} ≤ {S.maxLetters}`：不同字母数合格 → ==合法==' if len(S.cnt_dict) <= S.maxLetters
            else f'`{len(S.cnt_dict)} > {S.maxLetters}`：字母种类太多 → 不合法，不计入'),
        's_dict[now] = 1': '第一个子串合法：`s_dict[{now!r}] = 1`',
        'for index in range': lambda S, B, ret: (f'窗口右端新字符 `s[{S.index}] = {S.s[S.index]!r}`' if 'index' not in B or S.index != B.index else '遍历结束'),
        'cnt_dict[now[0]] -= 1': '`now` 最左边的 `{now[0]!r}` 要滑出去：`cnt_dict[{now[0]!r}]` → {cnt_dict[now[0]]}',
        'cnt_dict[s[index]] =': '新字符 `{s[index]!r}` 滑进来：`cnt_dict[{s[index]!r}]` → {cnt_dict[s[index]]}',
        'if cnt_dict[now[0]] == 0': lambda S, B, ret: (
            f'`{S.now[0]!r}` 的个数为 0 → ==pop 掉==，不然种类数会多算' if S.cnt_dict[S.now[0]] == 0
            else f'`{S.now[0]!r}` 还有 {S.cnt_dict[S.now[0]]} 个，保留'),
        'cnt_dict.pop': '弹出该字母，现在不同字母 `{len(cnt_dict)}` 种',
        'now = now[1:] + s[index]': '子串滑动一格：`now = {now!r}`',
        's_dict[now] = s_dict.get': '`s_dict[{now!r}]` → `{s_dict[now]}`',
        'if len(s_dict) == 0': '`s_dict` 有 `{len(s_dict)}` 种合法子串',
        'return max': '最大出现次数 `{max(s_dict.values())}`',
    },
    cards=dict(
        one_liner='子串若出现 k 次，它的所有子串至少也出现 k 次',
        complexity='时间 `O(n·minSize)`，空间 `O(n·minSize)`',
        problem=['找不同字母数 `≤ maxLetters`、长度在 `[minSize, maxSize]` 的子串',
                 '返回它出现次数的最大值',
                 f'本视频：`s = "{S0}"`，`maxLetters = {ML}`，`minSize = {MIN}` → `2`'],
        quote='若某个子串在s中出现了k次，那么其任意子串在s中也至少会出现k次。……我们只需要检测所有长度为minSize的字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案子串 s\' 出现 k 次 ⇒ 它里面长为 minSize 的子串也出现 ≥ k 次',
              '所以只扫长度为 minSize 的子串，用 ==滑动窗口== 维护字母种类',
              '合法就记进 `s_dict`，最后取最大值'],
        summary=['时间 `O(n·minSize)`，每次 `now[1:] + c` 要拷贝 minSize 个字符',
                 '易错：计数减到 0 要 `pop`，否则 `len(cnt_dict)` 不准',
                 '`s_dict` 为空时 `max` 会报错，所以先判断返回 0',
                 '对比灵神：灵神用 `s[left:i+1]` 切片、`defaultdict`；这里手动维护 `now`'],
    ),
)
