def _parts(S):
    p = S.get('part')
    if p is None:
        return '先把字符串切成连续相同字符的“段”：`[字符, 长度]`'
    cur = S.get('index')
    items = []
    for i, (c, n) in enumerate(p):
        t = f'`{c}×{n}`'
        if cur is not None and i == cur:
            t = f'==[{c}×{n}]=='
        items.append(t)
    return '段：' + '  '.join(items)


def _calc(S):
    if 'index' not in S or 'tmp' not in S or 'part' not in S:
        return ''
    i = S['index']
    c = S['part'][i][0]
    return f"字符 `{c}` 全串共 =={S['s'][c]}== 个　`tmp = {S['tmp']}`　`min(tmp, {S['s'][c]})` = =={min(S['tmp'], S['s'][c])}=="


CONFIG = dict(
    num=1156, title='单字符重复子串的最大长度', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='分段统计 · 枚举每段 + 跨过单个字符的拼接',
    tags=['难度分 1769'],
    code='''
class Solution(object):
    def maxRepOpt1(self, text):

        s = {}
        now = text[0]
        cnt = 1
        part = []
        for char in text[1:]:
            if char != now:
                part.append([now, cnt])
                s[now] = s.get(now, 0) + cnt
                now = char
                cnt = 1
            else:
                cnt += 1
        
        part.append([now, cnt])
        s[now] = s.get(now, 0) + cnt
        
        res = 0
        for index in range(len(part)):
            tmp = part[index][1] + 1
            if index >= 2 and part[index - 1][1] == 1 and part[index - 2][0] == part[index][0]:
                tmp += part[index - 2][1]
            
            res = max(res, min(tmp, s[part[index][0]]))
        
        return res
''',
    call="Solution().maxRepOpt1('aaabaaa')",
    expect=6,
    views=[
        dict(type='string', var='text', label='text', cell=100, h=170),
        dict(type='text', h=70, size=30, fn=_parts),
        dict(type='map', var='s', label='s（每种字符在全串中的总个数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=70, size=28, fn=_calc),
    ],
    watch=[('index', 'index', 'blue'), ('tmp', 'tmp', 'orange'), ('res', 'res', 'green')],
    captions={
        's = {}': '`s` 统计每种字符在全串出现的总次数',
        'now = text[0]': '`now` 是当前这一段的字符，`cnt` 是它的长度',
        'if char != now': lambda S, B, r: (f'`{S.char!r}` ≠ `{S.now!r}`：这一段结束了，存进 `part`' if S.char != S.now
                                           else f'`{S.char!r}` = `{S.now!r}`：还是同一段，长度加一'),
        'part.append([now, cnt])': '记下一段 `{part[-1]}`',
        's[now] = s.get': '`s[{now!r}]` 累加 → `{s}`',
        'now = char': '开始新的一段，字符 `{now!r}`',
        'cnt += 1': '这一段长度 `cnt = {cnt}`',
        'res = 0': '分段完成：`{part}`',
        'tmp = part[index][1] + 1': '方法 1：这段长 `{part[index][1]}`，再从别处换一个同字符来 → `tmp = {tmp}`',
        'if index >= 2': lambda S, B, r: ((f'前一段长度为 1（`{S.part[S.index - 1]}`），而再前一段也是 `{S.part[S.index][0]}`：换掉这个单字符，两段能接起来'
                                           if S.index >= 2 and S.part[S.index - 1][1] == 1 and S.part[S.index - 2][0] == S.part[S.index][0]
                                           else '不满足“中间只隔 1 个别的字符且两侧同字符”，不能拼接')),
        'tmp += part[index - 2][1]': '方法 2：把前面那段 `{part[index - 2]}` 接上 → `tmp = {tmp}`',
        'res = max': '换来的字符要真的存在：不能超过全串个数 `{s[part[index][0]]}`，所以取 `min({tmp}, {s[part[index][0]]})`，`res = {res}`',
        'return res': '最长单字符重复子串 `{res}`',
    },
    cards=dict(
        one_liner='只能换一次：要么延长一段，要么把隔着单个字符的两段接起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `text`，可以==交换其中两个字符一次==',
                 '求交换后，由单一字符组成的最长子串长度',
                 '示例：`"aaabaaa"` → `6`'],
        quote='对于形如AAAABAAAAA的子串，同样是从远处弄一个A来与这里的B交换，那么此时可以得到一个长度为两段A的长度之和再加上1的字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍，切成 `[字符, 长度]` 的段，同时统计每种字符的总数',
              '方法 1：一段长 `l`，从远处换一个同字符过来 → `l + 1`',
              '方法 2：`AAAA B AAAAA`，中间只隔一个字符，把 B 换成 A → 两段长度和 `+ 1`',
              '换来的字符必须存在：结果不能超过该字符的全串总数'],
        summary=['时间 `O(n)`，只扫两遍',
                 '易错：必须用 `min(tmp, 总数)`，没有多余的字符可换时不能加 1',
                 '易错：拼接只在中间段长度恰为 1 时成立',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '类似题：滑动窗口里“最多允许一个异类字符”的变形'],
    ),
)
