CONFIG = dict(
    num=3861, title='容量最小的箱子', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 直接比较答案对应容量',
    code='''
class Solution(object):
    def minimumIndex(self, capacity, itemSize):
        
        res = -1
        for index, c in enumerate(capacity):
            if c >= itemSize and (res == -1 or capacity[res] > c):
                res = index
        
        return res
''',
    call='Solution().minimumIndex([6,3,5,4,5,7], 4)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"物品大小 `itemSize = {S['itemSize']}`，当前答案 `res = {S['res']}`" + (f"（容量 {S['capacity'][S['res']]}）" if S.get('res', -1) >= 0 else '') if 'res' in S else f"物品大小 `itemSize = {S['itemSize']}`"),
        dict(type='array', var='capacity', pointers={'index': 'blue', 'res': 'green'}, h=330, label='capacity',
             color=lambda S, k, v: 'green' if S.get('res', -1) == k else None,
             dim=lambda S, k, v: v < S['itemSize']),
    ],
    watch=[('index', 'index', 'blue'), ('c', 'c', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = -1': '`res = -1`：初始答案为 -1，表示还没有可用的箱子',
        'if c >= itemSize': lambda S, B, r: (
            f'`c = {S.c} >= {S.itemSize}` 且 ' + ('`res == -1`，还没有答案 → ==成立==' if S.res == -1 and S.c >= S.itemSize
            else f'`capacity[res] = {S.capacity[S.res]} > {S.c}` → ==成立==，这个箱子更小' if S.c >= S.itemSize and S.capacity[S.res] > S.c
            else f'`capacity[res] = {S.capacity[S.res]} > {S.c}` 不成立 → 跳过') if S.c >= S.itemSize
            else f'`c = {S.c} < itemSize = {S.itemSize}`：装不下 → 跳过'),
        'res = index': '答案更新为当前下标：`res = {index}`',
        'return res': '遍历完成，答案 `res = {res}`',
    },
    cards=dict(
        one_liner='一趟遍历：装得下，且比当前答案的箱子更小就更新',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`capacity[index]` 是第 index 个箱子的容量',
                 '容量 `>= itemSize` 才能放下物品，求容量最小的箱子下标',
                 '多个容量相同取下标最小；没有可用箱子返回 `-1`'],
        quote='若当前的capacity[index]大于等于itemSize，且目前的答案为-1，或者目前答案对应的箱子容量大于当前的capacity[index]，就将答案更新为index即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把答案设为 `-1`，表示还没找到',
              '不额外存最小容量，而是用 `capacity[res]` 取出答案对应的容量来比较',
              '只在严格更小时才更新，所以相同容量保留下标靠前的'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res == -1` 要放在 `or` 前面：避免用 `capacity[-1]` 误取最后一个箱子',
                 '原文为 Python 2 风格，只删去了类型说明，无其他改动',
                 '对比灵神：灵神单独维护 `min_c`，yiduobo 通过 `capacity[res]` 间接取'],
    ),
)
