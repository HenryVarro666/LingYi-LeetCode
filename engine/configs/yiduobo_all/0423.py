S0 = 'owoztneoer'
ORDER = [(0, 'z', 'zero'), (2, 'w', 'two'), (4, 'u', 'four'), (3, 'r', 'three'), (1, 'o', 'one'),
         (5, 'f', 'five'), (6, 'x', 'six'), (7, 's', 'seven'), (8, 'h', 'eight'), (9, 'i', 'nine')]
NAMES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def _truth():
    cc = {}
    for ch in S0:
        cc[ch] = cc.get(ch, 0) + 1
    out = [0] * 10
    for d, ch, w in ORDER:
        k = cc.get(ch, 0)
        out[d] = k
        if k > 0:
            for x in w:
                cc[x] -= k
    return out


TRUTH = _truth()


def _cnt(S):
    c = S.get('cnt')
    if isinstance(c, list):
        return c
    if 'num' not in S:
        return None
    pos = [w for _, _, w in ORDER].index(S['num'])
    out = [0] * 10
    for d, ch, w in ORDER[:pos]:
        out[d] = TRUTH[d]
    return out


def _cur_digit(S):
    n = S.get('num')
    return NAMES.index(n) if n in NAMES else None


def _cnt_color(S, i, v):
    d = _cur_digit(S)
    if d is not None and i == d:
        return 'yellow'
    if v:
        return 'green'
    return None


def _cap_chk(S, B, ret):
    return f"检查 `{S.num}`：独有字母 `'{S.char}'` 在 `char_cnt` 里出现几次，这个数字就出现几次"


def _cap_cnt(S, B, ret):
    k = S.cnt
    if k > 0:
        return f"`char_cnt['{B.char}'] = {k}` > 0 → `{B.num}` 出现 =={k}== 次，把它的每个字母都扣掉 {k} 个"
    return f"`'{B.char}'` 一个也没有 → `{B.num}` 出现 ==0== 次，什么都不扣"


CONFIG = dict(
    num=423, title='从英文中重建数字', difficulty='Medium', category='字符串',
    author='yiduobo', technique='统计字母 · 独有字母定数字',
    tags=[],
    code='''
class Solution(object):
    def originalDigits(self, s):

        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1

        cnt = [0] * 10

        cnt[0] = self.check(char_cnt, 'z', 'zero')
        cnt[2] = self.check(char_cnt, 'w', 'two')
        cnt[4] = self.check(char_cnt, 'u', 'four')
        cnt[3] = self.check(char_cnt, 'r', 'three')
        cnt[1] = self.check(char_cnt, 'o', 'one')
        cnt[5] = self.check(char_cnt, 'f', 'five')
        cnt[6] = self.check(char_cnt, 'x', 'six')
        cnt[7] = self.check(char_cnt, 's', 'seven')
        cnt[8] = self.check(char_cnt, 'h', 'eight')
        cnt[9] = self.check(char_cnt, 'i', 'nine')
        
        res = ''.join([str(x) * cnt[x] for x in range(10)])
        return res

    def check(self, char_cnt, char, num):
        cnt = char_cnt.get(char, 0)
        if cnt > 0:
            for char in num:
                char_cnt[char] -= cnt

        return cnt
''',
    call=f'Solution().originalDigits({S0!r})',
    expect='012',
    skip=['for char in s:', 'for char in num', 'res = ', "char_cnt[char] = char_cnt.get(char, 0) + 1"],
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=170),
        dict(type='map', var='char_cnt', label='char_cnt（字母出现次数；被扣减的键黄色）', h=250, font=26,
             fmt=lambda k, v: f"'{k}': {v}"),
        dict(type='array', var=_cnt, label='cnt[d] = 数字 d 出现的次数（黄 = 正在检查的数字）', cell=70, h=190, color=_cnt_color),
    ],
    watch=[('char', 'char', 'blue'), ('num', 'num', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'char_cnt = {}': '先数 `s` 里每个字母出现的次数',
        'cnt = [0] * 10': '`cnt[d]` 记录数字 `d` 出现了几次',
        "cnt[0] = self.check": '先找 `z`：只有 ==zero== 里有 z → 用 `z` 的个数定 0 的个数',
        "cnt[2] = self.check": '`w` 只在 ==two== 里 → 定 2 的个数',
        "cnt[4] = self.check": '`u` 只在 ==four== 里 → 定 4 的个数',
        "cnt[3] = self.check": '`zero`、`four` 都扣掉后，`r` 只剩 ==three== → 定 3',
        "cnt[1] = self.check": '`zero`、`two`、`four` 扣掉后，`o` 只剩 ==one== → 定 1',
        "cnt[5] = self.check": '`four` 扣掉后，`f` 只剩 ==five== → 定 5',
        "cnt[6] = self.check": '`x` 只在 ==six== 里 → 定 6',
        "cnt[7] = self.check": '`six` 扣掉后，`s` 只剩 ==seven== → 定 7',
        "cnt[8] = self.check": '`three` 扣掉后，`h` 只剩 ==eight== → 定 8',
        "cnt[9] = self.check": '`five`、`six`、`eight` 扣掉后，`i` 只剩 ==nine== → 定 9',
        'def check': _cap_chk,
        'cnt = char_cnt.get(char, 0)': lambda S, B, r: f"`char_cnt.get('{S.char}', 0) = {S.cnt}`：`{S.num}` 的独有字母出现 {S.cnt} 次",
        'if cnt > 0': lambda S, B, r: (f'`cnt = {S.cnt} > 0` → 这个数字存在，要把它占用的字母从 `char_cnt` 里扣掉' if S.cnt > 0
                                       else '`cnt = 0` → 没有这个数字，不用扣'),
        'char_cnt[char] -= cnt': "`char_cnt['{char}'] -= {cnt}` → =={char_cnt[char]}==（这个字母被 `{num}` 用掉了）",
        'return cnt': '返回 `{cnt}`：数字出现的次数',
        "''.join": "按数字 0~9 的顺序，把每个数字重复 `cnt[x]` 次拼起来",
        'return res': '重建出的数字：`{res}`',
    },
    cards=dict(
        one_liner='先用独有字母定 0、2、4、6，再扣掉，逐步确定其余数字',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你一个乱序的字符串 `s`，它由某些数字 0~9 的英文单词（`zero`、`one` ……）打乱字母后拼成',
                 '按升序还原出这些数字，返回拼起来的字符串',
                 '示例：`"owoztneoer"` → `"012"`'],
        quote='某些单词具体独一无二的字母，例如zero的z和two的w。于是可以首先通过统计这些字母的个数来求出对应单词出现的次数，然后再根据剩下的字母来确定其他的单词。',
        quote_src='—— yiduobo 题解原文',
        idea=['`z` 只在 zero，`w` 只在 two，`u` 只在 four：个数直接就是答案',
              '每确定一个数字，就把它的字母从 `char_cnt` 里扣掉，其余单词的独有字母就暴露出来',
              '顺序：0, 2, 4, 3, 1, 5, 6, 7, 8, 9，用 `check` 一步完成「读个数 + 扣字母」'],
        summary=['时间 `O(n)`，空间 `O(1)`（字母表固定）',
                 '易错：检查顺序不能乱，例如 `o` 要等 0、2、4 扣掉后才只属于 one',
                 '`check` 里 `char_cnt.get` 防止字母不存在时 KeyError；`cnt > 0` 才扣',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
