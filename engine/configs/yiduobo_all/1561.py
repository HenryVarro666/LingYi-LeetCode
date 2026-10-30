CONFIG = dict(
    num=1561, title='你可以获得的最大硬币数目', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='去掉 Bob · 桶排序',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1406'],
    code='''
class Solution(object):
    def maxCoins(self, piles):

        cnt_list = [0] * 10001
        for pile in piles:
            cnt_list[pile] += 1

        n = len(piles) // 3
        delta = 0
        res = 0
        for now in range(10000, 0, -1):
            cnt_list[now] += delta
            tmp = cnt_list[now] // 2
            if n <= tmp:
                return res + now * n
            else:
                n -= tmp
                res += now * tmp
                delta = cnt_list[now] % 2
''',
    call='Solution().maxCoins([9998,10000,9999,9998,9997,9996])',
    expect=19997,
    views=[
        dict(type='map', var=lambda S: {k: v for k, v in enumerate(S['cnt_list']) if v}, label='cnt_list 中非零的桶（硬币数 → 堆数）',
             fmt=lambda k, v: f'{k}: {v} 堆', h=300),
        dict(type='text', size=26, fn=lambda S: (f"还要拿 `n = {S['n']}` 次，已得 `res = {S['res']}`，上一档剩 `delta = {S['delta']}` 堆带到下一档" if 'delta' in S else '')),
    ],
    watch=['n', ('now', 'now', 'blue'), 'tmp', 'delta', ('res', 'res', 'green')],
    captions={
        'cnt_list = [0]': '硬币数不超过 `10000`，堆数更多 → 用桶排序，`cnt_list[x]` = 有 `x` 枚硬币的堆数',
        'cnt_list[pile] += 1': '`cnt_list[{pile}]` = {cnt_list[pile]}',
        'n = len': '去掉 Bob 后，每轮 Alice 拿最多、我拿次多 → 我一共拿 `len // 3 = {n}` 堆',
        'delta = 0': '`delta`：上一档奇数个时多出的一堆，要和这一档配对',
        'res = 0': '`res` 累计我拿到的硬币',
        'for now in range': '从大到小看每一档 `now = {now}`',
        'cnt_list[now] += delta': '这一档的堆数加上上一档剩下的 `delta`：`cnt_list[{now}]` = {cnt_list[now]}',
        'tmp = cnt_list': '每 2 堆里我拿 1 堆（Alice 拿大的）：`{cnt_list[now]} // 2 = {tmp}` 堆归我',
        'if n <= tmp': lambda S, B, r: (f'还要 `{S.n}` 堆 <= 这一档能拿 `{S.tmp}` 堆 → 拿完就返回' if S.n <= S.tmp else f'还要 `{S.n}` 堆 > `{S.tmp}`，这一档全拿，继续往小的找'),
        'return res + now * n': '最后 `{n}` 堆都按 `{now}` 算：`{res} + {now} × {n}` = =={ret}==',
        'n -= tmp': '还要拿的堆数 {B.n} → =={n}==',
        'res += now * tmp': '`res` += `{now} × {tmp}` → =={res}==',
        'delta = ': '这一档剩 `{cnt_list[now]} % 2 = {delta}` 堆，带到下一档',
    },
    cards=dict(
        one_liner='先扔掉 Bob，再从大到小每两堆我拿一堆',
        complexity='时间 `O(n + 10000)`，空间 `O(10000)`',
        problem=['`3n` 堆硬币，每轮选 3 堆：Alice 取最多，我取次多，Bob 取最少',
                 '求我最多能拿多少硬币',
                 '本视频：`[9998,10000,9999,9998,9997,9996]` → `19997`'],
        quote='首先可以排除掉干扰项bob。由于bob每次拿的都是最少的，因此每次都可以安排当前剩下硬币中最少的给bob，那么问题就变成了两个人分n * 2/3个硬币。',
        quote_src='—— yiduobo 题解原文',
        idea=['Bob 拿最少的，不用管；剩下的堆 Alice 和我轮着分',
              'Alice 拿最大，所以我拿次大：不拿次大，它之后也会被 Alice 拿走',
              '硬币数最多 `10000` → 桶排序，从大到小每两堆拿一堆'],
        summary=['时间 `O(n + 10000)`，空间 `O(10000)`',
                 '原文为 Python 2 写法，`/` 做整数除法已改为 `//`',
                 '易错：一档堆数为奇数时，多出的一堆要用 `delta` 带到下一档配对',
                 '对比灵神：灵神排序后切片 `piles[n//3::2]`，yiduobo 用桶排序省掉排序'],
    ),
)
