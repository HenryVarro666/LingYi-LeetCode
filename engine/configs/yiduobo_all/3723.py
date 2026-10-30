def _txt(S):
    if 'nine' not in S:
        return f"要填 `num = {S['num']}` 位，数位和 `sum = {S['sum']}`（最多 `9×{S['num']} = {9*S['num']}`）"
    return f"`nine = {S['nine']}`：sum 里能分出 {S['nine']} 个 9，余数 `{S['sum'] - 9*S['nine']}`"


def _fin(S):
    if 'nine' not in S:
        return ''
    n, sm, nine = S['num'], S['sum'], S['nine']
    if nine == n:
        return f"前 {nine} 位全是 9"
    return f"`{'9'*nine}`（{nine} 个 9）+ `{sm - 9*nine}`（余数）+ `{'0'*(n-nine-1)}`（{n-nine-1} 个 0）"


CONFIG = dict(
    num=3723, title='数位平方和的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 9 集中在高位',
    tags=['灵神题单', '贪心与思维', '难度分 1537'],
    code='''
class Solution(object):
    def maxSumOfSquares(self, num, sum):
        
        if num * 9 < sum:
            return ""
        
        nine = sum // 9
        
        if nine == num:
            return '9' * num
        else:
            return '9' * nine + str(sum - 9 * nine) + '0' * (num - nine - 1)
''',
    call='Solution().maxSumOfSquares(5, 22)',
    expect='99400',
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='text', fn=_fin, size=26),
        dict(type='text', fn=lambda S: '平方和：一个 9 的平方 81，远大于把 9 拆开' if 'nine' in S else '', size=24),
    ],
    watch=['num', 'sum', 'nine'],
    captions={
        'if num * 9 < sum': lambda S, B, r: (f'全填 9 最多 `{S.num}×9 = {S.num*9}`，< `sum = {S.sum}` → 无解' if S.num * 9 < S.sum
                                            else f'`sum = {S.sum}` 在 `1` 到 `9×{S.num} = {S.num*9}` 之间 → 必有解'),
        'return ""': '无解，返回空字符串',
        'nine = sum // 9': '尽可能分出 9：`nine = {sum} // 9 = {nine}`，前 `nine` 位都填 9',
        'if nine == num': lambda S, B, r: (f'`nine = {S.nine}` == `num = {S.num}`：位数刚好用完' if S.nine == S.num
                                          else f'`nine = {S.nine}` < `num = {S.num}`：还有空位要填余数和 0'),
        "return '9' * num": '全是 9 → =={ret}==',
        "return '9' * nine": '`{nine}` 个 9 + 余数 `{sum - 9 * nine}` + `{num - nine - 1}` 个 0 → =={ret}==',
    },
    cards=dict(
        one_liner='和一定时，a²+b² 越不均匀越大：9 越多越好，并集中在前面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找恰好 `num` 位、各位数字之和为 `sum` 的整数',
                 '分数 = 各位数字平方和，求分数最大的；并列取最大的整数',
                 '示例：`num = 2, sum = 17` → `"98"`'],
        quote='对于一组和为s的非负整数a和b，要让a^2 + b^2最大，就应该让a取s，b取0，或者a取0，b取s。对于本题，则应该让值为9的数位尽可能的多。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sum` 在 `1` 到 `9×num` 之间必有解，大于它就返回空串',
              '`nine = sum // 9` 个 9 放在最高位（分数相同时数值最大）',
              '`nine < num`：下一位放余数 `sum − 9×nine`，其余补 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`nine == num` 要单独处理：此时没有空位放余数',
                 '`sum` 恰好被 9 整除时，余数位填的是 `0`，结果仍然正确',
                 '参数名 `sum` 盖住了内置函数 `sum`，只当整数用',
                 '对比灵神：灵神用 `s % 9` 判断是否有余数，再统一补 0；yiduobo 分两种情况返回'],
    ),
)
