CONFIG = dict(
    num=3645, title='最优激活顺序得到的最大总和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 · 逐个 l 取 limit 恰为 l 的前 l 个',
    tags=['灵神题单', '难度分 2019'],
    code='''
class Solution(object):
    def maxTotal(self, value, limit):
        
        info = sorted(zip(value, limit), key=lambda d:(d[1], -d[0]))
        p = 0
        res = 0
        for l in range(1, len(info) + 1):
            while p < len(info) and info[p][1] < l:
                p += 1
            if p == len(info):
                break
            
            cnt = 0
            while cnt < l and p < len(info) and info[p][1] == l:
                res += info[p][0]
                p += 1
                cnt += 1
        
        return res
''',
    call='Solution().maxTotal([4,1,5,2,7], [3,3,2,3,3])',
    expect=18,
    views=[
        dict(type='array', var='info', label='info = (value, limit)，按 limit 升序、value 降序', pointers={'p': 'blue'}, cell=120, h=240),
        dict(type='text', fn=lambda S: (f"阈值 `l = {S['l']}`，已选 `cnt = {S['cnt']}` 个（最多 `{S['l']}` 个）" if 'l' in S and 'cnt' in S else ('阈值 `l`：从 1 枚举到 n' if 'info' in S else '')), size=30, h=80),
    ],
    watch=[('p', 'p', 'blue'), 'l', 'cnt', ('res', 'res', 'green')],
    captions={
        'info = sorted': '先按 `limit` 从小到大、同 limit 里按 `value` 从大到小排好：==每组最前面的就是最值钱的==',
        'p = 0': '`p` 指向下一个还没处理的元素',
        'res = 0': '`res` 累计总和',
        'for l in range': '枚举 limit 阈值 `l = {l}`：只看 `limit` 恰为 {l} 的那一组',
        'info[p][1] < l': lambda S, B, r: (f'`info[{S.p}][1] < {S.l}`？limit 太小的组已经处理完 → `p` 后移' if S.p < len(S.info) and S.info[S.p][1] < S.l
                                           else '`limit` 已不小于 `l`，停在这一组的开头'),
        'p += 1\n': '`p` → {p}',
        'if p == len(info)': lambda S, B, r: ('`p` 走到末尾：没有 limit 更大的元素了 → 结束' if S.p == len(S.info) else '还有元素，继续取这一组'),
        'cnt = 0': '这一组已取 `0` 个',
        'while cnt < l': lambda S, B, r: (f'`cnt = {S.cnt} < l = {S.l}` 且 `limit == {S.l}` → 继续取' if S.cnt < S.l and S.p < len(S.info) and S.info[S.p][1] == S.l
                                           else (f'已取满 `{S.l}` 个，这组剩下的会永久失效 → 到下一个 `l`' if S.cnt >= S.l
                                                 else f'这一组取完了（不足 `{S.l}` 个也只能有多少算多少）')),
        'res += info[p][0]': '取这一组当前最大的 `{info[p][0]}`：`res` = =={res}==',
        'cnt += 1': '这组已取 `{cnt}` 个',
        'return res': '最大总和 `{res}`',
    },
    cards=dict(
        one_liner='按 limit 从小到大，每个 limit 只取最贵的 limit 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['激活元素要求当前活跃数小于它的 `limit`，激活可得 `value`',
                 '激活后活跃数为 x，`limit <= x` 的元素永久失效',
                 '示例：`value=[4,1,5,2], limit=[3,3,2,3]` → `12`'],
        quote='如果先激活limit较大的元素，limit较小的元素可能就无法再激活了。但是如果先激活limit较小的元素，是不会影响到limit较大的元素的。',
        quote_src='—— yiduobo 题解原文',
        idea=['limit 相同的元素，最多只能激活 `limit` 个，要选 ==value 最大==的',
              '全部元素先按 `(limit, -value)` 排序，同组里大的在前',
              '枚举 `l = 1..n`，指针 `p` 跳到 `limit >= l`，再取最多 `l` 个 `limit == l` 的'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '组内不足 `l` 个也没关系：后面的元素激活时它们会失效',
                 '`while p < len(info) and info[p][1] < l`：跳过 limit 更小、已经处理过的组',
                 '原文本身可直接在 Python 3 运行，没有改动',
                 '对比灵神：灵神用哈希表分组再排序；yiduobo 一次全局排序 + 指针扫'],
    ),
)
