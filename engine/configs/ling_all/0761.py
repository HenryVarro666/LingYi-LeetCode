CONFIG = dict(
    num=761, title='特殊的二进制字符串', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='合法括号 · 拆分递归排序', tags=[],
    code='''
class Solution:
    def makeLargestSpecial(self, s: str) -> str:
        if len(s) <= 2:
            return s

        # 把 s 划分成若干段合法括号字符串，记录在 substrings 中
        substrings = []
        diff = 0  # 左括号个数 - 右括号个数
        start = 0  # 子串开始下标
        for i, ch in enumerate(s):
            if ch == '1':  # 左括号
                diff += 1
            else:  # 右括号
                diff -= 1
                if diff == 0:
                    # 子串 [start, i] 是合法括号字符串，且无法继续划分
                    # 这意味着子串 [start, i] 只能是嵌套的括号，那么去掉外层的括号，递归解决 [start+1, i-1]
                    substrings.append("1" + self.makeLargestSpecial(s[start + 1: i]) + "0")
                    start = i + 1  # 下一个子串从 i+1 开始

        substrings.sort(reverse=True)
        return ''.join(substrings)
''',
    call='Solution().makeLargestSpecial("11011000")',
    expect='11100100',
    views=[
        dict(type='string', var='s', pointers={'start': 'blue', 'i': 'pink'}, h=215, label='s（1 = 左括号，0 = 右括号）'),
        dict(type='array', var='substrings', h=150, label='substrings（已划分出的合法括号段）'),
        dict(type='calls', h=230),
    ],
    watch=[('diff', 'diff', 'yellow'), ('start', 'start', 'blue'), ('i', 'i', 'pink'), ('substrings', 'substrings', 'green')],
    captions={
        'if len(s) <= 2': lambda S, B, r: (f'`len(s) = {len(S.s)} ≤ 2`：只可能是 `()`，==递归出口==' if len(S.s) <= 2 else f'`len(s) = {len(S.s)} > 2`：还能继续拆分'),
        'return s': '太短无法再划分，原样返回 `{ret}`',
        'substrings = []': '准备把 `s` 拆成若干段==拼接==的合法括号串',
        'start = 0': '`start` 记录当前这段的起点',
        'diff = 0': '`diff` = 左括号数 − 右括号数，回到 0 就说明凑成了一段合法串',
        'for i, ch': '看第 `{i}` 个字符 `{ch}`',
        "if ch == '1'": '`ch = {ch}`：{"是 1，当左括号" if ch == "1" else "是 0，当右括号"}',
        'diff += 1': '左括号：`diff` → =={diff}==',
        'diff -= 1': '右括号：`diff` → =={diff}==',
        'if diff == 0': lambda S, B, r: (f'`diff = 0`：`s[{S.start}..{S.i}]` 前后括号配平，是一段不可再分的合法串' if S.diff == 0 else f'`diff = {S.diff} > 0`：还没配平，继续往右'),
        'substrings.append': '这段只能是外层 `(` 套内层：去掉外层括号，==递归==处理 `s[{start+1}:{i}]`，再套回 `1…0` 放进 `substrings`',
        'start = i + 1': '下一段从 `{start}` 开始',
        'substrings.sort': '段与段可以相邻交换 = 冒泡排序 → ==从大到小排序==：`{substrings}`',
        "''.join": '拼接得到最大字典序：`{ret}`',
    },
    cards=dict(
        one_liner='把 1 当左括号：拼接的段从大到小排，嵌套的内部递归',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['特殊字符串：`0`、`1` 个数相等，且每个前缀里 `1` 不少于 `0`',
                 '操作：交换相邻的两个特殊子串，求字典序最大的结果',
                 '示例：`11011000` → `11100100`'],
        quote='把 1 看成左括号，0 看成右括号……这两个性质和特殊字符串的两个性质是完全一样的。用合法括号字符串思考更方便。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法括号串有两种组合：==拼接==和==嵌套==',
              '拼接：相邻子串可交换，相当于冒泡排序 → 从大到小排',
              '嵌套：去掉最外层括号，内部是规模更小的同一问题 → 递归'],
        summary=['时间 `O(n^2)`，瓶颈是递归中的字符串拼接；空间 `O(n)`',
                 '`diff` 回到 0 才切一段；切完要 `start = i + 1`',
                 '递归的是 `s[start+1:i]`（去掉外层括号），返回后要套回 `"1"` 和 `"0"`',
                 '同类题：合法括号字符串相关题（括号拆分/嵌套）'],
    ),
)
