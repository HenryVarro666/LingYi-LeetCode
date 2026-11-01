def _head(S):
    if 'i' not in S:
        return ''
    s, i = S['s'], S['i']
    if 'v' not in S:
        return f'试第一段 `s[:{i}] = "{s[:i]}"`'
    return f'第一段 `"{s[:i]}"` = =={int(s[:i])}==，后面要依次是 ==递减 1== 的数；当前要找 `v = {S["v"]}`'


def _while(S, B, ret):
    t = S.t
    if t == '':
        return '`t` 空了：整串都被拆完，每一段都对上了'
    return f'`t = "{t}"` 还没拆完，继续找下一段'


def _strip(S, B, ret):
    if len(S.t) > 1 and S.t[0] == '0':
        return f'`t` 开头是 `0` 且长度 > 1 → 去掉一个前导零：`t = "{S.t}"`（至少留一位）'
    return f'`t = "{S.t}"` 没有可去的前导零'


def _prefix(S, B, ret):
    tmp, t = S.tmp, S.t
    if t.startswith(tmp):
        return f'`t = "{t}"` 以 `"{tmp}"` 开头 → 这一段 ==对上了=='
    return f'`t = "{t}"` 不以 `"{tmp}"` 开头 → ==这个第一段不行==，换下一个 `i`'


CONFIG = dict(
    num=1849, title='将字符串拆分为递减的连续值', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='枚举第一段 + 逐段匹配（Go 原文转写）',
    tags=['链表树与回溯', '难度分 1747'],
    code='''
class Solution:
    def splitString(self, s: str) -> bool:
        for i in range(1, len(s)):  # next
            v = int(s[:i])  # 如果 s 很长，会返回最大 int
            v -= 1
            t = s[i:]
            while t != "":
                # 移除前导零，但不能全部移除，至少保留一位数字
                while len(t) > 1 and t[0] == '0':
                    t = t[1:]
                # 判断 v 是否符合
                tmp = str(v)
                if not t.startswith(tmp):
                    break  # continue next
                t = t[len(tmp):]
                v -= 1
            else:
                return True
        return False
''',
    call='Solution().splitString("050043")',
    expect=True,
    views=[
        dict(type='text', fn=_head, size=28),
        dict(type='string', var='s', label='s（蓝 = 第一段，绿 = 已拆出的后续段）', cell=84, pointers={'i': 'pink'},
             color=lambda S, k, v: ('blue' if k < S['i'] else ('green' if 't' in S and k < len(S['s']) - len(S['t']) else None)) if 'i' in S else None),
        dict(type='string', var='t', label='t（还没拆的剩余部分）', cell=84, h=150),
    ],
    watch=[('i', 'i', 'pink'), ('v', 'v', 'blue'), ('t', 't', 'green'), 'tmp'],
    skip=['t = s[i:]'],
    captions={
        'for i in range(1, len(s))': '枚举第一段 `s[:{i}]`：至少 1 位，且后面要留位置给其余段',
        'v = int(s[:i])': '第一段数值 `{v}`',
        'v -= 1': '下一段必须是 `{v}`',
        'while t != ""': _while,
        'while len(t) > 1': _strip,
        't = t[1:]': '去掉前导零 → `t = "{t}"`',
        'tmp = str(v)': '把要找的 `v = {v}` 写成字符串 `"{tmp}"`，去 `t` 头上比对',
        'if not t.startswith': _prefix,
        'break': '这个第一段失败，==跳出内层==，试更长的第一段',
        't = t[len(tmp):]': '吃掉这一段 → `t = "{t}"`',
        'else:': '`while` 正常结束（没被 break）→ 整串拆完',
        'return True': '`t` 被拆光，每段依次递减 1 → 返回 `True`',
        'return False': '所有第一段都试过了 → `False`',
    },
    max_steps=80,
    cards=dict(
        one_liner='第一段定了，后面每段的值就全定了：逐段对上去',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把数字串 `s` 拆成 ==两段或更多段==，数值依次递减且相邻差为 `1`',
                 '每段允许有前导零，如 `"05"` 的数值是 `5`',
                 '示例：`"050043"` → `["05","004","3"]` = `[5,4,3]` → `true`'],
        quote='移除前导零，但不能全部移除，至少保留一位数字',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['枚举第一段 `s[:i]`，它的值 `v` 一定后，后面每段的值依次是 `v-1, v-2, ...`',
              '每一轮：先去掉 `t` 的前导零，再看 `t` 是否以 `str(v)` 开头',
              '不是就换下一个 `i`；`t` 被吃光就成功'],
        result='第一段 `"05"` = 5，后面 `4`、`3` 都对上 → True ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`continue next` 用 `break` + `while...else`）',
                 '第一段最多枚举到 `len(s)-1`，保证至少两段',
                 '去前导零要保留一位：`"0"` 本身也是数值 0',
                 '`v` 减到负数时 `str(v)` 以 `-` 开头，必然匹配失败'],
    ),
)
