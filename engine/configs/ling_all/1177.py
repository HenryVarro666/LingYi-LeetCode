S0, Q0 = 'abcda', [[3, 3, 0], [1, 2, 0], [0, 3, 1], [0, 3, 2], [0, 4, 1]]


def _b(x):
    return format(x, '04b')


def _mask_txt(S):
    if 'sum' not in S:
        return ''
    if 'right' not in S or 'k' not in S:
        return '`sum[i]` = 前 i 个字母的奇偶性（4 位，从右到左 a b c d），1 = 奇数次'
    l, r, k = S['left'], S['right'], S['k']
    x = S['sum'][l] ^ S['sum'][r + 1]
    m = bin(x).count('1')
    return f'`{_b(S["sum"][l])} ^ {_b(S["sum"][r + 1])} = {_b(x)}`：{m} 种字母奇数次 → 需改 `{m}//2 = {m // 2}` 个，k = {k}'


CONFIG = dict(
    num=1177, title='构建回文串检测', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='异或前缀和 + 位运算',
    tags=['前缀和', '状态压缩前缀和', '难度分 1848'],
    code='''
class Solution:
    def canMakePaliQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        sum = [0]
        for c in s:
            bit = 1 << (ord(c) - ord('a'))
            sum.append(sum[-1] ^ bit)  # 该比特对应字母的奇偶性：奇数变偶数，偶数变奇数

        ans = []
        for left, right, k in queries:
            m = (sum[left] ^ sum[right + 1]).bit_count()
            ans.append(m // 2 <= k)
        return ans
''',
    call=f'Solution().canMakePaliQueries({S0!r}, {Q0!r})',
    expect=[True, False, False, True, True],
    views=[
        dict(type='string', var='s', label='s（框 = 当前询问的子串 [left, right]）', cell=90, h=130,
             window=('left', 'right')),
        dict(type='array', var='sum', label='sum（异或前缀和）', cell=90, h=230,
             pointers={'left': 'blue', 'right + 1': 'pink'}),
        dict(type='text', h=90, size=26, fn=_mask_txt),
        dict(type='array', var='ans', label='ans', cell=90, h=130,
             color=lambda S, i, v: 'green' if v else 'pink'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('k', 'k', 'yellow'), ('m', 'm', 'orange')],
    captions={
        'sum = [0]': '`sum[0] = 0`：空前缀，所有字母都出现 0 次（偶数）',
        'for c in s': lambda S, B, ret: (f'处理字母 `{S.c}`' if 'c' in S and 'bit' not in S or S.get('c') != B.get('c') else '字母处理完毕，开始回答询问'),
        'bit = 1 <<': '字母 `{c}` 对应第 `{ord(c) - 97}` 位：`bit = {bit:04b}`',
        'sum.append': '`{sum[-2]:04b} ^ {bit:04b} = {sum[-1]:04b}`：==只翻转 {c} 的奇偶性==，其它字母不变',
        'for left, right, k': lambda S, B, ret: ('所有询问处理完毕' if B.get('left') == S.left and B.get('right') == S.right and B.get('k') == S.k and 'm' in B
                                                 else f'询问 `[{S.left}, {S.right}, {S.k}]`：子串 `{S.s[S.left:S.right + 1]}`，最多改 {S.k} 个'),
        'm = (sum': '`sum[{left}] ^ sum[{right + 1}]` = `{sum[left] ^ sum[right + 1]:04b}`：相同的位抵消，==剩下的 1 就是子串里奇数次的字母==，共 `m = {m}` 种',
        'ans.append': lambda S, B, ret: (f'`m // 2 = {S.m // 2} <= k = {S.k}` → ==成立==：每改一个字母可以消掉两种奇数次字母'
                                         if S.m // 2 <= S.k else f'`m // 2 = {S.m // 2} > k = {S.k}` → ==不成立==：改的次数不够'),
        'return ans': '返回所有询问的结果 `{ans}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='只记每个字母出现次数的奇偶性：一个二进制数就够了',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['每次询问 `[left, right, k]`：子串可以==重新排列==，并最多替换 `k` 个字母',
                 '问能否变成回文串',
                 '示例：`s = "abcda"`，5 个询问 → `[true,false,false,true,true]`'],
        quote='如果有 m 种字母出现奇数次，只需修改其中 ⌊m/2⌋ 个字母。换句话说，如果第 i 次询问有 ⌊m/2⌋ ≤ k，那么 answer[i] 为真，反之为假。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能重排 → 偶数次的字母成对放两侧；奇数次的字母各多出一个',
              '多出的一个可以放中心，其余每两个奇数字母改一个就配对',
              '只关心奇偶 → 前缀和 `+` 换成 `^`，26 个计数压成一个整数'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '`sum[right + 1] ^ sum[left]` 是左闭右开前缀，下标别错一位',
                 '`m // 2` 向下取整：m 为奇数时有一个字母可放中心',
                 '灵神先写 26 个数组的前缀和，再改成 0/1 数组、异或、最后压成二进制数',
                 '`int.bit_count()` 需要 Python 3.10+，同类题：1371、1542、1915'],
    ),
)
