def _diff_txt(S):
    if 'mid' not in S or 'cnt' not in S:
        return f"`x = {S['x']}`，`y = {S['y']}`（y < x）" if 'x' in S else ''
    t = f"二分区间 `[{S['left']}, {S['right']})`，`mid = {S['mid']}`：共 {S['mid']} 次操作，每个数至少减 `{S['mid']}×{S['y']} = {S['mid']*S['y']}`"
    return t + f"，已需要额外的 x 次数 `cnt = {S['cnt']}`"


def _col(S, i, v):
    if 'mid' not in S or 'cnt' not in S:
        return None
    if S.get('_line') in (14, 15, 16, 17, 18, 19, 21) or True:
        d = v - S['mid'] * S['y']
        if d <= 0:
            return 'green'
        if 'v' in S and v == S['v']:
            return 'yellow'
    return None


CONFIG = dict(
    num=2702, title='使数字变为非正数的最小操作次数', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + 计算需要几次 x',
    tags=['二分算法'],
    code='''
class Solution(object):
    def minOperations(self, nums, x, y):

        left = 1
        right = max(nums) // y + 1
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            for v in nums:
                diff = v - mid * y
                if diff > 0:
                    r = diff // (x - y)
                    if diff % (x - y) != 0:
                        r += 1
                
                    cnt += r
            
            if cnt <= mid:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minOperations([3, 4, 1, 7, 6], 4, 2)',
    expect=3,
    skip=['for v in nums'],
    max_steps=90,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 只靠 y 就能减到 ≤ 0，黄 = 正在算的数）', cell=110, h=250,
             color=_col),
        dict(type='text', h=170, size=30, fn=_diff_txt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'green'),
           ('diff', 'diff', 'orange')],
    captions={
        'left = 1': '至少要 1 次操作：`left = 1`',
        'right = max': '上界：全都只减 y，最大的数也要约 `max(nums) // y + 1 = {right}` 次',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：继续二分' if B.left < B.right
                                               else f'`left = right = {B.left}`：最少操作次数找到了'),
        'mid = (left + right)': '操作越多越容易全部 ≤ 0 → 能二分。试 `mid = {mid}` 次操作',
        'cnt = 0': '`cnt`：为了够用，一共需要几次用 x（其余 `mid - cnt` 次用 y）',
        'diff = v': '看数 `{v}`：`mid` 次全减 y 后还剩 `{v} − {mid}×{y}` = =={diff}==',
        'if diff > 0': lambda S, B, r: (f'`diff = {B.diff} > 0`：光靠 y 不够，必须有些次数改用 x' if B.diff > 0
                                        else f'`diff = {B.diff} ≤ 0`：全用 y 就够了，不需要 x'),
        'r = diff //': '每把一次 y 换成 x 多减 `x − y = {x - y}`：先取整 `{diff} // {x - y}` = {r}，再看有没有余数',
        'if diff % (x - y)': lambda S, B, r: (f'`{B.diff} % {B.x - B.y} = {B.diff % (B.x - B.y)}` ≠ 0：有余数，还差一点' if B.diff % (B.x - B.y)
                                              else f'`{B.diff} % {B.x - B.y} = 0`：刚好整除'),
        'r += 1': '向上取整：`r = {r}`',
        'cnt += r': '这个数要用 `{r}` 次 x，累计 `cnt = {cnt}`',
        'if cnt <= mid': lambda S, B, r: (f'一共需要 `cnt = {B.cnt}` 次 x ≤ `mid = {B.mid}` 次操作 → ==够用==' if B.cnt <= B.mid
                                          else f'需要 `cnt = {B.cnt}` 次 x > `mid = {B.mid}`：操作次数不够放 x → ==不够用=='),
        'right = mid': '`{mid}` 次够用 → 答案 ≤ mid，`right = {right}`',
        'left = mid + 1': '`{mid}` 次不够 → 答案 > mid，`left = {left}`',
        'return left': '最少操作 `{left}` 次',
    },
    cards=dict(
        one_liner='操作次数越多越容易成功：二分次数，算要用几次 x',
        complexity='时间 `O(n log(max/y))`，空间 `O(1)`',
        problem=['数组 `nums`，每次操作选一个下标，让它减 `x`，其余下标都减 `y`（`y < x`）',
                 '求让所有数都 ≤ 0 的==最少操作次数==',
                 '本视频：`nums = [3,4,1,7,6]`，`x = 4, y = 2` → `3`'],
        quote='对于当前二分到的值mid，表示一共会进行mid次减法，也就是说一共只有mid个x可以减，其他时候都只能减去y。',
        quote_src='—— yiduobo 题解原文',
        idea=['先不管 x：`mid` 次操作每个数至少被减 `mid×y`',
              '还 > 0 的数，每次改用 x 多减 `x−y`，向上取整得要几次',
              '所有数需要的 x 次数之和 `cnt ≤ mid` 就可行'],
        summary=['时间 `O(n log(max/y))`',
                 '易错：`diff` 有余数要向上取整；`cnt` 超过 `mid` 就是不行',
                 '作者也提到可以贪心批量模拟，但相同值的细节繁杂，二分更省心',
                 '原文为 Python 2 写法，3 处整数除法 `/` 已改为 `//`'],
    ),
)
