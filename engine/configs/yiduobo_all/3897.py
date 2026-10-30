N1, N0 = [1, 3, 1, 2], [1, 0, 3, 0]

CONFIG = dict(
    num=3897, title='连接二进制片段得到的最大值', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='全 1 先放 + 排序 + 逐位累乘',
    tags=['灵神题单', '贪心与思维', '难度分 1998'],
    code='''
class Solution(object):
    def maxValue(self, nums1, nums0):
        
        other = []
        final = []
        for v1, v0 in zip(nums1, nums0):
            if v0 == 0:
                final.extend([1] * v1)
            else:
                other.append((v1, v0))
        
        other.sort(key=lambda d:(-d[0], d[1]))
        for v1, v0 in other:
            final.extend([1] * v1)
            final.extend([0] * v0)
        
        res = 0
        mod = 10 ** 9 + 7
        for v in final:
            res = res + res + v
            if res >= mod:
                res -= mod
        
        return res
''',
    call=f'Solution().maxValue({N1}, {N0})',
    expect=2024,
    views=[
        dict(type='array', var='nums1', label='nums1', h=130),
        dict(type='array', var='nums0', label='nums0', h=130),
        dict(type='text', fn=lambda S: 'other = ' + ' '.join(f'({a},{b})' for a, b in S['other']) if 'other' in S else '', size=30, h=70),
        dict(type='array', var='final', label='final（最终二进制数的每一位）', cell=44,
             color=lambda S, i, v: 'green' if v == 1 else None, h=170),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" if 'res' in S else '', size=30, h=70),
    ],
    watch=['v1', 'v0', 'v', ('res', 'res', 'green')],
    captions={
        'for v in final': '取下一位 `v = {v}`',
        'for v1, v0 in zip': '取下一个片段：`{v1}` 个 1、`{v0}` 个 0',
        'for v1, v0 in other': '按排好的顺序取片段：`{v1}` 个 1、`{v0}` 个 0',
        'if v0 == 0': '`v0 = {v0}`？没有 0 的全 1 片段 ==直接放最高位==' ,
        'final.extend([1] * v1)': '把 `{v1}` 个 1 追加到 `final`',
        'other.append': '带 0 的片段先存进 `other`，稍后排序：`{v1}` 个 1、`{v0}` 个 0',
        'other.sort': '排序：==1 多的在前==；1 一样多则 ==0 少的在前==（`110 1100` 优于 `1100 110`，第二段 1 更靠前）',
        'final.extend([0] * v0)': '紧接着追加 `{v0}` 个 0',
        'res = res + res + v': '从高位到低位：`res = 2×res + {v}` = =={res}==（相当于左移再加当前位）',
        'if res >= mod': lambda S, B, r: f'`{S.res} >= {S.mod}`？' + ('超了，下一行减掉 mod' if S.res >= S.mod else '没超，继续'),
        'res -= mod': '减去 `mod`，`res` = {res}',
    },
    cards=dict(
        one_liner='先造出整个二进制数，再逐位 ×2 + 当前位',
        complexity='时间 `O(n log n + L)`，空间 `O(L)`（L 为总位数）',
        problem=['`nums1[i]` 个 1 后跟 `nums0[i]` 个 0 组成一个片段，可任意重排后拼接',
                 '求拼出的二进制数最大值，对 `10^9+7` 取余',
                 f'示例：`nums1={N1}`，`nums0={N0}`'],
        quote='对于非全1的片段，应该按照1的数量倒序为第一关键字，0的数量正序为第二关键字进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['两片段拼接长度相同，所以高位要尽量多 1',
              '全 1 片段无条件放最前；其余按「1 多优先，0 少优先」',
              '总位数不超过 `2×10^5`，直接造出位数组，再秦九韶式从高位累乘'],
        summary=['时间 `O(n log n + L)`，空间 `O(L)`',
                 '易错：0 一样多时不是随意；必须让中间的 0 尽量少',
                 '取模只做减法：`res < mod` 时 `2res + v < 2mod`，减一次就够',
                 '对比灵神：灵神不造字符串，用 `2^k` 公式一次接整段'],
    ),
)
