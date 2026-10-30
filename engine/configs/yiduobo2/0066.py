def _num(S):
    d = S.get('digits')
    if not d:
        return ''
    return ''.join(map(str, d))


def _color(S, i, v):
    if 'pos' not in S:
        return None
    if i == S['pos']:
        return 'yellow'
    if i > S['pos'] and v == 0:
        return 'cyan'
    return None


def _while(S, B, ret):
    p, d = S.pos, S.digits
    if p > -1 and d[p] == 9:
        return f'`digits[{p}] = 9`：加 1 变成 10 → 本位置 0，==进位==到更高一位'
    if p == -1:
        return '`pos = -1`：已经越过最高位 → ==每一位都是 9==，循环结束'
    return f'`digits[{p}] = {d[p]}` 不是 9：进位到这里就停下'


def _if(S, B, ret):
    if S.pos == -1:
        return '`pos == -1`：==全都是 9== → 答案应该是 `1000…000`'
    return f'`pos = {S.pos}`：遇到了不是 9 的位 → 走 else'


CONFIG = dict(
    num=66, title='加一', difficulty='Easy', category='数学',
    author='yiduobo', technique='从低位往高位扫描进位',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def plusOne(self, digits):
        pos = len(digits) - 1
        while pos > -1 and digits[pos] == 9:
            digits[pos] = 0
            pos -= 1

        if pos == -1:
            digits[0] = 1
            digits.append(0)
        else:
            digits[pos] += 1

        return digits
''',
    call='''s = Solution()
a = s.plusOne([4, 9, 9])
b = s.plusOne([9, 9, 9])
[a, b]''',
    expect=[[5, 0, 0], [1, 0, 0, 0]],
    views=[
        dict(type='text', size=30, h=70,
             fn=lambda S: f"当前数组表示的整数：=={_num(S)}=="),
        dict(type='array', var='digits', pointers={'pos': 'yellow'}, cell=96, h=250, min_slots=5,
             label='digits（黄 = pos，青 = 进位后置 0 的位）', color=_color),
        dict(type='text', size=26, h=110, lines=3,
             fn=lambda S: '加法的进位==每次最多进 1==：\n是 9 就置 0 并继续，不是 9 就加 1 收工'),
    ],
    watch=[('pos', 'pos', 'yellow'), ('digits', 'digits', 'green')],
    captions={
        'pos = len(digits) - 1': '输入 `{digits}`：从最低位开始扫描，`pos = {pos}`',
        'while pos > -1 and': _while,
        'digits[pos] = 0': '当前位置 0（`9 + 1 = 10`，留下 0）',
        'pos -= 1': '进位给更高一位：`pos` → `{pos}`',
        'if pos == -1': _if,
        'digits[0] = 1': '此时数组全是 0：把最高位改成 1……',
        'digits.append(0)': '……再在末尾补一个 0 → `{digits}`，等价于在最前面插入 1',
        'digits[pos] += 1': '`digits[{pos}]` 加 1 变成 `{digits[pos]}`，不会再进位',
        'return digits': '返回 =={digits}==',
    },
    cards=dict(
        one_liner='进位每次最多进 1：是 9 就置 0 继续，不是 9 就加 1 返回',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`digits` 从高位到低位表示一个没有前导 0 的大整数，返回它 ==加 1== 后的数组',
                 '示例：`[1,2,3]` → `[1,2,4]`；`[9]` → `[1,0]`',
                 '本视频：`[4,9,9]` → `[5,0,0]`，`[9,9,9]` → `[1,0,0,0]`'],
        quote='注意到加法中的进位==每次最多进1==，于是可以从低位到高位扫描，如果当前位上是9，那么将当前位置0，并继续看下一位。如果当前位上不是9，那么当前位加上1返回结果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`while` 循环把末尾连续的 9 全部置 0，`pos` 停在第一个非 9 的位',
              '`pos == -1` 说明==全都是 9==，答案是 `1000…000`',
              '否则 `digits[pos] += 1` 即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：全是 9 时要在最高位加入 1，长度加一',
                 '小技巧：此时数组全为 0，==首位改 1、末尾补 0== 就等于前插 1，省掉 `insert(0, 1)` 的整体后移',
                 '原文为 Python 2 写法：只删去了类型说明文档字符串，逻辑未改'],
    ),
)
