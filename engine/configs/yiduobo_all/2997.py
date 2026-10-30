def _x(S):
    k = S['k']
    r = S.get('res', 0)
    return f"当前 k = `{k:04b}`（已把 nums 异或进来）　已数到 1 的个数 res = =={r}=="

CONFIG = dict(
    num=2997, title='使数组异或和等于 K 的最少操作次数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='异或后逐位数 1',
    tags=['灵神题单', '位运算', '难度分 1525'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):

        for v in nums:
            k ^= v
        
        res = 0
        while k:
            if k & 1:
                res += 1
            k >>= 1
        
        return res
''',
    call='Solution().minOperations([2,1,3,4], 1)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=150),
        dict(type='text', fn=_x, size=30, h=90),
    ],
    watch=['v', ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for v in': '遍历 `nums` 取数（取完则退出循环），当前 `v = {v}`，把它异或进 `k`',
        'k ^= v': '`k` 现在是“异或和 与 k 的差异”：`{B.k} ^ {v} = {k}`，值为 1 的位就是还不对的位',
        'res = 0': '`k` 里的 1 就是需要翻转的位，开始统计，`res = 0`',
        'while k': lambda S, B, ret: f"判断 `k = {S['k']}` 是否还有位没处理 → {'有，继续' if S['k'] else '全部处理完，退出'}",
        'if k & 1': '看最低位 `k & 1 = {k & 1}` → {"是 1：这一位要翻一次" if k & 1 else "是 0：不用动"}',
        'res += 1': '这一位不同，要一次操作：`res = {res}`',
        'k >>= 1': '右移一位，看下一位：`k = {k}`',
        'return res': '数完了所有位，最少操作次数 = =={res}==',
    },
    cards=dict(
        one_liner='一次操作改异或和的一位，数不同的位就行',
        complexity='时间 `O(n + log k)`，空间 `O(1)`',
        problem=['每次操作可翻转 `nums` 中任意一个数的任意一个二进制位',
                 '求让所有数异或和等于 `k` 的最少操作次数',
                 '示例：`nums=[2,1,3,4], k=1` → `2`'],
        quote='题目中的修改操作可以修改任意数的任意二进制位，实际上就相当于可以通过单次操作修改数组异或和的任意二进制位，于是只需计算数组异或和与k的不同数位数量即为最终答案。',
        quote_src='—— yiduobo 题解',
        idea=['翻转任意数的一位 = 翻转异或和的同一位',
              '所以只要数异或和与 `k` 有几位不同',
              '把 `k` 依次异或所有 `nums`，结果里 1 的个数就是不同位数，用 `k & 1` + 右移逐位数出来'],
        summary=['时间 `O(n + log k)`，空间 `O(1)`',
                 '先异或再数 1：不需要真的去翻转',
                 '数 1 也可用 `bin(k).count("1")`，或 `k &= k-1` 每次去掉最低位的 1',
                 '易错：`k >>= 1` 别漏，否则死循环'],
    ),
)
