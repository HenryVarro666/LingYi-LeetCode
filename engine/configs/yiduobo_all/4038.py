CONFIG = dict(
    num=4038, title='计算单个区间中出现的整数数量', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='first / last / cnt 三表对比',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countSpecialIntegers(self, nums):
        
        first = {}
        last = {}
        cnt = {}
        for index, v in enumerate(nums):
            if v not in first:
                first[v] = index
                cnt[v] = 0
            
            cnt[v] += 1
            last[v] = index
        
        res = 0
        for v in first:
            if last[v] - first[v] + 1 == cnt[v]:
                res += 1
        
        return res
''',
    call='Solution().countSpecialIntegers([3,3,1,2,2,1])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=190),
        dict(type='map', var='first', label='first（首次位置）', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
        dict(type='map', var='last', label='last（最后位置）', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
        dict(type='map', var='cnt', label='cnt（出现次数）', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'first = {}': '`first[x]`：x 第一次出现的下标',
        'last = {}': '`last[x]`：x 最后一次出现的下标',
        'cnt = {}': '`cnt[x]`：x 一共出现几次',
        'if v not in first': lambda S, B, r: (f'`{S.v}` 还没记录过 → 第一次出现' if S.v not in B.first else f'`{S.v}` 之前见过 → 只更新 last 和 cnt'),
        'first[v] = index': '首次出现，`first[{v}] = {index}`',
        'cnt[v] = 0': '`cnt[{v}]` 先置 0，下一行再加一',
        'cnt[v] += 1': '`cnt[{v}]` → {cnt[v]}',
        'last[v] = index': '每遇到一次都刷新：`last[{v}] = {index}`',
        'for v in first': '检查每种整数：{v}',
        'if last[v] - first[v] + 1 == cnt[v]': lambda S, B, r: (f'区间长度 `{S.last[S.v]} − {S.first[S.v]} + 1 = {S.last[S.v]-S.first[S.v]+1}`，出现次数 `{S.cnt[S.v]}` → '
                                                              + ('相等：区间内全是它，==特殊整数==' if S.last[S.v]-S.first[S.v]+1 == S.cnt[S.v] else '不等：中间夹了别的数')),
        'res += 1': '`res` → =={res}==',
        'return res': '特殊整数一共 `{res}` 个',
    },
    cards=dict(
        one_liner='首尾区间的长度 = 出现次数，说明中间没夹别的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['若 `x` 的所有出现位置都在同一个连续区间内，`x` 就是特殊整数',
                 '求 `nums` 中不同特殊整数的个数',
                 '示例：`[3,3,1,2,2,1]` → `2`'],
        quote='若cnt[x]与last[x] - first[x] + 1相等，就说明x确实是集中在这一段的，否则说明不是。',
        quote_src='—— yiduobo 题解原文',
        idea=['x 首尾之间一共有 `last − first + 1` 个位置',
              '如果 x 全部集中，这些位置都该是 x，数量正好等于 `cnt[x]`',
              '一趟遍历记下 first、last、cnt，再逐个判断'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`cnt` 要在第一次出现时初始化为 0',
                 '原文已是 Python 3 可运行写法，未改动',
                 '对比灵神：灵神只数段首，一次遍历边数边撤销，不需要三张表'],
    ),
)
