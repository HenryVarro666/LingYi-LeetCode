def _t(S):
    if 'first_part' in S and 'mid_part' in S:
        return f"回文数 = `first_part` ==`{S['first_part']}`== + `mid_part` ==`{S['mid_part']}`== + `first_part` 反转 → `{S['first_part']}{S['mid_part']}{str(S['first_part'])[::-1]}`"
    if 'start_num' in S:
        return f"枚举起点：前半 `start_num = {S['start_num']}`，中间位从 `mid = {S['mid']}` 开始"
    if 'length' in S:
        return f"`N = {S['N']}` 有 {len(str(S['N']))} 位；回文数的位数取奇数 `length = {S['length']}`"
    return '偶数位回文数必是 11 的倍数，除了 11 都是合数 → ==只枚举奇数位回文数=='


CONFIG = dict(
    num=866, title='回文素数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举奇数位回文数 + 素数试除',
    tags=['灵神题单·数学算法', '数学算法'],
    code='''
class Solution(object):
    def primePalindrome(self, N):

        f = [None] * 64
        x = 2
        while x < 64:
            if f[x] is None:
                f[x] = True
                tmp = x + x
                while tmp < 64:
                    f[tmp] = False
                    tmp += x
            if x == 2:
                x += 1
            else:
                x += 2
        
        prime_list = []
        for x in range(2, 64):
            if f[x]:
                prime_list.append(x)
        
        while N <= 11:
            if self.check(N, prime_list):
                return N
            N += 1
        
        length = len(str(N))
        if length % 2 == 0:
            length += 1

        while True:
            if length == len(str(N)):
                mid = int(str(N)[length//2])
                start = int(str(N)[:length//2])
                reverse_start = int(str(N)[:length//2][::-1])
                end = int(str(N)[length//2 + 1:])
                if reverse_start >= end:
                    start_num = start
                elif reverse_start < end:
                    if mid == 9:
                        mid = 0
                        start_num = start + 1
                    else:
                        mid += 1
                        start_num = start
            else:
                start_num = int('1' + '0' * (length//2 - 1))
                mid = 0

            for first_part in range(start_num, int('1' + '0' * (length//2))):
                for mid_part in range(mid, 10):
                    now = str(first_part) + str(mid_part) + str(first_part)[::-1]
                    if self.check(int(now), prime_list):
                        return now
                mid = 0
            length += 2

    def check(self, now, prime_list):
        if now == 1:
            return False
    
        pos = 0
        while prime_list[pos] ** 2 <= now:
            if now % prime_list[pos] == 0:
                return False
            pos += 1
        
        return True
''',
    call='Solution().primePalindrome(120)',
    expect='131',
    skip=['f = [None]', 'x = 2', 'while x < 64', 'if f[x] is None', 'f[x] = True', 'tmp = x + x',
          'while tmp < 64', 'f[tmp] = False', 'tmp += x', 'if x == 2', 'x += 1', 'x += 2',
          'for x in range(2, 64)', 'if f[x]', 'prime_list.append', 'prime_list = []'],
    views=[
        dict(type='string', var=lambda S: str(S['N']), label='N', h=190, cell=90),
        dict(type='string', var=lambda S: str(S['now']) if 'now' in S and 'first_part' in S else '', label='当前回文数 now（前半 + 中间位 + 前半反转）', h=190, cell=90),
        dict(type='text', size=28, h=120, fn=_t),
        dict(type='text', size=28, h=90, fn=lambda S: (f"试除：`prime_list[{S['pos']}] = {S['prime_list'][S['pos']]}`，平方 `{S['prime_list'][S['pos']] ** 2}` vs `{S['now']}`" if 'pos' in S and 'prime_list' in S and S['pos'] < len(S['prime_list']) else '')),
    ],
    watch=[('N', 'N', 'blue'), ('length', 'length'), ('start_num', 'start_num', 'cyan'), ('first_part', 'first_part', 'pink'), ('mid_part', 'mid_part', 'orange'), ('now', 'now', 'green')],
    max_steps=80,
    captions={
        'while N <= 11': lambda S, B, r: '`N > 11`：不用逐个试，直接枚举回文数',
        'length = len(str(N))': '`N = {N}` 有 `{len(str(N))}` 位',
        'if length % 2 == 0': lambda S, B, r: ('位数是偶数：偶数位回文数是 ==11 的倍数==，除 11 外都是合数，要换成奇数位' if S.length % 2 == 0 else '位数已经是奇数，不用调整'),
        'length += 1': '`length` → `{length}`：改成枚举 {length} 位回文数',
        'while True': '按位数 `length` 逐轮找，找不到就 `length += 2`',
        'if length == len(str(N))': lambda S, B, r: ('和 `N` 同位数：要从 N 附近开始，不能漏掉比 N 大的回文数' if S.length == len(str(S.N)) else '比 `N` 位数更多：最小回文数就是 `100…001`'),
        'mid = int(': '`N` 正中间那位 `mid = {mid}`',
        'start = int(str(N)[:length//2])': '`N` 的前半 `start = {start}`',
        'reverse_start = int': '前半反转 `reverse_start = {reverse_start}`',
        'end = int': '`N` 的后半 `end = {end}`',
        'if reverse_start >= end': lambda S, B, r: (f'`{S.reverse_start} >= {S.end}`：`{S.start}{S.mid}{S.reverse_start}` 已不小于 N → 从 `start` 和 `mid` 起枚举' if S.reverse_start >= S.end else f'`{S.reverse_start} < {S.end}`：同样中间位的回文数比 N 小 → 要进位'),
        'start_num = start': '枚举起点：前半 `start_num = {start_num}`，`mid = {mid}`',
        'start_num = int': '更长位数：前半从 `{start_num}` 开始，`mid = 0`',
        'for first_part in range': '枚举前半 `first_part = {first_part}`',
        'for mid_part in range': '枚举中间位 `mid_part = {mid_part}`',
        'now = str': '拼出回文数 `now = {now}`（前半 + 中间位 + 前半反转）',
        'if self.check(': lambda S, B, r: ('检查 `now` 是不是素数' if r is None else f'`{S.now}` ' + ('==是素数== → 返回' if r else '不是素数 → 换下一个')),
        'if now == 1': '`now = {now}`，不是 1（1 不是素数，要单独排除）',
        'pos = 0': '从最小的素数 `prime_list[0] = 2` 开始试除',
        'while prime_list[pos] ** 2 <= now': lambda S, B, r: f'`{S.prime_list[S.pos]}² = {S.prime_list[S.pos] ** 2}` ' + ('`≤ now`，继续试除' if S.prime_list[S.pos] ** 2 <= S.now else '`> now`，没有因数 → 是素数'),
        'if now % prime_list[pos] == 0': lambda S, B, r: (f'`{S.now} % {S.prime_list[S.pos]} == 0` → 是合数' if S.now % S.prime_list[S.pos] == 0 else f'`{S.now} % {S.prime_list[S.pos]} = {S.now % S.prime_list[S.pos]}`，不整除'),
        'return False': '有因数 → 不是素数',
        'pos += 1': '换下一个素数',
        'return True': '没有素数因数 → `{now}` 是素数',
        'mid = 0': '一轮中间位枚举完，下一个前半从 `mid = 0` 开始',
        'return now': '找到了：最小的回文素数是 =={now}==',
        'length += 2': '这一位数没找到，换更长的奇数位',
    },
    cards=dict(
        one_liner='偶数位回文数是 11 的倍数，只枚举奇数位回文数',
        complexity='时间约 `O(回文数个数 × π(√X))`，空间 `O(π(√X))`',
        problem=['求不小于 `N` 的最小==回文素数==（正着读倒着读都一样的素数）',
                 '示例：`N = 6` → `7`；`N = 8` → `11`；`N = 13` → `101`',
                 '本视频：`N = 120` → `131`（返回的是字符串 `"131"`）'],
        quote='对于位数为偶数的回文数，其必然是11的倍数，其中只有11为素数，其他都是合数，因此在N>11时就不需要考虑位数为偶数的回文数了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用筛法列出一批素数，试除只用这些素数',
              '回文数 = ==前半 + 中间位 + 前半反转==，枚举前半和中间位即可',
              '起点：同位数时从 `N` 的前半和中间位附近出发，不够就进位'],
        before=[dict(heading='先筛素数', lines=['原文筛到 16384（答案在 2×10^9 内）；本例数很小，视频里改筛到 64', '筛出素数放进 `prime_list`', '这一步循环很多，视频中直接略过', '素数判断：`check` 只拿 `prime_list` 里的素数试除'])],
        summary=['原文为 Python 2 写法，整数除法 `length/2` 已改为 `length//2`；筛素数的上界 16384 为演示改成了 64',
                 '易错点：==偶数位（除 11）一律不是素数==，所以 `length` 要改奇数',
                 '易错点：`mid == 9` 时进位，前半加一、中间位归零',
                 '`N <= 11` 单独逐个检查；注意返回值：小 `N` 返回整数，其余返回字符串（LeetCode 判题会转换）'],
    ),
)
