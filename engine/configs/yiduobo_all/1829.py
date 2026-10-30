def _bits(S):
    if 'now' not in S:
        return ''
    w = S['maximumBit']
    t = S['target'] if 'target' in S else None
    s = f"now = `{S['now']:0{w}b}`"
    if t is not None:
        s += f"　target = `{t:0{w}b}`　target ^ now = =={t ^ S['now']:0{w}b}=="
    return s

CONFIG = dict(
    num=1829, title='每个查询的最大异或值', difficulty='Medium', category='位运算',
    author='yiduobo', technique='前缀异或 + 倒序',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def getMaximumXor(self, nums, maximumBit):

        res = []
        now = 0
        target = (1 << maximumBit) - 1
        for num in nums:
            now ^= num
            res.append(target ^ now)
        
        res.reverse()
        return res
''',
    call='Solution().getMaximumXor([0,1,1,3], 2)',
    expect=[0, 3, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums（从左到右累积前缀异或）',
             color=lambda S, i, v: 'blue' if 'res' in S and S['_line'] >= 7 and i == len(S['res']) - (1 if S['_line'] == 9 else 0) else None, h=150),
        dict(type='text', fn=_bits, size=30, h=80),
        dict(type='array', var='res', label='res（每轮的最优 k）', h=150),
    ],
    watch=['now', 'target', ('num', 'num', 'blue')],
    captions={
        'res = []': '准备答案数组。后面是按“正序前缀”算的，最后再翻转',
        'now = 0': '`now` 保存当前前缀的异或，从 0 开始',
        'target =': '最多 `{maximumBit}` 位，最大异或值就是 `{maximumBit}` 个 1：`target = 2^{maximumBit} - 1 = {target}`',
        'for num in': '遍历 `nums` 取数（取完则退出循环），当前 `num = {num}`',
        'now ^= num': '前缀异或：`{B.now} ^ {num} = {now}`',
        'res.append': '要让 `now ^ k = target`，所以 `k = target ^ now = {target} ^ {now} = {target ^ now}`',
        'res.reverse': '题目是后缀逐个删除，而我们按前缀正序算的 → 翻转：`{B.res}` → `{res}`',
        'return res': '返回翻转后的答案 `{res}`',
    },
    cards=dict(
        one_liner='k = 全 1 ^ 当前异或和，倒着删变成正着加',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['给有序数组 `nums` 和位数上限 `maximumBit`，每轮选 `k < 2^maximumBit`',
                 '使 `nums` 全部异或再异或 `k` 最大，然后删掉末尾元素，重复 n 次',
                 '示例：`nums=[0,1,1,3], maximumBit=2` → `[0,3,2,3]`'],
        quote='每一轮最终的目标就是maximumBit个1，在十进制表示下就是target = 2^maximumBit - 1。由于每一轮都可以自由控制k的大小，因此每一轮都必然可以让结果成为target。',
        quote_src='—— yiduobo 题解',
        idea=['`nums[0]^...^nums[n-index]^k = target`，所以 `k = target ^ 前缀异或`',
              '每轮是从后往前删，前缀越来越短',
              '倒过来：前缀异或正着累积，边算边记 k，最后 `reverse`'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计答案）',
                 '`k` 一定能取到：它最多 `maximumBit` 位，且 `target ^ now` 不会超出范围',
                 '易错：答案顺序要翻转；`target = (1 << maximumBit) - 1`'],
    ),
)
