CONFIG = dict(
    num=444, title='序列重建', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序判唯一',
    tags=['图论算法', '拓扑排序'],
    code='''
class Solution(object):
    def sequenceReconstruction(self, nums, sequences):

        ind = {}
        g = {}
        for seq in sequences:
            if len(seq) == 1:
                if seq[0] not in ind:
                    ind[seq[0]] = 0
                continue

            for index in range(1, len(seq)):
                x, y = seq[index - 1], seq[index]
                if x not in g:
                    g[x] = set()
                if x not in ind:
                    ind[x] = 0
                if y not in ind:
                    ind[y] = 0
                
                if y not in g[x]:
                    ind[y] += 1
                    g[x].add(y)
        
        q = []
        for x in ind:
            if ind[x] == 0:
                q.append(x)
        
        if len(q) > 1:
            return False
        
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
            
            head, tail = tail, len(q)
            if tail - head > 1:
                return False

        if len(q) != len(ind):
            return False
        
        return q == nums
''',
    call='Solution().sequenceReconstruction([1, 2, 3, 4], [[1, 2], [1, 3], [2, 3], [3, 4]])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（要判断的唯一序列）', h=130,
             color=lambda S, i, v: 'green' if 'q' in S and i < len(S['q']) and S['q'][i] == v else None),
        dict(type='map', var='ind', label='ind：每个数的入度', h=170, fmt=lambda k, v: f'{k}: 入度 {v}'),
        dict(type='map', var='g', label='g：有向边 x → {y...}', h=170, fmt=lambda k, v: f'{k} → {sorted(v)}'),
        dict(type='array', var='q', label='q：拓扑序（head~tail 是当前这一层）', h=130, pointers={'head': 'blue', 'tail': 'pink'}),
    ],
    watch=['x', 'y', 'head', 'tail', ('q', 'q', 'cyan')],
    captions={
        'x, y = seq': '序列相邻两个数 `{x}` 必须在 `{y}` 前面：建边 `{x} → {y}`',
        'ind[y] += 1': '新边 `{x}→{y}`：`{y}` 入度 +1 → `{ind[y]}`（重复的边不再算）',
        'if len(seq) == 1': lambda S, B, r: f'序列 `{S.seq}` 长度 {len(S.seq)}' + ('：没有边，只登记这个数' if len(S.seq) == 1 else '，有相邻对，要建边'),
        'q.append(x)': '入度为 0 的点 `{x}` 入队，它们可以排在最前面',
        'if len(q) > 1': lambda S, B, r: f'起点有 `{len(S.q)}` 个' + ('：两个都能排第一 → 序列不唯一，返回 False' if len(S.q) > 1 else '：只有一个，排第一位是确定的'),
        'ind[next] -= 1': '删掉边 `{now}→{next}`：`{next}` 入度 -1 → `{ind[next]}`',
        'q.append(next)': '`{next}` 入度变 0，可以放进下一层',
        'head, tail = tail, len(q)': '这一层处理完，下一层是 `q[{head}:{tail}]`，共 `{tail-head}` 个',
        'if tail - head > 1': lambda S, B, r: f'下一层有 `{S.tail - S.head}` 个点' + ('：它们先后顺序不定 → 序列不唯一，返回 False' if S.tail - S.head > 1 else ('：只有一个，顺序唯一' if S.tail > S.head else '：没有新点了，拓扑结束')),
        'if len(q) != len(ind)': lambda S, B, r: f'排出 `{len(S.q)}` 个点，图里共 `{len(S.ind)}` 个点' + ('：有环或缺数 → False' if len(S.q) != len(S.ind) else '：全部排出'),
        'return q == nums': '拓扑序 `{q}` 是否等于 `nums`：=={q == nums}==',
    },
    skip=['ind = {}', 'g = {}', 'q = []', 'for seq in', 'for index in range', 'if x not in g', 'if x not in ind', 'if y not in ind',
          'g[x] = set()', 'ind[x] = 0', 'ind[y] = 0', 'g[x].add', 'continue', 'if y not in g[x]', 'head, tail = 0, 1', 'while head < tail',
          'for now in', 'for next in', 'for x in ind', 'if ind[x] == 0', 'if ind[next] == 0', 'if seq[0] not in ind', 'ind[seq[0]] = 0'],
    max_steps=100,
    cards=dict(
        one_liner='按序列相邻关系建图，逐层拓扑，每层只能有一个点',
        complexity='时间 `O(n + 序列总长)`，空间 `O(n + 序列总长)`',
        problem=['`nums` 是 `1..n` 的排列，`sequences` 里每个序列都是它的子序列',
                 '问：`nums` 是否==唯一的==、最短的、能让所有序列都是子序列的序列',
                 '本视频：`nums=[1,2,3,4]`，`[[1,2],[1,3],[2,3],[3,4]]` → `True`'],
        quote='若最终得到的序列是唯一的，且处理到了所有的n个点，那么就返回true，否则就返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['序列里相邻的 `x, y` 说明 `x` 必须在 `y` 前，连一条有向边',
              '拓扑排序结果唯一 ⇔ 每一层入度为 0 的点只有一个',
              '最后还要比较拓扑序是否等于 `nums`，并且点数要齐'],
        summary=['时间空间都是 `O(n + 序列总长)`',
                 '易错：==重复边不能重复加入度==，要用 `set` 去重',
                 '易错：长度为 1 的序列也要把这个数登记进 `ind`',
                 '任一层出现多个入度为 0 的点，立刻返回 False',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改'],
    ),
)
