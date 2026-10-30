def _num(S):
    d = S.get('digits')
    if not d:
        return ''
    return ''.join(map(str, d))


def _color(S, i, v):
    if 'i' not in S:
        return None
    if i == S['i']:
        return 'yellow'
    if i > S['i']:
        return 'cyan'
    return None


def _for(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '循环跑完都没有 `return`：说明 ==digits 全是 9=='
    if 'i' not in B:
        return f'输入 `{S.digits}`：从最右边 `i = {S.i}` 开始，`digits[{S.i}] = {S.digits[S.i]}`'
    return f'往左看第 `i = {S.i}` 位：`digits[{S.i}] = {S.digits[S.i]}`'


def _if(S, B, ret):
    d = S.digits[S.i]
    if d < 9:
        return f'`{d} < 9`：这一位加一==不会再进位== → 找到了“第一个不等于 9 的数”'
    return f'`digits[{S.i}] = 9`：加一变成 10 → 本位写 0，==进位==给左边一位'


CONFIG = dict(
    num=66, title='加一', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='从右往左找第一个不是 9 的数',
    tags=['面试经典150'],
    code='''
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1  # 进位
                return digits
            digits[i] = 0  # 进位数字的右边数字都变成 0

        # digits 全是 9，加一后变成 100...00
        return [1] + digits
''',
    call='''s = Solution()
a = s.plusOne([2, 3, 9, 9, 9])
b = s.plusOne([9, 9])
[a, b]''',
    expect=[[2, 4, 0, 0, 0], [1, 0, 0]],
    views=[
        dict(type='text', size=30, h=70,
             fn=lambda S: f"当前数组表示的整数：=={_num(S)}==" + ('　（输入 `23999`，答案 `24000`）' if len(S.get('digits') or []) == 5
                                                              else '　（输入 `99`，答案 `100`）')),
        dict(type='array', var='digits', pointers={'i': 'yellow'}, cell=96, h=250,
             label='digits（黄 = 当前位，青 = 已进位变成 0）', color=_color),
        dict(type='text', size=26, h=110, lines=3,
             fn=lambda S: '规律：`23999 + 1 = 24000`，`999 + 1 = 1000`\n末尾连续的 9 全变 0，==左边第一个非 9 的数加一=='),
    ],
    watch=[('i', 'i', 'yellow'), ('digits[i]', lambda S: S['digits'][S['i']]), ('digits', 'digits', 'green')],
    captions={
        'for i in range': _for,
        'if digits[i] < 9': _if,
        'digits[i] += 1': '进位：`digits[{i}]` 加一变成 `{digits[i]}`',
        'return digits': '更左边的数字都不受影响 → 直接返回 =={digits}==',
        'digits[i] = 0': '进位数字的右边数字都变成 0：`digits[{i}] = 0`，继续看左边一位',
        'return [1] + digits': '全是 9 的数加一变成 `100…00`：在前面补一个 1 → =={ret}==',
    },
    cards=dict(
        one_liner='从右往左找第一个不是 9 的数：它加一，右边全变 0',
        complexity='时间 `O(m)`（`m` 为末尾 9 的个数），空间 `O(1)`',
        problem=['`digits` 从高位到低位表示一个没有前导 0 的大整数，返回它 ==加 1== 后的数组',
                 '示例：`[1,2,3]` → `[1,2,4]`；`[9]` → `[1,0]`',
                 '本视频：`[2,3,9,9,9]` → `[2,4,0,0,0]`，`[9,9]` → `[1,0,0]`'],
        quote='比如 23999+1 = 24000，999+1=1000。……==从右往左找第一个不等于 9 的数==，记作 digits[i]。进位，把 digits[i] 加一，把下标在 [i+1,n-1] 中的数全变成 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遇到 9：本位写 0，继续往左看（进位）',
              '遇到不是 9 的数：加一后不会再进位 → ==立刻 return==',
              '特别地，如果所有数都等于 9，答案是 `[1, 0, …, 0]`'],
        summary=['时间 `O(m)`：只会扫过末尾连续的 9；空间 `O(1)`（返回值不计）',
                 '易错：==全是 9 时长度要加一==，`[1] + digits`（此时 digits 已全为 0）',
                 '找到非 9 的数加一后就可以返回，不必扫完整个数组',
                 '同类：2. 两数相加、415. 字符串相加、989. 数组形式的整数加法'],
    ),
)
