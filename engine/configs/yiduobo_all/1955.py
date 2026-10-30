def _state(S):
    return [S.get('zero_cnt', 0), S.get('one_cnt', 0), S.get('res', 0)]


def _txt(S):
    if 'zero_cnt' not in S:
        return '三个计数：`0` 的子序列、`0…01…1` 的子序列、特殊子序列'
    if 'num' not in S:
        return f"`zero_cnt={S['zero_cnt']}`  `one_cnt={S['one_cnt']}`  `res={S['res']}`"
    n = S['num']
    if n == 0:
        return f"当前是 ==0==：只会改变 `zero_cnt`，结果 `{S['zero_cnt']}`"
    if n == 1:
        return f"当前是 ==1==：只会改变 `one_cnt`，结果 `{S['one_cnt']}`"
    return f"当前是 ==2==：只会改变 `res`，结果 `{S['res']}`"


CONFIG = dict(
    num=1955, title='统计特殊子序列的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状态机 DP · 三个计数变量',
    tags=['灵神题单', '动态规划', '难度分 2125'],
    code='''
class Solution(object):
    def countSpecialSubsequences(self, nums):

        zero_cnt = 0
        one_cnt = 0
        res = 0
        mod = 10 ** 9 + 7
        for num in nums:
            if num == 0:
                zero_cnt += zero_cnt + 1
                zero_cnt %= mod
            elif num == 1:
                one_cnt += one_cnt + zero_cnt
                one_cnt %= mod
            else:
                res += res + one_cnt
                res %= mod

        return res
''',
    call='Solution().countSpecialSubsequences([0, 1, 2, 0, 1, 2])',
    expect=7,
    skip=['mod = ', '%= mod', 'one_cnt = 0', 'res = 0'],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 0，蓝 = 1，粉 = 2；当前处理的那个值会变亮）', h=200, cell=100,
             color=lambda S, i, v: ('green', 'blue', 'pink')[v] if S.get('num') == v else None,
             dim=lambda S, i, v: 'num' in S and S['num'] != v),
        dict(type='array', var=_state, label='[ zero_cnt,  one_cnt,  res ]  分别是  0…0 / 0…01…1 / 0…01…12…2  的子序列数', h=200, cell=130, index=False,
             color=lambda S, i, v: ('green', 'blue', 'pink')[i]),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('zero_cnt', 'zero_cnt', 'green'), ('one_cnt', 'one_cnt', 'blue'), ('res', 'res', 'pink'), 'num'],
    captions={
        'zero_cnt = 0': '`zero_cnt`：全是 0 的子序列个数',
        'if num == 0': '`num = {num}`：看是 0、1 还是 2，只有对应的那一个计数会变',
        'elif num == 1': '`num = {num}`，不是 0 → 继续判断是不是 1',
        'zero_cnt += zero_cnt + 1': '遇到 0：不选它（保底 {B.zero_cnt} 个）+ 接到旧子序列末尾（{B.zero_cnt} 个）+ 它自己单独成一个（1 个）→ `zero_cnt = {zero_cnt}`',
        'one_cnt += one_cnt + zero_cnt': '遇到 1：不选（{B.one_cnt}）+ 接在 0…01…1 后（{B.one_cnt}）+ 接在全 0 后（{zero_cnt}）→ `one_cnt = {one_cnt}`',
        'res += res + one_cnt': '遇到 2：不选（{B.res}）+ 接在特殊序列后（{B.res}）+ 接在 0…01…1 后（{one_cnt}）→ `res = {res}`',
        'return res': '`res` 就是 `f[n-1][2]`，特殊子序列一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='遇到 0/1/2 只更新对应的计数：不选 + 接在后面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['特殊序列 = 正整数个 `0`，接正整数个 `1`，再接正整数个 `2`',
                 '数 `nums` 中不同的特殊子序列个数（下标集合不同就算不同），对 `10^9+7` 取余',
                 '示例：`[0,1,2,0,1,2]` → `7`'],
        quote='首先就有f[i][1] = f[i - 1][1]，f[i][2] = f[i - 1][2]。接下来考虑f[i][0]。在这里可以不将s[i]加入到子序列中，那么就有f[i - 1][0]个子序列保底。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 `i` 项里，形如全 0 / `0…01…1` / 特殊序列的子序列数',
              '遇到 `j`：不选它，保底 `f[i-1][j]`；选它，可接在 `j` 型或 `j-1` 型末尾',
              '遇到 0 时还能自己单独成一个，所以 `+1`；每轮只依赖上一轮，三个变量即可'],
        summary=['时间 `O(n)`，空间 `O(1)`：把 `f[i][0..2]` 压缩成三个变量',
                 '每次累加后都要取模，别等到最后',
                 '遇到 0 的转移多一个 `+1`（单独成序列），遇到 1、2 是接在前一类后面',
                 '本题的原文代码没有 Python 2 专有写法，无需改动',
                 '对比灵神的 `f[i][j]` 状态机写法：这里把三种状态拆成三个变量，思路相同'],
    ),
)
