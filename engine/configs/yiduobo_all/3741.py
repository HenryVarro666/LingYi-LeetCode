CONFIG = dict(
    num=3741, title='三个相等元素之间的最小距离 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记上两次位置', tags=[],
    code='''
class Solution(object):
    def minimumDistance(self, nums):
        
        p1 = {}
        p2 = {}
        res = -1

        for index, v in enumerate(nums):
            if p2.get(v, None) is not None:
                dis = (index - p2[v]) * 2
                if res == -1 or res > dis:
                    res = dis
            
            p2[v], p1[v] = p1.get(v, None), index
        
        return res
''',
    call='Solution().minimumDistance([2,1,2,3,2,1,1])',
    expect=8,
    views=[
        dict(type='array', var='nums', h=200, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and 'v' in S and v == S['v'] and i <= S['index'] else None),
        dict(type='map', var='p1', h=170, label='p1：每个值上一次出现的位置'),
        dict(type='map', var='p2', h=170, label='p2：每个值上上次出现的位置'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('dis', 'dis', 'orange'), ('res', 'res', 'green')],
    captions={
        'p1 = {}': '`p1`：值 → 上一次出现的位置',
        'p2 = {}': '`p2`：值 → 上上次出现的位置',
        'res = -1': '`res = -1`：还没有有效三元组',
        'if p2.get': lambda S, B, r: (f'`p2[{S.v}] = {S.p2.get(S.v)}`：`{S.v}` 已出现过两次，当前是第三次 → 有三元组' if S.p2.get(S.v) is not None
                                      else f'`{S.v}` 之前出现不足两次，先不算'),
        'dis = (': '三元组最左 `{p2[v]}`，最右 `{index}`：`dis = ({index} − {p2[v]}) × 2` = =={dis}==',
        'if res == -1': lambda S, B, r: f'`res = {S.res}`，`dis = {S.dis}`：' + ('第一个答案或更小 → 更新' if (S.res == -1 or S.res > S.dis) else '没有更小 → 不更新'),
        'res = dis': '`res` 取更小的 `{res}`',
        'p2[v], p1[v]': '记录后移：`p2[{v}] = {p2[v]}`，`p1[{v}] = {p1[v]}`',
        'return res': '遍历完毕，最小距离 `{res}`',
    },
    cards=dict(
        one_liner='化简成 2(k−i)，一趟遍历维护最近两次位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums[i]==nums[j]==nums[k]` 且下标互不相同才是有效三元组',
                 '距离 `abs(i−j)+abs(j−k)+abs(k−i)`，求最小值，没有则 `-1`',
                 '本题 n 可达 `10^5`，要线性做法；示例 `[2,1,2,3,2,1,1]` → `8`'],
        quote='最终答案必然出自于某个元素在nums中所有下标的列表中的三个连续下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['默认 `i<j<k`，三个绝对值拆开后得 `2*(k-i)`',
              '想让 `k−i` 小，就取同一个值的连续三个下标',
              '遍历时 `p2[v]` 就是当前位置往前数第二个相同值，直接用它算'],
        summary=['时间 `O(n)`，空间 `O(n)`，和 I 是同一份代码，规模大也不怕',
                 '先算距离、再更新 `p2/p1`，否则会把当前位置当成自己的前驱',
                 '`p2[v]` 可能是 `None`，所以用 `.get` 并判断 `is not None`',
                 '对比灵神：灵神用数组、`-inf` 做初值并把乘 2 放到最后；这里用哈希表和 `-1` 标记'],
    ),
)
