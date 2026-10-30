WORDS = ["bcd", "aaa", "yza", "bcd", "zzz"]


def _show(c):
    return str(ord(c)) if len(c) == 1 and ord(c) < 26 else c


def _key(t):
    return '(' + ','.join(str(ord(c)) for c in t) + ')'


def _tcells(S):
    t = S.get('t')
    if t is None:
        return None
    return [_show(c) for c in t]


CONFIG = dict(
    num=3805, title='统计凯撒加密对数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='平移成首字母 a + 枚举右，维护左',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1624'],
    code='''
class Solution:
    def countPairs(self, words: List[str]) -> int:
        cnt = defaultdict(int)
        ans = 0
        for s, c in Counter(words).items():
            t = list(s)
            base = ord(t[0])
            for i in range(len(t)):
                t[i] = chr((ord(t[i]) - base) % 26)  # 保证结果在 [0, 25] 中
            t = ''.join(t)
            ans += cnt[t] * c + c * (c - 1) // 2  # c 个 s 中选 2 个有 C(c, 2) 种方案
            cnt[t] += c
        return ans
''',
    call=f'Solution().countPairs({WORDS})',
    expect=4,
    views=[
        dict(type='array', var='words', label='words', h=170, cell=110,
             color=lambda S, i, v: 'blue' if v == S.get('s') else None),
        dict(type='array', var=_tcells, label='t：每个字母减去首字母（数字 = 已平移成 0~25）', h=180, cell=96,
             pointers={'i': 'pink'},
             color=lambda S, i, v: 'green' if v.isdigit() else None),
        dict(type='map', var='cnt', label='cnt（平移后的串 → 个数；如 (0,1,2) 就是 abc）', fmt=lambda k, v: f'{_key(k)}: {v}', h=150, font=32),
    ],
    watch=[('s', 's', 'blue'), ('c', 'c', 'orange'), 'base', ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 统计左边每种“平移后的串”出现的次数',
        'ans = 0': '`ans` 累计相似对数',
        'for s, c in Counter': lambda S, B, r: (f'优化：相同的串一起处理，`{S.s!r}` 出现 `c = {S.c}` 次' if B.get('s') != S.s else '所有不同的串都处理完了'),
        't = list(s)': '把 `{s!r}` 拆成字母，准备整体平移',
        'base = ord(t[0])': '以首字母 `{s[0]!r}` 为基准：==平移到首字母变成 a==',
        'for i in range(len(t))': lambda S, B, r: (f'处理第 {S.i} 个字母' if B.get('i') != S.i or not isinstance(B.get('t'), list) else '平移完成'),
        't[i] = chr(': lambda S, B, r: f'`({S.s[S.i]!r} − {S.s[0]!r}) % 26 = {ord(S.t[S.i])}`：' + ('==负数取模==回到 [0, 25]' if ord(S.s[S.i]) < ord(S.s[0]) else '离首字母的距离'),
        "t = ''.join(t)": lambda S, B, r: f'`{S.s!r}` 平移后是 `{_key(S.t)}`：相似的串平移后==完全相同==',
        'ans += cnt[t]': lambda S, B, r: f'左边有 `{S.cnt[S.t]}` 个相似串，每个和这 `{S.c}` 个配对，组内再 `C({S.c}, 2)`：`ans` += `{S.ans - B.ans}` → =={S.ans}==',
        'cnt[t] += c': lambda S, B, r: f'维护左：`cnt[{_key(S.t)}]` → `{S.cnt[S.t]}`',
        'return ans': '共 `{ans}` 对相似字符串',
    },
    max_steps=75,
    cards=dict(
        one_liner='把每个串平移到首字母为 a，相似 ⇔ 平移后相同',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['一次操作把串的==每个字母==都变成下一个（z → a）',
                 '两个串能通过操作变相等就==相似==，求相似的 `(i < j)` 对数',
                 '示例：`["ab","aa","za","aa"]` → `2`',
                 '本视频：`["bcd","aaa","yza","bcd","zzz"]` → `4`'],
        quote='把字符串通过操作，改成==第一个字母是 a==，就能看出这两个字符串都是 abc 通过循环替换得到的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`bcd`、`yza` 平移后都是 `abc`（距离 0,1,2）→ 相似',
              '枚举右，维护左：先查 `cnt[t]` 加进答案，再把 `cnt[t]` 加一',
              '优化：同一个串出现 `c` 次，一次算 `cnt[t] × c + C(c, 2)`'],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '`(ord − base) % 26` 处理 `z → a` 的回绕，负数也能取模',
                 '优化前写法逐个串处理：`ans += cnt[t]; cnt[t] += 1`',
                 '答案与顺序无关，所以可以先用 `Counter` 合并相同串',
                 '也可以用长为 `m − 1` 的差分数组当哈希键'],
    ),
)
