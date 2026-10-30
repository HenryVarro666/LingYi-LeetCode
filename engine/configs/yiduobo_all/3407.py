S0 = 'abcde'
P0 = 'bc*cd'


def _s_color(S, i, v):
    st = S.get('star')
    if st is None:
        return None
    pre, suf = P0[:st], P0[st + 1:]
    L = S.get('left', -1)
    R = S.get('right', len(S0))
    if S['_line'] >= 7 and L >= 0 and L <= i < L + len(pre):
        return 'blue'
    if S['_line'] >= 14 and 0 <= R < len(S0) and R <= i < R + len(suf):
        return 'green'
    return None


def _p_color(S, i, v):
    st = S.get('star')
    if st is None:
        return None
    return 'yellow' if i == st else ('blue' if i < st else 'green')


def _text(S):
    if 'star' not in S:
        return '把 `p` 按星号切成三段：左段、星号、右段'
    st = S['star']
    t = f"星号在 `{st}`：左段 `{P0[:st]}`，右段 `{P0[st + 1:]}`；两段在 `s` 里==不能重叠=="
    if 'left' in S and 'right' in S:
        t = f"左段起点 `left` = {S['left']}，其末字符在 `{S['left'] + st - 1}`；右段起点 `right` = {S['right']}"
    return t


CONFIG = dict(
    num=3407, title='子字符串匹配模式', difficulty='Easy', category='字符串',
    author='yiduobo', technique='左段靠前 · 右段靠后 · 比较是否重叠',
    code='''
class Solution(object):
    def hasMatch(self, s, p):
        
        star = p.find('*')

        if star > 0:
            left = s.find(p[:star])
            if left == -1:
                return False
        else:
            left = -1

        if star < len(p) - 1:
            right = s.rfind(p[star + 1:])
            if right == -1:
                return False
        else:
            right = len(s)

        return left + star - 1 < right
''',
    call='Solution().hasMatch("abcde", "bc*cd")',
    expect=False,
    views=[
        dict(type='text', fn=_text, size=28, h=120),
        dict(type='string', var='s', label='s（蓝 = 左段最靠前的位置，绿 = 右段最靠后的位置）', color=_s_color, h=240),
        dict(type='string', var='p', label='p（蓝 = 左段，黄 = 星号，绿 = 右段）', color=_p_color, h=240),
    ],
    watch=['star', 'left', 'right'],
    captions={
        'star = p.find': '星号下标 `star = {star}`：`p[:star]` = `{p[:star]}`，`p[star+1:]` = `{p[star + 1:]}`',
        'if star > 0': lambda S, B, r: ('星号左边有内容，要先在 `s` 里找它' if S.star > 0 else '星号在开头，左段为空'),
        'left = s.find': lambda S, B, r: f"左段 `{S.p[:S.star]}` 在 `s` 中==第一次==出现在 `{S.left}`（越靠前越好，给右段让位）",
        'if left == -1': '`left = {left}`，找到了 → 继续',
        'left = -1': '左段为空：`left = -1`，不影响最后的比较',
        'if star < len(p) - 1': lambda S, B, r: ('星号右边有内容，要在 `s` 里找它' if S.star < len(S.p) - 1 else '星号在末尾，右段为空'),
        'right = s.rfind': lambda S, B, r: f"右段 `{S.p[S.star + 1:]}` 在 `s` 中==最后一次==出现在 `{S.right}`（越靠后越好）",
        'right = len(s)': '右段为空：`right = len(s)`，不影响最后的比较',
        'if right == -1': '`right = {right}`，找到了 → 继续',
        'return left + star': lambda S, B, r: f"左段末字符下标 `left + star - 1 = {S.left} + {S.star} - 1 = {S.left + S.star - 1}`，右段起点 `right = {S.right}`：" + (f"`{S.left + S.star - 1} < {S.right}` 左段在前、不重叠 → `True`" if r else f"`{S.left + S.star - 1} < {S.right}` 不成立，两段重叠 → ==False=="),
    },
    max_steps=30,
    cards=dict(
        one_liner='左段尽量靠前、右段尽量靠后，看两段会不会重叠',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['模式串 `p` 里恰有一个星号，可以替换成任意长度（含 0）的任意字符串',
                 '问替换后 `p` 能否成为 `s` 的子串',
                 '示例：`s = "leetcode"`，`p = "ee*e"` → `true`；本视频用 `s = "abcde"`，`p = "bc*cd"` → `false`'],
        quote='若通过修改p[star]可以使得p变为s的子串，那么就必须满足p[:star]以及p[star + 1:]都是s的子串，且这两个子串不重叠。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 切成左段、星号、右段，星号可吞掉中间任意内容',
              '为了不重叠：左段取最靠前的 `find`，右段取最靠后的 `rfind`',
              '左段末字符下标 `left + star - 1` 必须在 `right` 的左边',
              '某一段为空时，把 `left` 设为 -1、`right` 设为 `len(s)`，比较式照样成立'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错点：星号在开头或末尾时，空串的 `find` 会得到 0，所以要单独设 `left = -1`、`right = len(s)`',
                 '`left + star - 1` 是左段最后一个字符的位置，别漏掉 `- 1`',
                 '原文已是 Python 3 可运行的写法，未改动代码；本题 `find` + `rfind` 与灵神的「只用 find」殊途同归'],
    ),
)
