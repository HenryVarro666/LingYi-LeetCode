def _txt(S):
    if 'target' not in S:
        return ''
    if 'now' not in S or 'r' not in S:
        return f"原数组和 `{S['s']}`，模 `{S['p']}` 余 `target = {S['target']}`：要删的子数组也要余 {S['target']}"
    return (f"`r = (now − target + p) % p = ({S['now']} − {S['target']} + {S['p']}) % {S['p']}` = =={S['r']}=="
            f"（要找余数为 {S['r']} 的旧前缀）")


CONFIG = dict(
    num=1590, title='使数组和能被 P 整除', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 哈希表（记最后位置）',
    tags=['前缀和与哈希表', '同余', '难度分 2039'],
    code='''
class Solution(object):
    def minSubarray(self, nums, p):

        s = sum(nums)
        if s % p == 0:
            return 0
        
        target = s % p
        last_pos = {}
        last_pos[0] = -1
        now = 0
        res = len(nums)
        for index, num in enumerate(nums):
            now += num
            r = (now - target + p) % p
            if r in last_pos:
                res = min(res, index - last_pos[r])
            
            last_pos[now % p] = index
        
        if res == len(nums):
            res = -1
        
        return res
''',
    call='Solution().minSubarray([3,1,4,2], 6)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=200, cell=110),
        dict(type='map', var='last_pos', label='last_pos：前缀和 % p → 最后出现的位置', fmt=lambda k, v: f'{k}: {v}', h=210, font=32),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('target', 'target', 'orange'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        's = sum(nums)': '先求原数组之和 `s = {s}`',
        'if s % p == 0': lambda S, B, r: (f'`{S.s} % {S.p} = 0`：本来就是 p 的倍数，边界情况直接返回 0' if S.s % S.p == 0
                                          else f'`{S.s} % {S.p} = {S.s % S.p} ≠ 0`：得删一段子数组'),
        'return 0': '不用删，返回 `0`',
        'target = s % p': '`target = {target}`：被删子数组的和模 p 也必须是 {target}',
        'last_pos = {}': '哈希表：每种余数最后一次出现的位置',
        'last_pos[0] = -1': '空前缀余数是 0，位置记 `-1`：这样从头开始的子数组也能找到',
        'res = len(nums)': '`res` 先设成 `{res}`（整个数组，不允许删光；最后还等于它就无解）',
        'now = 0': '`now` 是当前前缀和',
        'for index, num': lambda S, B, r: (f'扫到 `nums[{S.index}] = {S.num}`' if 'index' not in B or S.index != B.index else '扫描结束'),
        'now += num': '`now = {B.now} + {num} = {now}`',
        'r = (now': '`r = ({now} − {target} + {p}) % {p} = {r}`：要在之前找余数为 `{r}` 的前缀，差值才余 target',
        'if r in last_pos': lambda S, B, r: (f'`{S.r}` 在 last_pos 里，位置 `{S.last_pos[S.r]}` → 能构成一个候选' if S.r in S.last_pos
                                             else f'`{S.r}` 不在 last_pos 里 → 前面没有合适的前缀'),
        'res = min': '子数组 `({last_pos[r]}, {index}]` 长 `{index} − ({last_pos[r]}) = {index - last_pos[r]}` → `res = {res}`',
        'last_pos[now % p] = index': '记下余数 `{now % p}` 最后出现在 `{index}`（最靠后，子数组才最短）',
        'if res == len(nums)': lambda S, B, r: ('`res` 还是整个数组长度 → 没找到' if S.res == len(S.nums) else f'`res = {S.res}` < 长度，找到了'),
        'res = -1': '无解，`res = -1`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='子数组和模 p 等于总和模 p：前缀和 + 哈希表找最近的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['移除一个最短子数组（不能是整个数组），让剩下的和是 `p` 的倍数',
                 '无法做到返回 `-1`；本来就是倍数则返回 `0`',
                 '示例：`[3,1,4,2], p = 6` → `1`（删去 `[4]`）'],
        quote='若原数组之和模P为t，那么被移除的子数组也必须满足模P等于t，那么此时问题就转化成了找出一个最短的子数组，使得这个子数组模P等于t。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：和已是 p 的倍数就返回 0',
              '当前前缀和 `now`，要找旧前缀余数 `(now − t + p) % p`，两者之差模 p 恰为 t',
              '哈希表只存每种余数==最后一次==出现的位置，一次 O(1) 就定位'],
        summary=['时间 `O(n)`，空间 `O(n)`（余数最多 p 种）',
                 '易错：先查询、后更新哈希表，且 `last_pos[0] = -1` 不能漏',
                 '最后若 `res` 仍等于数组长度，说明只能删光，返回 -1',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神先更新 last 再查（允许删空段）；这里先把 x=0 的情况单独返回'],
    ),
)
