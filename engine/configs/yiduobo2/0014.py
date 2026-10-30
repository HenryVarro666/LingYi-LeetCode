STRS = ['leetcode', 'leet', 'lees']


def _row(S):
    """for string in strs[1:] 没有下标：按字符串找回行号（示例里三个串互不相同）"""
    if S.get('_line') not in (12, 13, 14):
        return None
    s = S.get('string')
    strs = S.get('strs') or []
    return strs.index(s) if s in strs else None


def _color(S, i, j, v):
    if 'len_list' not in S:
        return None
    m = min(S['len_list'])
    if j >= m:
        return 'purple' if S.get('_line') == 9 else None   # 超出最短串长度的列根本不会枚举
    res = S.get('res') or ''
    if j < len(res):
        return 'green'              # 已经累加进 res 的列
    pos = S.get('pos')
    if j == pos and S.get('_line') in (11, 12, 13, 14, 15):
        if i == 0:
            return 'cyan'           # now = strs[0][pos]，标准字母
        r = _row(S)
        if r is not None and S.get('_line') == 14 and i == r:
            return 'red'
        if r is not None and (i < r or (i == r and S.get('_line') == 13 and S['string'][pos] == S['now'])):
            return 'cyan'
        if S.get('_line') == 15:
            return 'cyan'
    return None


def _formula(S):
    if 'len_list' not in S:
        return '按位枚举：第 `pos` 位所有串都相同，就把这个字符累加进 `res`'
    m = min(S['len_list'])
    res = S.get('res', '')
    return f'`min(len_list) = {m}`：最多枚举 {m} 位；当前 `res` = =={res or "（空）"}=='


def _for_pos(S, B, ret):
    if B.get('pos') != S.get('pos') or S.get('_line') == 10 and 'now' not in B:
        return f'枚举第 `pos = {S.pos}` 位'
    return '最短串的每一位都比完了'


def _if_cap(S, B, ret):
    s, p, now = S.string, S.pos, S.now
    if s[p] != now:
        return f'`"{s}"[{p}] = \'{s[p]}\'` ≠ `now = \'{now}\'`：出现不同 → ==直接返回==当前 `res`'
    return f'`"{s}"[{p}] = \'{s[p]}\'` = `now`，相同，继续看下一个串'


def _for_string(S, B, ret):
    if B.get('string') != S.string or B.get('pos') != S.pos or 'now' not in B or B.get('now') != S.now:
        return f'和后面的串比：`"{S.string}"[{S.pos}]`'
    return f'其他串的第 {S.pos} 位都是 `\'{S.now}\'` → 可以累加进答案'


CONFIG = dict(
    num=14, title='最长公共前缀', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按位枚举 · 相同就累加',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def longestCommonPrefix(self, strs):
        pos = 0
        res = ''

        if not strs:
            return res

        len_list = [len(x) for x in strs]
        for pos in range(min(len_list)):
            now = strs[0][pos]
            for string in strs[1:]:
                if string[pos] != now:
                    return res
            res += now

        return res
''',
    call=f'Solution().longestCommonPrefix({STRS})',
    expect='lee',
    skip=['pos = 0'],
    views=[
        dict(type='text', fn=_formula),
        dict(type='grid', var='strs', label='strs（绿 = 已累加进 res，青 = 与 now 相同，红 = 不同）', h=470, cell=100,
             rows=lambda S: list(range(len(S['strs']))), cols=lambda S: list(range(max(len(x) for x in S['strs']))),
             color=_color, cursors=[(_row, 'pos', 'yellow')]),
    ],
    watch=[('pos', 'pos', 'yellow'), ('now', 'now', 'cyan'), ('string', 'string', 'blue'), ('res', 'res', 'green')],
    captions={
        "res = ''": '`res` 存答案，一位一位往后累加',
        'if not strs': '`strs` 非空，继续',
        'len_list = ': '`len_list = {len_list}`：答案长度==不会超过最短的串== `{min(len_list)}`（紫色列不会被枚举）',
        'for pos in range': _for_pos,
        'now = strs[0][pos]': '以第一个串为准：`now = strs[0][{pos}] = \'{now}\'`',
        'for string in strs[1:]': _for_string,
        'if string[pos] != now': _if_cap,
        14: '第 {pos} 位不全相同 → 公共前缀就是已经累加好的 =={ret}==',
        17: '最短串的每一位都相同 → 返回 `res = "{res}"`',
        'res += now': '所有串第 {pos} 位都是 `\'{now}\'` → 累加：`res = "{res}"`',
    },
    cards=dict(
        one_liner='按位枚举：所有串这一位都相同就累加，否则立刻返回',
        complexity='时间 `O(nk)`，空间 `O(1)`（`k` 为答案长度）',
        problem=['给一个字符串数组 `strs`，求它们的==最长公共前缀==',
                 '不存在公共前缀时返回空串 `""`',
                 '示例：`["flower","flow","flight"]` → `"fl"`',
                 '本视频：`["leetcode","leet","lees"]` → `"lee"`'],
        quote='直接按位枚举每一个字符，然后判断其他串中的这个字符是否相同，==相同则累加到答案中==，否则直接返回即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先算出所有串的长度，`pos` 只枚举到 `min(len_list) - 1`，==不用担心越界==',
              '第 `pos` 位以 `strs[0][pos]` 为准，和后面每个串比',
              '全相同 → `res += now`；有一个不同 → 直接返回 `res`'],
        summary=['时间 `O(nk)`：`n` 个串，`k` 为答案长度（不超过最短串长）',
                 '先取 `min(len_list)` 做枚举上界，内层就不用判断越界',
                 '易错：`return res` 写在内层 for 里，==遇到不同就立刻结束==，不是 break',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用 `s0[:j]` 截取，yiduobo 用 `res` 逐位累加'],
    ),
)
