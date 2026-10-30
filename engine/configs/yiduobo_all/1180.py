S0 = 'aaabbaa'


def _fval(res, cnt):
    return res + cnt * (cnt + 1) // 2


def _k(S):
    """已经处理完的字符个数（由 res / cnt 反推）"""
    if 'res' not in S:
        return None
    cur = _fval(S['res'], S['cnt'])
    if cur == 0:
        return 0
    s = S['s']
    last, cnt, res = None, 0, 0
    for k, ch in enumerate(s, 1):
        if ch == last:
            cnt += 1
        else:
            res += cnt * (cnt + 1) // 2
            last, cnt = ch, 1
        if _fval(res, cnt) == cur:
            return k
    return None


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return None
    if i < k:
        last = S['s'][k - 1]
        return 'green' if v == last and i >= k - S['cnt'] else 'cyan'
    return None


def _text(S):
    if 'res' not in S:
        return '一段长为 `k` 的相同字符，能切出 `1+2+...+k = k(k+1)/2` 个合法子串'
    cnt = S['cnt']
    return f'当前连续段长 `cnt = {cnt}`（绿色）；已结算的段累计 `res = {S["res"]}`'


def _for(S, B, ret):
    if _k(S) == len(S['s']):
        return '`s` 里的字符都遍历完了，循环结束'
    return f"取下一个字符 `char = '{S.char}'`，上一个字符 `last = {S.last!r}`"


CONFIG = dict(
    num=1180, title='统计只包含单一字母的子串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 连续段求和公式',
    code='''
class Solution(object):
    def countLetters(self, s):

        last = None
        cnt = 0
        res = 0
        for char in s:
            if char == last:
                cnt += 1
            else:
                res += cnt * (cnt + 1) // 2
                last = char
                cnt = 1
        
        return res + cnt * (cnt + 1) // 2
''',
    call=f'Solution().countLetters("{S0}")',
    expect=12,
    views=[
        dict(type='text', fn=_text, h=70, size=26),
        dict(type='string', var='s', label='s（青 = 已结算的段，绿 = 正在累计的段）', cell=96, color=_color, h=230),
        dict(type='text', fn=lambda S: f'`s = "{S["s"]}"`：三段 `aaa`、`bb`、`aa` → 6 + 3 + 3 = ==12==', h=60, size=26),
    ],
    watch=[('last', 'last', 'blue'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green'), 'char'],
    captions={
        'last = None': '`last` 记录上一个字符，开头还没有字符',
        'cnt = 0': '`cnt`：当前同字符区间的长度',
        'res = 0': '`res`：已经结算完的区间贡献的子串数',
        'for char in s': _for,
        'if char == last': lambda S, B, r: (f"`'{S.char}' == '{S.last}'` → 还在同一段里" if S.char == S.last
                                            else f"`'{S.char}' ≠ {S.last!r}` → 新的一段开始，先结算上一段"),
        'cnt += 1': '同一段又多一个字符：`cnt` → {cnt}',
        'res += cnt': '上一段长 `{B.cnt}`，贡献 `{B.cnt} × {B.cnt + 1} / 2` = =={B.cnt * (B.cnt + 1) // 2}== 个子串 → `res = {res}`',
        'last = char': '`last` 换成新字符 `{last}`',
        'cnt = 1': '新的一段从长度 `1` 开始',
        'return': '最后一段还没结算：补上 `{cnt} × {cnt + 1} / 2` = {cnt * (cnt + 1) // 2} → 答案 =={ret}==',
    },
    cards=dict(
        one_liner='长为 k 的同字符段，恰好有 k(k+1)/2 个合法子串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计字符串 `s` 中只含==一种字母==的子串个数',
                 '相同位置不同的子串要分别计数',
                 '本视频：`s = "aaabbaa"` → `12`'],
        quote='对于一个长度为k的由同一个字符构成的区间而言，其可以形成k个长度为1的合法子串，k - 1个长度为2的合法子串，...，1个长度为k的合法子串，也就是说一共可以形成(1 + k) * k / 2个合法子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，找出每个由同一字符构成的区间长度 `k`',
              '每段贡献 `k × (k+1) / 2` 个子串，累加到 `res`',
              '遇到新字符才结算上一段，所以循环外要再补最后一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：最后一段没有新字符触发结算，要在 `return` 处补上',
                 '`cnt` 初值为 0，第一个字符进入 else 时 `0 × 1 // 2 = 0`，不影响答案'],
    ),
)
