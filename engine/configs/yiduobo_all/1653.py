S0 = 'abababab'


def _pos(S):
    """当前处理到 S0 的哪个下标（用 (char, f, g) 在小例子上唯一反推）"""
    if 'f' not in S:
        return -1
    if 'char' not in S:
        return 0
    f, g = (0, 1) if S0[0] == 'a' else (1, 0)
    for p, ch in enumerate(S0[1:], 1):
        states = {(f, g)}
        if ch == 'a':
            g += 1
            states.add((f, g))
        else:
            g = min(f, g)
            states.add((f, g))
            f += 1
            states.add((f, g))
        if ch == S['char'] and (S['f'], S['g']) in states:
            return p
    return len(S0) - 1


def _fml(S):
    if 'f' not in S:
        return '`f`：整段变成 ==全是 a== 的最少删除；`g`：整段变成 ==以 b 结尾== 的最少删除'
    if 'char' not in S:
        return f"第 0 个字符 `{S0[0]}`：`f = {S['f']}`，`g = {S['g']}`"
    ch = S['char']
    if ch == 'a':
        return '新字符是 `a`：`f` 不变（保留这个 a），`g` 要删掉它 → `g + 1`'
    return '新字符是 `b`：`g` 取 `min(f, g)`（b 接在 a 串或 b 串后面都行），`f` 要删掉它 → `f + 1`'


CONFIG = dict(
    num=1653, title='使字符串平衡的最少删除次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='两个状态的滚动 DP（以 a 结尾 / 不以 a 结尾）',
    tags=['灵神题单·动态规划', '难度分 1794'],
    code='''
class Solution(object):
    def minimumDeletions(self, s):

        if s[0] == 'a':
            f = 0
            g = 1
        else:
            f = 1
            g = 0
        
        for char in s[1:]:
            if char == 'a':
                g += 1
            else:
                g = min(f, g)
                f += 1
        
        return min(f, g)
''',
    call=f'Solution().minimumDeletions({S0!r})',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（蓝 = 正在处理，灰 = 已处理）', h=210, cell=80,
             color=lambda S, i, v: 'blue' if i == _pos(S) else None,
             dim=lambda S, i, v: 0 <= i < _pos(S)),
        dict(type='text', fn=_fml, size=26, h=100),
    ],
    watch=[('char', 'char', 'blue'), ('f', 'f', 'pink'), ('g', 'g', 'orange')],
    captions={
        "if s[0] == 'a'": '先处理第 0 个字符：`f` 和 `g` 的边界值',
        'f = 0': '首字符是 `a`：保留它即全 a 串，`f = 0`',
        'g = 1': '想让它“不以 a 结尾”只能删掉它，`g = 1`',
        'f = 1': '首字符是 `b`：想变成全 a 串要删掉它，`f = 1`',
        'g = 0': '以 `b` 结尾的串里它可以保留，`g = 0`',
        'for char in s': lambda S, B, r: ('字符串扫完了，循环结束' if _pos(S) == len(S0) - 1 and (S.f, S.g) == (4, 3) else f'看下一个字符 `{S.char}`'),
        "if char == 'a'": '`char = {char}`：{"是 a，只影响 g" if char == "a" else "是 b，f 和 g 都要更新"}',
        'g += 1': '这个 `a` 不能出现在 b 之后：`g` 要删掉它，`g` → =={g}==；`f` 保持 `{f}`',
        'g = min(f, g)': '这个 `b` 可以接在全 a 串（`f = {B.f}`）或 b 结尾串（`g = {B.g}`）后面 → `g` = =={g}==',
        'f += 1': '全 a 串里不能有 `b`，必须删掉它：`f` → =={f}==（注意用的是旧的 `f` 去更新 `g`，所以 `g` 在前）',
        'return min': '两种形态取小：`min({f}, {g})` = =={ret}==',
    },
    cards=dict(
        one_liner='f 记“全是 a”要删几个，g 记“以 b 结尾”要删几个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a` 和 `b`，可以删任意字符',
                 '平衡：不存在 `i < j` 使得 `s[i] = b` 且 `s[j] = a`',
                 '示例：`"aababbab"` → `2`；本视频用 `"abababab"` → `3`'],
        quote='上面这种方法需要执行两趟扫描，个人感觉不是太优美。我在这里采用的是动态规划的做法，虽然时间复杂度并没有区别，但是只需要一趟扫描就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f`：前缀变成==以 a 结尾==（全是 a）的平衡串，最少删几个',
              '`g`：前缀变成==不以 a 结尾==的平衡串，最少删几个',
              '遇 `a`：`g` 要删它，`g + 1`；遇 `b`：`g = min(f, g)`，`f` 要删它，`f + 1`',
              '最后答案是 `min(f, g)`'],
        summary=['时间 `O(n)`，空间 `O(1)`（原文用数组推导，再滚动成两个变量）',
                 '易错：遇 `b` 时要==先用旧 `f` 更新 `g`，再给 `f` 加一==',
                 '`g` 里 b 可以接在 a 串后面，形成 `aaa…ab`',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串',
                 '对比灵神：灵神只记一个 `f` 加 `cnt_b`，yiduobo 记两个形态'],
    ),
)
