CONFIG = dict(
    num=915, title='分割数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前缀最大 + 后缀最小',
    code='''
class Solution(object):
    def partitionDisjoint(self, A):

        max_list = [A[0]]
        for num in A[1:]:
            max_list.append(max(max_list[-1], num))
        
        min_list = [A[-1]]
        for num in A[::-1][1:]:
            min_list.append(min(min_list[-1], num))
        
        min_list.reverse()

        res = 0
        while max_list[res] > min_list[res + 1]:
            res += 1
        
        return res + 1
''',
    call='Solution().partitionDisjoint([5,0,3,8,6,9])',
    expect=3,
    views=[
        dict(type='array', var='A', h=200, label='A', index=True,
             color=lambda S, i, v: 'green' if 'res' in S and i <= S['res'] else None),
        dict(type='array', var='max_list', h=200, label='max_list（前缀最大，下标 i = A[0..i] 的最大值）',
             pointers={'res': 'blue'}),
        dict(type='array', var='min_list', h=200, label='min_list（先倒着存，reverse 后 min_list[i] = A[i..] 的最小值）',
             pointers={'res + 1': 'pink'}),
    ],
    watch=['num', ('res', 'res', 'blue')],
    captions={
        'max_list = [A[0]]': '`max_list[i]` = `A[0..i]` 的最大值，先放第一个 `{A[0]}`',
        'max_list.append': '`max({max_list[-2]}, {num})` → 前缀最大 `{max_list[-1]}`',
        'min_list = [A[-1]]': '从右往左：`min_list` 先放最后一个 `{A[-1]}`',
        'min_list.append': '`min({min_list[-2]}, {num})` → 后缀最小 `{min_list[-1]}`',
        'min_list.reverse': '把倒着存的后缀最小反转：现在 `min_list[i]` = `A[i..]` 的最小值',
        'res = 0': '从分割点 `res = 0` 开始枚举：左部分 = `A[0..res]`',
        'while max_list[res]': lambda S, B, r: (f'左部分最大 `{S.max_list[S.res]}` > 右部分最小 `{S.min_list[S.res+1]}`？ ==成立== → 左边有数比右边大，分割点右移'
                                               if S.max_list[S.res] > S.min_list[S.res + 1]
                                               else f'左部分最大 `{S.max_list[S.res]}` ≤ 右部分最小 `{S.min_list[S.res+1]}` → ==合法分割==，停'),
        'res += 1': '分割点右移：`res` → {res}',
        'return res + 1': '左部分有 `res + 1 = {ret}` 个数（长度最短）',
    },
    cards=dict(
        one_liner='左边每个数 ≤ 右边每个数，等价于：左边最大 ≤ 右边最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把数组 `A` 分成左右两段（都非空），左段每个数 ≤ 右段每个数',
                 '返回满足条件的左段的最小长度',
                 '本视频：`[5,0,3,8,6,9]` → `3`（左 `[5,0,3]`，右 `[8,6,9]`）'],
        quote='前面这个部分的最大值小于等于后面这个部分的最小值，也就是最大前缀以及最小后缀。这两个值可以通过正反两趟扫描求解出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['正向扫一遍：`max_list[i]` = 前缀最大值',
              '反向扫一遍再 `reverse`：`min_list[i]` = 后缀最小值',
              '从 0 枚举分割点：`max_list[res] <= min_list[res+1]` 就停，答案 `res + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个辅助数组）',
                 '易错点：右段最小值是 `min_list[res + 1]`，别忘了 `+1`',
                 '易错点：左段长度是 `res + 1`，不是 `res`',
                 '题目保证存在合法分割，所以 `while` 不会越界'],
    ),
)
