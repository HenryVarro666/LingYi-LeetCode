S0, Q0 = 'abcda', [[0, 3, 1], [0, 4, 1]]


def _txt(S):
    if 'cnt_dict_list' not in S:
        return ''
    if 'odd' not in S:
        return '`cnt_dict_list[i]` = s[0..i] 里每个字母的出现次数（字典的拷贝）'
    if S.get('index') is None or 'char' not in S or S['_line'] not in (19, 20):
        return f'本次询问 `[{S["l"]}, {S["r"]}, {S["k"]}]`：区间长 {S["r"] - S["l"] + 1}，`odd = {S["odd"]}`，`2k = {2 * S["k"]}`'
    c = S['char']
    return f'字母 `{c}`：前缀 r 里 `{S["cnt_dict_list"][S["r"]].get(c, 0)}` 次 − 前缀 l−1 里 `{S["cnt_dict_list"][S["l"] - 1].get(c, 0) if S["l"] > 0 else 0}` 次 = ==区间内 {S["cnt"]} 次==，已统计奇数次的字母 `odd = {S["odd"]}`'


CONFIG = dict(
    num=1177, title='构建回文串检测', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='计数前缀数组 + 奇数次字符配对',
    tags=['前缀和', '状态压缩前缀和', '难度分 1848'],
    code='''
class Solution(object):
    def canMakePaliQueries(self, s, queries):

        cnt_dict = {}
        cnt_dict_list = []
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
            cnt_dict_list.append(cnt_dict.copy())
        
        res = []
        for l, r, k in queries:
            odd = 0
            for index in range(26):
                char = chr(index + 97)
                cnt = cnt_dict_list[r].get(char, 0)
                if l > 0:
                    cnt -= cnt_dict_list[l - 1].get(char, 0)
                
                if cnt % 2 == 1:
                    odd += 1
            
            if (r - l + 1) % 2 == 1:
                odd -= 1
            
            res.append(odd <= k + k)
        
        return res
''',
    call=f'Solution().canMakePaliQueries({S0!r}, {Q0!r})',
    expect=[False, True],
    views=[
        dict(type='string', var='s', label='s（框 = 当前询问的区间 [l, r]）', cell=90, h=170, window=('l', 'r')),
        dict(type='map', var='cnt_dict', label='cnt_dict（当前前缀里各字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
        dict(type='text', h=110, size=26, fn=_txt),
        dict(type='array', var='res', label='res', cell=90, h=130, color=lambda S, i, v: 'green' if v else 'pink'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('k', 'k', 'yellow'), ('odd', 'odd', 'orange')],
    skip=['for index in range(26)', 'if cnt % 2 == 1', 'char = chr', 'cnt = cnt_dict_list', 'if l > 0', 'cnt -= '],
    captions={
        'cnt_dict[char] =': '`{char}` 又出现一次：当前前缀里 `{char}` 共 `{cnt_dict[char]}` 次',
        'cnt_dict_list.append': '把这一刻的计数==拷贝==存下来（`copy()`），它就是长为 `{len(cnt_dict_list)}` 的前缀的次数表',
        'for l, r, k': lambda S, B, ret: (f'询问 `[{S.l}, {S.r}, {S.k}]`：区间 `{S.s[S.l:S.r + 1]}`' if B.get('l') != S.l or B.get('r') != S.r or 'odd' not in B or B.get('res') != S.get('res') else '询问处理完毕'),
        'odd = 0': '`odd` 统计区间里==出现奇数次==的字母种数，先清零；接着逐个检查 26 个字母（视频只停在奇数次的字母上）',
        'for index in range(26)': lambda S, B, ret: ('逐个检查 26 个字母（视频里只高亮有变化的）' if S.index == 0 else f'检查字母 `{chr(S.index + 97)}`'),
        'if cnt % 2 == 1': lambda S, B, ret: (f'`{S.char}` 在区间里出现 `{S.cnt}` 次，奇数 → 无法配对' if S.cnt % 2 == 1 else f'`{S.char}` 出现 `{S.cnt}` 次，偶数（含 0）→ 可以成对放两侧'),
        'odd += 1': '`{char}` 在区间里出现 `{cnt}` 次，奇数 → 无法配对，`odd` → {odd}',
        'if (r - l + 1) % 2 == 1': lambda S, B, ret: (f'区间长 `{S.r - S.l + 1}` 是奇数：落单字符里有一个可放在==最中间==，所以 `odd − 1`' if (S.r - S.l + 1) % 2 else f'区间长 `{S.r - S.l + 1}` 是偶数：没有中心，不用减'),
        'odd -= 1': '`odd` → {odd}（中心位置消掉一个）',
        'res.append': lambda S, B, ret: (f'`odd = {S.odd} <= 2k = {2 * S.k}` → ==能==：每次修改可以让两个落单字符配对' if S.odd <= 2 * S.k else f'`odd = {S.odd} > 2k = {2 * S.k}` → ==不能==：修改次数不够'),
        'return res': '返回 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='数奇数次的字符：每次修改最多让两个落单字符配对',
        complexity='时间 `O(26·(n+q))`，空间 `O(26·n)`（每个前缀存一份字典）',
        problem=['每次询问 `[l, r, k]`：区间内字符可以==任意重排==，并最多替换 `k` 个',
                 '问能否变成回文串',
                 '本视频：`s = "abcda"`，询问 `[0,3,1]`、`[0,4,1]` → `[false, true]`'],
        quote='设给定区间有n个出现奇数次的字符，若区间长度为奇数则需要将n减去1，表示目前一共有n个字符无法配对。那么在一次修改之后，我们可以将其中两个字符配对。',
        quote_src='—— yiduobo 题解原文',
        idea=['出现偶数次的字符对称放两侧；奇数次的各剩一个落单',
              '区间长度为奇数时，可以把一个落单字符放中间',
              '剩下 `odd` 个落单，k 次修改最多配掉 `2k` 个 → 比较 `odd` 与 `2k`',
              '区间内次数 = 前缀 r 的次数 − 前缀 l−1 的次数'],
        summary=['时间 `O(26(n+q))`，空间 `O(26n)`，比位运算写法慢但直观',
                 '`l == 0` 时没有前缀 `l-1`，不能减',
                 '`odd` 要先减去中心再和 `2k` 比较，不是 `k`',
                 '原文已是 Python 3 可运行的写法，仅保留代码不改',
                 '对比灵神：灵神把 26 个计数压成一个二进制数，用异或和 `bit_count` 一步得到 `m`'],
    ),
)
