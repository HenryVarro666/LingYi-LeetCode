CONFIG = dict(
    num=2743, title='计算没有重复字符的子字符串数量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 枚举左边界',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def numberOfSpecialSubstrings(self, s):

        n = len(s)
        left = 0
        right = left + 1
        res = 0
        char_set = set([s[0]])
        while left < n:
            while right < n and s[right] not in char_set:
                char_set.add(s[right])
                right += 1
            
            res += right - left

            char_set.remove(s[left])
            left += 1
        
        return res
''',
    call="Solution().numberOfSpecialSubstrings('abcab')",
    expect=12,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 [left, right)，里面没有重复字符）', cell=100, h=250,
             pointers={'left': 'blue', 'right': 'pink'},
             window=(lambda S: S.get('left', 0), lambda S: min(S.get('right', 1), len(S['s'])) - 1)),
        dict(type='set', var='char_set', label='char_set（窗口内的字符）', fmt=lambda x: f"'{x}'", h=130, font=36),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"以 {S['left']} 为左边界：右边界停在 {S['right']}，合法子串 `{S['right']}-{S['left']}` = =={S['right']-S['left']}== 个"
                           if 'right' in S and S['_line'] >= 14 and S['left'] < len(S['s']) else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'right = left + 1': '`right` 指向窗口右边界的==下一个==位置（开区间），窗口 `[left, right)` 里先放着 `s[0]`',
        'char_set = set': '`char_set` 记录窗口里已有的字符，用来判重',
        'while left < n': lambda S, B, r: (f'`left = {S.left} < {S.n}`：枚举这个左边界' if S.left < S.n else '`left` 走完了所有位置 → 结束'),
        'while right < n and s[right] not in char_set': lambda S, B, r: (
            (f'`s[{S.right}] = {S.s[S.right]!r}` 不在窗口里 → 可以向右扩展' if S.s[S.right] not in S.char_set
             else f'`s[{S.right}] = {S.s[S.right]!r}` 已在窗口里 → ==出现重复==，右边界停在 `{S.right}`')
            if S.right < S.n else f'`right = {S.right}` 已到字符串末尾，停止扩展'),
        'char_set.add': '把 `{s[right]!r}` 加入窗口',
        'right += 1': '`right` → {right}',
        'res += right - left': '以 `left = {left}` 为左边界的合法子串：长度 `1..{right - left}`，共 `{right} - {left}` = =={right - left}== 个 → `res = {res}`',
        'char_set.remove': '左边界右移前，把 `s[{left}] = {s[left]!r}` 移出窗口',
        'left += 1': '`left` → {left}。`left+1` 的窗口至少延伸到上一轮的 `right`，不必回退',
        'return res': '所有左边界累加，一共 `{res}` 个',
    },
    cards=dict(
        one_liner='枚举左边界，右边界只增不减，每个左边界贡献 right-left 个',
        complexity='时间 `O(n)`，空间 `O(1)`（字符集有限）',
        problem=['数字符串 `s` 中，==每个字符都只出现一次==的子字符串个数（位置不同算不同）',
                 '示例：`abcd` → `10`；`ooo` → `3`',
                 '本视频：`abcab` → `12`'],
        quote='对于每个位置left，找出以left为左边界，且不包含任何重复字符的子串的最大右边界right，那么以left为左边界的没有重复字符的子字符串数量就有right - left个。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典变长滑窗：固定左边界，右边界尽量向右扩展到快要重复为止',
              '`left + 1` 时，`[left+1, right-1]` 一定无重复 → `right` 无需回退',
              '用 `set` 判重，移走左端字符后继续从原来的 `right` 往右扩'],
        summary=['时间 `O(n)`：`left`、`right` 各最多走 n 步，空间只与字符集大小有关',
                 '`right` 是开区间端点，个数是 `right - left`，不是 `+ 1`',
                 '`right` 初值为 `left + 1`，因为 `s[0]` 已先放进 `char_set`',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '同类题：第 3 题无重复字符的最长子串'],
    ),
)
