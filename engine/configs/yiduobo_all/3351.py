def _txt(S):
    if 'v' not in S or 'cnt' not in S:
        return '`left[i]` = 以 `nums[i]` 结尾的好子序列数；`right[i]` = 以它开头的个数'
    v = S['v']
    c = S['cnt']
    if S.get('_line', 0) >= 21 and 'res' in S:
        return f"贡献 = `nums[i] × left[i] × right[i]`；累计 `res` = =={S['res']}=="
    return f"`cnt[{v-1}] + cnt[{v+1}] + 1` = `{c.get(v-1,0)} + {c.get(v+1,0)} + 1`：能接在 `v±1` 结尾的数列后，再加自己"


CONFIG = dict(
    num=3351, title='好子序列的元素之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贡献法 · 左右两遍 DP 个数',
    tags=['灵神题单', '难度分 2086'],
    code='''
class Solution(object):
    def sumOfGoodSubsequences(self, nums):
        
        mod = 10 ** 9 + 7
        n = len(nums)

        left = [1]
        cnt = {nums[0] : 1}
        for v in nums[1:]:
            left.append((cnt.get(v - 1, 0) + cnt.get(v + 1, 0) + 1) % mod)
            cnt[v] = (cnt.get(v, 0) + left[-1]) % mod
        
        right = [1]
        cnt = {nums[-1] :1}
        for v in nums[-2::-1]:
            right.append((cnt.get(v - 1, 0) + cnt.get(v + 1, 0) + 1) % mod)
            cnt[v] = (cnt.get(v, 0) + right[-1]) % mod
        right.reverse()

        res = 0
        for index, v in enumerate(nums):
            res = (res + left[index] * right[index] % mod * v % mod) % mod
        
        return res
''',
    call='Solution().sumOfGoodSubsequences([1,2,1,2])',
    expect=33,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=90,
             pointers={'index': 'pink'}),
        dict(type='array', var='left', label='left[i]：以 nums[i] 结尾的好子序列数', h=170, cell=90),
        dict(type='array', var='right', label='right[i]：以 nums[i] 开头的好子序列数（先倒着填）', h=170, cell=90),
        dict(type='map', var='cnt', label='cnt[v]：目前以 v 结尾的个数', fmt=lambda k, v: f'{k}: {v}', h=110, font=28),
        dict(type='text', h=80, size=26, fn=_txt),
    ],
    watch=[('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'left = [1]': '第一个数只能自己成一个子序列：`left[0] = 1`',
        'left.append': '`left[i]` = `cnt[v-1] + cnt[v+1] + 1` = `{left[-1]}`：接在 `v±1` 结尾的数列后，或单独成一个',
        'cnt[v] = (cnt.get(v, 0) + left[-1])': '以 `{v}` 结尾的个数加上新增的 `{left[-1]}`：`cnt[{v}]` = =={cnt[v]}==',
        'right = [1]': '`right` 和 `left` 对称：从后往前再来一遍，最后一个数 `right = 1`',
        'right.append': '从后往前：`right` 新增 `{right[-1]}` 个以 `{v}` 开头的好子序列',
        'cnt[v] = (cnt.get(v, 0) + right[-1])': '以 `{v}` 开头的个数累加：`cnt[{v}]` = =={cnt[v]}==',
        'right.reverse': '`right` 是倒着填的，翻转后下标和 `nums` 对齐',
        'res = (res': '`nums[{index}]` = {v} 出现在 `left × right` = `{left[index]} × {right[index]}` 个好子序列里 → 贡献 `{v}` × {left[index]*right[index]}，`res` = =={res}==',
        'return res': '所有好子序列的元素和 = `{res}`',
    },
    cards=dict(
        one_liner='共享法：每个数的贡献 = 值 × 包含它的好子序列数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['相邻两数绝对差恰好为 1 的子序列是好子序列，单个元素也算',
                 '求所有好子序列的元素和，对 `10^9+7` 取模',
                 '示例：`[1,2,1]` → `14`；本视频：`[1,2,1,2]` → `33`'],
        quote='对于这类求全体之和的题目，一种常见的思路是共享法。问题就转化成了如何高效计算包含每个nums[index]的好子序列的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['以 `nums[i]` 为分割点：左半是以它结尾的、右半是以它开头的好子序列',
              '包含它的好子序列数 = `left[i] × right[i]`，乘上 `nums[i]` 就是它的贡献',
              '`left` 从左往右 DP，`right` 对称地从右往左 DP，各用一个哈希表 `cnt`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`right` 是倒着 append 的，==要 reverse== 才和下标对齐',
                 '乘法每一步都要取模，避免溢出（Python 不溢出但会变慢）',
                 '对比灵神：灵神直接维护「元素和」f，yiduobo 只数个数再用贡献法乘回去'],
    ),
)
