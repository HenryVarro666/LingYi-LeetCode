def _info(S):
    if 'j' not in S or 'i' not in S:
        return '先把 `_` 去掉，比较剩下的 `L` `R` 序列是否一致'
    i, j, c = S['i'], S['j'], S.get('c')
    if c is None or c == '_':
        return ''
    t = S['target']
    if j < len(t) and t[j] != '_':
        return f"start[{i}] = `{c}`，对应 target[{j}]：`{c}` 要从 {i} 走到 {j}"
    return f"start[{i}] = `{c}`，正在 target 里找它的落点"


CONFIG = dict(
    num=2337, title='移动片段得到字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 对齐非空字符',
    tags=['灵神题单', '难度分 1693'],
    code='''
class Solution:
    def canChange(self, start: str, target: str) -> bool:
        if start.replace('_', '') != target.replace('_', ''):
            return False
        j = 0
        for i, c in enumerate(start):
            if c == '_':
                continue
            while target[j] == '_': 
                j += 1
            if i != j and (c == 'L') == (i < j):
                return False
            j += 1
        return True
''',
    call='Solution().canChange("_L__R__R_", "L______RR")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='string', var='start', pointers={'i': 'blue'}, label='start', h=150,
             color=lambda S, i, v: ('blue' if 'i' in S and i == S['i'] and v != '_' else None)),
        dict(type='string', var='target', pointers={'j': 'pink'}, label='target', h=150,
             color=lambda S, i, v: ('pink' if 'j' in S and i == S['j'] and v != '_' else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'c'],
    captions={
        "start.replace": lambda S, B, r: ("去掉 `_` 后：start 剩 `" + S['start'].replace('_', '') + "`，target 剩 `"
                                          + S['target'].replace('_', '') + "` → ==相同==，L 和 R 不会互相穿过，顺序没被破坏"),
        'j = 0': '`j` 指向 target 里「下一个还没配对的片段」，从 0 开始',
        "if c == '_'": lambda S, B, r: (f"start[{S.i}] 是 `_` → 空位不用管，跳过" if S.c == '_' else f"start[{S.i}] 是片段 `{S.c}`，要找它在 target 里的位置"),
        "target[j] == '_'": lambda S, B, r: (f"target[{S.j}] 是 `_` → 不是片段，`j` 继续右移" if S.target[S.j] == '_' else f"target[{S.j}] = `{S.target[S.j]}` 是片段，==这就是 start[{S.i}] 对应的落点=="),
        'j += 1': lambda S, B, r: (f"`j` → {S.j}" if S.get('_line') == 10 else f"`j` → {S.j}：这个片段配对完，看下一个"),
        'if i != j': lambda S, B, r: (f"`i = {S.i}`，`j = {S.j}`：位置相同，不用移动" if S.i == S.j else
                                       (f"`{S.c}` 要从 {S.i} 移到 {S.j}：" + ("`L` 只能向左（j<i）" if S.c == 'L' else "`R` 只能向右（j>i）") + "，方向 ==合法==" if (S.c == 'L') != (S.i < S.j) else
                                        f"`{S.c}` 要从 {S.i} 移到 {S.j}：" + ("`L` 不能向右 → ==返回 False==" if S.c == 'L' else "`R` 不能向左 → ==返回 False=="))),
        'return True': '所有片段都能走到目标位置 → ==True==',
    },
    skip=['continue'],
    cards=dict(
        one_liner='片段不能互相穿过：对齐每个 L/R，再看方向对不对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`start` 里 `L` 只能向左挪、`R` 只能向右挪，`_` 是空位',
                 '问能否移动若干次变成 `target`',
                 '示例：`_L__R__R_` → `L______RR` 返回 `true`'],
        quote='无论怎么移动，由于 `L` 和 `R` 无法互相穿过对方，那么去掉 `_` 后的剩余字符应该是相同的，否则返回 `false`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['去掉 `_` 后两串必须相同，所以第 k 个片段对应第 k 个片段',
              '`i` 扫 start 的片段，`j` 跟着找 target 里对应的落点',
              '`L` 在 i<j 就要右移、`R` 在 i>j 就要左移 → 不可能'],
        summary=['时间 `O(n)`，空间 `O(n)`（`replace` 生成新串）',
                 '第一步 `replace` 判断必不可少，否则 `while target[j]` 可能越界',
                 '方向判断：`(c == "L") == (i < j)` 即方向反了',
                 '同类题：第 777 题（`X` 换成 `_`，一模一样）'],
    ),
)
