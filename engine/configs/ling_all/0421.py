def _b(S, k):
    return format(S[k], '05b') if k in S else '-----'


def _hit(S):
    return 'x' in S and 'new_ans' in S and (S['new_ans'] ^ S['x']) in S.get('seen', set())


CONFIG = dict(
    num=421, title='数组中两个数的最大异或值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='试填法 + 哈希表（两数之和）',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构', '难度分 2000'],
    code='''
class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        ans = mask = 0
        high_bit = max(nums).bit_length() - 1
        for i in range(high_bit, -1, -1):  # 从最高位开始枚举
            mask |= 1 << i
            new_ans = ans | (1 << i)  # 这个比特位可以是 1 吗？
            seen = set()
            for x in nums:
                x &= mask  # 低于 i 的比特位置为 0
                if new_ans ^ x in seen:
                    ans = new_ans  # 这个比特位可以是 1
                    break
                seen.add(x)
        return ans
''',
    call='Solution().findMaximumXOR([3, 10, 5, 25, 2, 8])',
    expect=28,
    views=[
        dict(type='array', var='nums', h=165, label='nums', cell=90),
        dict(type='text', size=34, fn=lambda S: f"`ans     = {_b(S, 'ans')}`" if 'ans' in S else ''),
        dict(type='text', size=34, fn=lambda S: f"`mask    = {_b(S, 'mask')}`   `new_ans = {_b(S, 'new_ans')}`" if 'new_ans' in S else (f"`mask    = {_b(S, 'mask')}`" if 'mask' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"`x & mask = {format(S['x'], '05b')}`   `new_ans ^ x = {format(S['new_ans'] ^ S['x'], '05b')}` " + ('==在 seen 里！==' if _hit(S) else '不在 seen')) if 'x' in S and 'new_ans' in S and S['x'] < 32 else ''),
        dict(type='set', var='seen', h=170, label='seen（x & mask 的集合）', fmt=lambda x: f'{x:b}', font=30),
    ],
    watch=[('i', 'i', 'cyan'), ('x', 'x', 'pink'), ('ans', 'ans', 'green'), ('mask', 'mask', 'blue'), ('new_ans', 'new_ans', 'yellow')],
    captions={
        'ans = mask = 0': '`ans` 从 0 开始逐位试填，`mask` 记录已经看过的高位',
        'high_bit =': '最大数 `{max(nums)}` 的二进制长度减一 = `{high_bit}`：更高位异或必为 0，不用试',
        'for i in range': lambda S, B, r: (f'==从最高位开始==，试第 `{S.i}` 位能不能是 1（高位权重大于所有低位之和）' if not (S.i == 0 and B.i == 0) else '每一位都试完了，退出循环'),
        'mask |= ': '`mask` 加入第 `{i}` 位：只看高于等于 `{i}` 的比特位 = `{mask:b}`',
        'new_ans =': '假设这一位可以是 1：`new_ans = {new_ans:b}`（带着已填好的高位）',
        'seen = set()': '清空 `seen`，判断「能否选出两个数异或等于 new_ans」',
        'for x in nums': lambda S, B, r: (f'枚举 `b = {S.x}`' if S.x != B.x or S.x not in S.nums[-1:] else '扫完了一遍：没有一对满足 → 这一位只能是 0，`ans` 不变'),
        'x &= mask': '把低于第 `{i}` 位的比特置 0：`x = {x:b}`',
        'if new_ans ^ x in seen': lambda S, B, r: (f'`a ^ b = new_ans` ⇒ `a = new_ans ^ b` = `{S.new_ans ^ S.x:b}`：在 seen 里 → ==存在一对==' if (S.new_ans ^ S.x) in S.seen else f'`new_ans ^ x` = `{S.new_ans ^ S.x:b}` 不在 seen（像两数之和，还没遇到另一半）'),
        'ans = new_ans': '找到了：这一位可以是 1，`ans = {ans:b}`',
        'break': '这一位已经确定，不用再扫，去试下一位',
        'seen.add(x)': '把 `{x:b}` 放进 `seen`，等后面的数来配对',
        'return': '逐位试填完成：最大异或 `{ans}`（5 ^ 25 = 28）',
    },
    max_steps=66,
    cards=dict(
        one_liner='从高位往低位试填：这一位能是 1 吗？用「两数之和」判断',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，返回 `nums[i] XOR nums[j]` 的最大值',
                 '示例：`[3,10,5,25,2,8]` → `28`（`5 XOR 25`）'],
        quote='设 newAns = ans + 2^i，看能否从 nums 中选两个数（低于 i 的比特位当作 0），满足这两个数的异或和等于 newAns。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案越大越好 → ==高位优先==，一位一位试填 1',
              '判断「两数异或 = new_ans」：`a ^ b = new_ans` ⇒ `a = new_ans ^ b`，把减法换成异或的两数之和',
              '`ans` 继承了高位的 1，所以后面的判断也要满足之前的高位'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '==不能从最低位开始==：低位大了，高位可能就只能是 0',
                 '`x &= mask` 让低位清零，只比较「已确定的前缀」',
                 '同类：0-1 字典树解法（题单 6.4），本题用哈希表更短'],
    ),
)
