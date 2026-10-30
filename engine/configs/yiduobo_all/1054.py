CONFIG = dict(
    num=1054, title='距离相等的条形码', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最大堆 · 每轮取最多的两种',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def rearrangeBarcodes(self, barcodes):

        num_dict = {}
        for num in barcodes:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        heap = [[-x[1], x[0]] for x in num_dict.items()]
        heapq.heapify(heap)

        res = []
        while heap:
            if len(heap) < 2:
                res.append(heap[0][1])
                break
            
            cnt1, num1 = heapq.heappop(heap)
            cnt2, num2=  heapq.heappop(heap)
            res.append(num1)
            res.append(num2)

            cnt1 += 1
            if cnt1 < 0:
                heapq.heappush(heap, [cnt1, num1])
            
            cnt2 += 1
            if cnt2 < 0:
                heapq.heappush(heap, [cnt2, num2])
        
        return res
''',
    call='Solution().rearrangeBarcodes([1,1,1,2,2,3,3])',
    expect=[1, 2, 1, 3, 1, 2, 3],
    views=[
        dict(type='array', var='barcodes', label='barcodes', h=170),
        dict(type='map', var='num_dict', label='num_dict（条形码 → 次数）', fmt=lambda k, v: f'{k}: {v}', h=140),
        dict(type='heap', var='heap', label='heap', fmt=lambda x: f'{x[1]}×{-x[0]}', h=230),
        dict(type='array', var='res', label='res（已排好）', h=170),
    ],
    watch=['cnt1', 'num1', 'cnt2', 'num2', ('res', 'res', 'green')],
    captions={
        'num_dict[num] =': '统计次数：`{num}` 出现 =={num_dict[num]}== 次',
        'heap = [': '把 `(次数, 条形码)` 放进堆，次数取负 → ==堆顶是剩余最多的==',
        'cnt1, num1 = heapq.heappop': '弹出剩余最多的：条形码 `{num1}`，还剩 `{-cnt1}` 个',
        'cnt2, num2=': '再弹出次多的：条形码 `{num2}`，还剩 `{-cnt2}` 个',
        'res.append(num1)': '`{num1}` 放前面',
        'res.append(num2)': '`{num2}` 紧跟其后：==一组两个不同的数，永远不会相邻重复==',
        'cnt1 += 1': '用掉一个 `{num1}`，剩余 `{-cnt1}` 个（取负后 +1）',
        'cnt2 += 1': '用掉一个 `{num2}`，剩余 `{-cnt2}` 个',
        'if cnt1 < 0': '`{num1}` 还剩 `{-cnt1}` 个 → {"==放回堆里，下一轮继续竞争==" if cnt1 < 0 else "==用完了，不再放回=="}',
        'if cnt2 < 0': '`{num2}` 还剩 `{-cnt2}` 个 → {"==放回堆里==" if cnt2 < 0 else "==用完了，不再放回=="}',
        'if len(heap) < 2': '堆里不足两种了吗？`len(heap) = {len(heap)}`',
        'res.append(heap[0][1])': '只剩一种：直接放最后一个（题目保证有解，这里只会剩 1 个）',
    },
    cards=dict(
        one_liner='每轮取剩余最多的两种，各放一个',
        complexity='时间 `O(n log k)`，空间 `O(k)`（k 为种类数）',
        problem=['给一个条形码数组 `barcodes`，重新排列使 ==相邻两个不相同==',
                 '题目保证答案存在，返回任意一个即可',
                 '示例：`[1,1,1,2,2,3,3]` → 如 `[1,2,1,3,1,2,3]`'],
        quote='每一轮都应该尽可能地使用掉当前剩下条形码中数目最多的那一种。……可以两个条形码为一组，每次从条形码中选出剩余数量最多以及第二多的那两种即可。',
        quote_src='—— yiduobo 题解',
        idea=['数量最多的最容易“撞车”，所以优先消耗它',
              '两个不同的数为一组：组内不可能重复',
              '下一组里次多的 B 不会比 A 多，所以不会出现 `(B, X)` 紧接 `A, B` 的冲突'],
        summary=['时间 `O(n log k)`，每个数最多进出堆一次/轮',
                 '堆里存 `[-次数, 数值]`：Python 只有最小堆，取负变最大堆',
                 '只剩一种时直接追加；有解保证它只剩 1 个',
                 '原文为 Python 2 写法，本题代码无需修改即可在 Python 3 运行'],
    ),
)
