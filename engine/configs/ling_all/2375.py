CONFIG = dict(
    num=2375, title='根据模式串构造最小数字', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分组贪心 · 每段取最小的几个数',
    tags=['灵神题单·贪心与思维', '难度分 1642'],
    setup='from string import digits',
    code='''
class Solution:
    def smallestNumber(self, pattern: str) -> str:
        i, cur, n = 0, 1, len(pattern)
        ans = [''] * (n + 1)
        while i < n:
            if i and pattern[i] == 'I':
                i += 1
            while i < n and pattern[i] == 'I':
                ans[i] = digits[cur]
                cur += 1
                i += 1
            i0 = i
            while i < n and pattern[i] == 'D':
                i += 1
            for j in range(i, i0 - 1, -1):
                ans[j] = digits[cur]
                cur += 1
        return ''.join(ans)
''',
    call='Solution().smallestNumber("IIDDID")',
    expect='1254376',
    views=[
        dict(type='string', var='pattern', label='pattern', cell=84, h=190,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else None)),
        dict(type='array', var='ans', label='ans（逐位填入的数字）', cell=84, h=230,
             pointers={'i0': 'pink', 'j': 'yellow'},
             color=lambda S, k, v: 'green' if v != '' else None),
        dict(type='text', size=26, fn=lambda S: (
            f"下一个可用的最小数字：`cur = {S['cur']}`" if 'cur' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('i0', 'i0', 'pink'), ('j', 'j', 'yellow'), ('cur', 'cur', 'green')],
    captions={
        'i, cur, n': '`i` 扫 pattern，`cur = 1` 是下一个要用的最小数字，共要填 `n + 1 = {n + 1}` 位',
        'ans = [': '先准备 `{n + 1}` 个空位',
        'while i < n:': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有一组 I…D 没处理' if S.i < S.n
                                         else f'`i = {S.i} == n`：整个模式串处理完'),
        "if i and pattern[i] == 'I'": lambda S, B, r: (
            f"`i = {B.i}`，`pattern[{B.i}] = 'I'` → ==这个 I 的左端已在上一段 D 的末位填过==，跳过它" if B.i and S.pattern[B.i] == 'I'
            else '第一段，或当前是 D，不用跳'),
        "while i < n and pattern[i] == 'I'": lambda S, B, r: (
            f"`pattern[{S.i}] = 'I'` → 先把 I 段每个位置填最小数" if S.i < S.n and S.pattern[S.i] == 'I'
            else '这一段 I 处理完了'),
        'ans[i] = digits[cur]': '上升段位置 `{i}` 填最小的数 `{cur}`：越靠前越小，字典序才小',
        'cur += 1': '`cur` → {cur}',
        'i += 1': '`i` → {i}',
        'i0 = i': '记下 D 段起点 `i0 = {i0}`：D 段的数要整体倒着填',
        "while i < n and pattern[i] == 'D'": lambda S, B, r: (
            f"`pattern[{S.i}] = 'D'` → 下降段变长，需要多留一个数字" if S.i < S.n and S.pattern[S.i] == 'D'
            else '这一段 D 数完了'),
        'for j in range': lambda S, B, r: (
            f"从 `j = {S.j}` 往回填到 `{S.i0}`：剩余最小的 `{S.i - S.i0 + 1}` 个数倒序放，下降且最小" if S.j == S.i and B.get('j') != S.j
            else (f'`j = {S.j}` → 往前一格，数字更大才满足下降' if B.get('j') != S.j or S.j > S.i0
                  else 'j 已填到 `i0`，这一组 D 段填完')),
        'ans[j] = digits[cur]': '位置 `{j}` 填 `{cur}`：从右往左填，右边小、左边大 → ==D 满足==',
        "return ''.join": '拼起来：`{\'\'.join(ans)}`',
    },
    cards=dict(
        one_liner='按 I…D 分段，每段用剩余最小的几个数：I 递增填，D 倒着填',
        complexity='时间 `O(n)`，空间 `O(n)`，`n = len(pattern)`',
        problem=['`pattern` 由 `I`（上升）和 `D`（下降）组成，构造 `n+1` 位数字串',
                 '数字取自 `1~9`，每个至多用一次，求==字典序最小==',
                 '示例：`"IIIDIDDD"` → `"123549876"`；本视频：`"IIDDID"` → `"1254376"`'],
        quote='把 pattern 按照 III⋯IDDD⋯D 分组，每组前一段是 I，后一段是 D。遍历每一段，设当前段的长度为 x，我们应该把剩余最小的 x 个数字填到该段上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['I 的位置按顺序填最小的数，保证字典序小',
              'D 段要整体下降：这一段需要的数字个数是 `段长 + 1`，==取剩余最小的几个，倒序填==',
              '一段 I…D 用掉连续的数字，下一段接着用 `cur`'],
        result='`ans = 1 2 5 4 3 7 6` → `"1254376"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`if i and pattern[i] == \'I\'` 那一行：跳过的 I，其左端数字已在上一个 D 段里填好',
                 '`digits` 是 `string.digits`，下标从 1 取，不要从 0 开始',
                 '题解视频里还有一种更优雅的栈做法，本视频只演示分组模拟'],
    ),
)
