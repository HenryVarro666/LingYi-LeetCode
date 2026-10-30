S0 = '3242415'


def _b(x):
    return format(x, '06b')


def _txt(S):
    if 'now' not in S or 'index' not in S or S.get('char') is None:
        return '`now` 的第 p 位 = 数字 p 出现次数的奇偶性（只画低 6 位）'
    sd, now, i = S['status_dict'], S['now'], S['index']
    if S['_line'] == 20:
        return f'`now = {_b(now)}` 首次出现，记入表中：下标 `{i}`'
    hit = [(p, sd[now ^ p]) for p in S['pow2'] if (now ^ p) in sd]
    ev = sd.get(now)
    parts = []
    if ev is not None and S['_line'] >= 17:
        parts.append(f'编码 0：`{_b(now)}` 在 `{ev}` 出现过 → 长 {i - ev}')
    for p, q in hit:
        parts.append(f'异或 `{_b(p)}` 命中，下标 {q} → 长 {i - q}')
    return f'`now = {_b(now)}`　' + ('；'.join(parts) if parts else '没有可匹配的状态')


CONFIG = dict(
    num=1542, title='找出最长的超赞子字符串', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='状态编码前缀 + 哈希表最早位置',
    tags=['前缀和', '状态压缩前缀和', '难度分 2222'],
    code='''
class Solution(object):
    def longestAwesome(self, s):

        pow2 = [1]
        for index in range(10):
            pow2.append(pow2[-1] + pow2[-1])
        status_dict = {0 : -1}
        now = 0
        res = 0
        for index, char in enumerate(s):
            now ^= (1 << int(char))
            for p in pow2:
                tmp = now ^ p
                if tmp in status_dict:
                    res = max(res, index - status_dict[tmp])
            
            if now in status_dict:
                res = max(res, index - status_dict[now])
            else:
                status_dict[now] = index

        return res
''',
    call=f'Solution().longestAwesome({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（指针 = 当前读到的 index）', cell=100, h=210, pointers={'index': 'blue'}),
        dict(type='map', var=lambda S: {format(k, '06b'): v for k, v in S['status_dict'].items()},
             label='status_dict（状态编码 → 最早出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=220, font=26),
        dict(type='text', h=130, size=26, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'format(now, "06b")', 'yellow'), ('res', 'res', 'green')],
    skip=['for index in range(10)', 'pow2.append', 'for p in pow2', 'tmp = now ^ p', 'if tmp in status_dict'],
    captions={
        'pow2 = [1]': '`pow2` 存 `1, 2, 4, …, 1024`：每个数字出现奇数次对应的编码 `2^p`',
        'status_dict = {0': '`status_dict`：各状态==最早==出现的位置；空前缀状态 0 在 `-1`',
        'now = 0': '`now`：`s[0..index]` 里各数字奇偶性的二进制编码',
        'res = 0': '`res` 记录最长超赞子串长度',
        'for index, char': lambda S, B, ret: (f'读入 `s[{S.index}] = {S.char}`' if 'index' in S and S.get('index') != B.get('index') and 'char' in S and S.get('char') is not None else '遍历结束'),
        'now ^= ': '数字 `{char}` 出现一次，翻转第 `{char}` 位：`{B.now:06b}` → ==`{now:06b}`==',
        'res = max(res, index - status_dict[tmp])': lambda S, B, ret: (
            f'`now ^ {S.p}` = `{S.tmp:06b}` 在下标 `{S.status_dict[S.tmp]}` 出现过：区间编码恰为 `2^p`（一个数字奇数次）→ 长度 `{S.index - S.status_dict[S.tmp]}`，'
            + (f'`res` {B.res} → =={S.res}==' if S.res != B.res else f'不比 `res = {S.res}` 长')),
        'if now in status_dict': lambda S, B, ret: (f'`now = {S.now:06b}` 之前出现过：区间内每个数字都是偶数次' if S.now in S.status_dict else f'`now = {S.now:06b}` 第一次出现，没有偶数匹配'),
        'res = max(res, index - status_dict[now])': '区间编码为 0：长度 `{index} − {status_dict[now]}` = `{index - status_dict[now]}` → `res = {res}`',
        'status_dict[now] = index': '首次出现，记录 `status_dict[{now:06b}] = {index}`；只记最早的，之后区间更长',
        'return res': '最长超赞子串长度 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='超赞子串 = 区间编码是 0 或某个 2^p',
        complexity='时间 `O(10·n)`，空间 `O(2^10)`',
        problem=['超赞子串：非空子串，交换字符后能变成回文串',
                 '`s` 只含数字，求最长超赞子串长度',
                 '示例：`"3242415"` → `5`'],
        quote='若其每个数字出现次数都是偶数次，那么其编码就是0；若其各个数字出现次数中有一个奇数，那么其编码必然是2^p，其中p的取值范围为0到9。',
        quote_src='—— yiduobo 题解原文',
        idea=['回文：至多一个字符出现奇数次 → 用 10 位二进制记奇偶',
              '前缀编码 `now`，区间编码 = 两个前缀编码的异或',
              '对每个 `now`，查 `now` 本身和 `now ^ 2^p` 是否出现过',
              '哈希表只存最早位置，区间才最长'],
        summary=['时间 `O(10n)`，空间 `O(2^10)`',
                 '`status_dict = {0: -1}` 表示空前缀，别漏',
                 '先查表更新答案，再把 `now` 记入哈希表（已有就不覆盖）',
                 '`pow2` 循环多生成了一个 1024，不影响结果',
                 '对比灵神：灵神用数组 `pos` 和 `d in range(D)` 枚举，yiduobo 用字典和预存的 `pow2`'],
    ),
)
