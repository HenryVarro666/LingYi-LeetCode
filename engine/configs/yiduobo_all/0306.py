def _info(S):
    if 'first_num' not in S:
        return '枚举第一个数 `first_num` 和第二个数 `second_num`，再检查后面能否一直是「前两数之和」'
    s = f"`first_num = {S['first_num']}`"
    if 'second_num' in S:
        s += f"，`second_num = {S['second_num']}`"
    if 'c' in S and 'now' in S:
        s += f"，`c = {S['c']}`"
    return s


def _color(S, k, v):
    if 'first_num' not in S:
        return None
    i = S.get('i')
    j = S.get('j')
    if i is None:
        return None
    if k <= i:
        return 'blue'
    if j is not None and 'second_num' in S and i < k <= j:
        return 'pink'
    if 'c' in S and 'now' in S and 'second_num' in S and j is not None:
        if S['now'] <= k < S['now'] + len(str(S['c'])):
            return 'green'
    return None


CONFIG = dict(
    num=306, title='累加数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='枚举前两个数 + 逐项验证',
    tags=[],
    code='''
class Solution(object):
    def isAdditiveNumber(self, num):

        for i in range(0, len(num) - 2):
            if i > 0 and num[0] == '0':
                break
            first_num = int(num[:i + 1])

            for j in range(i + 1, len(num) - 1):
                if j > i + 1 and num[i + 1] == '0':
                    break
                second_num = int(num[i + 1 : j + 1])
                a = first_num
                b = second_num
                now = j + 1
            
                while True:
                    c = a + b
                    if now + len(str(c)) - 1 >= len(num):
                        break
                    if int(num[now : now + len(str(c))]) != c:
                        break

                    now += len(str(c))
                    if now == len(num):
                        return True
                    a = b
                    b = c
        
        return False
''',
    call='Solution().isAdditiveNumber("199100199")',
    expect=True,
    views=[
        dict(type='string', var='num', label='num（蓝 = 第一个数，粉 = 第二个数，绿 = 正在验证的 c）', cell=80, h=190,
             pointers={'now': 'green'}, color=_color),
        dict(type='text', h=90, size=28, fn=_info),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`a = {S['a']}`，`b = {S['b']}`，`c = a + b = {S['c']}`" if 'c' in S else
                           (f"`a = {S['a']}`，`b = {S['b']}`" if 'a' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'first_num', 'second_num', 'a', 'b', 'c', ('now', 'now', 'green')],
    captions={
        'for i in range': '枚举第一个数的结尾 `i = {i}`（至少给后两个数留位置）',
        "if i > 0 and num[0] == '0'": lambda S, B, r: ("第一个数有前导 0 且长度 > 1 → ==不合法==，后面更长的也不行，`break`" if S.i > 0 and S.num[0] == '0'
                                                       else "没有前导 0 问题，继续"),
        'first_num = int': '第一个数 `num[:{i + 1}]` = =={first_num}==',
        'for j in range': '枚举第二个数的结尾 `j = {j}`',
        "if j > i + 1 and num[i + 1] == '0'": lambda S, B, r: ("第二个数有前导 0 且长度 > 1 → ==不合法==，`break`" if S.j > S.i + 1 and S.num[S.i + 1] == '0'
                                                              else "第二个数没有前导 0 问题，继续"),
        'second_num = int': '第二个数 `num[{i + 1}:{j + 1}]` = =={second_num}==',
        'a = first_num': '`a` = 前一个数 {a}',
        'b = second_num': '`b` = 后一个数 {b}',
        'now = j + 1': '`now = {now}`：下一个数应该从这个位置开始',
        'c = a + b': '应出现的下一个数 `c = {a} + {b}` = =={c}==',
        'if now + len(str(c)) - 1 >= len(num)': lambda S, B, r: (f"`c = {S.c}` 要占 {len(str(S.c))} 位，从 {S.now} 开始会==超出末尾== → 这组前两数失败"
                                                               if S.now + len(str(S.c)) - 1 >= len(S.num) else
                                                               f"`c = {S.c}` 占 {len(str(S.c))} 位，没有超出末尾，继续"),
        'if int(num[now : now': lambda S, B, r: (f"`num[{S.now}:{S.now + len(str(S.c))}]` = {int(S.num[S.now:S.now + len(str(S.c))])} ≠ `{S.c}` → ==不匹配==，换下一组"
                                                 if int(S.num[S.now:S.now + len(str(S.c))]) != S.c else
                                                 f"`num[{S.now}:{S.now + len(str(S.c))}]` = {S.c} == `c` → 匹配，继续往后"),
        'now += len(str(c))': '匹配的数占 {len(str(c))} 位，`now` → {now}',
        'if now == len(num)': lambda S, B, r: ("==恰好用完整个字符串== → 是累加数" if S.now == len(S.num) else f"`now = {S.now}` 还没到末尾 `{len(S.num)}`，继续"),
        'a = b': '前移一位：`a` = {a}',
        'b = c': '`b` = {b}，再算下一个和',
        'return False': '所有枚举都失败 → `False`',
        'return True': '整个字符串被拆成了累加序列 → `True`',
    },
    cards=dict(
        one_liner='枚举前两个数，后面每个数都由前两数之和决定',
        complexity='时间 `O(n^3)`（两层枚举 + 逐项验证），空间 `O(n)`',
        problem=['累加数：字符串拆成至少 3 个数，==除前两个外每个数都等于前两数之和==',
                 '数字不能有前导 0（`0` 本身可以）',
                 '例如 `199100199`：1 + 99 = 100，99 + 100 = 199 → `True`'],
        quote='目前只想到最暴力的枚举法，即枚举第一个数和第二个数，然后逐个计算后面的数并验证。需要注意枚举的数最高位如果为0，那么这个数就只能为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一个数和第二个数一旦确定，整个序列就==唯一确定==',
              '用 `now` 指向下一个数的起点，比较 `num` 里的这一段是否等于 `a + b`',
              '前导 0：开头是 0 就只能取单个 0，所以一发现就 `break`'],
        summary=['时间 `O(n^3)`，空间 `O(n)`',
                 '前导 0 要同时检查第一个数和第二个数',
                 '`now + len(str(c)) - 1 >= len(num)`：先判断越界，再切片比较',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码无需其他改动',
                 '本题库里没有题面，题意按题名与代码整理'],
    ),
)
