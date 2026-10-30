def _win(S):
    if 'l' not in S or 'nums' not in S:
        return '按长度 `l` 枚举：同长度的子数组才可能重复，所以每个 `l` 单独去重'
    idx = S.get('index')
    if idx is None:
        return f'当前枚举长度 `l = {S["l"]}`'
    lo = max(0, idx - S['l'] + 1) if idx >= S['l'] - 1 else 0
    return f"窗口 `{S['nums'][lo:idx + 1]}`，可整除元素 `cnt = {S.get('cnt', 0)}`（上限 `k = {S['k']}`）"


def _span(S):
    l, idx = S.get('l'), S.get('index')
    if l is None or idx is None:
        return None
    return max(0, idx - l + 1), idx


CONFIG = dict(
    num=2261, title='含最多 K 个可整除元素的子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按长度枚举 + 定长窗口 + 双模 RK 哈希',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串'],
    code='''
class Solution(object):
    def countDistinct(self, nums, k, p):

        base = 209
        mod1 = 10 ** 9 + 7
        mod2 = 2147483647

        pow1 = pow2 = 1

        res = 0
        for l in range(1, len(nums) + 1):
            now1 = 0
            now2 = 0
            used1 = set()
            used2 = set()

            pow1 = pow1 * base % mod1
            pow2 = pow2 * base % mod2

            cnt = 0
            for index in range(l):
                if nums[index] % p == 0:
                    cnt += 1
                now1 = (now1 * base + nums[index]) % mod1
                now2 = (now2 * base + nums[index]) % mod2
            
            if cnt <= k:
                used1.add(now1)
                used2.add(now2)
                res += 1
            
            for index in range(l, len(nums)):
                now1 = (now1 * base + nums[index] - (nums[index - l] * pow1) % mod1 + mod1) % mod1
                now2 = (now2 * base + nums[index] - (nums[index - l] * pow2) % mod2 + mod2) % mod2
                if nums[index] % p == 0:
                    cnt += 1
                if nums[index - l] % p == 0:
                    cnt -= 1

                if cnt <= k and (now1 not in used1 or now2 not in used2):
                    res += 1
                    used1.add(now1)
                    used2.add(now2)
        
        return res
''',
    call='Solution().countDistinct([2, 3, 3], 1, 2)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=150,
             window=('max(0, index - l + 1)', 'index'),
             color=lambda S, i, v: 'orange' if v % S['p'] == 0 else None),
        dict(type='set', var='used1', label='used1（本长度下见过的窗口哈希）', fmt=lambda x: str(x), h=200),
        dict(type='text', h=60, size=26, fn=_win),
    ],
    watch=[('l', 'l', 'blue'), ('index', 'index', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'base = 209': '哈希参数：进制 `base = 209`，两个模数 `mod1`、`mod2`（双哈希防冲突）',
        'pow1 = pow2 = 1': '`pow1 / pow2` 以后用来把窗口最左边的数「减掉」',
        'for l in range': lambda S, B, r: (f'枚举子数组长度 `l = {S.l}`：==不同长度不可能重复==，每个长度各自去重；哈希、`used`、`cnt` 都重新开始' if S.l != B.get('l')
                                           else '长度都枚举完了'),
        'pow1 = pow1 * base': '`pow = base^{l}`：窗口左移时要减去 `nums[index-l] * base^l`；`used` 只记长度 `{l}` 的窗口哈希',
        22: lambda S, B, r: f'先算第一个窗口：`nums[{S.index}] % {S.p}`，同时把它滚进哈希：' + ('==能被整除==，`cnt` 加 1' if S.nums[S.index] % S.p == 0 else '不能整除'),
        'if cnt <= k:\n': '',
        'if cnt <= k:': lambda S, B, r: f'第一个窗口：`cnt = {S.cnt} ≤ k = {S.k}` → ' + ('合格，记录哈希，`res` 加 1' if S.cnt <= S.k else '不合格，跳过'),
        'res += 1': '`res` → =={res}==',
        35: lambda S, B, r: f'新进窗口的 `nums[{S.index}]`：' + ('==能被整除==，`cnt` 加 1' if S.nums[S.index] % S.p == 0 else '不能整除，`cnt` 不变'),
        33: '窗口右移一格 `index = {index}`：加入 `nums[{index}]`，减去离开的 `nums[{index - l}]`（乘 `base^l`）→ `now1 = {now1}`',
        'if nums[index] % p == 0:\n': '',
        'if nums[index - l] % p == 0': lambda S, B, r: f'离开的 `nums[{S.index - S.l}]`：' + ('能被整除 → `cnt` 减 1' if S.nums[S.index - S.l] % S.p == 0 else '不能整除，`cnt` 不变'),
        'if cnt <= k and': lambda S, B, r: (f'`cnt = {S.cnt}`，`k = {S.k}`：' + ('超过上限，不合格' if S.cnt > S.k else
                                            ('哈希没见过 → ==新的不同子数组==，计数' if (S.now1 not in S.used1 or S.now2 not in S.used2)
                                             else '合格，但哈希在 `used` 里已有 → 重复，不计数'))),
        'return res': '一共 `{res}` 个不同的合格子数组',
    },
    skip=['now2 = 0', 'used2 = set()', 'pow2 = pow2', 'mod1 = 10', 'mod2 = 2147', 'now2 = (now2', 'used2.add', 'cnt += 1', 'cnt -= 1', 'used1.add', 'pow1 = pow2 = 1', 'now1 = 0', 'used1 = set()', 'cnt = 0', 'now1 = (now1 * base + nums[index]) % mod1', 21, 32],
    max_steps=130,
    cards=dict(
        one_liner='不同长度不会重复：按长度枚举，定长窗口 + 滚动哈希去重',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`nums`、`k`、`p`：数出「最多含 `k` 个能被 `p` 整除的元素」的==不同==子数组个数',
                 '内容相同的子数组只算一次',
                 '本视频：`nums=[2,3,3]`，`k=1`，`p=2` → `5`'],
        quote='由于不同长度的子串之间是不可能出现重复的，因此可以先枚举字符串的长度l，然后检测所有长度等于l的子串是否符合条件，同时对符合条件的子串进行去重。',
        quote_src='—— yiduobo 题解原文',
        idea=['乍看像变长滑窗，但要去重，所以改成：枚举长度 `l`，每个长度用==定长窗口==',
              '窗口里统计能被 `p` 整除的个数；同时用 RK 滚动哈希表示窗口内容',
              '两组不同模数的哈希同时判断，防止哈希冲突；哈希没见过才计数'],
        summary=['时间 `O(n²)`（满足进阶），空间 `O(n)`',
                 '长度从 1 到 `n`，每个长度的 `used` 都要清空',
                 '先对第一个窗口单独判断，再右移：右移时要减掉离开的元素',
                 '哈希有极小的冲突概率，所以用了两个模数',
                 '原文可直接在 Python 3 运行，没有改动；视频只画 `used1`，`used2` 同步更新'],
    ),
)
