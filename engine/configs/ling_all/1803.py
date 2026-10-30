def _bits(S):
    if 'high' not in S:
        return '把「异或值在 `[low, high]`」拆成两个前缀问题：`< high+1` 减去 `< low`'
    h, l = S['high'], S['low']
    return (f'`high = {h}`（二进制 `{h:b}`），`low = {l}`（二进制 `{l:b}`）；'
            f'每轮把 cnt 的键和 low、high 一起右移一位，只比较剩下的前缀')


CONFIG = dict(
    num=1803, title='统计异或值在范围内的数对有多少', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='自底向上的字典树 · 逐比特哈希表',
    tags=['灵神题单·位运算', '难度分 2479'],
    code='''
class Solution:
    def countPairs(self, nums: List[int], low: int, high: int) -> int:
        cnt = Counter(nums)
        ans = 0
        high += 1
        while high:
            nxt = Counter()
            for x, c in cnt.items():
                if high & 1: ans += c * cnt[x ^ (high - 1)]
                if low & 1:  ans -= c * cnt[x ^ (low - 1)]
                nxt[x >> 1] += c
            cnt = nxt
            low >>= 1
            high >>= 1
        return ans // 2
''',
    call='Solution().countPairs([1, 4, 2, 7], 2, 6)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=170),
        dict(type='map', var='cnt', label='cnt（当前保留的高位前缀 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='map', var='nxt', label='nxt（右移一位后的下一轮 cnt）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='text', h=110, size=26, fn=_bits),
    ],
    watch=[('low', 'low', 'blue'), ('high', 'high', 'pink'), ('x', 'x', 'orange'), ('c', 'c', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter(nums)': '先统计每个数出现的次数：`{dict(cnt)}`',
        'ans = 0': '`ans` 累计「异或值 < high+1」的有序对数 − 「异或值 < low」的有序对数',
        'high += 1': '`high` 改成 `{high}`：问题变成数异或值 ==小于 `{high}`== 的数对（左闭右开）',
        'while high': lambda S, B, r: (f'`high = {S.high}` 还没移空，继续统计一个比特' if S.high else '`high` 移成 0，所有比特都统计完了'),
        'nxt = Counter()': '`nxt` 用来存右移一位后的键，下一轮直接用，不用重新遍历 `nums`',
        'for x, c in cnt.items()': lambda S, B, r: (f'看前缀 `x = {S.x}`（{S.c} 个）' if sum(S.nxt.values()) < sum(S.cnt.values()) else '这一轮的前缀都看完了'),
        'if high & 1': lambda S, B, r: (f'`high` 末位是 1：与 `x` 异或恰得 `{S.high - 1}`（high 末位改成 0）的是 `{S.x ^ (S.high - 1)}`，这样的数对异或值==小于 high== → `ans += {S.c} × cnt[{S.x ^ (S.high - 1)}]` → {S.ans}'
                                        if S.high & 1 else '`high` 末位是 0，这一位不新增数对'),
        'if low & 1': lambda S, B, r: (f'`low` 末位是 1：同理减去异或值小于 `low` 的：搭档 `{S.x ^ (S.low - 1)}` → `ans -= {S.c} × cnt[{S.x ^ (S.low - 1)}]` → {S.ans}'
                                       if S.low & 1 else '`low` 末位是 0，不用减'),
        'nxt[x >> 1] += c': '`x` 右移一位 → 键 `{x >> 1}`，`nxt[{x >> 1}] = {nxt[x >> 1]}`',
        'cnt = nxt': '换成右移后的 `cnt`：`{dict(cnt)}`',
        'low >>= 1': '`low` 右移一位 → `{low}`',
        'high >>= 1': '`high` 右移一位 → `{high}`',
        'return ans // 2': '每个无序数对被 `(x, y)` 和 `(y, x)` 数了两次 → `{ans} // 2 = {ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='自底向上的字典树：每轮把所有数右移一位，哈希表代替字典树',
        complexity='时间 `O(n + n·log(U/n))`，空间 `O(n)`',
        problem=['数对 `(i, j)`，`i < j`，且 `low ≤ nums[i] xor nums[j] ≤ high`，求个数',
                 '示例：`nums = [1,4,2,7]`，`low = 2`，`high = 6` → `6`',
                 '本视频：同一个示例'],
        quote='代码实现时，可以按照「统计前 k 个比特、统计前 k-1 个比特、……、统计前 1 个比特」执行。在遍历 cnt 的同时，可以把每个键都右移 1 位，从而得到下一次要统计的 cnt，这样不用重新遍历 nums。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异或值在 `[low, high]` = `< high+1` 的个数 − `< low` 的个数',
              '`high` 某一位是 1：异或值这一位取 0、前面各位和 high 相同，后面比特==随便==，一次统计一大批',
              '每轮把键右移一位，只剩高位前缀，相当于字典树从最深一层往根走'],
        summary=['时间 `O(n + n·log(U/n))`，比字典树写法更省',
                 '`cnt[x] * cnt[x ^ t]`：x 有 c 个，配对的值有 `cnt[x^t]` 个，乘起来就是对数',
                 '有序对被数了两次，最后要 `// 2`；`t = 0` 的错误结果会在两次相减中抵消',
                 '这里用的是「自底向上」写法；题解另有字典树版本可对照'],
    ),
)
