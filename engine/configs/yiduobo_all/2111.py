CONFIG = dict(
    num=2111, title='使数组 K 递增的最少操作次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按间隔 K 拆分 · 每组 LIS', tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1941'],
    code='''
class Solution(object):
    def kIncreasing(self, arr, k):

        res = 0
        for start in range(k):
            f = [arr[start]]
            for index in range(start + k, len(arr), k):
                if arr[index] >= f[-1]:
                    f.append(arr[index])
                else:
                    l = 0
                    r = len(f) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if arr[index] >= f[mid]:
                            l = mid + 1
                        else:
                            r = mid
                    f[l] = arr[index]
                    res += 1

        return res
''',
    call='Solution().kIncreasing([5,2,4,1,3,6,2,3], 2)',
    expect=5,
    views=[
        dict(type='array', var='arr', h=200, label='arr（蓝框 = 当前这一组的位置）',
             color=lambda S, i, v: ('yellow' if 'index' in S and i == S['index'] else 'blue' if 'start' in S and i % S['k'] == S['start'] else None),
             pointers={'index': 'pink'}),
        dict(type='array', var='f', h=200, label='f：当前这组的不减序列', pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='text', fn=lambda S: (f"第 `{S['start']}` 组（下标 ≡ {S['start']} mod {S['k']}），已需修改 `res = {S['res']}`" if 'start' in S else '')),
    ],
    watch=[('start', 'start', 'cyan'), ('index', 'index', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计需要修改的个数',
        'for start in range': '按间隔 `k` 拆开：这一组是 `arr[{start}], arr[{start}+k], ...`，组与组互不影响',
        'f = [arr[start]]': '`f` 从这一组的第一个数 `{f[0]}` 开始',
        'for index in range': lambda S, B, r: (f'看这一组的下一个数：`arr[{S.index}] = {S.arr[S.index]}`' if B.get('index') != S.index else '这一组扫完了'),
        'if arr[index] >= f[-1]': lambda S, B, r: (f'`{S.arr[S.index]} >= {S.f[-1]}`：不小于末尾，保持不动，直接接上' if S.arr[S.index] >= S.f[-1]
                                                   else f'`{S.arr[S.index]} < {S.f[-1]}`：接不上，必须改动某个数'),
        'f.append': '`f` 加入 `{arr[index]}`，这个数不用改',
        'l = 0': '二分区间 `[0, {len(f) - 1}]`：找 `f` 中第一个 `> {arr[index]}` 的位置',
        'while l < r': lambda S, B, r_: (f'区间 `[{S.l}, {S.r}]` 未收缩完' if S.l < S.r else f'`l = r = {S.l}`：位置找到'),
        'mid = ': '`mid = {mid}`',
        'if arr[index] >= f[mid]': lambda S, B, r: (f'`{S.arr[S.index]} >= f[{S.mid}] = {S.f[S.mid]}`：可以接在它后面，`l = mid + 1`' if S.arr[S.index] >= S.f[S.mid]
                                                    else f'`{S.arr[S.index]} < f[{S.mid}] = {S.f[S.mid]}`：位置在 mid 或更左，`r = mid`'),
        'f[l] = arr[index]': '`f[{l}]` 换成 `{arr[index]}`：这一位的末尾更小，后面更容易接上',
        'res += 1': '这个数没能接进最长不减序列，必须修改：`res = {res}`',
        'return res': '全部组需要修改的个数：=={res}==',
    },
    cards=dict(
        one_liner='隔 K 拆成独立的几组，每组留下最长不减子序列',
        complexity='时间 `O(n log n)`，空间 `O(n / k)`',
        problem=['`arr[i-k] <= arr[i]` 对所有 `i >= k` 成立，称 K 递增',
                 '每次可把一个数改成任意正整数，求最少操作次数',
                 '示例：`[4,1,5,2,6,2], k=3` → `2`；本视频：`[5,2,4,1,3,6,2,3], k=2` → `5`'],
        quote='不同K递增数组之间是互不影响的，因此可以先按间隔K将数组拆开得到若干个子序列，然后对每个子序列分别操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标模 k 相同的数连成一组，每组要变成不减的',
              '每组里最长不减序列保持不动，其余改掉',
              '代码里每次 `f[l] = ...` 的替换就计 1 次修改'],
        summary=['时间 `O(n log n)`，空间 `O(n / k)`',
                 '“不减”允许相等：二分用 `>=` 往右走',
                 '此写法用「接不上就记 1 次」计数，等于该组长度减最长不减子序列长度',
                 '原文是 Python 3 可运行写法，无需修改',
                 '同类题：300、1964、2826'],
    ),
)
