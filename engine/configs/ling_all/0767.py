CONFIG = dict(
    num=767, title='重构字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='出现次数最多的先填，隔一个位置填',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1681'],
    code='''
class Solution:
    def reorganizeString(self, s: str) -> str:
        n = len(s)
        a = Counter(s).most_common()  # 按出现次数从大到小排序
        m = a[0][1]
        if m > n - m + 1:
            return ""

        ans = [''] * n
        i = 0
        for ch, cnt in a:
            for _ in range(cnt):
                ans[i] = ch
                i += 2
                if i >= n:
                    i = 1  # 填完偶数填奇数
        return ''.join(ans)
''',
    call='Solution().reorganizeString("aaabbc")',
    expect='ababac',
    views=[
        dict(type='string', var='s', label='s', h=110),
        dict(type='array', var='ans', label='ans（填好的位置）', pointers={'i': 'blue'}, h=170),
        dict(type='text', fn=lambda S: (f"n = `{S['n']}`，最多的字母出现 `m = {S['m']}` 次，上限 `n − m + 1` = =={S['n'] - S['m'] + 1}==" if 'm' in S else ''), h=60),
    ],
    watch=[('n', 'n', 'blue'), ('m', 'm', 'orange'), ('ch', 'ch', 'pink'), ('cnt', 'cnt', 'cyan'), ('i', 'i', 'green')],
    captions={
        'a = Counter': '统计每个字母的次数，==出现最多的排最前==：`{a}`',
        'm = a[0][1]': '`m` = 出现最多的字母的次数 = =={m}==',
        'if m > n - m + 1': lambda S, B, r: (f'`m = {S.m} > n - m + 1 = {S.n - S.m + 1}`：最多的字母比其余字母多太多，怎么排都会相邻 → ==无解=='
                                            if S.m > S.n - S.m + 1 else
                                            f'`m = {S.m} ≤ n - m + 1 = {S.n - S.m + 1}`：可以做到，开始填'),
        "ans = ['']": '`ans` 先放 `{n}` 个空位',
        'i = 0': '从下标 `0` 开始，每次隔一个位置填',
        'for ch, cnt in a': lambda S, B, r: ('所有字母都填完了' if all(S.ans) else f'轮到字母 `{S.ch}`，要填 `{S.cnt}` 个'),
        'for _ in range': lambda S, B, r: (f'`{S.ch}` 已经填够 {S.cnt} 个，换下一个字母' if S.ans.count(S.ch) >= S.cnt
                                           else f'`{S.ch}` 还差 {S.cnt - S.ans.count(S.ch)} 个，继续填'),
        'ans[i] = ch': '把 `{ch}` 填到下标 `{i}`',
        'i += 2': '隔一个位置：`i` → {i}，同一个字母不会相邻',
        'if i >= n': lambda S, B, r: (f'`i = {S.i} >= n = {S.n}`：偶数位填满了，改填奇数位' if S.i >= S.n
                                      else f'`i = {S.i} < n`，继续往后填'),
        'i = 1': '偶数位填完 → `i = 1`，==从奇数位开始填==',
        "return ''.join": '拼起来：相邻字母都不同 → =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='出现最多的字母先填偶数位，其余接着填，隔一个就不会相邻',
        complexity='时间 `O(n + |Σ|log|Σ|)`，空间 `O(n)`',
        problem=['重排字符串 `s`，使任意两个相邻字符不同；不行就返回 `""`',
                 '`aab` → `aba`；`aaab` → `""`',
                 '本视频：`aaabbc` → `ababac`（a 出现 3 次，刚好卡在上限 4 以内）'],
        quote='设 n 为 s 的长度，m 为是出现次数最多的字母的出现次数。结论：如果 m≤n−m+1，则可以做到，否则无法做到。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用结论判断：最多的字母 `m` 超过 `n − m + 1` 就无解',
              '否则==按次数从大到小==，依次填下标 `0,2,4,…`，填满后再填 `1,3,5,…`',
              '最多的字母占满偶数位的前面，其余字母隔开它们，所以不会相邻'],
        summary=['时间 `O(n + |Σ|log|Σ|)`，字符集 26 个，空间 `O(n)`',
                 '易错：必须==最多的字母先填==，否则 aaabb 会排成 babaa',
                 '灵神写法二：只让最多的先填，其余不排序，复杂度 `O(n + |Σ|)`',
                 '同类：§1.8 相邻不同；思考题：要求字典序最小怎么做'],
    ),
)
