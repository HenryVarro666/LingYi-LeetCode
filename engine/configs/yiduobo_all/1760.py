NUMS = [9, 4]
OPS = 3


def _color(S, i, v):
    if 'l' not in S:
        return None
    if i < S['l']:
        return 'red'
    if i >= S['r']:
        return 'green'
    return None


def _per(S):
    if 'mid' in S and S['_line'] in (8, 9, 10, 11, 12, 14):
        m = S['mid']
        return [x // m - (1 if x % m == 0 else 0) for x in NUMS]
    return []


def _top(S):
    if 'cnt' in S and 'mid' in S and S['_line'] in (8, 9, 10, 11, 12):
        return f"k = `{S['mid']}`：目前累计操作 `cnt = {S['cnt']}` 次（上限 `{OPS}`）"
    if 'l' not in S:
        return f'最多操作 `{OPS}` 次：k 越大操作越少 → ==二分答案=='
    l, r = S['l'], S['r']
    if l < r:
        return f'答案在 `[{l}, {r}]` 里：`{l}` 之前都不行，`{r}` 一定可行'
    return f'`l == r = {l}`：区间收成一点 → 答案 =={l}=='


CONFIG = dict(
    num=1760, title='袋子里最少数目的球', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 顶着 k 分',
    tags=['灵神题单·二分算法', '难度分 1940'],
    code='''
class Solution(object):
    def minimumSize(self, nums, maxOperations):

        l = 1
        r = max(nums)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for num in nums:
                cnt += num // mid
                if num % mid == 0:
                    cnt -= 1
            
            if cnt > maxOperations:
                l = mid + 1
            else:
                r = mid
        
        return l
''',
    call=f'Solution().minimumSize({NUMS}, {OPS})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(max(NUMS) + 1)),
             label='候选 k（红 = 太小，绿 = 可行，灰 = 还没判断）',
             cell=70, index=False, color=_color, pointers={'l': 'red', 'mid': 'yellow', 'r': 'green'}, h=240),
        dict(type='array', var='nums', label='nums：各袋子里的球数', cell=100, h=170),
        dict(type='array', var=_per, label='每个袋子顶着 k 分，需要的操作次数', cell=100, index=False, h=170),
    ],
    watch=[('l', 'l', 'red'), ('r', 'r', 'green'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan'), 'maxOperations'],
    captions={
        'l = 1': '`l = 1`：二分下限，每袋至少 1 个球',
        'r = max': '`r = max(nums) = {r}`：最大的袋子不动，一定可行',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：区间还没收成一点 → 继续' if S.l < S.r
                                         else f'`l = r = {S.l}`：区间收成一点，==答案就是它=='),
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`：试试每袋至多 `{mid}` 球',
        'cnt = 0': '`cnt` 记录总操作次数',
        'cnt += num // mid': '`num = {num}`：顶着 `{mid}` 分，得到 `{num} // {mid} = {num // mid}` 份 → 先记 `{num // mid}` 次，`cnt` = =={cnt}==',
        'if num % mid == 0': lambda S, B, ret: (f'`{S.num} % {S.mid} = 0`：正好分完，份数比操作数多 1 → ==减掉 1 次=='
                                               if S.num % S.mid == 0 else f'`{S.num} % {S.mid} = {S.num % S.mid} ≠ 0`：有余数多出一份：份数 = `{S.num // S.mid}` + 1，操作数正好是 `{S.num // S.mid}` → 不用减'),
        'cnt -= 1': '`cnt` 减 1 → =={cnt}==（`k` 份只要 `k − 1` 次操作）',
        'if cnt > maxOperations': lambda S, B, ret: (f'`cnt = {S.cnt} > {S.maxOperations}`：操作超了，`k = {S.mid}` ==太小=='
                                                    if S.cnt > S.maxOperations else f'`cnt = {S.cnt} ≤ {S.maxOperations}`：`k = {S.mid}` ==可行=='),
        'l = mid + 1': '`k = {B.mid}` 不行，更小的更不行 → `l = {l}`',
        'r = mid': '`k = {mid}` 可行，但可能更小 → `r = {r}`',
        'return l': '`l` 是最小的可行 k → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='每袋至多 k 球，顶着 k 分最省操作；k 越大操作越少 → 二分',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`nums[i]` 是第 `i` 个袋子的球数，每次操作把一个袋子分成两个非空袋子',
                 '最多操作 `maxOperations` 次，使最大袋子里的球数最小',
                 '示例：`nums = [9], maxOperations = 2` → `3`；本视频：`[9, 4], 3` → `3`'],
        quote='随着答案的增大，需要分的次数必然是越来越小的，反过来也成立。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个袋子 `num` 球、每袋不超过 `k`：==顶着 k 分==最省操作',
              '有余数：`num // k + 1` 份，操作 `num // k` 次；恰好整除：`num // k` 份，操作 `num // k − 1` 次',
              '总操作 `cnt ≤ maxOperations` 就收 `r`，否则抬 `l`'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `num / mid` 已改为 `num // mid`',
                 '易错：整除时要减 1（8 球每袋 2 个 = 4 份只要 3 次）',
                 '对比灵神：灵神用 `(x − 1) // m` 把整除与否合成一个式子'],
    ),
)
