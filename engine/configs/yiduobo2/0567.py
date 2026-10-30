S1, S2 = 'abb', 'eabcbba'


def _wl(S):
    i = S.get('index')
    if i is None:
        return None
    return max(0, i - len(S['s1']) + 1)


def _eq_txt(S):
    if 'now_dict' not in S:
        return '思路：长度相同 + ==每个字符出现次数完全一致== ⇔ 是 s1 的排列'
    eq = S['now_dict'] == S['count_dict']
    return '`now_dict == count_dict` → ' + ('==相等==：找到排列！' if eq else '不相等')


CONFIG = dict(
    num=567, title='字符串的排列', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='滑动窗口 · 两个 dict 比较字符次数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def checkInclusion(self, s1, s2):
        if len(s1) > len(s2):
            return False

        count_dict = {}
        for char in s1:
            count_dict[char] = count_dict.get(char, 0) + 1

        now_dict = {}
        for index in range(len(s1)):
            now_dict[s2[index]] = now_dict.get(s2[index], 0) + 1
        if count_dict == now_dict:
            return True

        for index in range(len(s1), len(s2)):
            remove = s2[index - len(s1)]
            now_dict[remove] -= 1
            now_dict[s2[index]] = now_dict.get(s2[index], 0) + 1
            if now_dict[remove] == 0:
                now_dict.pop(remove)

            if now_dict == count_dict:
                return True

        return False
''',
    call=f'Solution().checkInclusion({S1!r}, {S2!r})',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1', cell=96, h=150),
        dict(type='string', var='s2', label='s2（框 = 长度为 len(s1) 的窗口）', cell=110, h=210,
             pointers={'index': 'blue'}, window=(_wl, 'index')),
        dict(type='map', var='count_dict', label='count_dict（s1 每个字符的次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='map', var='now_dict', label='now_dict（当前窗口每个字符的次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=80, size=28, fn=_eq_txt),
    ],
    watch=[('index', 'index', 'blue'), ('remove', 'remove', 'pink')],
    captions={
        'if len(s1) > len(s2)': '子串长度必须等于 `len(s1)`：s1 更长就不可能',
        'count_dict = {}': '`count_dict` 统计 s1 中每个字符出现的次数',
        'for char in s1': lambda S, B, ret: ('s1 统计完毕' if sum(S.count_dict.values()) == len(S.s1)
                                             else f'数 s1 的字符 {S.char!r}'),
        'count_dict[char] = count_dict.get': '`count_dict[{char!r}] = {count_dict[char]}`',
        'now_dict = {}': '`now_dict`：窗口中每个字符的次数',
        'for index in range(len(s1)):': lambda S, B, ret: (f'先放入第一个窗口的 `s2[{S.index}] = {S.s2[S.index]!r}`'
                                                           if 'index' not in B or S.index != B.index else '第一个窗口放满了'),
        'now_dict[s2[index]] = now_dict.get(s2[index], 0) + 1': lambda S, B, ret: (
            f'右侧字符 {S.s2[S.index]!r} 加入：`now_dict[{S.s2[S.index]!r}] = {S.now_dict[S.s2[S.index]]}`'),
        'if count_dict == now_dict': lambda S, B, ret: ('第一个窗口和 s1 的计数==一致== → 找到' if S.count_dict == S.now_dict
                                                        else '第一个窗口计数和 s1 ==不一致== → 继续往右滑'),
        'for index in range(len(s1), len(s2))': lambda S, B, ret: (f'窗口右移：右端到 `index = {S.index}`'
                                                                    if S.index != B.index else '滑到头了'),
        'remove = s2[index - len(s1)]': '左侧字符 `{remove!r}` 要移出窗口',
        'now_dict[remove] -= 1': '`now_dict[{remove!r}]` 减一 → `{now_dict[remove]}`',
        'if now_dict[remove] == 0': lambda S, B, ret: (f'`now_dict[{S.remove!r}]` 变成 0 → ==必须删掉这个键==，否则 dict 比较不相等'
                                                       if S.now_dict.get(S.remove, -1) == 0
                                                       else f'`now_dict[{S.remove!r}] = {S.now_dict[S.remove]}`，保留'),
        'now_dict.pop(remove)': '删掉键 `{remove!r}`',
        'if now_dict == count_dict': lambda S, B, ret: (f'窗口 `{S.s2[S.index - len(S.s1) + 1:S.index + 1]!r}` 的计数和 s1 ==完全一致==！'
                                                        if S.now_dict == S.count_dict
                                                        else f'窗口 `{S.s2[S.index - len(S.s1) + 1:S.index + 1]!r}` 计数不一致'),
        'return True': '返回 `True`',
        'return False': '所有窗口都不匹配，返回 `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='排列 = 每个字符的次数完全一致：滑窗维护一个计数 dict',
        complexity='时间 `O(n·|Σ|)`（每次比较 dict），空间 `O(|Σ|)`',
        problem=['判断 `s2` 是否包含 `s1` 的某个==排列==（作为连续子串）',
                 '示例：`s1 = "ab", s2 = "eidbaooo"` → `true`（含 `"ba"`）',
                 '本视频：`s1 = "abb", s2 = "eabcbba"` → `true`（含 `"bba"`）'],
        quote='对于字符的排列这种说法，实际上只需要两个串中每个字符出现的次数完全一致即可，因此可以使用一个dict保存s1中每个字符出现的次数，同时在窗口滑动的过程中维护另一个dict',
        quote_src='—— yiduobo 题解',
        idea=['子串是 s1 的排列 → 长度必等于 `len(s1)` → 定长滑动窗口',
              '`count_dict` 存 s1 的次数，`now_dict` 存窗口的次数',
              '滑动时：右侧字符加入、左侧字符移除，两个 dict 相等就找到了'],
        summary=['时间 `O(n·|Σ|)`：每次 dict 比较最多 26 个键',
                 '易错：次数减到 0 的键==要 pop 掉==，否则 `{a:0}` 和 `{}` 不相等',
                 '先单独处理第一个窗口，再从 `len(s1)` 开始滑动',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：用一个 less 计数把每次判断降到 `O(1)`'],
    ),
)
