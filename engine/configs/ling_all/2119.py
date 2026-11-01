CONFIG = dict(
    num=2119, title='反转两次的数字', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='看末尾是否为 0（Go 原文转写）', tags=[],
    code='''
class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        return num == 0 or num % 10 > 0
''',
    call='Solution().isSameAfterReversals(1800)',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: f"`num = {S['num']}`：个位是 `{S['num'] % 10}`" + ('，末尾是 0 → 反转后丢掉前导零，回不来' if S['num'] % 10 == 0 and S['num'] else ''), size=30),
        dict(type='text', fn=lambda S: f"反转 `{S['num']}` → `{str(S['num'])[::-1].lstrip('0') or '0'}` → 再反转 `{(str(S['num'])[::-1].lstrip('0') or '0')[::-1].lstrip('0') or '0'}`", size=28),
    ],
    watch=[('num', 'num', 'blue'), ('num % 10', 'num % 10', 'pink')],
    captions={
        'return num': '`num == 0` 为 {num == 0}；`num % 10 = {num % 10}` {"> 0" if num % 10 > 0 else "不大于 0"} → 返回 =={ret}==：末尾有 0 的数反转两次会丢零',
    },
    cards=dict(
        one_liner='只有末尾带 0 的数，反转两次才会变',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['反转整数会倒置所有位，且不保留前导零；`1800` 反转得 `81`',
                 '反转两次后与原数相同吗？',
                 '示例：`526` → `true`；`1800` → `false`；`0` → `true`'],
        before=[dict(heading='先看例子', lines=['`526` → `625` → `526`：相同', '`1800` → `0081` 去零成 `81` → `18`：==不同==', '`0` → `0` → `0`：相同', '规律：只有末尾的 0 会在反转时变成前导零被丢掉']), dict(heading='为什么', lines=['没有末尾 0 的数：反转后没有前导零，不丢位，再反转就回来', '有末尾 0 的数：反转时 0 变成前导零被丢，位数变少，回不来', '`0` 是特例：反转还是 `0`，所以答案是 true'])],
        quote='func isSameAfterReversals(num int) bool { return num == 0 || num%10 > 0 }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['原数没有前导零，第一次反转只会在末尾有 0 时丢零',
              '丢了零第二次反转就回不到原数',
              '所以：末尾非 0，或者 `num` 本身就是 0'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（单行表达式）',
                 '时间 `O(1)`，空间 `O(1)`',
                 '易错点：`0` 末尾是 0，但答案是 true，要单独判断'],
    ),
)
