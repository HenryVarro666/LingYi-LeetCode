S0 = 'abbc'


def _bal(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'cnt' not in S:
        return None
    return i - j + 1 == len(S['cnt']) * S['max_cnt']


def _sc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if j is not None and S.get('_line') in (9, 10, 11, 12) and j <= k <= i:
        return 'green' if (S.get('_line') in (11, 12) and _bal(S)) else 'yellow'
    return 'blue' if k == i else None


def _fc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if k == i + 1:
        return 'yellow'
    if j is not None and S.get('_line') in (11, 12) and k == j and _bal(S):
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return '`f[k]` = 前 `k` 个字符最少分成几段；子串平衡 ⇔ 长度 = 种类数 × 最大次数'
    if j is not None and S.get('_line') in (9, 10, 11, 12) and 'cnt' in S:
        L, k, m = i - j + 1, len(S['cnt']), S['max_cnt']
        if S.get('_line') == 9:
            return f'`s[{j}..{i}] = "{S["s"][j:i + 1]}"`：把 `s[{j}]` 计入 `cnt`'
        return f'长度 `{L}`，种类 `{k}` × 最大次数 `{m}` = `{k * m}` → ' + ('==相等，平衡==' if L == k * m else '不等，不平衡')
    return f'求 `f[{i + 1}]`：倒着枚举最后一段的起点 `j`，边扩张边数字符'


CONFIG = dict(
    num=3144, title='分割字符频率相等的最少子字符串', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（倒序枚举 + 长度 = 种类数 × 最大次数）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1917'],
    code='''
class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        n = len(s)
        f = [0] + [inf] * n
        for i in range(n):
            cnt = defaultdict(int)
            max_cnt = 0
            for j in range(i, -1, -1):
                cnt[s[j]] += 1
                max_cnt = max(max_cnt, cnt[s[j]])
                if i - j + 1 == len(cnt) * max_cnt:
                    f[i + 1] = min(f[i + 1], f[j] + 1)
        return f[n]
''',
    call=f'Solution().minimumSubstringsInPartition({S0!r})',
    expect=2,
    skip=['for j in range', 'max_cnt = 0', 'max_cnt = max'],
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s（蓝 = 位置 i，黄 = 当前子串 s[j..i]，绿 = 平衡）', h=190, cell=70, pointers={'j': 'pink', 'i': 'blue'}, color=_sc),
        dict(type='map', var='cnt', label='cnt：s[j..i] 里每个字符的出现次数', h=100, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f[k]（黄 = 正在算 f[i+1]，绿 = 平衡时用到的 f[j]）', h=170, cell=70, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('max_cnt', 'max_cnt', 'yellow'), ('f[n]', 'f[-1]', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [0] + [inf] * n': '`f[0] = 0`：空串 0 段（对应 `dfs(-1) = 0`），其余先设成 `inf`；单个字母必平衡，所以一定有解',
        'for i in range(n)': lambda S, B, r: (f'`i = {S.i}`：剩余字符串是 `s[0..{S.i}]`，要把 `f[{S.i+1}]` 算出来' if S.get('i') != B.get('i')
                                              else '所有 `i` 都算完了'),
        'cnt = defaultdict': '每个 `i` 新开一张计数表、`max_cnt = 0`（子串里出现次数最多的字符的次数），再往左边扩张子串',
        'cnt[s[j]] += 1': '子串向左扩一格，纳入 `s[{j}] = {s[j]}`：`cnt[{s[j]}]` = {cnt[s[j]]}，现在是 `s[{j}..{i}] = "{s[j:i+1]}"`',
        'if i - j + 1 == len(cnt)': lambda S, B, r: (f'长度 `{S.i - S.j + 1}`，`len(cnt) × max_cnt` = `{len(S.cnt)} × {S.max_cnt}` = {len(S.cnt) * S.max_cnt} → ==相等==：每个字符都恰好出现 {S.max_cnt} 次，平衡'
                                                    if S.i - S.j + 1 == len(S.cnt) * S.max_cnt
                                                    else f'长度 `{S.i - S.j + 1}` ≠ `{len(S.cnt)} × {S.max_cnt}` = {len(S.cnt) * S.max_cnt} → 有字符出现次数不够，不平衡'),
        'f[i + 1] = min': '把 `s[{j}..{i}]` 当最后一段：前面剩 `f[{j}]` = {f[j]} 段，`f[{i+1}] = min({B.f[i+1]}, {f[j]} + 1)` = =={f[i+1]}==',
        'return f[n]': '整串最少分成 `f[{n}]` = =={ret}== 个平衡子串',
    },
    cards=dict(
        one_liner='倒着枚举最后一段，平衡 ⇔ 长度 = 种类数 × 最大次数',
        complexity='时间 `O(n^2)`，空间 `O(n + |Σ|)`',
        problem=['把 `s` 分成若干「平衡」子串：每个字符出现的次数都相同',
                 '求最少能分成几个平衡子串（单个字母一定平衡，所以一定有解）',
                 '示例：`"fabccddg"` → `3`；视频用 `"abbc"` → `2`（`"ab"` + `"bc"`）'],
        quote='设子串中有 k 种字母，字母出现次数的最大值为 maxCnt。子串是平衡的，当且仅当子串长度 i-j+1 等于 k·maxCnt。',
        quote_src='—— 灵茶山艾府题解（二、状态定义与状态转移方程）',
        idea=['`f[i+1]` 表示 `s[0..i]` 最少分几段：枚举最后一段 `s[j..i]`，平衡就 `f[j] + 1`',
              '倒序枚举 `j` 的同时用哈希表计数，不用每次重新数',
              '判平衡不用检查每个字符：次数最大值 × 种类数 = 长度，说明所有字符都一样多'],
        summary=['时间 `O(n^2)`：状态 `O(n)`，每个状态枚举 `j` 是 `O(n)`',
                 '易错：`cnt`、`max_cnt` 必须在每个 `i` 重新初始化；`f` 开 `n+1` 格',
                 '`f[0] = 0` 对应空串，`f[j]` 里的 `j` 正好是前面剩下的长度',
                 '题解先给了 `@cache` 记忆化搜索；还有手动 if 比大小的写法二，思路相同'],
    ),
)
