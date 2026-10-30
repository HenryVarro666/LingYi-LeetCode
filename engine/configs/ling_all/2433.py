CONFIG = dict(
    num=2433, title='找出前缀异或的原始数组', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='异或差分（相邻两两异或）',
    tags=['异或的性质', '难度分 1367'],
    code='''
class Solution:
    def findArray(self, pref: List[int]) -> List[int]:
        return [pref[0]] + [x ^ y for x, y in pairwise(pref)]
''',
    call='Solution().findArray([5,2,0,3,1])',
    expect=[5, 7, 2, 3, 2],
    views=[
        dict(type='array', var='pref', label='pref（前缀异或）', cell=90, h=170),
        dict(type='array', var=lambda S: [S['pref'][0]] + [x ^ y for x, y in zip(S['pref'], S['pref'][1:])] if 'pref' in S else None,
             label='arr = pref[0] 接上相邻两项异或', cell=90, h=170,
             color=lambda S, i, v: 'green'),
        dict(type='text', fn=lambda S: '`arr[i] = pref[i-1] ^ pref[i]`：`5^2=7`，`2^0=2`，`0^3=3`，`3^1=2`' if 'pref' in S else '', size=26, h=110),
    ],
    watch=[('pref', 'pref')],
    captions={
        'return': '`arr[0] = pref[0] = {pref[0]}`，后面每项 `arr[i] = pref[i-1] ^ pref[i]`：前缀异或的差分就是原数组 → =={ret}==',
    },
    cards=dict(
        one_liner='前缀异或的「差分」就是原数组：相邻两项异或',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['`pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]`，已知 `pref`，还原 `arr`',
                 '示例：`pref = [5,2,0,3,1]` → `arr = [5,7,2,3,2]`'],
        quote='问题本质上是给你前缀和，还原回原数组。由于前缀和的差分是原数组，因此直接两两异或即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把异或看成「不进位的加法」：`pref` 就是 `arr` 的前缀和',
              '前缀和的差分是原数组；异或的逆运算是它自己',
              '所以 `arr[i] = pref[i-1] ^ pref[i]`，首项照抄'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计返回值）',
                 '`pairwise(pref)` 产生相邻对 `(pref[i-1], pref[i])`',
                 '易错：别忘了首项 `pref[0]` 要单独放在最前面',
                 '同类：差分与前缀和互为逆运算，异或里 `x ^ x = 0`'],
        after=[dict(heading='验证一下', lines=['`5 ^ 7 = 2`，等于 pref[1]', '`5 ^ 7 ^ 2 = 0`，等于 pref[2]', '`5 ^ 7 ^ 2 ^ 3 = 3`，等于 pref[3]', '逐项还原，每一步都对得上'])],
    ),
)
