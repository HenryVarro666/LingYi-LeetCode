def _bin(x):
    return format(x, 'b') if x else '0'


def _fn(S):
    if 'num' not in S:
        return ''
    n = S['num']
    return (f"num = `{_bin(n)}`（{n}）　`res` = =={S.get('res', 0)}==　`max_l` = =={S.get('max_l', 0)}==")


CONFIG = dict(
    num=1558, title='得到目标数组的最少函数调用次数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='按位统计 1 的个数与最大位数',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        res = 0
        max_l = 0
        for num in nums:
            l = 0
            while num:
                res += num % 2
                num //= 2
                l += 1
            
            max_l = max(max_l, l - 1)

        return res + max_l
''',
    call='Solution().minOperations([4,2,5])',
    expect=6,
    views=[
        dict(type='text', fn=_fn, size=30, h=90),
        dict(type='array', var='nums', label='nums（4=100，2=10，5=101）', h=200),
    ],
    watch=[('num', "S.get('num')", 'blue'), ('l', "S.get('l')", 'cyan'), ('res', 'res', 'green'), ('max_l', 'max_l', 'orange')],
    captions={
        'res = 0': '`res` 累计所有数二进制里 ==1 的个数==（加 1 的操作次数）',
        'max_l = 0': '`max_l` 记录最大位数 − 1（乘 2 的操作次数）',
        'l = 0': '换下一个数，位数计数 `l` 清零',
        'while num': lambda S, B, r: (f'`num = {S.num}` 还没变成 0，继续拆二进制位' if S.num else '`num` 已经是 0：这个数的所有位都看完了'),
        'res += num % 2': lambda S, B, r: (f'末位是 1（`{S.num}` 为奇数）→ 需要一次加 1 操作：`res` = =={S.res}==' if S.res != B.res
                                           else f'末位是 0（`{S.num}` 为偶数）→ 乘 2 就能得到，不用加：`res` 仍为 {S.res}'),
        'num //= 2': '右移一位（整除 2），看下一位：`num` = {num}',
        'l += 1': '又看了一位：这个数共 `l` = {l} 位',
        'max_l = max': '乘 2 操作全体共用，只要满足位数最多的那个：`max_l = max({B.max_l}, {l} − 1)` = =={max_l}==',
        'return res': '答案 = 所有 1 的个数 `{res}` + 乘 2 次数 `{max_l}` = =={res + max_l}==',
    },
    cards=dict(
        one_liner='加 1 的次数看 1 的个数，乘 2 的次数看最大位数 − 1',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['从全 0 数组出发，两种操作：==某个元素加 1==，或==所有元素乘 2==',
                 '求变成目标数组 `nums` 的最少操作次数',
                 '示例：`[4,2,5]` → `6`'],
        quote='乘以2这种操作本身是不会产出1的，因此对于一个数而言，若其二进制表示中有k个1，那么至少需要k次操作来添加这些1。',
        quote_src='—— yiduobo 题解原文',
        idea=['二进制里每个 1 都得靠一次「加 1」产生，所以 1 的个数全部累加',
              '乘 2 对所有数同时生效，位数少的数先保持 0 陪跑，所以只需 ==最大位数 − 1== 次',
              '两部分互不影响，直接相加'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`max_l` 存的是 `l - 1`：最高位那个 1 不需要再乘 2',
                 '数为 0 时 `l = 0`，`max(…, -1)` 不会拉低答案',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
