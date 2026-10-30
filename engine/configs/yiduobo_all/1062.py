CONFIG = dict(
    num=1062, title='最长重复子串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='二分长度 + 滚动哈希',
    tags=['字符串哈希', '难度分 1044'],
    code='''
class Solution(object):
    def longestRepeatingSubstring(self, s):

        n = len(s)
        left = 0
        right = n - 1

        mod = 10 ** 9 + 7

        def check(length):
            p = 1
            now = 0

            for char in s[:length]:
                now = (now * 26 + ord(char) - 97) % mod
                p = p * 26 % mod
            
            vis = set([now])
            for index, char in enumerate(s[length:]):
                now = (now * 26 - (ord(s[index]) - 97) * p % mod + mod + ord(char) - 97) % mod
                if now in vis:
                    return True
                vis.add(now)
            
            return False

        while left < right:
            mid = (left + right + 1) // 2
            if check(mid):
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().longestRepeatingSubstring("aabcaab")',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"二分长度：`left={S['left']}`，`right={S['right']}`" + (f"，试 `mid={S['mid']}`" if 'mid' in S else '')) if 'left' in S and 'right' in S else ''),
        dict(type='string', var='s', h=200,
             window=('index+1', 'index+length')),
        dict(type='set', var='vis', h=260),
    ],
    watch=['left', 'right', 'mid', 'length', 'now', ('p', 'p'), ('res', 'left', 'green')],
    captions={
        'right = n - 1': '长度最多 `n-1`，所以答案在 `[0, {right}]` 里二分',
        'mid = ': '`mid = (left + right + 1) // 2 = {mid}`：==向上取整==，否则 `left = mid` 时会死循环',
        'for char in s[:length]': '先算第一个长度为 `{length}` 的窗口的哈希，同时累出 `26^length`',
        'now = (now * 26 + ord(char) - 97) % mod': '把 `{char}` 按 26 进制接到末尾：`now = {now}`',
        'p = p * 26': '`p = 26^k`，之后滑窗要用它去掉最左字符',
        'vis = set': '哈希表 `vis` 记录出现过的子串哈希：`{vis}`',
        'now = (now * 26 - ': '滑窗：乘 26、减去移出的 `{s[index]}`×p、加上新字符 `{char}` → `now = {now}`',
        'if now in vis': lambda S, B, r: ('`now = %d` 已在 vis 里 → 有两个相同的子串' % S.now) if S.now in S.vis else '`now = %d` 没见过 → 继续滑' % S.now,
        'vis.add': '记下这个哈希：`vis` 现有 {len(vis)} 个',
        'return True': '长度 `{length}` 存在重复子串 → 可行',
        'return False': '长度 `{length}` 没有重复子串 → 不可行',
        'if check(mid)': '调用 `check({mid})`：有没有两个长为 `{mid}` 的相同子串？',
        'left = mid': '可行 → 答案至少是 `{mid}`，`left = {left}`',
        'right = mid - 1': '不可行 → 更长也不行，`right = {right}`',
        'return left': '二分收敛，最长重复子串长度 `{left}`',
    },
    cards=dict(
        one_liner='长度满足单调性：能重复长 b，就能重复长 a<b，二分长度',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一个字符串 `s`，求最长重复子串的长度（可以重叠，没有则 `0`）',
                 '示例：`"aabcaab"` → `3`（`"aab"` 出现两次）'],
        quote='若字符串中存在长度为b的重复子串，那么也必然存在长度为a的重复子串。……这也就意味着最长重复子串的长度符合二分的性质',
        quote_src='—— yiduobo 题解原文',
        idea=['正统做法是后缀数组 + height，但数据规模不大，作者换了更简单的写法',
              '二分长度，每次用 rk（滚动哈希）一趟扫出所有定长子串的哈希',
              '哈希进 `set`，遇到见过的哈希就说明有重复'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`mid` 要向上取整，配合 `left = mid`',
                 '只用单个模数，哈希冲突时可能误判，本题数据下通过',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`'],
    ),
)
