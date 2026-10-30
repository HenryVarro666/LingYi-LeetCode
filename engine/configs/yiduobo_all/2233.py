def _tbl(S):
    sc = S.get('sorted_cnt')
    return [f'{a}×{b}' for a, b in sc] if sc else []


def _info(S):
    if 'now' not in S:
        return '先数出每个数出现几次，再按数值从小到大排好'
    if 'delta' in S:
        return f"剩下 `k` 次平分给 `now` = {S['now']} 个最小值：每个加 `delta` = {S['delta']}，还多 `k % now` 个再加 1"
    return f"当前最小的 `{S['now']}` 个数一样高，还剩 `k` = =={S['k']}== 次可用"


CONFIG = dict(
    num=2233, title='K 次增加后的最大乘积', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='计数排序 + 抬平最小值（不用堆）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1686'],
    code='''
class Solution(object):
    def maximumProduct(self, nums, k):

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        sorted_cnt = sorted(cnt_dict.items(), key=lambda d:d[0])

        mod = 10 ** 9 + 7
        now = sorted_cnt[0][1]
        for index in range(1, len(sorted_cnt)):
            diff = sorted_cnt[index][0] - sorted_cnt[index - 1][0]
            if diff * now <= k:
                k -= diff * now
                now += sorted_cnt[index][1]
            else:
                res = 1
                for num, cnt in sorted_cnt[index:]:
                    for _ in range(cnt):
                        res = res * num % mod
                
                delta = k // now
                k %= now
                for _ in range(k):
                    res = res * (sorted_cnt[index - 1][0] + delta + 1) % mod
                for _ in range(k, now):
                    res = res * (sorted_cnt[index - 1][0] + delta) % mod
                
                return res

        res = 1
        delta = k // now
        k %= now
        for _ in range(k):
            res = res * (sorted_cnt[-1][0] + delta + 1) % mod
        for _ in range(k, now):
            res = res * (sorted_cnt[-1][0] + delta) % mod
        
        return res
''',
    call='Solution().maximumProduct([6, 3, 3, 2], 2)',
    expect=216,
    views=[
        dict(type='array', var=_tbl, label='sorted_cnt：数值 × 出现次数（从小到大）', pointers={'index': 'yellow'}, cell=110, h=190),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='text', fn=lambda S: (f"积累的乘积 `res` = =={S['res']}==" if 'res' in S else ''), size=26, h=60),
    ],
    watch=[('k', 'k', 'blue'), ('now', lambda S: S.get('now'), 'orange'), ('diff', lambda S: S.get('diff'), 'pink'), ('res', lambda S: S.get('res'), 'green')],
    skip=['for num in nums', 'for _ in range', 'cnt_dict[num] ='],
    captions={
        'cnt_dict = {}': '用字典 `cnt_dict` 统计每个数出现的次数',
        'mod = ': '答案对 `10^9 + 7` 取模，边乘边取',
        'sorted_cnt = sorted': '先统计每个数出现几次，再按数值排序：`sorted_cnt` = =={sorted_cnt}==',
        'now = sorted_cnt[0][1]': '`now` = 当前==最小值==的个数 = `{now}`（操作只会落在这些数上）',
        'for index in range(1, len(sorted_cnt))': lambda S, B, r: (
            f'看下一档：最小值是 `{S.sorted_cnt[S.index - 1][0]}`，次小值是 `{S.sorted_cnt[S.index][0]}`' if 'index' in S and B.get('diff') is None
            else '逐档往上看：把当前最小的几个数抬到次小值那么高'),
        'diff = ': '把 `now` = {now} 个最小值抬到次小值，每个要加 `diff` = =={diff}==',
        'if diff * now <= k': lambda S, B, r: (f'一共需要 `{S.diff} × {S.now}` = {S.diff * S.now} 次，`k` = {S.k}：' +
                                              ('够用 → 全部抬到次小值' if S.diff * S.now <= S.k else '==不够== → 把剩下的 `k` 次平均分给它们')),
        'k -= diff * now': '花掉 {diff * now} 次，剩 `k` = =={k}==',
        'now += sorted_cnt[index][1]': '次小值并入最小的一档：现在有 `{now}` 个数一样高',
        'res = 1': '`k` 不够再往上抬了：先把更大的数（不会再动）连乘起来',
        'res = res * num % mod': '`res = {B.res} × {num} % mod` = =={res}==',
        'delta = k // now': '剩下 `k` = {k} 次平分给 `{now}` 个数：每个加 `{k} // {now}` = =={delta}==',
        'k %= now': '还多出 `k % now` = =={k}== 次：这几个数再多加 1',
        'res = res * (sorted_cnt[index - 1][0] + delta + 1)': '多加了 1 的数是 `{sorted_cnt[index - 1][0]} + {delta} + 1` = {sorted_cnt[index - 1][0] + delta + 1}，`res` = =={res}==',
        'res = res * (sorted_cnt[index - 1][0] + delta) ': '没多加的数是 `{sorted_cnt[index - 1][0]} + {delta}` = {sorted_cnt[index - 1][0] + delta}，`res` = =={res}==',
        'return res': '返回 =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='把操作全用在最小值上：先抬平，抬不动了再平均分',
        complexity='时间 `O(n log n)`（排序）+ `O(n)`，空间 `O(n)`',
        problem=['非负整数数组 `nums`，每次可以让任意一个数加 `1`，最多 `k` 次',
                 '求操作后数组的==最大乘积==，对 `10^9 + 7` 取模',
                 '本视频：`nums = [6,3,3,2]`，`k = 2` → `216`'],
        quote='首先可以明确的一点是，每一次都应该将当前的最小值加1。……我采用的做法是先统计每个数出现的次数，然后按数值的大小从小到大将这个次数数组进行排序。',
        quote_src='—— yiduobo 题解',
        idea=['结论：每一次都给==当前最小值==加 1（交换论证：不操作最小值，换成操作它不会更差）',
              '用堆一次次加 1 太慢？这里把最小值按档位「一起抬」：`diff × now` 次把最小的 `now` 个数抬到次小值',
              '`k` 不够抬一档时，把剩下的次数==平均分==：每个加 `k // now`，多出 `k % now` 个再加 1'],
        summary=['排序 `O(n log n)`，之后一趟扫描；空间 `O(n)`',
                 '原文为 Python 2 写法：`delta = k / now` 是整数除法，已改为 `k // now`',
                 '易错：`k` 不够抬一档，和「所有数都抬到最大值」是两个出口，平分的逻辑一样写了两遍',
                 '平均分才让最小的几个数尽量接近，乘积最大；另解：最小堆每次加 1（灵神写法）'],
    ),
)
