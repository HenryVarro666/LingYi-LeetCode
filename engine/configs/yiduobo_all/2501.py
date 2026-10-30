NUMS = [16, 2, 5, 4, 256, 9, 3]


def _col(S, i, v):
    if 'num' not in S or 'vis' not in S:
        return None
    if v == S['num']:
        return 'blue'
    if v in S['vis']:
        return 'green'
    return None


def _txt(S):
    if 'cnt' not in S or 'num' not in S or S.get('_line', 0) < 12:
        return '从小到大扫描，没访问过的数就当作新链条的起点'
    return f'当前链条：从 `num = {S["num"]}` 往上平方，已有 `cnt = {S["cnt"]}` 项；最长 `res = {S["res"]}`'


CONFIG = dict(
    num=2501, title='数组中最长的方波', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='集合 + 从小到大扫描，访问过的数不再当起点',
    tags=['灵神题单', '动态规划', '难度分 1480'],
    code='''
class Solution(object):
    def longestSquareStreak(self, nums):

        num_set = set(nums)
        vis = set()

        res = 0
        for num in sorted(list(num_set)):
            if num not in vis:
                cnt = 1
                vis.add(num)
                while num * num in num_set:
                    num *= num
                    vis.add(num)
                    cnt += 1
                
                res = max(res, cnt)
        
        if res == 1:
            return -1
        
        return res
''',
    call=f'Solution().longestSquareStreak({NUMS!r})',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前数，绿 = 已访问）', h=190, cell=100, color=_col),
        dict(type='set', var='vis', label='vis（已经在某条链里的数）', fmt=lambda x: str(x), h=170, font=30),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'num_set = set': '先把所有数放进集合 `num_set`，用来判断某个平方数在不在数组里',
        'vis = set': '`vis` 记录已经走过的数：它们已经属于某条链，不必再当起点',
        'res = 0': '`res` 记录最长链的长度',
        'for num in sorted': lambda S, B, r: (f'从小到大取到 `num = {S.num}`' if B.get('_line') != 8 else '所有数都扫完了'),
        'if num not in vis': lambda S, B, r: (f'`{S.num}` 已经在别的链里，跳过：==链的起点一定是最小的数==' if S.num in S.vis
                                              else f'`{S.num}` 还没访问过 → 它是新链的起点'),
        'cnt = 1': '起点自己算一项：`cnt = 1`',
        'vis.add(num)': '标记 `{num}` 已访问',
        'while num * num in num_set': lambda S, B, r: (f'`{S.num}² = {S.num * S.num}` 在集合里 → 链还能延长' if S.num * S.num in S.num_set
                                                       else f'`{S.num}² = {S.num * S.num}` 不在集合里 → 链结束'),
        'num *= num': '走到下一项：`num = {num}`',
        'cnt += 1': '链长加一：`cnt = {cnt}`',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'if res == 1': lambda S, B, r: ('`res == 1`：没有任何数能接上平方 → 不存在方波，返回 -1' if S.res == 1
                                         else f'`res = {S.res} > 1`，存在方波'),
        'return res': '最长方波长度 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='从小到大扫，没走过的数就是新链起点，沿着平方一路走',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['子序列排序后，除第一个数外每个数是前一个的==平方==，长度至少为 2',
                 '求最长方波长度，没有就返回 `-1`',
                 '示例：`[4,3,6,16,8,2]` → `3`；本视频：`[16,2,5,4,256,9,3]` → `4`'],
        quote='若x没有被访问过，那么就通过集合检测x^2是否出现在数组中，若出现过，则将x迭代为x^2并将其标记为访问过，重复此过程直到x^2没有出现在集合中为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['先去重放进集合，再==从小到大==遍历',
              '一个数如果已被访问，说明它在更小起点的链里，不用再算',
              '过程中访问的数字数量就是当前链的长度'],
        summary=['时间 `O(n log n)`（排序主导），空间 `O(n)`',
                 '易错：单个数 `cnt = 1` 不算方波，`res == 1` 要返回 `-1`',
                 '`vis` 保证每个数只被走一次',
                 '对比灵神：灵神直接枚举每个起点（不排序、不标记），因为链很短'],
    ),
)
