CONFIG = dict(
    num=1663, title='具有给定数值的最小字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='高位尽量填 a · 剩余位用 z 兜底',
    tags=['灵神题单', '贪心算法'],
    code='''
class Solution(object):
    def getSmallestString(self, n, k):

        res = []
        now = 0
        max_rest = 26 * n
        while now < n:
            if max_rest - k > 24:
                res.append('a')
                max_rest -= 26
                k -= 1
            else:
                res.append(chr(97 + (k - 1) % 26))
                break
        
        while len(res) < n:
            res.append('z')
        
        return ''.join(res)
''',
    call='Solution().getSmallestString(5, 73)',
    expect='aaszz',
    views=[
        dict(type='text', fn=lambda S: (f"`max_rest - k = {S['max_rest']} - {S['k']} = {S['max_rest'] - S['k']}`，"
                                        + ('> 24 → 当前位放 a，后面仍凑得到' if S['max_rest'] - S['k'] > 24 else '≤ 24 → 当前位不能再放 a')
                                        ) if 'max_rest' in S and 'res' in S and S['_line'] in (9, 10) else
             (f"后面的位全放 z，所以这一位 = `(k − 1) % 26 + 1 = {(S['k'] - 1) % 26 + 1}`" if 'res' in S and S['_line'] == 14 else ''), size=26),
        dict(type='array', var='res', label='res（目前已确定的高位字母）', cell=84,
             color=lambda S, i, v: 'green' if v == 'a' else ('yellow' if v == 'z' else 'blue')),
        dict(type='text', fn=lambda S: f"还需凑 `k = {S['k']}`，剩余位置最大能凑到 `max_rest = {S['max_rest']}`" if 'max_rest' in S else '', size=24),
    ],
    watch=['n', ('k', 'k', 'blue'), ('max_rest', 'max_rest', 'orange'), ('len(res)', 'len(res)')],
    captions={
        'res = []': '`res` 从高位到低位存字母',
        'now = 0': '（`now` 只用来写循环条件，循环靠 break 结束）',
        'max_rest = 26 * n': '全填 z 时数值最大：`max_rest = 26 * {n} = {max_rest}`',
        'while now < n': '继续考察下一位',
        'if max_rest - k > 24': lambda S, B, r: (f"当前位放 a 后，剩下 `n-1` 位最多 `max_rest - 26 = {S.max_rest - 26}`，要凑 `k - 1 = {S.k - 1}`。"
                                                  + (f"`{S.max_rest - 26} ≥ {S.k - 1}` 成立 → ==能放 a==" if S.max_rest - S.k > 24
                                                     else f"`{S.max_rest - 26} < {S.k - 1}` 不成立 → ==不能放 a==")),
        "res.append('a')": '放 a，`res = {res}`',
        'max_rest -= 26': '剩余位少一位：`max_rest` → {max_rest}',
        'k -= 1': 'a 的数值是 1：`k` → {k}',
        'res.append(chr': '后面全放 z，这一位只能 `(k-1) % 26 + 1`：放 `{res[-1]}`',
        'break': '这一位已经受限，后面不再有放 a 的机会',
        'while len(res) < n': lambda S, B, r: (f'`len(res) = {len(S.res)} < {S.n}`：还差几位，用 z 补' if len(S.res) < S.n else '长度够了'),
        "res.append('z')": '补一个 z：`res = {res}`',
        'return': '拼成答案：`{ret}`',
    },
    cards=dict(
        one_liner='高位尽量放 a，直到后面必须靠 z 才能凑够',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['小写字母 a~z 的数值是 1~26',
                 '求长度为 `n`、数值之和为 `k` 的==字典序最小==字符串',
                 '示例：`n = 5, k = 73` → `"aaszz"`'],
        quote='若当前的rest - 26 >= k - 1时，就将当前位填充上a，并将rest减去26，k减去1，然后继续考察下一位。',
        quote_src='—— yiduobo 题解原文',
        idea=['字典序最小 → 高位尽量放 a；前提是后面的位还能凑到 `k - 1`',
              '`max_rest` 是剩余位全放 z 的最大数值，放 a 的条件就是 `max_rest - 26 >= k - 1`',
              '不能放 a 时，这一位受限：后面全放 z，这一位取 `(k - 1) % 26 + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`max_rest - k > 24` 就是原文条件 `max_rest - 26 >= k - 1` 的整数写法',
                 '易错：受限位之后全部放 z，不是继续放 a',
                 '原文 `now` 变量没有自增，循环靠 `break` 退出；这里保持原样'],
    ),
)
