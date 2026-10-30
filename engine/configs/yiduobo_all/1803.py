def _bn(S):
    return S.get('binary_now')


def _info(S):
    if 'root' not in S:
        return '把 `[low, high]` 拆成「异或值 ≤ high」减「异或值 ≤ low−1」，每个数都用 15 位二进制表示'

    def cnt(n):
        return '无' if n is None else f'cnt = =={n.cnt}=='
    s = f'trie 里已有 =={S["root"].cnt}== 个数'
    if 'p_high' in S and 'p_low' in S:
        s += f'；`p_high`：{cnt(S["p_high"])}，`p_low`：{cnt(S["p_low"])}'
    return s


CONFIG = dict(
    num=1803, title='统计异或值在范围内的数对有多少', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='差分 + 01 字典树逐位统计',
    tags=['灵神题单·位运算', '难度分 2479'],
    code='''
class Node(object):

    def __init__(self):
        self.sons = [None, None]
        self.cnt = 0

class Solution(object):
    def countPairs(self, nums, low, high):

        pow2 = [1]
        for index in range(14):
            pow2.append(pow2[-1] + pow2[-1])

        low -= 1
        binary_low = [0] * 15
        binary_high = [0] * 15 
        for index in range(14, -1, -1):
            if low >= pow2[index]:
                binary_low[index] = 1
                low -= pow2[index]
            if high >= pow2[index]:
                binary_high[index] = 1
                high -= pow2[index]

        root = Node()
        res = 0
        nums = sorted(nums)
        for num in nums:
            binary_now = [0] * 15
            for index in range(14, -1, -1):
                if num >= pow2[index]:
                    binary_now[index] = 1
                    num -= pow2[index]
            
            p_low = root
            p_high = root
            for index in range(14, -1, -1):
                if p_high and p_high.cnt > 0:
                    same_son = binary_high[index] ^ binary_now[index]
                    other_son = 1 ^ same_son
                    if binary_high[index] == 1 and p_high.sons[other_son]:
                        res += p_high.sons[other_son].cnt
                    p_high = p_high.sons[same_son]

                if p_low and p_low.cnt > 0:
                    same_son = binary_low[index] ^ binary_now[index]
                    other_son = 1 ^ same_son
                    if binary_low[index] == 1 and p_low.sons[other_son]:
                        res -= p_low.sons[other_son].cnt
                    p_low = p_low.sons[same_son]
            
            if p_high:
                res += p_high.cnt
            if p_low:
                res -= p_low.cnt

            tree = root
            for index in range(14, -1, -1):
                tree.cnt += 1
                if tree.sons[binary_now[index]] is None:
                    tree.sons[binary_now[index]] = Node()
                tree = tree.sons[binary_now[index]]

            tree.cnt += 1

        return res
''',
    call='Solution().countPairs([1, 3], 1, 2)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（已排序后遍历）', cell=70, h=150),
        dict(type='array', var='binary_high', label='binary_high（high 的 15 位，下标 = 位权）', cell=44, h=130,
             pointers={'index': 'blue'}),
        dict(type='array', var='binary_now', label='binary_now（当前数的 15 位）', cell=44, h=130,
             pointers={'index': 'blue'}),
        dict(type='text', h=100, size=26, fn=_info),
    ],
    watch=[('index', 'index', 'blue'), ('low', 'low', 'cyan'), ('res', 'res', 'green')],
    captions={
        14: '`low -= 1`：要数的是「异或值 ≤ `{low}`」（原来的 low − 1）',
        15: '`binary_low`：limit = `{low}` 的 15 位二进制（稍后填好）',
        16: '`binary_high`：`high = {high}` 的 15 位二进制（稍后填好）',
        25: '建一棵空 trie：根节点 `cnt = 0`，两条边 `sons[0]` / `sons[1]` 都为空。这时 `binary_low`、`binary_high` 已按位填好',
        26: '`res` 累计「≤ high 的对数 − ≤ low−1 的对数」',
        27: '先排序：`{nums}`，更小的数在高位上更早被淘汰',
        28: lambda S, B, r: (f'取下一个数 `{S.num}`' if S.root.cnt < len(S.nums) else '数都遍历完了'),
        29: '`binary_now`：把这个数转成 15 位二进制（下标 = 位权）',
        35: lambda S, B, r: f'`binary_now` 把数转成 15 位二进制（下标 = 位权）：当前数  `{sum(b << i for i, b in enumerate(S.binary_now))}` = `{"".join(map(str, reversed(S.binary_now)))}`；`p_low`、`p_high` 从根出发，沿 trie 往下走',
        36: '`p_high` 沿 trie 往下走，统计之前的数里和当前数异或后 ≤ high 的个数',
        42: lambda S, B, r: f'第 {S.index} 位：`high` 这位是 1，另一个儿子（异或这位取 0 → ==必小于 high==）整棵子树都算：`res += {S.p_high.sons[1 ^ (S.binary_high[S.index] ^ S.binary_now[S.index])].cnt if S.p_high else 0}`' if False else f'第 {S.index} 位：`high` 这位是 1，异或取 0 的那一支整棵子树都 ==小于 high==，`res` 加上它的 cnt → `res = {S.res}`',
        43: lambda S, B, r: f'第 {S.index} 位：`p_high` 走向异或后与 high 相同的儿子' + ('' if S.p_high is not None else '（没有这个儿子 → None）'),
        49: lambda S, B, r: f'第 {S.index} 位：`low−1` 这位是 1，异或取 0 的那一支整棵子树都 ==小于 limit==，`res` 减去它的 cnt → `res = {S.res}`',
        50: lambda S, B, r: f'第 {S.index} 位：`p_low` 走向异或后与 limit 相同的儿子' + ('' if S.p_low is not None else '（没有这个儿子 → None，后面不用再统计）'),
        52: lambda S, B, r: ('走到底了：异或值和 high ==完全相同== 的情况，加上终点的 cnt' if S.p_high is not None and S.p_high.cnt > 0
                             else ('trie 还是空的，`p_high` 停在根，cnt = 0，加 0' if S.p_high is not None else '`p_high` 已经是 None：没有异或值恰好等于 high 的数，不加')),
        53: '`res += p_high.cnt` → `res = {res}`',
        54: lambda S, B, r: ('`p_low` 走到底：异或值恰好等于 low−1 的也属于「≤ low−1」，要减掉' if S.p_low is not None and S.p_low.cnt > 0
                             else ('trie 为空，减 0' if S.p_low is not None else '`p_low` 是 None：没有数和当前数异或恰为 low−1，不减')),
        55: '`res -= p_low.cnt` → `res = {res}`',
        57: '查询完毕，现在把当前数插入 trie：从根开始，每经过一个节点 `cnt += 1`，缺少的儿子就新建',
        64: lambda S, B, r: f'插入完成：trie 现在有 {S.root.cnt} 个数；当前数的终点节点 `cnt = {S.tree.cnt}`',
        66: '`res` = ≤ high 的对数 − ≤ low−1 的对数 = `{res}`',
    },
    skip=[15, 16, 26, 29, 36, 4, 5, 10, 11, 12, 17, 18, 19, 20, 21, 22, 23, 30, 31, 32, 33, 37, 38, 39, 40, 41, 45, 46, 47, 48, 58, 59, 60, 61, 62],
    max_steps=130,
    cards=dict(
        one_liner='异或值 ≤ high 的对数，减去 ≤ low−1 的对数',
        complexity='时间 `O(n·15)`，空间 `O(n·15)`',
        problem=['数对 `(i, j)`，`i < j`，`low ≤ nums[i] xor nums[j] ≤ high`，求个数',
                 '示例：`nums = [1,4,2,7]`，`low = 2`，`high = 6` → `6`',
                 '本视频：`[1,3]`，`low = 1`，`high = 2` → `1`（1 xor 3 = 2）'],
        quote='一个经典的转化就是分别求出异或值在[0, high]之间的数对数量，以及异或值在[0, low - 1]内的数对数量，然后用前者减去后者就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['2^15 = 32768 > 20000，所有数和异或结果都能用 15 位表示',
              '从高位往下和 limit 比：limit 这位是 1，且异或这位取 0 的数全部算上',
              '用 trie 记录每个前缀有几个数，一步就能数出一批'],
        summary=['时间、空间都是 `O(15n)`',
                 '`limit` 某位为 1 时，这位异或为 0 的子树整体加入；一路走到底时再加上完全相等的 `cnt`',
                 '先把 `low − 1` 当 limit，所以代码开头有 `low -= 1`',
                 '先 `sorted(nums)` 是作者提到的小技巧，复杂度不变，原文代码为 Python 2 风格但无需改动'],
    ),
)
