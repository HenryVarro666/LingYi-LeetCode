CONFIG = dict(
    num=810, title='黑板异或游戏', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='博弈 · 小规模归纳', tags=['位运算', '数学算法'],
    code='''
class Solution(object):
    def xorGame(self, nums):

        s = 0
        for num in nums:
            s ^= num
        
        if s == 0:
            return True
        
        return len(nums) % 2 == 0
''',
    call='Solution().xorGame([1,1,2])',
    expect=False,
    views=[
        dict(type='array', var='nums', label='黑板上的数 nums', h=190, pointers={}),
        dict(type='text', fn=lambda S: (f"异或和 s = =={S['s']}== = `{bin(S['s'])[2:]}`　　数字个数 N = ==" + str(len(S['nums'])) + '==' if 's' in S else ''), h=70),
        dict(type='text', fn=lambda S: ('N 为偶数：先手必胜；N 为奇数：只有 s = 0 先手才胜' if 's' in S else ''), h=70),
    ],
    watch=[('s', 's', 'cyan'), ('N', 'len(nums)', 'blue')],
    captions={
        's = 0': '`s` 记录黑板上所有数的异或和，初始为 0',
        'for num in nums': '依次异或进每个数：当前 `{num}`',
        's ^= num': '`s = {B.s} ^ {num} = {s}`',
        'if s == 0': lambda S, B, r: ('`s = 0`：先手一开始就赢（按规则，轮到谁时异或为 0，谁赢）' if S.s == 0
                                      else f'`s = {S.s} ≠ 0`：看数字个数 N 的奇偶'),
        'return True': '先手直接获胜',
        'return len(nums) % 2 == 0': lambda S, B, r: (f'`N = {len(S.nums)}`：' + ('偶数 → 先手必胜' if len(S.nums) % 2 == 0 else '奇数且 s ≠ 0 → 先手必败（后手必胜）') + f'，返回 =={r}=='),
    },
    cards=dict(
        one_liner='异或和为 0 先手赢；否则 N 偶数先手赢，N 奇数先手输',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['黑板上写着数组 `nums`，Alice 先手，两人轮流擦掉一个数',
                 '擦完后若黑板所有数异或为 0，擦的人输；若轮到某人时异或已为 0，该人赢',
                 '双方最优，问 Alice 是否获胜。示例：`[1,1,2]` → `false`'],
        quote='通过上面的分析可以发现，当N为偶数时，先手必胜；当N为奇数时，若初始局面所有数异或值为0，那么先手必胜，否则后手必胜。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 N=1、2、3、4 的小情况入手找规律',
              '偶数 N、异或和 `S≠0`：若每个选择都必败，则 `S^X[i]=0` 共 N 个式子相异或，推出 `S=0`，矛盾',
              '所以偶数 N 先手总能留下异或和非 0 的局面，必胜'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先判 `s == 0`，再看奇偶',
                 '证明用反证法：假设必败，把所有“必败”式子异或',
                 '本例 `[1,1,2]`：`s = 2 ≠ 0` 且 N=3 为奇数 → `False`'],
    ),
)
