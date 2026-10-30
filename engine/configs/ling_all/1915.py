W = 'abaab'


def _i(S):
    return sum(S['cnt']) - (1 if S['_line'] == 10 else 0) if 'cnt' in S else None


def _bits(s):
    return format(s, '010b')


def _par(S):
    if 's' not in S:
        return '用 ==10 位二进制== 记每个字母出现次数的奇偶：第 i 位为 1 表示字母 i 出现奇数次'
    s = S['s']
    odd = [chr(97 + i) for i in range(10) if s >> i & 1]
    return f'前缀状态 `s = {_bits(s)}`：奇数次的字母 ==' + ('、'.join(odd) if odd else '无') + '=='


CONFIG = dict(
    num=1915, title='最美子字符串的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='状态压缩前缀和 + 异或',
    tags=['前缀和', '状态压缩前缀和', '难度分 2235'],
    code='''
class Solution:
    def wonderfulSubstrings(self, word: str) -> int:
        cnt = [0] * 1024
        cnt[0] = 1  # 初始前缀和为 0，需将其计入出现次数
        ans = s = 0
        for c in word:
            s ^= 1 << (ord(c) - ord('a'))  # 计算当前前缀和
            ans += cnt[s]  # 所有字母均出现偶数次
            ans += sum(cnt[s ^ (1 << i)] for i in range(10))  # 枚举其中一个字母出现奇数次，反转该字母的出现次数的奇偶性
            cnt[s] += 1  # 更新前缀和出现次数
        return ans
''',
    call=f'Solution().wonderfulSubstrings({W!r})',
    expect=11,
    views=[
        dict(type='string', var='word', label='word', pointers={'sum(cnt) - (_line == 10)': 'blue'}, pointer_labels={'sum(cnt) - (_line == 10)': '当前字符'}, cell=100, h=230),
        dict(type='text', h=90, size=30, fn=_par),
        dict(type='map', var=lambda S: {_bits(i): v for i, v in enumerate(S['cnt']) if v} if 'cnt' in S else {},
             label='cnt（出现过的前缀状态 → 次数）', fmt=lambda k, v: f'{k}: {v}', h=330, font=30),
    ],
    watch=[('s', "format(s, '010b')", 'blue'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [0]': '`cnt[x]`：前缀状态为 `x` 的前缀出现了几次，状态只有 `2^10 = 1024` 种',
        'cnt[0] = 1': '空前缀的状态是 `0`，先记一次：这样从开头起的子串也能被数到',
        'ans = s = 0': '`ans` 和前缀状态 `s` 都从 0 开始',
        's ^= 1 <<': '读到 `{c}`：把第 `{ord(c) - 97}` 位翻转（异或 = 模 2 加法）→ `s = {format(s, "010b")}`',
        'ans += cnt[s]  #': '之前有 `{cnt[s]}` 个前缀状态和 `s` 相同：它们之间的子串每个字母都出现偶数次 → `ans` = =={ans}==',
        'ans += sum': '再翻转一位去查：差一位的前缀恰好让 ==一个字母为奇数次==，这一步累加后 `ans` = =={ans}==',
        'cnt[s] += 1': '当前前缀也记进去，供后面的字符使用：`cnt[{format(s, "010b")}]` = {cnt[s]}',
        'return ans': '共有 `{ans}` 个最美子字符串',
    },
    cards=dict(
        one_liner='只关心奇偶：前缀异或后，差 0 位或 1 位的前缀配对',
        complexity='时间 `O(10n)`，空间 `O(2^10)`',
        problem=['至多一个字母出现奇数次的子串叫最美子串',
                 '字符串只含 `a` 到 `j`，统计最美子串个数',
                 '示例：`"aabb"` → `9`；本视频：`"abaab"` → `11`'],
        quote='异或运算的本质是在模 2 剩余系中进行加法运算，刚好对应奇偶性的变化。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把「每个字母的出现次数」压成「奇偶性」，用 10 位二进制数表示',
              '前缀状态相同 → 中间子串全是偶数次；差恰好一位 → 恰好一个奇数次',
              '用 `cnt` 数组统计每个状态出现次数，枚举 10 个比特翻转后查表'],
        summary=['时间 `O(10n)`，空间 `O(1024)`',
                 '`cnt[0] = 1` 不能漏：空前缀也是一个前缀',
                 '先查 `cnt` 再更新 `cnt[s]`，否则会数到空子串',
                 '同类题：1371、1542、974、560'],
    ),
)
