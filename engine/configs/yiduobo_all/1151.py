def _l(S):
    i = S.get('index')
    return 0 if i is None else i + 1


def _r(S):
    i = S.get('index')
    return S['k'] - 1 if i is None else i + S['k']


CONFIG = dict(
    num=1151, title='最少交换次数来组合所有的1', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗 · 窗口内 1 最多',
    tags=['会员题'],
    code='''
class Solution(object):
    def minSwaps(self, data):

        k = sum(data)
        now = sum(data[:k])
        res = k - now
        for index, num in enumerate(data[k:]):
            now += num - data[index]
            res = min(res, k - now)
        
        return res
''',
    call='Solution().minSwaps([1,0,1,0,1,0,0,1,1,0,1])',
    expect=3,
    views=[
        dict(type='array', var='data', label='data（框 = 长 k 的窗口，k = 1 的总数）', window=(_l, _r),
             color=lambda S, i, v: 'green' if v == 1 else None, h=210, cell=84),
        dict(type='text', h=90, size=32,
             fn=lambda S: (f'窗口内已有 `{S["now"]}` 个 1，还差 `{S["k"]} − {S["now"]}` = =={S["k"] - S["now"]}== 个要换进来'
                           if 'now' in S else '交换后 1 会连成长为 k 的一段，k = 1 的总数')),
    ],
    watch=[('k', 'k', 'cyan'), ('now', 'now', 'blue'), ('res', 'res', 'green'), ('index', 'index')],
    captions={
        'k = sum(data)': '所有 1 最终会挤成一段，长度就是 1 的总数 `k = {k}`',
        'now = sum(data[:k])': '第一个窗口（前 `k` 格）里已有 `{now}` 个 1',
        'res = k - now': '这个窗口要换进 `k - now = {res}` 个 1，先当作答案',
        'for index, num in enumerate(data[k:])': lambda S, B, r: ('所有窗口都滑完了' if 'index' in B and S.index == B.index else f'窗口右移：右边进来 `data[{S.index + S.k}] = {S.num}`，左边出去 `data[{S.index}] = {S.data[S.index]}`'),
        'now += num - data[index]': '`now += {num} − {data[index]}` → `{now}`：进来的是 1 就加，出去的是 1 就减',
        'res = min': '这个窗口代价 `k − now = {k - now}`，`res = min({B.res}, {k - now}) = {res}`：==窗口里 1 越多代价越小==',
        'return res': '最少交换 `{res}` 次',
    },
    max_steps=60,
    cards=dict(
        one_liner='换完后 1 连成长 k 的一段：找 1 最多的长 k 窗口',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `data`，每次可交换任意两个位置，求把所有 1 ==组合到一起==的最少交换次数',
                 '示例：`[1,0,1,0,1]` → `1`',
                 '本视频：`[1,0,1,0,1,0,0,1,1,0,1]` → `3`'],
        quote='交换完成后数组中必然会得到一段长度为k的连续的1，而交换的代价就是k减去这一段中原本就是1的位置的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` = 1 的总数，目标段长度固定为 `k`',
              '某个窗口里有 `now` 个 1，只需把外面的 `k − now` 个 1 换进来',
              '代价最小 ⇔ 窗口里的 1 最多，定长滑窗枚举所有窗口'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：求的是窗口里 ==1 的最大数==，等价于代价 `k − now` 最小',
                 '`k = 0` 时窗口为空，答案 0',
                 '窗口右移只更新进出的两个数：`now += num − data[index]`'],
    ),
)
