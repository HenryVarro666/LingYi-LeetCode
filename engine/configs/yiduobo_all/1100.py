def _win(S):
    k = S['k']
    i = S.get('index')
    if i is None:
        return (0, k - 1)
    line = S.get('_line', 0)
    if line <= 17:
        return (i, i + k - 1)
    if line == 18:
        return (i, i + k)
    return (i + 1, i + k)


def _txt(S):
    if 'cnt' not in S:
        return f"窗口长度 `k = {S['k']}`：哈希表里恰好 k 种字符 → 每个字符都只出现 1 次"
    zero = [c for c, v in S['cnt'].items() if v == 0]
    if zero:
        return f"`{zero[0]}` 的次数已是 0，还留在表里 → ==len 虚高，必须 pop=="
    n = len(S['cnt'])
    return f"哈希表有 `{n}` 种字符，`k = {S['k']}` → " + ('==没有重复，合法==' if n == S['k'] else '有重复，不合法')


CONFIG = dict(
    num=1100, title='长度为K的无重复字符子串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长窗口 + 计数哈希表',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numKLenSubstrNoRepeats(self, s, k):

        n = len(s)
        if n < k:
            return 0
        
        cnt = {}
        for char in s[:k]:
            cnt[char] = cnt.get(char, 0) + 1
        
        if len(cnt) == k:
            res = 1
        else:
            res = 0
        
        for index, char in enumerate(s[k:]):
            cnt[char] = cnt.get(char, 0) + 1
            cnt[s[index]] -= 1
            if cnt[s[index]] == 0:
                cnt.pop(s[index])
            
            if len(cnt) == k:
                res += 1
        
        return res
''',
    call="Solution().numKLenSubstrNoRepeats('abcbdea', 3)",
    expect=4,
    views=[
        dict(type='string', var='s', label='s', h=190, cell=84,
             window=(lambda S: _win(S)[0], lambda S: _win(S)[1])),
        dict(type='map', var='cnt', label='cnt（窗口内字符次数）', h=250, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=['index', 'char', ('res', 'res', 'green'), 'k'],
    captions={
        'n = len': '字符串长度 `n = {n}`',
        'if n < k': lambda S, B, r: f'`n = {S.n}` {"<" if S.n < S.k else "≥"} `k = {S.k}` → ' + ('不够 k 个字符，答案必为 0' if S.n < S.k else '够长，正常开窗口'),
        'cnt = {}': '`cnt` 记录窗口内每个字符出现的次数',
        'for char in s[:k]': lambda S, B, r: f'前 {S.k} 个字符都计入了，第一个窗口建好' if sum(S.cnt.values()) == S.k else f'第一个窗口：把 `{S.char}` 计入 `cnt`',
        'cnt[char] = cnt.get(char, 0) + 1': '`cnt[{char}]` = {cnt[char]}',
        'if len(cnt) == k': lambda S, B, r: f'`len(cnt) = {len(S.cnt)}`，`k = {S.k}` → ' + ('==相等：每个字符恰好一次，合法=='  if len(S.cnt) == S.k else '不等：窗口里有重复，不合法'),
        'res = 1': '第一个窗口合法：`res = 1`',
        'res = 0': '第一个窗口不合法：`res = 0`',
        'for index, char in enumerate(s[k:])': lambda S, B, r: ('所有字符都滑过了，循环结束' if B.get('index') == S.get('index') else f'窗口右移：新字符 `{S.char}` 进来，离开的是 `s[{S.index}] = {S.s[S.index]}`'),
        'cnt[s[index]] -= 1': '左端 `{s[index]}` 离开：`cnt[{s[index]}]` → =={cnt[s[index]]}==',
        'if cnt[s[index]] == 0': lambda S, B, r: f"`cnt[{S.s[S.index]}] = {S.cnt[S.s[S.index]]}` " + ('→ ==次数为 0，要删掉这个 key==，否则 len 会算多' if S.cnt[S.s[S.index]] == 0 else '→ 还在窗口里，保留'),
        'cnt.pop': '删除 `{s[index]}`',
        'res += 1': '这个窗口合法：`res` → {res}',
        'return res': '一共 `{res}` 个合法窗口',
    },
    cards=dict(
        one_liner='哈希表里的 key 数恰好等于 k，说明窗口内全不重复',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['给字符串 `s` 和整数 `k`，求长度为 `k`、且 ==没有重复字符== 的子串个数',
                 '本视频：`s = "abcbdea"`，`k = 3` → `4`',
                 '（`abc`、`cbd`、`bde`、`dea`；`bcb` 有重复）'],
        quote='若此时哈希表中的key恰好是k个，说明当前窗口中有k个字符，且每个字符恰好出现了一次，因此需要初始化答案为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['窗口只有 `k` 个字符，==key 数 = k 当且仅当没有重复==',
              '右移时：新字符计数 +1，旧字符计数 −1',
              '旧字符减到 0 必须 `pop`，否则 key 数会虚高'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '`n < k` 要先返回 0',
                 '计数为 0 的 key ==一定要删掉==，再用 `len(cnt)` 判断',
                 '同类题：3 无重复字符的最长子串；567 字符串的排列'],
    ),
)
