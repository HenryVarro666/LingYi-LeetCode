def _build(s):
    d, now, res, cnt = {}, None, 0, 0
    for i, ch in enumerate(s):
        st = [(7, ch, now, cnt, res), (8, ch, now, cnt, res)]
        if ch != now:
            res = max(res, cnt); st.append((9, ch, now, cnt, res)); now = ch
            st.append((10, ch, now, cnt, res)); cnt = 1; st.append((11, ch, now, cnt, res))
        else:
            cnt += 1; st.append((13, ch, now, cnt, res))
        for x in st:
            d[x] = i
    return d


_POS = _build('abbcccddcc')


def _pos(S):
    if 'char' not in S:
        return None
    return _POS.get((S['_line'], S['char'], S['now'], S['cnt'], S['res']))


class _P:
    def __init__(self, name, fn):
        self.name, self.fn = name, fn

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _run(S):
    p = _pos(S)
    if p is None:
        return None
    end = p if S['_line'] in (11, 13) else p - 1
    return (end - S['cnt'] + 1, end) if S['cnt'] > 0 and end >= 0 else None


CONFIG = dict(
    num=1446, title='连续字符', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · 计数连续段',
    tags=['分组循环'],
    code='''
class Solution(object):
    def maxPower(self, s):

        now = None
        res = 0
        cnt = 0
        for char in s:
            if char != now:
                res = max(res, cnt)
                now = char
                cnt = 1
            else:
                cnt += 1
        
        return max(res, cnt)
''',
    call="Solution().maxPower('abbcccddcc')",
    expect=3,
    views=[
        dict(type='string', var='s', label='s（箭头 = 当前字符，青框 = 当前这一段）', h=200,
             pointers={_P('char', _pos): 'blue'},
             window=(lambda S: (_run(S) or (0, -1))[0], lambda S: (_run(S) or (0, -1))[1])),
        dict(type='text', fn=lambda S: f"当前字符 `{S.get('char')}`，上一个字符 `{S.get('now')}`，当前连续段长度 `cnt` = =={S.get('cnt')}==，历史最长 `res` = =={S.get('res')}==" if 'cnt' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), ('now', 'now', 'pink'), ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'now = None': '`now` 记录当前这一段的字符，开始时还没有',
        'res = 0': '`res`：目前见过的最长连续段',
        'cnt = 0': '`cnt`：当前这一段已经有多长',
        'for char in s': '看下一个字符 `char = {char}`',
        'if char != now': lambda S, B, r: (f"`'{S.char}' != '{S.now}'` → ==新的一段开始==，先结算上一段" if S.char != S.now
                                           else f"`'{S.char}' == '{S.now}'` → 还在同一段里"),
        'res = max': '上一段结束了，用它的长度更新答案：`res = max({B.res}, {cnt}) = {res}`',
        'now = char': '`now` 改成新字符 `{now}`',
        'cnt = 1': '新的一段已经有 1 个字符：`cnt = 1`',
        'cnt += 1': '和前一个相同，连续段加长：`cnt` → {cnt}',
        'return max': lambda S, B, r: f'==最后一段还没结算==，用最后的 `cnt = {S.cnt}` 再更新一次 → 返回 {r}',
    },
    cards=dict(
        one_liner='一趟扫描：字符变了就结算上一段，别忘最后一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串的「能量」是只含一种字符的最长非空子串的长度',
                 '给定字符串 `s`，返回它的能量',
                 '示例：`"abbcccddcc"` → `3`（`ccc`）'],
        quote='若当前字符与前一个字符相同，那么将cnt加上1，否则使用cnt更新答案，并更新cnt为1。扫描完成后，还需要使用最后这个cnt更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 存当前段的字符，`cnt` 存当前段长度',
              '遇到不同字符：说明上一段结束，用 `cnt` 更新 `res`，再从 1 重新计数',
              '最后一段后面没有“不同字符”来触发结算，所以 return 时要再取一次 max'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：循环结束后要 `max(res, cnt)`，否则以结尾的最长段会漏掉',
                 '`now = None` 让第一个字符也走“新的一段”分支，此时 `cnt = 0` 不影响答案',
                 '同类题：1869、485 连续 1 的最大个数'],
    ),
)
