S0 = 'eleetmin'


def _b(x):
    return format(x, '05b')


def _txt(S):
    if 'now' not in S or 'index' not in S:
        return '编码：`a=1, e=2, i=4, o=8, u=16`；`now` 的五位从右到左是 a e i o u 的奇偶性'
    now, i, pd = S['now'], S['index'], S['pos_dict']
    if now in pd and pd[now] != i:
        return f'`now = {_b(now)}`　上次出现在下标 `{pd[now]}`：之后到 `{i}` 的元音==全是偶数次== → 长度 `{i - pd[now]}`'
    return f'`now = {_b(now)}`　第一次出现，记在下标 `{i}`' if now in pd else f'`now = {_b(now)}`'


CONFIG = dict(
    num=1371, title='每个元音包含偶数次的最长子字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='元音奇偶二进制编码 + 哈希表',
    tags=['前缀和', '状态压缩前缀和', '难度分 2041'],
    code='''
class Solution(object):
    def findTheLongestSubstring(self, s):

        val = {'a': 1, 'e': 2, 'i': 4, 'o': 8, 'u': 16}
        pos_dict = {0: -1}

        now = 0
        res = 0
        for index, char in enumerate(s):
            if char in val:
                now ^= val[char]
                if now not in pos_dict:
                    pos_dict[now] = index
                
            res = max(res, index - pos_dict[now])

        return res
''',
    call=f'Solution().findTheLongestSubstring({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（指针 = 当前读到的 index）', cell=100, h=210, pointers={'index': 'blue'}),
        dict(type='map', var=lambda S: {format(k, '05b'): v for k, v in S['pos_dict'].items()},
             label='pos_dict（元音奇偶编码 → 第一次出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=200, font=28),
        dict(type='text', h=110, size=26, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'format(now, "05b")', 'yellow'), ('res', 'res', 'green')],
    captions={
        'val = {': '给 5 个元音编码：`a=1, e=2, i=4, o=8, u=16`，各占一个二进制位',
        'pos_dict = {0': '`pos_dict`：每种奇偶状态==第一次==出现的下标；空前缀状态 0 记为 `-1`',
        'now = 0': '`now`：当前前缀里五个元音出现次数的奇偶性，开始全是偶数',
        'res = 0': '`res` 记录最长合法子串长度',
        'for index, char': lambda S, B, ret: (f'读入 `s[{S.index}] = {S.char!r}`' if S.get('char') is not None and S.get('index') != B.get('index') else '遍历结束'),
        'if char in val': lambda S, B, ret: (f'`{S.char}` 是元音，要翻转它的奇偶位' if S.char in S.val else f'`{S.char}` 不是元音，`now` 不变'),
        'now ^= val[char]': '异或 `{val[char]}`：元音 `{char}` 的奇偶翻转，`{B.now:05b}` → ==`{now:05b}`==',
        'if now not in pos_dict': lambda S, B, ret: (f'`{S.now:05b}` 没见过 → 记下首次位置' if S.now not in S.pos_dict else f'`{S.now:05b}` 见过了，保留更早的下标'),
        'pos_dict[now] = index': '首次出现：`pos_dict[{now:05b}] = {index}`',
        'res = max': lambda S, B, ret: (f'刚记下的新状态，区间长 0，`res` 不变' if S.pos_dict[S.now] == S.index else f'同一状态在 `{S.pos_dict[S.now]}` 和 `{S.index}` 都出现：中间这段元音全是偶数次，长 `{S.index - S.pos_dict[S.now]}`，'
                                        + (f'`res` {B.res} → =={S.res}==' if S.res != B.res else f'不比 `res = {S.res}` 长')),
        'return res': '最长子串长度 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='两个前缀的奇偶状态相同，中间一段元音就全是偶数次',
        complexity='时间 `O(n)`，空间 `O(2^5)`',
        problem=['求最长子串，使其中 a e i o u 每个元音都出现偶数次',
                 '示例：`"eleetminicoworoep"` → `13`',
                 '本视频：`"eleetmin"` → `5`'],
        quote='首先，题目只需要判断奇偶，具体出现的次数实际上并不重要，那么我们可以用二进制来表示某个元音字符出现的次数是奇数还是偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到朴素做法：对每个位置回头找合法起点，太慢',
              '只看奇偶：5 个元音用 5 位二进制编码，`a e i o u` 对应 `1 2 4 8 16`',
              '同一编码出现两次 → 中间元音全是偶数次；哈希表存==最早==位置'],
        summary=['时间 `O(n)`，空间 `O(2^5)`',
                 '`pos_dict = {0: -1}` 表示空前缀，否则从头开始的子串会漏',
                 '辅音不改变 `now`，但也要更新 `res`（`res = max` 在 if 外面）',
                 '只在首次出现时记下标，保证子串最长',
                 '同类题：1542（10 位编码）、1177、1915'],
    ),
)
