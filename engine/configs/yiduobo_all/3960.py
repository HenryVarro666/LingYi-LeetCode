CONFIG = dict(
    num=3960, title='频率平衡子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举起点 + 频率的频率',
    code='''
class Solution(object):
    def getLength(self, nums):
        
        res = 0
        for start in range(len(nums)):
            freq = {}
            freq_freq = {}
            for index in range(start, len(nums)):
                v = nums[index]
                freq[v] = freq.get(v, 0) + 1
                if freq[v] == 1:
                    freq_freq[1] = freq_freq.get(1, 0) + 1
                else:
                    freq_freq[freq[v] - 1] -= 1
                    if freq_freq[freq[v] - 1] == 0:
                        freq_freq.pop(freq[v] - 1)
                    freq_freq[freq[v]] = freq_freq.get(freq[v], 0) + 1

                if len(freq) == 1 or (len(freq_freq) == 2 and max(freq.values()) == 2 * min(freq.values())):
                    res = max(res, index - start + 1)

        return res
''',
    call='Solution().getLength([1,2,2,3,3])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前子数组）', cell=90, h=240,
             pointers={'start': 'blue', 'index': 'pink'},
             window=(lambda S: S.get('start') if 'freq' in S else None, lambda S: S.get('index') if 'freq' in S else None)),
        dict(type='map', var='freq', label='freq（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='map', var='freq_freq', label='freq_freq（出现次数 → 有几种元素）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', h=90, size=30, fn=lambda S: (f"频率种类 `{len(S['freq_freq'])}`，最大/最小 = `{max(S['freq'].values())}` / `{min(S['freq'].values())}`" if S.get('freq') and S.get('freq_freq') else '')),
    ],
    watch=[('start', 'start', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记最长的频率平衡子数组长度',
        'for start in': '枚举子数组起点 `start = {start}`，哈希表清空重来',
        'freq = {}': '`freq` 记子数组里每个元素的频率',
        'freq_freq = {}': '`freq_freq` 记「每种频率有几种元素」',
        'for index in': '向右扩展终点 `index = {index}`，把 `nums[{index}]` 加入子数组',
        'v = nums[index]': '新加入元素 `v = {v}`',
        'freq[v] = freq.get': '`freq[{v}]` 加一 → =={freq[v]}==',
        'if freq[v] == 1': lambda S, B, r: (f'`freq[{S.v}] = 1`：新元素，出现 1 次的元素多一种' if S.freq[S.v] == 1 else f'`freq[{S.v}] = {S.freq[S.v]}`：老元素，它的频率从 {S.freq[S.v]-1} 升到 {S.freq[S.v]}'),
        'freq_freq[1] = ': '`freq_freq[1]` → {freq_freq[1]}',
        'freq_freq[freq[v] - 1] -= 1': '频率 `{freq[v]-1}` 的元素少了一种（`v` 升级走了）',
        'if freq_freq[freq[v] - 1] == 0': '频率 `{freq[v]-1}` 已没有元素 → 删掉这一项，保证 `len(freq_freq)` 就是不同频率的种数',
        'freq_freq.pop': '`pop` 掉频率 {freq[v]-1}',
        'freq_freq[freq[v]] = ': '频率 `{freq[v]}` 的元素多了一种 → `freq_freq[{freq[v]}]` = {freq_freq[freq[v]]}',
        'if len(freq) == 1': lambda S, B, r: (
            f'只有 1 种元素 → ==平衡==' if len(S.freq) == 1 else
            (f'恰好 2 种频率，最大 `{max(S.freq.values())}` == 2 × 最小 `{min(S.freq.values())}` → ==平衡==' if len(S.freq_freq) == 2 and max(S.freq.values()) == 2 * min(S.freq.values())
             else (f'有 {len(S.freq_freq)} 种频率，不是「恰好 2 种」→ 不平衡' if len(S.freq_freq) != 2 else f'2 种频率但 `{max(S.freq.values())}` ≠ 2 × `{min(S.freq.values())}` → 不平衡'))),
        'res = max(res': '子数组 `[{start}..{index}]` 平衡：`res = max({B.res}, {index - start + 1})` = =={res}==',
        'return res': '最长频率平衡子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='枚举起点，用「频率的频率」判断两种频率是否 1:2',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['子数组平衡：只含一种元素，或各元素频率只有两种 `f` 与 `2f`',
                 '求最长的平衡子数组长度，`n ≤ 1000`',
                 '本视频：`[1,2,2,3,3]` → `5`（频率 1、2、2）'],
        quote='恰好包含两种不同频率的子数组，且较大的频率是较小频率的两倍。需要注意这里的两种不同频率，对应的不一定是只有两种元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 只有 1000，直接枚举起点 `start`，再逐个加入终点',
              '`freq` 记元素频率，`freq_freq` 记「某个频率有几种元素」',
              '`len(freq) == 1`，或 `freq_freq` 恰有 2 项且最大频率 == 2×最小频率，则平衡'],
        summary=['时间 `O(n²)`（`max/min(freq.values())` 在种类多时更慢），空间 `O(n)`',
                 '易错点：频率降到 0 的项必须 `pop`，否则 `len(freq_freq)` 会算错',
                 '只有一种元素是单独的一类，不能靠 `freq_freq` 判断',
                 '对比灵神：灵神先特判并以最长连续段为初值，再剪枝；yiduobo 不剪枝',
                 '原文为 Python 2 写法，在 Python 3 下无需改动'],
    ),
)
