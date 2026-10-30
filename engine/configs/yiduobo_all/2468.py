def _txt(S):
    if 'b' not in S:
        return ''
    s = f"枚举分段数 `b = {S['b']}`"
    if 'suffix_len' in S:
        s += f"    所有结尾总长 `suffix_len = {S['suffix_len']}`"
    if S.get('_line', 0) >= 14 and 'suffix_len' in S:
        s += f"    需要 `n + suffix_len = {len(S['message']) + S['suffix_len']}` ≤ `limit × b = {S['limit'] * S['b']}`"
    return s


def _done(S):
    n = 0
    for j, x in enumerate(S.get('res') or []):
        suf = '<%d/%d>' % (j + 1, S['b'])
        n += len(x) - len(suf) if x.endswith(suf) else len(x)
    return n


def _res(S):
    r = S.get('res')
    if not r:
        return ''
    return '已切出：' + '  '.join(f'`{x or chr(8709)}`' for x in r)


CONFIG = dict(
    num=2468, title='根据限制分割消息', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='枚举段数 b + 分段求结尾总长',
    tags=['贪心算法', '思维题', '难度分 2382'],
    code='''
class Solution(object):
    def splitMessage(self, message, limit):

        res = []
        for b in range(1, len(message) + 1):
            if b < 10:
                suffix_len = 5 * b
            elif b < 100:
                suffix_len = 7 * (b - 10 + 1) + 6 * 9
            elif b < 1000:
                suffix_len = 9 * (b - 100 + 1) + 8 * 90 + 7 * 9
            elif b < 10000:
                suffix_len = 11 * (b - 1000 + 1) + 10 * 900 + 9 * 90 + 8 * 9
            else:
                suffix_len = 13 + 12 * 9000 + 11 * 900 + 10 * 90 + 9 * 9

            if len(message) + suffix_len <= limit * b:
                max_suffix = '<%d/%d>' % (b, b)
                if len(max_suffix) >= limit:
                    break

                a = 1
                suffix = '<%d/%d>' % (a, b)
                cnt = 0
                for char in message:
                    if cnt == 0:
                        res.append('')
                    res[-1] += char
                    cnt += 1
                    if cnt + len(suffix) == limit:
                        res[-1] += suffix
                        a += 1
                        suffix = '<%d/%d>' % (a, b)
                        cnt = 0
                
                if cnt > 0:
                    res[-1] += suffix
                break
        
        return res
''',
    call='Solution().splitMessage("abcdefgh", 8)',
    expect=['abc<1/3>', 'def<2/3>', 'gh<3/3>'],
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='message', h=200, cell=64, label='message（char 逐个放入当前段）',
             color=lambda S, i, v: 'green' if 'a' in S and i < _done(S) else None),
        dict(type='text', fn=_res, size=26),
    ],
    watch=['b', 'suffix_len', 'a', 'cnt', ('char', 'char', 'cyan'), 'suffix'],
    captions={
        'res = []': '`res` 存分好的各段',
        'for b in range': '枚举分成 `b` 段：==b 越小越好==，所以从小到大找第一个可行的；`b ≤ n` 否则会有空段',
        'suffix_len = 5 * b': '`b = {b}` 是一位数：每段结尾 `<a/b>` 长 5，共 `5 × {b} = {suffix_len}`',
        'suffix_len = 7': '`b` 两位数：`a` 在 1~9 的 9 段结尾长 6，`a` 在 10~b 的结尾长 7 → `suffix_len = {suffix_len}`',
        'suffix_len = 9': '`b` 三位数：结尾长 7、8、9 分三档 → `suffix_len = {suffix_len}`',
        'suffix_len = 11': '`b` 四位数：结尾长 8、9、10、11 分四档 → `suffix_len = {suffix_len}`',
        'suffix_len = 13': '`b = 10000`：五档结尾长相加 → `suffix_len = {suffix_len}`',
        'if len(message) + suffix_len': lambda S, B, r: (f"`n + suffix_len = {len(S.message)} + {S.suffix_len} = {len(S.message) + S.suffix_len}`" + (' ≤ ' if len(S.message) + S.suffix_len <= S.limit * S.b else ' > ') + f"`limit × b = {S.limit * S.b}`" + (' → ==b 段装得下==，就是最小的 b' if len(S.message) + S.suffix_len <= S.limit * S.b else ' → 装不下，b 加 1')),
        'max_suffix = ': '最长的结尾 `{max_suffix}`，长度 `{len(max_suffix)}`',
        'if len(max_suffix) >= limit': lambda S, B, r: (f"`len(max_suffix) = {len(S.max_suffix)}` ≥ `limit = {S.limit}`？" + ('成立：一段装不下字符 → 无解' if len(S.max_suffix) >= S.limit else '不成立：每段至少能装 1 个字符，开始切')),
        'a = 1': '`a` 是当前段编号，`cnt` 是当前段已放的字符数',
        'cnt = 0': '当前段字符数清零',
        'for char in message': lambda S, B, r: ('字符都放完了，退出循环' if getattr(B, 'char', None) == S.char and S.char == S.message[-1] and 'a' in B else f'取下一个字符 `{S.char}`'),
        'if cnt == 0': lambda S, B, r: ('`cnt == 0`：新开一段，先放一个空字符串' if S.cnt == 0 else f'`cnt = {S.cnt}`：继续往当前段里放'),
        'res[-1] += char': '把 `{char}` 放进当前段 → `{res[-1]}`',
        'cnt += 1': '`cnt = {cnt}`',
        'if cnt + len(suffix) == limit': lambda S, B, r: (f"`{S.cnt} + len({S.suffix}) = {S.cnt + len(S.suffix)}`" + (' == ' if S.cnt + len(S.suffix) == S.limit else ' ≠ ') + f"`limit = {S.limit}`" + (' → ==这一段刚好满==，贴上结尾' if S.cnt + len(S.suffix) == S.limit else ' → 还没满')),
        'if cnt > 0': lambda S, B, r: ('`cnt > 0`：最后一段没满，补上结尾' if S.cnt > 0 else '`cnt = 0`：最后一段刚好满，不用补'),
        'return res': '返回 `{res}`',
    },
    skip=['cnt = 0', 'a += 1', "suffix = '<%d/%d>' % (a, b)"],
    cards=dict(
        one_liner='先找最小段数 b，再逐字符装段、装满就贴结尾',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `message` 切成若干段，每段末尾加 `<a/b>`（第几段/总段数）',
                 '除最后一段外每段长度==恰好== `limit`，段数最少；无解返回空数组',
                 '本视频：`"abcdefgh", 8` → `["abc<1/3>","def<2/3>","gh<3/3>"]`'],
        quote='由于题目要求数组越短越小，那么也就是要求b越小越好。对于一个给定的b，其尖括号里的内容，即字符串<a/b>的长度是可以提前预处理出来的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`b` 不会超过 `n`，否则有空段，去掉更短',
              '`b` 固定时，按 `a` 的位数分档，直接算出所有结尾的总长 `suffix_len`',
              '最小的 `b` 满足 `n + suffix_len <= limit * b`；然后逐字符装段，满了就贴结尾'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`<b/b>` 长度 `>= limit` 时无解，要先 `break`，否则会出现空段或超长',
                 '分档：1~9 长 5；两位数 6 / 7；三位数 7 / 8 / 9；四位数 8~11',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神逐段累加容量，进位时扣减；yiduobo 每个 b 直接算出总结尾长'],
    ),
)
