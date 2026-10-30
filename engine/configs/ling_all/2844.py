CONFIG = dict(
    num=2844, title='生成特殊数字的最少操作', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从右往左一次遍历 · 找 00/25/50/75',
    tags=['贪心算法', '思维题', '难度分 1588'],
    code='''
class Solution:
    def minimumOperations(self, num: str) -> int:
        n = len(num)
        found0 = found5 = False
        for i in range(n - 1, -1, -1):
            c = num[i]
            if found0 and c in "05" or found5 and c in "27":
                return n - i - 2
            if c == '0':
                found0 = True
            elif c == '5':
                found5 = True
        return n - found0
''',
    call='Solution().minimumOperations("2908305")',
    expect=3,
    views=[
        dict(type='text', size=32, h=70, fn=lambda S: '能被 25 整除 ⇔ 末尾是 `00` `25` `50` `75`（或整个数是 0）'),
        dict(type='string', var='num', h=260, label='num（从右往左找末尾两位）',
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('yellow' if (S.get('found0') and v == '0' and i > S.get('i', 99)) or (S.get('found5') and v == '5' and i > S.get('i', 99)) else None) if 'i' in S else None,
             dim=lambda S, i, v: 'i' in S and i > S['i'] and not ((S.get('found0') and v == '0') or (S.get('found5') and v == '5'))),
        dict(type='text', size=34, h=80, fn=lambda S: f"已找到：`0` ==`{S['found0']}`==　`5` ==`{S['found5']}`==" if 'found5' in S else ''),
    ],
    watch=['n', 'i', 'c', ('found0', 'found0', 'yellow'), ('found5', 'found5', 'yellow')],
    captions={
        'c = num[i]': '从右往左看第 `{i}` 位：`c = {c!r}`',
        'if found0 and c in': lambda S, B, ret: (f"`found0` = {S.found0}，`found5` = {S.found5}，`c = '{S.c}'`："
            + ('右边已有 0，现在又是 0 或 5 → ==凑成 00 或 50 结尾==' if S.found0 and S.c in '05' else
               '右边已有 5，现在又是 2 或 7 → ==凑成 25 或 75 结尾==' if S.found5 and S.c in '27' else
               '还凑不成 00/50/25/75 的结尾，继续往左')),
        'return n - i - 2': '这两位保留，它们之间和右边多余的数字全删：`{n} - {i} - 2` = =={ret}== 次',
        "if c == '0'": lambda S, B, ret: "`c` 是 0：标记==找到了 0==，它可以当 00、50 的最后一位" if S.c == '0' else "`c` 不是 0，再看是不是 5",
        "elif c == '5'": lambda S, B, ret: "`c` 是 5：标记==找到了 5==，它可以当 25、75 的最后一位" if S.c == '5' else "`c` 也不是 5，这一位对结尾没用，往左看下一位",
        'found0 = True': '`found0 = True`：往左再遇到 0 或 5 就能成',
        'found5 = True': '`found5 = True`：往左再遇到 2 或 7 就能成',
        'return n - found0': '没凑成任何结尾：全删得 0，需 `n` 次；有 0 就留一个 0，需 `n - 1` 次',
    },
    cards=dict(
        one_liner='25 的倍数只可能以 00、25、50、75 结尾，从右往左一次找到',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除 `num` 中任意位的数字，使它能被 `25` 整除（删光变成 `0`），求最少删除次数',
                 '示例：`"2908305"` → `3`，删成 `"2900"`',
                 '`num` 不含前导零'],
        quote='在从右往左遍历的过程中：在之前找到 0 的情况下，如果当前数字 num[i] 是 0 或者 5，则立刻返回 n−i−2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能被 `25` 整除的数，末尾只能是 `00`、`25`、`50`、`75`，或者整个数是 `0`',
              '从右往左找：先找到的右半部分（0 或 5）用标记记住',
              '再找到左半部分（0/5 配 0，2/7 配 5）就停，保留这两位，删掉后面多余的 `n-i-2` 位'],
        summary=['时间 `O(n)`，空间 `O(1)`，只扫一遍',
                 '方法一是每个结尾单独枚举，用 `rfind` 找位置，本方法把它们合并成一次遍历',
                 '全删得到 `0` 也算合法：有 `0` 时只需 `n-1` 次，否则 `n` 次',
                 '不会只得到 `00`：`num` 无前导零，任何 0 的左边都有非 0 数字'],
    ),
)
