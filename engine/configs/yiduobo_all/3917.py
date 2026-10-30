NUMS = [3, 8, 5, 6, 2, 7]


def _cur(S):
    if 'res' not in S or 'nums' not in S:
        return None
    n, k = len(S['nums']), len(S['res'])
    i = n - 1 - k if S.get('_line') in (6, 7) else n - k
    return i if 0 <= i < n and 'v' in S else None


def _col(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    if i == c:
        return 'yellow'
    if i > c:
        return 'green' if v % 2 == 0 else 'purple'
    return None


def _dim(S, i, v):
    c = _cur(S)
    return c is not None and i < c


def _txt(S):
    if 'res' not in S:
        return '`cnt = [偶数个数, 奇数个数]`，统计的是==后缀=='
    return f'`res` 是倒着收集的：`{S["res"]}`，最后要再反转一次'


CONFIG = dict(
    num=3917, title='统计下标的相反奇偶性得分', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='后缀奇偶计数 · 倒序收集再反转',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def countOppositeParity(self, nums):
        
        cnt = [0, 0]
        res = []
        for v in nums[::-1]:
            v %= 2
            res.append(cnt[1 - v])
            cnt[v] += 1
        
        return res[::-1]
''',
    call=f'Solution().countOppositeParity({NUMS})',
    expect=[3, 2, 2, 1, 1, 0],
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前元素；后缀：绿 = 偶数，紫 = 奇数）',
             color=_col, dim=_dim, cell=100, h=230),
        dict(type='array', var='cnt', label='cnt[0] 后缀偶数个数 / cnt[1] 后缀奇数个数', cell=100, h=180,
             color=lambda S, i, v: 'green' if i == 0 else 'purple'),
        dict(type='array', var='res', label='res（倒序追加）', cell=100, h=180,
             color=lambda S, i, v: 'orange' if S.get('_line') == 8 and i == len(S['res']) - 1 else None),
        dict(type='text', fn=_txt, size=30, h=80),
    ],
    watch=[('v', 'v', 'yellow')],
    captions={
        'cnt = [0, 0]': '`cnt[0]` / `cnt[1]`：当前==后缀==中偶数 / 奇数的数量',
        'res = []': '`res` 按从后往前的顺序收集得分',
        'for v in nums[::-1]': lambda S, B, ret: (f'从后往前取下一个元素 `v = {S.v}`'
                                                  if len(S.res) < len(S.nums) else '遍历结束'),
        'v %= 2': lambda S, B, ret: f'只关心奇偶：`v % 2` → `{S.v}`（{"奇" if S.v else "偶"}数）',
        'res.append': lambda S, B, ret: (f'得分 = 后缀中{"偶" if S.v else "奇"}数的数量 `cnt[1 − {S.v}] = {S.res[-1]}`，追加到 res'),
        'cnt[v] += 1': lambda S, B, ret: f'把当前元素并入后缀：`cnt[{S.v}]` → {S.cnt[S.v]}，继续向前',
        'return res[::-1]': '`res` 是倒序的，==反转==后返回 `{ret}`',
    },
    cards=dict(
        one_liner='得分就是后缀里另一种奇偶性的元素个数',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['下标 i 的得分 = 满足 `i < j < n` 且 `nums[i]`、`nums[j]` ==奇偶性不同==的 j 的数量',
                 '返回每个下标的得分',
                 '示例：`[1,2,3,4]` → `[2,1,1,0]`'],
        quote='对于每个下标，其得分实际上就是==其右侧的后缀中奇数或者偶数的数量==。于是可以从后往前一趟遍历，使用一个长度为2的数组cnt维护后缀中偶数与奇数的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `nums[::-1]` 直接倒着遍历值，`v %= 2` 只留奇偶性',
              '得分是 `cnt[1 − v]`：追加到 `res` 后再 `cnt[v] += 1`',
              '`res` 收集顺序与下标相反，最后 `res[::-1]` 翻回来'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计答案）',
                 '易错：先记录得分再更新 cnt，否则会把自己算进后缀',
                 '易错：别忘了最后反转 `res`',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神按下标倒序写 `ans[i]`，不需要反转'],
    ),
)
