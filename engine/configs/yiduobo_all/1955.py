def _txt(S):
    if 'res' not in S:
        return '三个计数：`zero_cnt` 全 0，`one_cnt` 先 0 后 1，`res` 特殊子序列'
    n = S.get('num')
    if n is None:
        return ''
    if n == 0:
        return f"遇到 `0`：新 zero_cnt = 保底 `{S['zero_cnt']}` + 末尾追加 + 单独一个 `1`"
    if n == 1:
        return '遇到 `1`：不选 + 接在 1 的后面 + 接在 0 的后面'
    return '遇到 `2`：不选 + 接在 2 的后面 + 接在 01 的后面'


CONFIG = dict(
    num=1955, title='统计特殊子序列的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三变量滚动 DP',
    tags=['灵神题单·动态规划', '难度分 2125'],
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
    skip=['mod = '],
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=170),
        dict(type='array', var=lambda S: [S.get('zero_cnt', 0), S.get('one_cnt', 0), S.get('res', 0)],
             label='[ zero_cnt（0…0） ,  one_cnt（0…01…1） ,  res（0…01…12…2） ]', cell=130, h=200,
             color=lambda S, i, v: 'yellow' if S.get('num') == i and S.get('_line', 0) in (10, 11, 12, 13, 14, 15, 16, 17) else None),
        dict(type='text', fn=_txt, size=26, h=100),
    ],
    watch=[('num', 'num', 'blue'), ('zero_cnt', 'zero_cnt', 'pink'), ('one_cnt', 'one_cnt', 'purple'), ('res', 'res', 'green')],
    captions={
        'zero_cnt = 0': '`zero_cnt`：`f[i][0]`，全是 0 的子序列个数',
        'one_cnt = 0': '`one_cnt`：`f[i][1]`，形如 0…01…1 的子序列个数',
        'res = 0': '`res`：`f[i][2]`，特殊子序列个数，也就是最终答案',
        'for num in nums': '取下一个数（`num` 现在是 {num}）：只更新对应的一个计数，其余保持不变；取完就结束',
        'num == 0': '`num` 是 `0` 吗：{num == 0}',
        'num == 1': '`num` 是 `1` 吗：{num == 1}',
        'zero_cnt += zero_cnt': '不选 {B.zero_cnt} 个，接在它们后面又 {B.zero_cnt} 个，再单独拎出 1 个 → `{B.zero_cnt} + {B.zero_cnt} + 1` = =={zero_cnt}==',
        'one_cnt += one_cnt': '不选 {B.one_cnt} 个 + 接在 1 后面 {B.one_cnt} 个 + 接在 0 后面 {zero_cnt} 个 = =={one_cnt}==',
        'res += res': '不选 {B.res} 个 + 接在 2 后面 {B.res} 个 + 接在 01 后面 {one_cnt} 个 = =={res}==',
        '%= mod': '对 `10^9+7` 取余（小例子里还没超出）',
        'return res': '`f[n-1][2]` 就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='把 f[i][0..2] 拆成三个变量，逐个数字迭代',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['特殊序列：若干个 0、再若干个 1、最后若干个 2（每段至少一个）',
                 '`nums` 里只有 `0/1/2`，数不同的特殊子序列有多少个，对 `10^9+7` 取余',
                 '示例：`[0,1,2,0,1,2]` → `7`'],
        quote='将s[i]加入到f[i - 1][1]中所有子序列的末尾，以及将s[i]加入到f[i - 1][0]中所有子序列的末尾，因此就有 f[i][1] = f[i - 1][1] + f[i - 1][1] + f[i - 1][0]',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][0]` 全 0；`f[i][1]` 形如 0…01…1；`f[i][2]` 形如 0…01…12…2',
              '遇到 0：保底 + 接在末尾 + 单独成一个 → `2f+1`',
              '遇到 1 或 2：保底 + 接在同类后面 + 接在前一类后面',
              '每轮只依赖上一轮，用变量代替数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：遇到 0 要多 `+1`（单独一个 0 也算全 0 子序列）',
                 '`+= x + y` 要注意是在原值上累加，等于 `2×原值 + y`',
                 '原文本身就是 Python 3 可运行的写法，代码未改'],
    ),
)
