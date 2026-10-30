W = 'aabbzz'


def _seg(S):
    if 'st' not in S:
        return None
    return S['st'], S.get('i', S['st'])


def _win(S):
    if 'right' not in S or 'st' not in S or 'm' not in S:
        return None
    return S['st'] + max(0, S['right'] + 1 - S['k'] * S['m'])


def _hi(S):
    if 'right' not in S or 'st' not in S or 'm' not in S:
        return None
    return S['st'] + S['right']


def _info(S):
    if 'm' in S and 's' in S:
        return (f'子串 `s = {S["s"]!r}`，枚举 `m = {S["m"]}` 种字符 → 窗口长 `k×m = {S["k"] * S["m"]}`，'
                f'每种字符都要恰好 `{S["k"]}` 次')
    if 'st' in S:
        return f'当前这一段是 `word[{S["st"]}:{S.get("i", S["st"])}]`（相邻字母差 ≤ 2）'
    return '先按「相邻字母差 ≤ 2」把 word 切成若干段，每段单独处理'


def _hit(S):
    if 'cnt' in S and 'm' in S:
        return '窗口里每个字符的次数：' + '、'.join(f"{c}={v}" for c, v in S['cnt'].items() if v) + f'（需要全是 {S["k"]}）'
    return ''


CONFIG = dict(
    num=2953, title='统计完全子字符串', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 + 枚举字符种数的定长滑窗',
    tags=['难度分 2449'],
    code='''
class Solution:
    def countCompleteSubstrings(self, word: str, k: int) -> int:
        def f(s: str) -> int:
            res = 0
            for m in range(1, 27):
                if k * m > len(s):
                    break
                cnt = defaultdict(int)
                for right, c in enumerate(s):
                    cnt[c] += 1
                    left = right + 1 - k * m
                    if left >= 0:
                        res += all(c == 0 or c == k for c in cnt.values())
                        cnt[s[left]] -= 1
            return res

        n = len(word)
        ans = i = 0
        while i < n:
            st = i
            i += 1
            while i < n and abs(ord(word[i]) - ord(word[i - 1])) <= 2:
                i += 1
            ans += f(word[st:i])
        return ans
''',
    call=f'Solution().countCompleteSubstrings({W!r}, 2)',
    expect=4,
    views=[
        dict(type='string', var='word', label='word（亮 = 当前这一段，框 = 滑窗）', cell=100, h=230,
             pointers={'st': 'purple'}, window=(_win, _hi),
             dim=lambda S, i, v: 'st' in S and not (S['st'] <= i < S.get('i', S['st'] + 1))),
        dict(type='map', var='cnt', label='cnt（窗口内各字符次数）', fmt=lambda k, v: f"'{k}': {v}", h=140, font=34),
        dict(type='text', h=100, size=28, fn=_info),
        dict(type='text', h=70, size=28, fn=_hit),
    ],
    watch=[('st', 'st', 'purple'), ('m', 'm', 'orange'), ('right', 'right', 'blue'), ('left', 'left', 'pink'), ('res', 'res', 'green'), ('ans', 'ans', 'cyan')],
    captions={
        'n = len(word)': '`n = {n}`',
        'ans = i = 0': '`ans` 累计答案，`i` 是分组循环的扫描位置',
        'while i < n:': lambda S, B, r: (f'`i = {S.i} < n`：还有一段没处理' if S.i < S.n else '`i` 到头了，所有段都处理完'),
        'st = i': '新的一段从 `st = {st}` 开始',
        21: '先把 `word[{st}]` 划进这一段，`i = {i}`',
        23: '`word[{i - 1}]` 并入这一段，`i = {i}` → 继续看下一个字母',
        'while i < n and abs': lambda S, B, r: (f'`|{S.word[S.i]} − {S.word[S.i-1]}| = {abs(ord(S.word[S.i]) - ord(S.word[S.i-1]))} ≤ 2`：并入这一段，`i` 继续右移'
                                                  if S.i < S.n and abs(ord(S.word[S.i]) - ord(S.word[S.i - 1])) <= 2
                                                  else (f'`|{S.word[S.i]} − {S.word[S.i-1]}| = {abs(ord(S.word[S.i]) - ord(S.word[S.i-1]))} > 2`：这一段到 `{S.i}` 为止' if S.i < S.n
                                                        else '已到末尾，这一段结束')),
        'ans += f(word[st:i])': lambda S, B, r: f'这一段 `{S.word[S.st:S.i]!r}` 有 `{r if r is not None else S.ans - B.ans}` 个完全子串，`ans = {S.ans}`' if 'ans' in B and S.ans != B.ans or r is not None else f'进入 `f({S.word[S.st:S.i]!r})` 处理这一段',
        'res = 0': '`res` 统计这一段内的完全子串数',
        'for m in range(1, 27)': lambda S, B, r: (f'枚举这一段里有 `m = {S.m}` 种字符' if 'm' in S and ('m' not in B or S.m != B.m or True) else ''),
        'if k * m > len(s)': lambda S, B, r: (f'`k×m = {S.k * S.m} > len(s) = {len(S.s)}`：窗口比整段还长，更大的 m 也不行 → ==break==' if S.k * S.m > len(S.s)
                                              else f'`k×m = {S.k * S.m} ≤ len(s) = {len(S.s)}`：窗口长 `{S.k * S.m}` 放得下，`cnt` 清零重新计数'),
        'cnt[c] += 1': '`s[{right}] = {c!r}` 进入窗口：`cnt[{c!r}] = {cnt[c]}`',
        'if left >= 0': lambda S, B, r: (f'`right = {S.right}`，窗口左端点 `left = {S.right} + 1 − {S.k}×{S.m} = {S.left}`：'
                                          + ('`< 0`，窗口还没长到 `k×m`，继续右扩' if S.left < 0 else '`≥ 0`，窗口刚好 `k×m` 长，可以判断')),
        'res += all': lambda S, B, r: (f'每种出现过的字符都恰好 `{S.k}` 次？{"==是==，`res`+1" if S.res != B.res else "否，不计数"} → `res = {S.res}`（值为 0 的是已移出的字符，忽略）'),
        'cnt[s[left]] -= 1': '左端点字符 `{s[left]!r}` 离开窗口：`cnt[{s[left]!r}] = {cnt[s[left]]}`',
        'break': '跳出 m 的枚举',
        'return res': '这一段共 `{res}` 个完全子串',
        'return ans': '所有段加起来，答案 =={ans}==',
    },
    skip=['for right, c in enumerate(s)', 'left = right + 1', 'cnt = defaultdict(int)', 'res = 0', 'n = len(word)'],
    max_steps=110,
    cards=dict(
        one_liner='先按字母差切段，再枚举种数 m，窗口长度就定了',
        complexity='时间 `O(n|Σ|²)`，空间 `O(|Σ|)`',
        problem=['完全子串：每个字符==恰好== `k` 次，且相邻字符字母差 ≤ 2',
                 '求 `word` 中完全子串的个数',
                 '示例：`"igigee", k=2` → `3`；本视频：`"aabbzz", k=2` → `4`'],
        quote='「相邻字母相差至多为 2」这个约束把 word 划分成了多个子串 s，每个子串分别处理。……我们可以枚举有 m 种字符，这样问题就变成了：长度固定为 m·k 的滑动窗口，判断每种字符是否都出现了恰好 k 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻差 > 2 的位置不可能同在一个完全子串里 → ==分组循环==切段',
              '一段里若有 `m` 种字符，每种恰好 `k` 次 → 子串长度必为 `m·k`',
              '枚举 `m = 1..26`，对每个 `m` 做一次定长滑窗，检查次数是否全为 `k`'],
        summary=['时间 `O(n|Σ|²)`；原文注明可优化到 `O(n|Σ|)`（维护「次数 ≠ k」的字符数）',
                 '易错：离开窗口后 `cnt` 里会留下值为 0 的键，判断时要写 `c == 0 or c == k`',
                 '`k * m > len(s)` 时直接 break，后面更大的 m 更不可能',
                 '分组循环：`st = i` 后先 `i += 1`，再向右扩到差 > 2 为止',
                 '同类：395、1763（枚举字母种类数 + 滑窗）'],
    ),
)
