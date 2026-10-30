def _bits(S):
    n = S.get('n')
    return bin(n)[2:] if n else None


def _pos(S):
    n, i = S.get('n'), S['_inner'].get('i')
    if n is None or i is None or i < 0:
        return None
    return n.bit_length() - 1 - i


def _fill(S):
    i = S['_inner'].get('i')
    return i


CONFIG = dict(
    num=600, title='不含连续1的非负整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（记忆化搜索）',
    tags=['灵神题单', '数位 DP'],
    code='''
class Solution:
    def findIntegers(self, n: int) -> int:
        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（一行代码实现记忆化）
        def dfs(i: int, pre1: bool, is_limit: bool) -> int:
            if i < 0:
                return 1
            up = n >> i & 1 if is_limit else 1
            res = dfs(i - 1, False, is_limit and up == 0)  # 填 0
            if not pre1 and up == 1:  # 可以填 1
                res += dfs(i - 1, True, is_limit)  # 填 1
            return res
        return dfs(n.bit_length() - 1, False, True)  # 从高位到低位
''',
    call='Solution().findIntegers(5)',
    expect=5,
    views=[
        dict(type='string', var=_bits, label='n = 5 的二进制（从高位往低位填；蓝箭头 = 当前要填的位 i）', cell=64, h=170,
             pointers={_pos: 'blue'}, pointer_labels={_pos: 'i'}),
        dict(type='text', h=60, fn=lambda S: (
            f"第 `{S['_inner']['i']}` 位：`pre1 = {S['_inner']['pre1']}`，`is_limit = {S['_inner']['is_limit']}`"
            + (f"，上限 `up = {S['_inner']['up']}`" if 'up' in S['_inner'] else '')) if 'pre1' in S['_inner'] else ''),
        dict(type='calls', h=300),
    ],
    watch=[('i', "_inner['i']", 'blue'), ('pre1', "_inner['pre1']", 'pink'), ('is_limit', "_inner['is_limit']", 'purple'),
           ('res', "_inner.get('res')", 'green')],
    captions={
        'if i < 0': lambda S, B, r: ('`i < 0`：所有数位都填完了，没有出现连续 1 → ==这是一个合法数字，返回 1==' if S['_inner']['i'] < 0
                                     else '`i >= 0`，还有数位要填，继续'),
        'up = n': lambda S, B, r: (f'`is_limit = True`：还贴着 n 的上界，这一位至多填 n 的第 {S.i} 位 = =={S.up}==' if S.is_limit
                                   else f'`is_limit = False`：前面已经比 n 小，这一位随便填，至多填 =={S.up}=='),
        'res = dfs(i - 1, False': '这一位填 `0` 永远合法：下一位 `pre1 = False`；若这里填的是 up=0 才继续贴着上界 → `is_limit = {is_limit and up == 0}`',
        'if not pre1': lambda S, B, r: (f'`pre1 = {S.pre1}`，`up = {S.up}`：' + ('前一位不是 1 且这位能填 1 → ==可以填 1==' if (not S.pre1 and S.up == 1)
                                        else ('前一位是 1，这位再填 1 就连续了 → ==不能填 1==' if S.pre1 else '上界是 0，填不了 1 → 只有填 0 一条路'))),
        'res += dfs(i - 1, True': '填 `1`：下一位 `pre1 = True`（它不能再填 1），`is_limit` 保持 `{is_limit}`；累加得 `res = {res}`',
        'return res': '这一层的方案数 `res = {res}`，返回给上一层',
        'return dfs(n.bit_length()': '`n.bit_length() - 1` 是最高位的下标；开始从最高位往下填，初始 `is_limit = True`',
    },
    cards=dict(
        one_liner='从高位到低位逐位填 0/1，前一位是 1 就不能再填 1',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['统计 `[0, n]` 中二进制表示里没有连续 1 的整数个数',
                 '示例：`n = 5` → `5`（0~5 中只有 3 = 11 不合法）',
                 '本视频：`n = 5` 是示例 1，答案 `5`'],
        quote='`pre1` 表示前一个比特位是否为 1。如果是 1，则当前比特位不能填 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, pre1, is_limit)`：构造第 `i` 位及之后数位的合法方案数',
              '`is_limit` 为真时第 `i` 位至多填 `n >> i & 1`，否则可以填 1',
              '本题前导零对答案无影响，所以省略了 `is_num`'],
        summary=['时间 `O(log n)`：状态数 `O(log n)`，单个状态 `O(1)`',
                 '`(i, pre1, True)` 在整个递归中至多出现一次，真正被缓存命中的是 `is_limit = False` 的状态',
                 '易错点：填 0 时 `is_limit and up == 0`；填 1 时 `is_limit` 原样传下去',
                 '`is_num` 只在前导零会影响答案时才需要（如要求每个数字出现偶数次）'],
    ),
)
