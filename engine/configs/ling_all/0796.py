CONFIG = dict(
    num=796, title='旋转字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='s+s 中 KMP 匹配 goal',
    tags=['灵神题单', '字符串'],
    code='''
# 在文本串 text 中查找模式串 pattern，返回所有成功匹配的位置（pattern[0] 在 text 中的下标）
def kmp_search(text: str, pattern: str) -> List[int]:
    m = len(pattern)
    pi = [0] * m
    cnt = 0
    for i in range(1, m):
        b = pattern[i]
        while cnt and pattern[cnt] != b:
            cnt = pi[cnt - 1]
        if pattern[cnt] == b:
            cnt += 1
        pi[i] = cnt

    pos = []
    cnt = 0
    for i, b in enumerate(text):
        while cnt and pattern[cnt] != b:
            cnt = pi[cnt - 1]
        if pattern[cnt] == b:
            cnt += 1
        if cnt == len(pattern):
            pos.append(i - m + 1)
            cnt = pi[cnt - 1]
    return pos

class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        return len(s) == len(goal) and len(kmp_search(s + s, goal)) > 0
''',
    call='Solution().rotateString("aabab", "ababa")',
    expect=True,
    views=[
        dict(type='text', size=26, h=70, fn=lambda S: (
            f"文本串 `s+s`、模式串 `goal`；`cnt` = 当前已匹配的前缀长度" if 'text' in S else '')),
        dict(type='string', var='text', label='text = s + s', cell=80, h=190,
             pointers={'i if pos is not None else None': 'pink'}, pointer_labels={'i if pos is not None else None': 'i'},
             color=lambda S, k, v: 'green' if S.get('pos') is not None and S.get('cnt', 0) and k <= S.get('i', -1) and k > S.get('i', -1) - S['cnt'] else None),
        dict(type='string', var='pattern', label='pattern = goal', cell=80, h=230,
             pointers={'cnt': 'blue', 'i if _line < 14 else None': 'pink'}, pointer_labels={'i if _line < 14 else None': 'i'}),
        dict(type='array', var='pi', label='pi[i]：pattern[:i+1] 的最长相等前后缀', cell=80, h=170),
        dict(type='text', size=26, h=70, fn=lambda S: f"已找到的匹配位置 `pos = {S['pos']}`" if S.get('pos') is not None else ''),
    ],
    watch=[('i', 'i', 'pink'), ('b', 'b'), ('cnt', 'cnt', 'blue'), ('pos', 'pos', 'green')],
    captions={
        'pi = [0] * m': '`pi[i]` 记录 pattern 前 i+1 个字符里，最长的「前缀 = 后缀」长度',
        'cnt = 0': '`cnt` 是当前已经匹配上的长度（也就是下一个要比较的下标）',
        'while cnt and pattern[cnt] != b': lambda S, B, r: (
            f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` ≠ `b = {S.b}`：失配，`cnt` 退到 `pi[{S.cnt-1}] = {S.pi[S.cnt-1]}` 再试" if S.cnt and S.pattern[S.cnt] != S.b
            else (f"`cnt = 0`，没得退了" if not S.cnt else f"`pattern[{S.cnt}] = {S.b}` 匹配，不用回退")),
        'cnt = pi[cnt - 1]': '失配后不从头来：利用 `pi` 回退，`cnt` → {cnt}',
        'if pattern[cnt] == b': lambda S, B, r: (
            f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` == `b = {S.b}` → 匹配长度 +1" if S.pattern[S.cnt] == S.b
            else f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` ≠ `b = {S.b}` → 这一位没有匹配"),
        'cnt += 1': '匹配长度加一：`cnt` → {cnt}',
        'pi[i] = cnt': '`pi[{i}] = {cnt}`：记下来，供后面失配时回退用',
        'pos = []': '模板：收集所有匹配位置；本题只要有一个就够了',
        'for i, b in enumerate(text)': '拿 `text` 的每个字符 `b = {b}` 去和 pattern 比，指针 `i` 永不回退',
        'if cnt == len(pattern)': lambda S, B, r: (
            f"`cnt = {S.cnt} == len(pattern) = {len(S.pattern)}` → ==完整匹配==" if S.cnt == len(S.pattern)
            else f"`cnt = {S.cnt} < {len(S.pattern)}`，还没匹配完"),
        'pos.append': '匹配成功：起点是 `i - m + 1 = {i - m + 1}`，`pos = {pos}`',
        'cnt = pi[cnt - 1]': '失配后不从头来：利用 `pi` 回退，`cnt` → {cnt}',
        'return pos': '共找到 `{len(pos)}` 个匹配位置 `{pos}`',
        'return len(s)': lambda S, B, r: "长度相等，且 `s+s` 里找到了 `goal` → ==返回 True==",
    },
    cards=dict(
        one_liner='旋转后的串一定是 s+s 的子串，转成字符串匹配',
        complexity='KMP 时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 每次把最左字符移到最右，问若干次旋转后能否变成 `goal`',
                 '示例：`s = "abcde"`，`goal = "cdeab"` → `true`；本视频用 `aabab` → `ababa`',
                 '`goal = "abced"` → `false`'],
        quote='旋转后的字符串是 s 的后缀加上 s 的前缀……所以无论 s 如何旋转，旋转后的字符串一定是 s+s 的子串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s+s = abcdeabcde`，任意长为 n 的子串 = 后缀 + 前缀',
              '问题等价于：`goal` 是否是 `s+s` 的子串（注意先判长度相等）',
              '用 KMP 做到 `O(n)`：先算 `pattern` 的 `pi` 数组，再扫一遍 `text`'],
        summary=['方法一：`goal in s + s`，一行搞定，时间 `O(n^2)`；方法二（本视频）：KMP，`O(n)`',
                 '易错：必须先判 `len(s) == len(goal)`，否则短串会误判',
                 '本题找到一个就能返回；灵神保留了完整 KMP 模板，可直接套到其他匹配题',
                 'Z 函数、字符串哈希同样能 `O(n)` 解决'],
    ),
)
