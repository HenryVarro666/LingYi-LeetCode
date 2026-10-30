CONFIG = dict(
    num=1056, title='易混淆数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐位翻转后比较',
    code='''
class Solution(object):
    def confusingNumber(self, n):

        r = 0

        same = set([0, 1, 8])
        invalid = set([2, 3, 4, 5, 7])

        tmp = n
        while tmp:
            digit = tmp % 10
            tmp //= 10
            if digit in invalid:
                return False
            
            if digit in same:
                r = r * 10 + digit
            else:
                r = r * 10 + 15 - digit

        return r != n
''',
    call='Solution().confusingNumber(89)',
    expect=True,
    views=[
        dict(type='text', size=40, fn=lambda S: f"原数 `n = {S['n']}`，已翻转出的新数 `r = {S['r']}`" if 'r' in S else f"原数 `n = {S['n']}`"),
        dict(type='text', size=34, fn=lambda S: f"还没分离的部分 `tmp = {S['tmp']}`" if 'tmp' in S else ''),
        dict(type='set', var='same', fmt=lambda x: str(x), label='same（旋转后不变）', h=130),
        dict(type='set', var='invalid', fmt=lambda x: str(x), label='invalid（旋转后无效）', h=130),
    ],
    watch=['n', 'tmp', 'digit', ('r', 'r', 'green')],
    captions={
        'digit = tmp % 10': '取最低位 `digit = {tmp_before} % 10 = {digit}`'.replace('{tmp_before}', '{B.tmp}'),
        'tmp //= 10': '去掉最低位：`tmp` → {tmp}',
        'if digit in invalid': lambda S, B, r: (f'`{S.digit}` 旋转后不是数字 → 不是易混淆数' if S.digit in S.invalid else f'`{S.digit}` 不在 invalid 中，可以旋转'),
        'if digit in same': lambda S, B, r: (f'`{S.digit}` 旋转后不变（0/1/8）' if S.digit in S.same else f'`{S.digit}` 是 6 或 9，旋转后互换（6↔9）'),
        'r = r * 10 + digit': '不变的数位直接接到 `r` 末尾：`r = {B.r}×10 + {digit}` = =={r}==',
        'r = r * 10 + 15': '6↔9 互换：`15 − {digit} = {15 - digit}`，`r = {B.r}×10 + {15 - digit}` = =={r}==',
        'return r != n': lambda S, B, r: f'翻转后 `r = {S.r}`，原数 `n = {S.n}`：' + ('不同 → ==是易混淆数==' if S.r != S.n else '相同 → 不是易混淆数'),
        'return False': '出现无法旋转的数位 → 直接返回 `False`',
    },
    cards=dict(
        one_liner='从低位到高位翻转，把翻出来的新数和原数比',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把数字旋转 180 度：0、1、8 不变，6 和 9 互换，2/3/4/5/7 无效',
                 '旋转后得到有效且与原数不同的数，叫易混淆数',
                 '示例：`6` → `true`（变成 9）；`89` → `true`（变成 68）；`11` → `false`；`25` → `false`'],
        quote='从最低位开始逐位分离n的数位，并将这个数位翻转后加入到新的数当中。若期间出现了无法翻转的情况，直接返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['最低位旋转后会变成最高位，所以每次把新数位接在 `r` 的末尾：`r = r*10 + 数位`',
              '6 变 9、9 变 6，所以用 `15 - digit` 一步搞定',
              '遇到 2/3/4/5/7 立刻返回 `False`；全部处理完再比较 `r != n`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错点：旋转后和原数相同（如 `11`、`88`、`69`）不算易混淆数',
                 '原文为 Python 2 写法，整数除法 `tmp /= 10` 已改为 `tmp //= 10`',
                 '示例用 `89`：低位先翻，得 `6`，再得 `68`，与 `89` 不同 → `true`'],
    ),
)
