CONFIG = dict(
    num=2808, title='使循环数组所有元素相等的最少秒数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表收集位置 · BFS 扩散推导',
    tags=[],
    code='''
class Solution(object):
    def minimumSeconds(self, nums):

        pos = {}
        for index, v in enumerate(nums):
            if v not in pos:
                pos[v] = []
            pos[v].append(index)
        
        res = None
        for v in pos:
            if len(pos[v]) == 1:
                if res is None or res > len(nums)// 2:
                    res = len(nums) // 2
            else:
                ma = (len(nums) - 1 - pos[v][-1] + pos[v][0] + 1) // 2
                for index in range(1, len(pos[v])):
                    ma = max(ma, (pos[v][index] - pos[v][index - 1]) // 2)
                
                if res is None or res > ma:
                    res = ma
        
        return res
''',
    call='Solution().minimumSeconds([2, 1, 3, 3, 2, 1, 3, 4])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 当前目标值 v 出现的位置）', cell=84, h=200,
             color=lambda S, i, v: 'green' if 'v' in S and 'pos' in S and S['v'] in S['pos'] and i in S['pos'][S['v']] and 'res' in S else None),
        dict(type='map', var='pos', label='pos[v] = v 出现的下标', h=240, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=28, fn=lambda S: (f"目标 `v = {S['v']}`：当前最大空隙一半 `ma = {S['ma']}`" if 'ma' in S and 'v' in S and 'res' in S and len(S['pos'][S['v']]) > 1 else '')),
    ],
    watch=['v', ('ma', 'ma', 'pink'), ('res', 'res', 'green')],
    captions={
        'pos[v].append': '`{v}` 出现在下标 `{index}`：`pos[{v}] = {pos[v]}`',
        'res = None': '`res` 记录目标值里最小的步数，先设为空',
        'if len(pos[v]) == 1': '目标 `v = {v}` 出现 `{len(pos[v])}` 次 → {"只有一个，要扩散整个环" if len(pos[v]) == 1 else "有多个，看相邻两个之间的空隙"}',
        'res = len(nums)': '只有一个 `{v}`：向两边 BFS，轮次 = `n // 2 = {len(nums) // 2}` → `res = {res}`',
        'ma = (len': '环形的头尾也要算：`(n - 1 - 最后位置 + 第一个位置 + 1) // 2` = =={ma}==',
        'for index in range(1': '再逐对看相邻位置的空隙：共 `{len(pos[v]) - 1}` 对',
        'ma = max': '相邻两个 `{v}` 之间距离 `{pos[v][index] - pos[v][index - 1]}`，从中间碰头要 `// 2` 轮 → `ma = {ma}`',
        'res = ma': '目标 `{v}` 需要 `{ma}` 轮，比当前最优小 → `res = {res}`',
        'return res': '所有目标值里最少的轮数 =={ret}==',
    },
    cards=dict(
        one_liner='枚举目标值，从它所有位置同时 BFS，最后碰头的位置决定轮数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每秒每个位置可换成自己或左右邻居的值（环形，同时替换）',
                 '求让整个数组相等的最少秒数',
                 '示例：`[2,1,3,3,2]` → `2`；视频用 `[2,1,3,3,2,1,3,4]`'],
        quote='不妨设当前的目标值为target，那么问题就相当于从数组中所有原始值为target的位置出发，每一轮向左右两侧进行bfs直到遍历完整个数组位置。',
        quote_src='—— yiduobo 题解',
        idea=['目标值只能是 `nums` 里已有的数，先用哈希表收集每个数的所有位置',
              '多个 `target` 同时扩散，最后碰头在两个相邻位置的正中间，轮数 = 距离 `// 2`',
              '只有一个 `target` 时轮数是 `n // 2`；环形的头尾间距也要算'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错点：头尾间距是 `n - 1 - 最后 + 第一个 + 1`，别漏掉',
                 '`res` 初值为 `None`，第一次比较要特判'],
    ),
)
