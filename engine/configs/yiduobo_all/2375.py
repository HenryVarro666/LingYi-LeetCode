CONFIG = dict(
    num=2375, title='根据模式串构造最小数字', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先排 1..n+1 · 连续 D 区间翻转',
    tags=['灵神题单·贪心与思维', '难度分 1642'],
    code='''
class Solution(object):
    def smallestNumber(self, pattern):

        n = len(pattern)
        res = list(range(1, n + 2))
        p = 0
        while p < n:
            while p < n and pattern[p] == 'I':
                p += 1
            
            if p == n:
                break

            left = p
            while p < n and pattern[p] == 'D':
                p += 1

            right = p
            while left < right:
                res[left], res[right] = res[right], res[left]
                left += 1
                right -= 1
        
        return ''.join([str(x) for x in res])
''',
    call='Solution().smallestNumber("IDDIDD")',
    expect='1432765',
    views=[
        dict(type='string', var='pattern', label='pattern', cell=84, h=190,
             pointers={'p': 'blue'}),
        dict(type='array', var='res', label='res（初始 1..n+1，翻转 D 段）', cell=84, h=230,
             pointers={'left': 'pink', 'right': 'yellow'},
             color=lambda S, k, v: ('pink' if k == S.get('left') else 'yellow' if k == S.get('right') else None)
             if S.get('_line', 0) >= 19 else None),
        dict(type='text', size=26, fn=lambda S: (
            f"D 段对应 `res[{S['left']}..{S['right']}]`，整段翻转" if S.get('_line', 0) >= 16 and 'left' in S and 'right' in S else '')),
    ],
    watch=[('p', 'p', 'blue'), ('left', 'left', 'pink'), ('right', 'right', 'yellow')],
    skip=['n = len(pattern)'],
    captions={
        'res = list': '先按 `1 ~ n+1` 递增排好：全是 I 时它就是最小答案，`res = {res}`',
        'p = 0': '`p` 扫描 pattern',
        'while p < n:': lambda S, B, r: (f'`p = {S.p} < n = {S.n}`，继续找下一段连续 D' if S.p < S.n
                                         else f'`p = {S.p}` == n，扫完了'),
        "pattern[p] == 'I'": lambda S, B, r: (
            f"`pattern[{S.p}] = 'I'` → 递增已经满足，不用动，`p` 右移" if S.p < S.n and S.pattern[S.p] == 'I'
            else ('`p` 走到末尾' if S.p >= S.n else f"`pattern[{S.p}] = 'D'` → 遇到 D，停下")),
        'p += 1': lambda S, B, r: (
            f"`p` → {S.p}" if S.get('_line') else f'`p` → {S.p}'),
        'if p == n': lambda S, B, r: ('`p == n`：后面没有 D 了，结束' if S.p == S.n
                                      else f'`p = {S.p} != n`：这里有一段 D 要处理'),
        'left = p': '`left = {left}`：连续 D 从这里开始，这些位置要「预留」更大的数',
        "pattern[p] == 'D'": lambda S, B, r: (
            f"`pattern[{S.p}] = 'D'` → 连续 D 又多一个，`p` 右移" if S.p < S.n and S.pattern[S.p] == 'D'
            else '连续 D 到头了'),
        'right = p': '`right = {right}`：D 段覆盖 `res[{left}..{right}]`（D 的个数 + 1 个数）',
        'while left < right': lambda S, B, r: (
            f'`left = {S.left} < right = {S.right}`：两端还没碰头，继续交换' if S.left < S.right
            else '两端碰头，这一段翻转完成'),
        'res[left], res[right]': '交换 `res[{left}]` 与 `res[{right}]` → `{res}`：段内变成递减，且仍是最小',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'return': lambda S, B, r: f"拼成字符串 `{r}`",
    },
    cards=dict(
        one_liner='先排成 1,2,…,n+1，再把每段连续 D 对应的区间翻转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`pattern` 的 `I` 表示上升，`D` 表示下降，要构造 `n+1` 位数字串',
                 '数字取 `1~9`，每个至多用一次，求==字典序最小==',
                 '示例：`"DDD"` → `"4321"`；本视频：`"IDDIDD"` → `"1432765"`'],
        quote='在D出现的时候预留出足够的后续数字，这个预留的大小取决于这一组连续D的数目，而在I出现的时候，则只需将剩余的最小数字填充进去就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['为使字典序小，小数放前面；但连续 D 需要后面有足够小数，所以 D 段要「预留」',
              '结果等价于：先排好 `1..n+1`，再把==每段连续 D 影响到的区间翻转==',
              '双指针 `left/right` 交换，翻转后段内递减，段外依旧递增'],
        result='`1 2 3 4 5 6 7` 翻转 `[1..3]` 与 `[4..6]` → `"1432765"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；也可暴力搜索（最多 9 位）',
                 '原文为 Python 2 写法，`range(1, n + 2)` 在 Python 3 中不是列表，已改为 `list(range(1, n + 2))`',
                 '翻转的区间是 `res[left..right]`，包含 D 段后面那个数，长度为 D 个数 + 1',
                 '对比灵神：灵神是直接给每段分配剩余最小的几个数（倒着填），yiduobo 是先排好再翻转'],
    ),
)
