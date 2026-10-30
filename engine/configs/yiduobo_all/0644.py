NUMS = [6, -3, 10, -9, 6, -5]
K = 2


def _iv(S):
    iv = S.get('intervals')
    if iv is None:
        return None
    return [f'{round(a, 1):g}/{c}' for a, c in iv]


def _win(S):
    if 'now' not in S:
        return '窗口 = 最后 k 个数 + 左边还没被移除的区间'
    return f'窗口：和 `{S["now"]:g}` ÷ 个数 `{S["cnt"]}` = =={S["now"] / S["cnt"]:.2f}=='


CONFIG = dict(
    num=644, title='子数组最大平均数 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='区间合并 + 双端队列',
    tags=['二分算法'],
    code='''
class Solution(object):
    def findMaxAverage(self, nums, k):

        intervals = deque()

        now = sum(nums[:k]) * 1.0
        cnt = k
        res = now / cnt
        for index, num in enumerate(nums[k:]):
            now += num
            cnt += 1
            s = nums[index] * 1.0
            s_cnt = 1
            while intervals:
                last_s, last_cnt = intervals[-1]
                if last_s * s_cnt >= s * last_cnt:
                    intervals.pop()
                    s += last_s
                    s_cnt += last_cnt
                else:
                    break
            
            intervals.append([s, s_cnt])

            while intervals:
                first_s, first_cnt = intervals[0]
                if first_s * cnt <= now * first_cnt:
                    intervals.popleft()
                    now -= first_s
                    cnt -= first_cnt
                else:
                    break
            
            res = max(res, now / cnt)
        
        return res
''',
    call=f'Solution().findMaxAverage({NUMS}, {K})',
    expect=13 / 3,
    views=[
        dict(type='array', var='nums', label='nums（暗 = 已移出窗口，蓝框 = 当前窗口，index = 本轮刚能移除的数）',
             pointers={'index': 'pink'}, cell=100, h=230,
             dim=lambda S, i, v: 'cnt' in S and 'index' in S and not (S['index'] + K + 1 - S['cnt'] <= i <= S['index'] + K),
             color=lambda S, i, v: 'pink' if S.get('index') == i else None),
        dict(type='array', var=_iv, label='intervals：可移除的区间（和/个数），从左到右平均值递增', cell=130, h=170),
        dict(type='text', fn=_win, size=26, h=80),
    ],
    watch=[('now', 'now', 'blue'), ('cnt', 'cnt', 'blue'), ('s', 's', 'orange'), ('s_cnt', 's_cnt', 'orange'), ('res', 'res', 'green')],
    skip=['intervals = deque()', 'cnt = k', 'cnt += 1', 's_cnt = 1', 'last_s, last_cnt', 'first_s, first_cnt',
          's_cnt += last_cnt', 'cnt -= first_cnt', 'break'],
    captions={
        'now = sum(nums[:k])': '先取最前面 `k = {k}` 个数当窗口：和 `now` = =={now:g}==（窗口至少要 k 个数）',
        'res = now / cnt': '当前窗口平均 `{now:g} / {cnt}` = =={res:.2f}==，先记为答案',
        'enumerate(nums[k:])': lambda S, B, r: ('所有数都处理完，for 循环结束' if 'index' in B and B['index'] == S['index'] else f'右边界扩到 `{S["num"]}`；保证最后 k 个数留在窗口后，`nums[{S["index"]}] = {S["nums"][S["index"]]}` 成了本轮==可以被移除==的数'),
        'now += num': '新数 `{num}` 进窗口：和 `now` = {now:g}，个数 `cnt` = {cnt}',
        's = nums[index]': '把可移除的 `{nums[index]}` 先当成一个==独立区间==：和 `s` = {s:g}，个数 1',
        'if last_s * s_cnt >= s * last_cnt': lambda S, B, r: (
            f'比平均（交叉相乘免除法）：左边区间 `{S["last_s"]:g}/{S["last_cnt"]}` = {S["last_s"] / S["last_cnt"]:.2f}，'
            f'新区间 `{S["s"]:g}/{S["s_cnt"]}` = {S["s"] / S["s_cnt"]:.2f} → '
            + ('新区间不比左边好：选了它就该连左边一起选，==两段并成一段==' if S['last_s'] * S['s_cnt'] >= S['s'] * S['last_cnt']
               else '新区间更好，保持独立')),
        'intervals.pop()': '左边的区间从队尾弹出，准备和新区间合并',
        's += last_s': '合并：新区间变成 `{s:g}/{s_cnt + last_cnt}`（平均 {s / (s_cnt + last_cnt):.2f}），再继续和更左边的比',
        'intervals.append': ('队尾放入这个区间 `{s:g}/{s_cnt}`：它比左边的区间都好，'
                             '所以 `intervals` 的平均值==从左到右递增=='),
        'if first_s * cnt <= now * first_cnt': lambda S, B, r: (
            f'比队头区间平均 `{S["first_s"] / S["first_cnt"]:.2f}` 和窗口平均 `{S["now"] / S["cnt"]:.2f}`：'
            + ('队头不比整体好，==在拖后腿，整段移出==' if S['first_s'] * S['cnt'] <= S['now'] * S['first_cnt']
               else '队头比整体好，留着；它是平均最低的一段，后面更不用看')),
        'intervals.popleft()': '队头是平均最低的一段，先把它从队列拿掉',
        'now -= first_s': '窗口里扣掉这一整段：`now` = =={now:g}==，`cnt` 随后减去它的个数',
        'res = max': '用当前窗口平均更新答案：`max({B.res:.2f}, {now:g}/{cnt}={now / cnt:.2f})` = =={res:.2f}=='.replace('{B.res:.2f}', '{B.res:.2f}'),
        'return res': '返回最大平均数 =={res:.4f}=='
    },
    cards=dict(
        one_liner='窗口移除的不是单个数，而是一整段平均更低的区间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums`，找长度 ==至少为 k== 的连续子数组，使平均数最大',
                 '返回这个最大平均数',
                 '示例：`[6,-3,10,-9,6,-5]`，`k = 2` → `13/3 ≈ 4.333`（子数组 `[6,-3,10]`）'],
        quote='如果其平均值比之前的区间要好，就应该将其保持独立；反过来，就应该将其融入到之前的区间中。重复此过程直到出现情况1。',
        quote_src='—— yiduobo 题解原文',
        idea=['好数会给坏数“打掩护”：`[50,-100,-100,150]` 里 50 保护了后面的 -100',
              '所以窗口左端按“区间”移除：新可移除的数，平均不如左边就并入左边',
              '`intervals` 平均值递增；队头比窗口平均低就整段弹出，用双端队列 `O(n)`'],
        summary=['时间 `O(n)`：每个数最多合并一次、弹出一次',
                 '比较平均用交叉相乘 `a*c2 >= b*c1`，避免除法精度问题',
                 '易错：窗口里至少留 k 个数，所以只能处理 `nums[index]`（离右端 k 之外）',
                 '这是会员题；也可以二分平均值 + 前缀和判断，原文用区间合并',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
