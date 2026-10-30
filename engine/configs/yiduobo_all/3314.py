def _bits(S):
    if 'v' not in S:
        return ''
    v = S['v']
    ln = S['_line']
    if len(S['res']) == len(S['nums']):
        return '全部处理完'
    if ln in (14, 15, 16, 17):
        return f'拼答案：当前 `v` = `{bin(v)[2:]}`（{v}），低位连续 1 共 `cnt` = =={S["cnt"]}== 个'
    return f'`v` = `{bin(v)[2:]}`（{v}）' + (f'，已数出低位连续的 1：`cnt` = =={S["cnt"]}==' if 'cnt' in S and ln >= 9 else '')


CONFIG = dict(
    num=3314, title='构造最小位运算数组 I', difficulty='Easy', category='位运算',
    author='yiduobo', technique='低位连续 1 · 最高位的 1 变 0',
    tags=[],
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
    call='Solution().minBitwiseArray([2, 3, 5, 7, 11, 13])',
    expect=[-1, 1, 4, 3, 9, 12],
    views=[
        dict(type='text', fn=_bits, size=26, h=60),
        dict(type='array', var='nums', h=170, pointers={'len(res)': 'blue'}, label='nums（蓝箭头 = 当前处理的位置）'),
        dict(type='array', var='res', h=170, label='res（已算出的答案）', color=lambda S, i, x: 'green' if x != -1 else 'red'),
    ],
    watch=[('v', 'v', 'blue'), ('cnt', 'cnt', 'orange')],
    captions={
        'res = []': '`res` 收集每个数对应的最小 `ans`',
        'for v in nums': lambda S, B, r: ('nums 遍历完了' if len(S.res) == len(S.nums) else f'取下一个质数 `v = {S.v}`（二进制 `{bin(S.v)[2:]}`）'),
        'if v == 2': lambda S, B, r: ('`2 = 10`，最低位是 0：ans 与 ans+1 按位或的最低位必为 1 → ==无解== ' if S.v == 2
                                      else f'`v = {S.v}` 是奇数（质数里只有 2 是偶数）→ 有解，看低位连续的 1'),
        'res.append(-1)': '2 是偶数，==无解== → 放入 `-1`',
        'cnt = 0': '`cnt`：低位连续 1 的个数',
        'while v & 1': lambda S, B, r: (f'`v = {S.v}`（`{bin(S.v)[2:]}`）最低位是 1 → 继续数' if S.v & 1 else f'`v = {S.v}`（`{bin(S.v)[2:]}`）最低位是 0 → 低位的连续 1 数完了，共 `{S.cnt}` 个'),
        'cnt += 1': '`cnt` = {cnt}',
        'v >>= 1': '右移一位去掉最低位 → `v = {v}`（`{bin(v)[2:]}`）',
        14: '先左移一位：给==最高位的那个 1 变成的 0==留出位置，`v = {v}`',
        'for _ in range': '后面还要补回 `cnt - 1 = {cnt - 1}` 个 1（低位连续 1 里除最高位外的其余几个）',
        16: '左移一位，腾出最低位 → `v = {bin(v)[2:]}`',
        'v |= 1': '最低位置 1 → `v = {bin(v)[2:]}`（{v}）',
        'res.append(v)': '得到最小的 `ans = {v}`（二进制 `{bin(v)[2:]}`）',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='把 nums[i] 低位连续 1 中最高的那个 1 变成 0',
        complexity='时间 `O(n log U)`，空间 `O(1)`（`U` 为数值上限）',
        problem=['质数数组 `nums`，求每个位置最小的 `ans[i]`，使 `ans[i] OR (ans[i]+1) == nums[i]`，无解为 `-1`',
                 '示例：`[2,3,5,7]` → `[-1,1,4,3]`',
                 '本视频：`[2,3,5,7,11,13]` → `[-1,1,4,3,9,12]`'],
        quote='当nums[i]为奇数时，为了使得答案最小，就应该让nums[i]低位连续的1中最高位的那个变为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x` 是奇数时写成 `X..X0111`，`x+1` 是 `X..X1000`，两者按位或 = `X..X1111`',
              '所以 nums[i] 的低位连续 1 里，任意一个变成 0 都是解；==变最高的那个最小==',
              '质数里只有 2 是偶数：低位是 `10`，或的最低位必为 1，无解'],
        summary=['时间 `O(n log U)`：每个数最多数一遍二进制位',
                 '易错：`for _ in range(cnt - 1)` 补回的是被右移掉的 `cnt - 1` 个 1，不是 cnt 个',
                 '先右移数出 cnt，再左移一位（腾出的 0），再补 cnt-1 个 1',
                 '原文已是 Python 3 可运行写法，代码未做修改'],
    ),
)
