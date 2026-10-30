CONFIG = dict(
    num=2207, title='字符串中最多数目的子序列', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='贪心 · 一次遍历计数',
    tags=[],
    code='''
class Solution:
    def maximumSubsequenceCount(self, text: str, pattern: str) -> int:
        x, y = pattern
        ans = cnt_x = cnt_y = 0
        for c in text:
            if c == y:
                ans += cnt_x
                cnt_y += 1
            if c == x:
                cnt_x += 1
        return ans + max(cnt_x, cnt_y)
''',
    call='Solution().maximumSubsequenceCount("abdcdbc", "ac")',
    expect=4,
    views=[
        dict(type='string', var='text', h=150, pointers={},
             color=lambda S, i, v: ('green' if v == S['x'] else 'pink' if v == S['y'] else None) if 'x' in S else None),
        dict(type='text', h=70, fn=lambda S: (f"x = `{S['x']}`（绿），y = `{S['y']}`（粉）：遇到 y，就能和左边每个 x 配一对" if 'x' in S else '')),
    ],
    watch=['x', 'y', 'c', ('cnt_x', 'cnt_x', 'green'), ('cnt_y', 'cnt_y', 'pink'), ('ans', 'ans', 'yellow')],
    captions={
        'x, y = pattern': '`x = {x}`，`y = {y}`：子序列要 ==先 x 后 y==',
        'ans = cnt_x': '`ans` 是原串里 pattern 的个数；`cnt_x` / `cnt_y` 是 x / y 出现次数',
        'for c in text': '看当前字母 `c = {c}`',
        'if c == y': '`c == y` 吗？{"是：左边有 " + str(cnt_x) + " 个 x，各配一对" if c == y else "不是 y"}',
        'ans += cnt_x': '左边 `{cnt_x}` 个 x 都能和这个 y 组成 pattern：`ans` {B.ans} → =={ans}==',
        'cnt_y += 1': '`cnt_y` → {cnt_y}',
        'if c == x': '`c == x` 吗？{"是" if c == x else "不是 x"}',
        'cnt_x += 1': '`cnt_x` → {cnt_x}（放在 ans 之后更新，x = y 时不会自己配自己）',
        'return ans + max': '插入 x 放最左：多 `cnt_y = {cnt_y}`；插入 y 放最右：多 `cnt_x = {cnt_x}`；取大 → `{ans} + {max(cnt_x, cnt_y)}` = =={ans + max(cnt_x, cnt_y)}==',
    },
    cards=dict(
        one_liner='x 插最左、y 插最右：先数原有的，再加 max(cnt_x, cnt_y)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `text` 任意位置插入一个字符，必须是 `pattern[0]` 或 `pattern[1]`',
                 '求插入后，`pattern` 作为子序列最多出现几次',
                 '示例：`text = "abdcdbc"`，`pattern = "ac"` → `4`'],
        quote='x 插入的位置越靠左，pattern 子序列的个数越多；y 插入的位置越靠右，pattern 子序列的个数越多。那么 x 应插在 text 最左侧，y 应插在 text 最右侧。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数插入之前的：遇到 `y`，把左边 `x` 的个数 `cnt_x` 加进答案',
              '插 x 在最左：和每个 y 配对，多 `cnt_y`；插 y 在最右：多 `cnt_x`',
              '两种取最大，一次遍历搞定'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：x == y 时，要先更新 ans 再更新 cnt_x，保证 cnt_x 只含当前字母左边的 x',
                 '思考题：pattern 长度为 3 或 m 时，要改成 DP 来数子序列'],
    ),
)
