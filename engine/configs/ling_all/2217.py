def _txt(S):
    if 'base' not in S:
        return ''
    L, ln = S['intLength'], S['_line']
    s = S['_inner'].get('s')
    if s is not None and ln in (7, 8, 9):
        left = s[:(L + 1) // 2]
        r = left[::-1]
        if ln == 7:
            return f"左半 `{left}` = `base + q - 1` = `{S['base']} + {S['q']} - 1`"
        return f"左半 `{left}` + 反转 `{r}` " + (f"（砍掉最低位 → `{r[1:]}`）" if L % 2 else '') + f" = =={left + r[L % 2:]}=="
    return f"`base = 10^((len-1)//2)` = =={S['base']}==：最小的左半边，之后逐个加 1"


CONFIG = dict(
    num=2217, title='找到指定长度的回文数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='只枚举左半边 · 反转拼接',
    tags=['灵神题单·数学算法', '难度分 1822'],
    code='''
class Solution:
    def kthPalindrome(self, queries: List[int], intLength: int) -> List[int]:
        ans = [-1] * len(queries)
        base = 10 ** ((intLength - 1) // 2)
        for i, q in enumerate(queries):
            if q <= 9 * base:
                s = str(base + q - 1)  # 回文数左半部分
                s += s[::-1][intLength % 2:]
                ans[i] = int(s)
        return ans
''',
    call='Solution().kthPalindrome([1, 2, 90, 91], 3)',
    expect=[101, 111, 999, -1],
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='queries', pointers={'i': 'blue'}, label='queries', h=200),
        dict(type='array', var='ans', pointers={'i': 'pink'}, label='ans', h=200,
             color=lambda S, i, v: 'green' if v != -1 and 'i' in S and i <= S['i'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('q', 'q', 'cyan'), ('base', 'base', 'orange'), 's'],
    captions={
        'ans = [-1]': '先全部填 `-1`：不存在第 `q` 个回文数时就保持 -1',
        'base = 10': '`intLength = {intLength}`，左半边最短的数是 `10^{(intLength-1)//2}` = =={base}==，这就是第 1 个回文数的左半部分',
        'for i, q': lambda S, B, r: (f'处理第 `{S.i}` 个查询：要第 `{S.q}` 小的回文数' if S.get('q') != B.get('q') or S.get('i') != B.get('i') else '所有查询处理完，循环结束'),
        'if q <= 9 * base': lambda S, B, r: (f'左半边共 `9 × {S.base}` = {9 * S.base} 种（首位不能为 0）；`{S.q} <= {9 * S.base}` → ==存在=='
                                             if S.q <= 9 * S.base else f'`{S.q} > 9 × {S.base}` = {9 * S.base}：回文数不够 → ==保持 -1=='),
        's = str(': '第 `q` 个回文数的左半 = `base + q - 1` = `{base} + {q} - 1` = =={s}==',
        's += s[::-1]': '把左半反转拼到后面；长度 `{intLength}` 为奇数时先砍掉最低位（中间那位不重复）→ `{s}`',
        'ans[i] = int': '`ans[{i}] = {s}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='回文数由左半边决定：第 q 个的左半边 = 10^a + q − 1',
        complexity='时间 `O(n·L)`（n 个查询，L = intLength），空间 `O(1)`',
        problem=['给 `queries` 和 `intLength`，求长度为 `intLength` 的正回文数中第 `queries[i]` 小的',
                 '不存在就填 `-1`，回文数不能有前导 0',
                 '示例：`[1,2,3,4,5,90], 3` → `[101,111,121,131,141,999]`',
                 '本视频：`[1,2,90,91], 3` → `[101,111,999,-1]`'],
        quote='只看回文数的左半部分，可以发现左半部分是从 `1000…0` 开始，逐渐增加的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左半边越小，整个回文数越小；所以左半边从 `10^a` 开始一个个加 1',
              '第 `q` 个的左半边 = `10^a + q - 1`，`a = (intLength-1)//2`',
              '反转后拼在后面；长度为奇数时中间那一位不重复'],
        summary=['时间 `O(n·L)`，空间 `O(1)`（返回值不计入）',
                 '左半边最多 `9 × base` 种，`q` 超过就是 `-1`',
                 '易错点：奇数长度要用 `s[::-1][intLength % 2:]` 去掉中间位',
                 '这里的 `//` 保证 `base` 是整数；`q` 最大 `10^9`，Python 大整数没有溢出问题']),
)
