W = 'aba'


def _i(S):
    return sum(S['cnt_dict'].values()) - (1 if S['_line'] == 13 else 0) if 'cnt_dict' in S else None


def _bits(s):
    return format(s, '010b')


def _par(S):
    if 'now' not in S:
        return '10 个字母 → 用 ==2 进制状态码== 表示每个字母的奇偶性'
    s = S['now']
    odd = [chr(97 + i) for i in range(10) if s >> i & 1]
    return f'`now = {_bits(s)}`：奇数次的字母 ==' + ('、'.join(odd) if odd else '无') + '=='


CONFIG = dict(
    num=1915, title='最美子字符串的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='奇偶状态码 + 哈希表计数',
    tags=['前缀和', '状态压缩前缀和', '难度分 2235'],
    code='''
class Solution(object):
    def wonderfulSubstrings(self, word):

        cnt_dict = {0 : 1}
        now = 0
        res = 0
        for char in word:
            now = now ^ (1 << (ord(char) - 97))
            res += cnt_dict.get(now, 0)
            for index in range(10):
                res += cnt_dict.get(now ^ (1 << index), 0)
            
            cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        return res
''',
    call=f'Solution().wonderfulSubstrings({W!r})',
    expect=4,
    views=[
        dict(type='string', var='word', label='word', pointers={'sum(cnt_dict.values()) - (_line == 13)': 'blue'}, pointer_labels={'sum(cnt_dict.values()) - (_line == 13)': '当前字符'}, cell=100, h=230),
        dict(type='text', h=90, size=30, fn=_par),
        dict(type='map', var=lambda S: {_bits(k): v for k, v in S['cnt_dict'].items()} if 'cnt_dict' in S else {},
             label='cnt_dict（奇偶状态 → 前缀个数）', fmt=lambda k, v: f'{k}: {v}', h=330, font=30),
    ],
    skip=['for index in'],
    watch=[('now', "format(now, '010b')", 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {0': '哈希表记每种奇偶状态的前缀个数；空前缀状态为 0，先记 1 个',
        'now = 0': '`now`：到当前字符为止的前缀奇偶状态；`res` 累计答案',
        'now = now ^': '第 1 步：用 `{char}` 更新 `now`，翻转第 `{ord(char) - 97}` 位 → `{format(now, "010b")}`',
        'res += cnt_dict.get(now, 0)': '第 2 步：以前有 `{cnt_dict.get(now, 0)}` 个前缀状态也是 `now` → 它们到当前之间每个字母都是偶数次 → `res` = =={res}==',
        'for index': '第 3 步：枚举 10 个字母，看谁可以出现奇数次',
        'res += cnt_dict.get(now ^': '假设字母 `{chr(97 + index)}` 为奇数次，状态码 `{format(now ^ (1 << index), "010b")}`，查到 {cnt_dict.get(now ^ (1 << index), 0)} 个 → `res` = {res}',
        'cnt_dict[now] =': '第 4 步：把 `now` 记入哈希表 → `{format(now, "010b")}`: {cnt_dict[now]}',
        'return res': '一共 `{res}` 个最美子字符串',
    },
    cards=dict(
        one_liner='区间转前缀：两个前缀奇偶状态相同或差一位',
        complexity='时间 `O(10n)`，空间 `O(2^10)`',
        problem=['至多一个字母出现奇数次 → 最美字符串',
                 '`word` 只含 `a` 到 `j`，求最美子串个数',
                 '示例：`"aba"` → `4`；`"aabb"` → `9`'],
        quote='题目只需要关注子字符串中各个字母的奇偶性，而不关心具体的数值。注意到题目中只有10个字符，那么可以使用2进制状态压缩来表示字符串的奇偶性。',
        quote_src='—— yiduobo 题解原文',
        idea=['子串的奇偶性 = 两个前缀奇偶状态的异或（区间转前缀）',
              '一趟遍历：哈希表 `cnt_dict` 记每种状态的前缀数，`now` 记当前状态',
              '先查「相同状态」，再枚举 10 位「差一位」，最后更新哈希表'],
        summary=['时间 `O(10n)`，空间 `O(2^10)`',
                 '原文哈希表用 `get(…, 0)` 取默认值，状态码只有 1024 种',
                 '更新哈希表要放在查询之后',
                 '对比灵神：灵神用 `cnt` 数组，这里用字典；思路相同'],
    ),
)
