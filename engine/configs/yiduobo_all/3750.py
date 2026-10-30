CONFIG = dict(
    num=3750, title='最少翻转次数得到反转二进制字符串', difficulty='Easy', category='位运算',
    author='yiduobo', technique='模 2 取位 + 左右双指针',
    tags=['灵神题单', '位运算', '难度分 1289'],
    code='''
class Solution(object):
    def minimumFlips(self, n):
        
        digits = []
        while n:
            digits.append(n % 2)
            n //= 2
        
        left, right = 0, len(digits) - 1
        res = 0
        while left < right:
            if digits[left] != digits[right]:
                res += 2
            left += 1
            right -= 1
        
        return res
''',
    call='Solution().minimumFlips(44)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"`n` 的二进制是 `{S['_inner']['_n0']:b}`，下面 `digits` 是它从低位到高位的样子" if False else
                                         ('把 `n` 一位一位拆进 `digits`（低位在前）' if 'digits' in S else '')), size=24, h=80),
        dict(type='array', var='digits', label='digits（蓝 = left，粉 = right，绿 = 一对已核对相同，红 = 不同）', cell=84,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=lambda S, i, v: (None if 'right' not in S else
                                    ('red' if (i < S['left'] or i > S['right']) and S['digits'][i] != S['digits'][len(S['digits']) - 1 - i] else
                                     'green' if (i < S['left'] or i > S['right']) else None)),
             dim=lambda S, i, v: 'right' in S and (i < S['left'] or i > S['right']) and False, h=330),
        dict(type='text', fn=lambda S: (f"`digits[{S['left']}] = {S['digits'][S['left']]}`，`digits[{S['right']}] = {S['digits'][S['right']]}` → " +
                                        ('==不同==，两位都要翻转，`res + 2`' if S['digits'][S['left']] != S['digits'][S['right']] else '相同，不用动')) if 'right' in S and S['left'] < S['right'] else '', size=26, h=90),
    ],
    watch=[('n', 'n', 'blue'), ('left', lambda S: S.get('left'), 'blue'), ('right', lambda S: S.get('right'), 'pink'), ('res', lambda S: S.get('res'), 'green')],
    captions={
        'digits = []': '准备一个列表 `digits`，装 `n` 的二进制位（低位在前）',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，还要取一位' if S.n else '`n = 0`：所有二进制位都取出来了'),
        'digits.append(n % 2)': '`n % 2 = {n % 2}` 是当前最低位，放进 `digits`：`{digits}`',
        'n //= 2': '去掉最低位：`n` → {n}',
        'left, right = 0, len': '两个指针指向两端：`left = 0`，`right = {right}`',
        'res = 0': '`res` 累计翻转次数',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，还有没核对的一对' if S.left < S.right
                                                else f'`left = {S.left} ≥ right = {S.right}`：指针相遇，中间那位（若有）和自己比必然相同 → 结束'),
        'if digits[left] != digits[right]': lambda S, B, r: (
            f'反转后 `s[left]` 的位置放的是 `s[right]`：比较 `{S.digits[S.left]}` 和 `{S.digits[S.right]}` → '
            + ('==不同=='  if S.digits[S.left] != S.digits[S.right] else '相同，这一对不用翻')),
        'res += 2': '两位不同：必须==两位都翻转==，才能互相变成对方 → `res = {res}`',
        'left += 1': '`left` → {left}，向中间靠',
        'right -= 1': '`right` → {right}，向中间靠',
        'return res': '所有对都核对完，共翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='首尾配对：每一对不同的位，要翻两次',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['正整数 `n` 的二进制串 `s`，每次可翻转其中一位',
                 '要让 `s` 变成它自己的反转串，最少翻几次',
                 '示例：`n = 10`（`1010`）→ `4`；本视频：`n = 44`（`101100`）→ `2`'],
        quote='若s[left]与s[right]相同，那么就不需要操作，反之就需要将s[left]以及s[right]都变为对方，需要进行两次翻转操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用「模 2、除以 2」把 `n` 拆成 `digits`',
              '`left`、`right` 从两端往中间走：`s[left]` 在反转串里对应的就是 `s[right]`',
              '一对不同 → 两边都要改，`res += 2`；相同 → 不用管；指针相遇即结束'],
        result='只有最外面一对不同 → 返回 `2` ✓',
        summary=['时间、空间都是 `O(log n)`（二进制位数）',
                 '易错：不同的一对要加 `2`，不是加 `1`',
                 '易错：`while left < right`，中间那位不用比',
                 '原文本来就能在 Python 3 运行，`//` 已经是整除，代码未改动',
                 '对比灵神：灵神用位反转 + 异或 + `bit_count`，这里是直接双指针'],
    ),
)
