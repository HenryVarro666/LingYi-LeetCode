def _b(x):
    return format(x, 'b') if x >= 0 else str(x)


def _fn(S):
    if 'v' not in S:
        return ''
    s = f"v = `{_b(S['v'])}`（{S['v']}）"
    if 'cnt' in S:
        s += f"　低位连续 1 的个数 `cnt` = =={S['cnt']}=="
    return s


CONFIG = dict(
    num=3315, title='构造最小位运算数组 II', difficulty='Medium', category='位运算',
    author='yiduobo', technique='数低位连续 1，把其中最高的 1 变 0',
    tags=['灵神题单·位运算', '难度分 1715'],
    code='''
class Solution(object):
    def minBitwiseArray(self, nums):

        res = []
        for v in nums:
            if v == 2:
                res.append(-1)
            else:
                cnt = 0
                while v & 1:
                    cnt += 1
                    v >>= 1
                
                v <<= 1
                for _ in range(cnt - 1):
                    v <<= 1
                    v |= 1
                
                res.append(v)
        
        return res
''',
    call='Solution().minBitwiseArray([2,5,11,13])',
    expect=[-1, 4, 9, 12],
    views=[
        dict(type='text', fn=_fn, size=30, h=90),
        dict(type='array', var='nums', label='nums（输入）', h=170),
        dict(type='array', var='res', label='res（已构造的答案）', h=170),
    ],
    watch=[('v', "S.get('v')", 'blue'), ('cnt', "S.get('cnt')", 'orange'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 收集每个位置的答案',
        'for v in nums': lambda S, B, r: (f'取出 `v = {S.v}`，二进制 `{format(S.v, "b")}`' if len(S.res) < len(S.nums) else '所有数都处理完了，退出循环'),
        'if v == 2': lambda S, B, r: ('`v = 2` 是偶数：`ans OR (ans+1)` 末位必为 1，凑不出 → ==无解==' if S.v == 2 else f'`v = {S.v}` 是奇数，有解'),
        'res.append(-1)': '无解：加入 `-1`',
        'cnt = 0': '数一数低位连续有多少个 1',
        'while v & 1': lambda S, B, r: (f'末位是 1，继续统计（`v` = `{format(S.v, "b")}`）' if S.v & 1 else f'末位是 0：低位连续的 1 共 =={S.cnt}== 个，统计完毕'),
        'cnt += 1': '又一个连续的 1：`cnt` = {cnt}',
        'v >>= 1': '右移丢掉这个 1：`v` = `{format(v, "b")}`',
        14: '先左移一位，末位补 0：这个 0 的位置就是原来低位连续 1 的==最高位==（变成 0 的那一位）：`v` = `{format(v, "b")}`',
        'for _ in range': '剩下的 `cnt - 1` = {cnt - 1} 个 1 要补回来（每次左移再补 1）',
        16: '腾出一位：`v` = `{format(v, "b")}`',
        'v |= 1': '低位补回 1：`v` = `{format(v, "b")}`（共补回 cnt−1 个 1）',
        'res.append(v)': '这个数的答案是 =={v}==，加入 `res`',
        'return res': '全部完成：`{res}`',
    },
    cards=dict(
        one_liner='低位连续 1 里，把最高的那个 1 变成 0 最小',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['给质数数组 `nums`，对每个 `nums[i]` 找最小的 `ans[i]`',
                 '满足 `ans[i] OR (ans[i]+1) == nums[i]`，找不到填 `-1`',
                 '示例：`[2,3,5,7]` → `[-1,1,4,3]`'],
        quote='当nums[i]为奇数时，为了使得答案最小，就应该让nums[i]低位连续的1中最高位的那个变为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数 `x = ...0111..1`，`x+1 = ...1000..0`，或起来得到 `...1111..1`',
              '所以 `nums[i]` 低位连续的 1 里，任意一个变 0 都是可行解',
              '要最小就变最高的那个；`2` 是偶数，一定无解'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '先数出低位连续 1 的个数 `cnt`，再把最高那位变 0、剩下 `cnt-1` 位补回 1',
                 '`v` 被移位后已不是原值，重建时要把剩下的 1 补回去',
                 '对比灵神的 `x ^= (~x & -~x) >> 1`：思路相同，灵神一步到位'],
    ),
)
