def _txt(S):
    if 'bit' not in S or 'x' not in S or 'i' not in S:
        return ''
    n = int(''.join(map(str, S['nums'][:S['i'] + 1])), 2)
    return f"前缀 `{''.join(map(str, S['nums'][:S['i'] + 1]))}` = 十进制 {n}，中途取模后 `x = {S['x']}`（真值 {n} % 5 = {n % 5}）"


CONFIG = dict(
    num=1018, title='可被 5 整除的二进制前缀', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='边算前缀边取模',
    tags=['数学算法', '难度分 1376'],
    code='''
class Solution:
    def prefixesDivBy5(self, nums: List[int]) -> List[bool]:
        ans = [False] * len(nums)
        x = 0
        for i, bit in enumerate(nums):
            x = (x << 1 | bit) % 5
            ans[i] = x == 0
        return ans
''',
    call='Solution().prefixesDivBy5([1, 0, 1, 0, 1, 0, 0, 1])',
    expect=[False, False, True, True, False, False, False, False],
    views=[
        dict(type='array', var='nums', label='nums（二进制位，从高位到低位）', pointers={'i': 'blue'}, h=170,
             window=(lambda S: 0, 'i'),
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='ans', label='ans（True = 能被 5 整除）', h=170,
             color=lambda S, i, v: 'green' if v is True else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
    ],
    watch=[('i', 'i', 'blue'), 'bit', ('x', 'x', 'yellow')],
    captions={
        'for i, bit': lambda S, B, r: ('`nums` 扫完了' if B.get('i') == len(S.nums) - 1 else f'取下一位：`i = {S.i}`，`bit = {S.bit}`'),
        'ans = [False]': '先准备好和 `nums` 一样长的答案数组，默认全是 `False`',
        'x = 0': '`x` 保存当前前缀的值模 5，空前缀就是 0',
        'x = (x << 1': '`x << 1 | bit`：旧值左移一位再补上 `{bit}`；立刻 `% 5`：`({B.x} * 2 + {bit}) % 5` = =={x}==。中途取模不影响余数',
        'ans[i] = x == 0': '`x = {x}`，{"余数为 0 → 能被 5 整除，记 ==True==" if x == 0 else "余数不是 0 → 不能整除，记 False"}',
        'return ans': '每个前缀都判断完了，返回 `ans`',
    },
    cards=dict(
        one_liner='前缀的二进制值太大，只保存它模 5 的余数',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['`nums` 是二进制位数组，第 `i` 个前缀 `nums[0..i]` 看成一个二进制数 `x_i`',
                 '返回每个 `x_i` 是否能被 `5` 整除的布尔列表',
                 '示例：`[0,1,1]` → `[true,false,false]`；本视频用 `[1,0,1,0,1,0,0,1]`'],
        quote='注意本题 nums 很长，算出的二进制数 x 很大，但我们只需要判断 x mod 5 = 0 是否成立。可以在==中途取模==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['十进制里 `12` 右边加 `3` 是 `12*10+3`；二进制里 `110` 右边加 `1` 是 `110*2+1`，即 `x << 1 | bit`',
              '每次算出新 `x` 立刻换成 `x % 5`，数值永远小于 5，不会溢出',
              '模运算对加法和乘法封闭，所以中途取模不改变最终余数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：必须==每一步都取模==，否则 `x` 会变成 10^5 位的大数',
                 '`ans[i] = x == 0`：先比较再赋值，写成 `x == 0` 即可，不用 if',
                 '同类思路：任何「前缀数值能否被 k 整除」的题，都维护余数'],
    ),
)
