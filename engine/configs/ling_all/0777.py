def _info(S):
    if 'i' not in S:
        return '把「XL→LX」看成 L 左移，「RX→XR」看成 R 右移'
    c = S.get('c')
    if c is None or c == 'X' or 'j' not in S:
        return ''
    return f"当前片段 `{c}`：start 里在 {S['i']}，target 里的落点在 {S['j']}"


CONFIG = dict(
    num=777, title='在 LR 字符串中交换相邻字符', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 对齐非 X 字符',
    tags=['灵神题单', '难度分 2337'],
    code='''
class Solution:
    def canTransform(self, start: str, target: str) -> bool:
        if start.replace('X', '') != target.replace('X', ''):
            return False
        j = 0
        for i, c in enumerate(start):
            if c == 'X':
                continue
            while target[j] == 'X':
                j += 1
            if i != j and (c == 'L') != (i > j):
                return False
            j += 1
        return True
''',
    call='Solution().canTransform("RXXLRXRXL", "XRLXXRRLX")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='string', var='start', pointers={'i': 'blue'}, label='start', h=150,
             color=lambda S, i, v: ('blue' if 'i' in S and i == S['i'] and v != 'X' else None)),
        dict(type='string', var='target', pointers={'j': 'pink'}, label='target', h=150,
             color=lambda S, i, v: ('pink' if 'j' in S and i == S['j'] and v != 'X' else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'c'],
    captions={
        "start.replace": lambda S, B, r: ("去掉 `X` 后：start 剩 `" + S['start'].replace('X', '') + "`，target 剩 `"
                                          + S['target'].replace('X', '') + "`" + (" → ==相同==，L、R 无法互相穿过，顺序不会变" if S['start'].replace('X', '') == S['target'].replace('X', '') else " → 不同 → ==False==")),
        'j = 0': '`j` 指向 target 里「下一个还没配对的片段」',
        "if c == 'X'": lambda S, B, r: (f"start[{S.i}] 是 `X` → 空位，不用管" if S.c == 'X' else f"start[{S.i}] 是片段 `{S.c}`，去 target 里找它的落点"),
        "target[j] == 'X'": lambda S, B, r: (f"target[{S.j}] 是 `X` → 不是片段，`j` 继续右移" if S.target[S.j] == 'X' else f"target[{S.j}] = `{S.target[S.j]}` ==就是 start[{S.i}] 的落点=="),
        'j += 1': lambda S, B, r: (f"`j` → {S.j}" if S.get('_line') == 10 else f"`j` → {S.j}：这个片段配对完"),
        'if i != j': lambda S, B, r: (f"`i = j = {S.i}`：不用动" if S.i == S.j else
                                       (f"`{S.c}` 从 {S.i} 到 {S.j}：" + ("`L` 往左（j<i）" if S.c == 'L' else "`R` 往右（j>i）") + "，==合法==" if (S.c == 'L') == (S.i > S.j) else
                                        f"`{S.c}` 从 {S.i} 到 {S.j}：" + ("`L` 不能往右 → ==False==" if S.c == 'L' else "`R` 不能往左 → ==False=="))),
        'return True': '每个片段的方向都对 → ==True==',
    },
    skip=['continue'],
    cards=dict(
        one_liner='XL→LX 就是 L 左移、RX→XR 就是 R 右移，片段不能互穿',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一次操作：把 `XL` 换成 `LX`，或把 `RX` 换成 `XR`',
                 '问 `start` 能否经若干次操作变成 `result`',
                 '示例：`RXXLRXRXL` → `XRLXXRRLX` 返回 `true`'],
        quote='替换操作可以转换成，把 `L` 往左移动（需要左边是 `X`），把 `R` 往右移动（需要右边是 `X`）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`L`、`R` 不能互相穿过 → 去掉 `X` 后剩余字符必须相同',
              '`i` 扫 start 的片段，`j` 找 target 里对应的落点',
              '`L` 在 i<j 要右移、`R` 在 i>j 要左移 → 做不到'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先 `replace` 比较，保证 `target[j]` 不越界',
                 '方向判断 `(c == "L") != (i > j)`：L 需 i≥j，R 需 i≤j',
                 '和第 2337 题完全一样，只是 `_` 换成 `X`'],
    ),
)
