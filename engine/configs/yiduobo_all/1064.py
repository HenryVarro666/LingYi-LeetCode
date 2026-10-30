CONFIG = dict(
    num=1064, title='不动点', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='减去下标后二分',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def fixedPoint(self, arr):

        n = len(arr)
        b = [arr[i] - i for i in range(n)]
        left = 0
        right = n - 1
        res = -1
        while left <= right:
            mid = (left + right) // 2
            if b[mid] == 0:
                res = mid
                right = mid - 1
            elif b[mid] < 0:
                left = mid + 1
            else:
                right = mid - 1
        
        return res
''',
    call='Solution().fixedPoint([-10,-5,0,3,7,8,10,12])',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr（严格递增的整数）', h=190,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='array', var='b', label='b[i] = arr[i] - i（单调不减）', h=190,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             color=lambda S, i, v: 'green' if v == 0 else None,
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'b = [': '令 `b[i] = arr[i] - i`，找 `arr[i] = i` 就是找 ==`b[i] = 0`==。`arr` 严格递增，所以 `b` 单调不减：`{b}`',
        'left = 0': '二分下界 `left = 0`',
        'right = n - 1': '二分上界 `right = n - 1 = {right}`',
        'res = -1': '先假设没有不动点：`res = -1`',
        'while left <= right': lambda S, B, r: f'`left = {S.left} <= right = {S.right}`，还有候选下标' if S.left <= S.right else f'`left = {S.left} > right = {S.right}`：区间空了，结束',
        'mid = (left': '取中点 `mid = {mid}`，`b[{mid}] = {b[mid]}`',
        'if b[mid] == 0': lambda S, B, r: f'`b[{S.mid}] = {S.b[S.mid]}` 等于 0 → ==找到不动点==' if S.b[S.mid] == 0 else f'`b[{S.mid}] = {S.b[S.mid]}` 不等于 0',
        'res = mid': '记下 `res = {res}`',
        'right = mid - 1': lambda S, B, r: f'要的是==最小==下标：继续往左找，`right = {S.right}`' if S.b[S.mid] == 0 else f'`b[{S.mid}] = {S.b[S.mid]} > 0`：右边只会更大，去左边，`right = {S.right}`',
        'elif b[mid] < 0': lambda S, B, r: f'`b[{S.mid}] = {S.b[S.mid]}` < 0 → ==成立==' if S.b[S.mid] < 0 else f'`b[{S.mid}] = {S.b[S.mid]}` < 0 不成立（它大于 0）',
        'left = mid + 1': '`b[mid] < 0`：左边只会更小，不可能为 0 → 往右，`left = {left}`',
        'return res': '返回最小的不动点下标 ==`{ret}`==',
    },
    cards=dict(
        one_liner='arr[i] 减去 i 以后单调不减，在里面二分第一个 0',
        complexity='时间 `O(n)`（建 b）+ `O(log n)`（二分），空间 `O(n)`',
        problem=['给一个严格递增的整数数组 `arr`，找最小的下标 `i` 使得 `arr[i] == i`',
                 '不存在则返回 `-1`',
                 '示例：`[-10,-5,0,3,7]` → `3`；本视频：`[-10,-5,0,3,7,8,10,12]` → `3`'],
        quote='题目要求找出最小的满足arr[i] = i的下标i，那么在这里可以将数组先转化为b[i] = arr[i] - i，问题就转化成了找出最小的下标i满足b[i] = 0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr` 严格递增的整数 → 每步至少 +1，减去 `i` 后 `b` 不减',
              '`b[mid] < 0` 往右，`> 0` 往左',
              '`== 0` 先记下 `res`，再往左找更小的'],
        summary=['找最小下标：命中后不能直接返回，要 `right = mid - 1` 继续往左',
                 '`res` 初值 `-1` 对应无解',
                 '原文为 Python 2 写法，`mid = (left + right) / 2` 已改为 `//`',
                 '额外建了数组 `b`，其实直接比较 `arr[mid] - mid` 即可，空间 `O(1)`'],
    ),
)
