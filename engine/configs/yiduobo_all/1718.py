_NOW = lambda S: S['_inner'].get('now')


def _pair(S):
    i = S['_inner']
    if 'num' in i and 'now' in i and i['num'] != 1 and 0 <= i['now'] + i['num'] < len(S['res']):
        return i['now'] + i['num']
    return None


CONFIG = dict(
    num=1718, title='构造字典序最大的可行序列', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='构造开头 + DFS 回溯',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def constructDistancedSequence(self, n):

        if n == 1:
            return [1]
        elif n == 2:
            return [2, 1, 2]
        else:
            res = [n, n - 2] + [0] * (n * 2 - 3)
            res[n] = n
            if n > 3:
                res[n - 1] = n - 2
            rest = set(range(n))
            rest.remove(n - 2)
            self.dfs(2, res, n, rest)
            return res
    
    def dfs(self, now, res, n, rest):
        if now == n * 2 - 1:
            return True
        
        if res[now]:
            return self.dfs(now + 1, res, n, rest)

        for num in range(n - 1, 1, -1):
            if num in rest and now + num < n * 2 - 1 and res[now + num] == 0:
                res[now] = res[now + num] = num
                rest.remove(num)
                if self.dfs(now + 1, res, n, rest):
                    return True
                rest.add(num)
                res[now] = res[now + num] = 0
        
        if 1 in rest:
            res[now] = 1
            rest.remove(1)
            if self.dfs(now + 1, res, n, rest):
                return True
            rest.add(1)
            res[now] = 0

        return False
''',
    call='Solution().constructDistancedSequence(5)',
    expect=[5, 3, 1, 4, 3, 5, 2, 4, 2],
    views=[
        dict(type='array', var='res', label='res（0 = 空位；粉 = 正在填的位置，黄 = 它的闭合位置）', h=200, cell=80,
             pointers={_NOW: 'pink'}, pointer_labels={_NOW: 'now'},
             color=lambda S, i, v: 'yellow' if i == _pair(S) else ('green' if v else None)),
        dict(type='set', var=lambda S: S['_inner'].get('rest', set()), label='rest：还没用的数字', h=110),
        dict(type='calls', h=210, hide=('constructDistancedSequence',)),
    ],
    watch=[('now', _NOW, 'pink'), ('num', lambda S: S['_inner'].get('num'), 'yellow'), ('n', 'n')],
    skip=['if n == 1', 'elif n == 2', 'return [1]', 'return [2, 1, 2]', 'if n > 3', 'if res[now]', 'rest.remove(num)', 'rest.add(num)', 'rest.remove(1)', 'rest.add(1)', 'res[now] = 1', 'res[now] = 0', 'if self.dfs(now + 1, res, n, rest)'],
    captions={
        'res = [n, n - 2]': '先写好开头 `[n, n-2]`，其余 `{len(res) - 2}` 个位置为 0（空位）：序列总长 `2n-1 = {len(res)}`',
        'res[n] = n': '两个 `n` 距离为 `n`：把第二个 `n` 直接填在下标 `{n}`',
        'res[n - 1] = n - 2': '两个 `n-2` 距离也为 `n-2`：第二个 `n-2` 填在下标 `{n - 1}`',
        'rest = set(range(n))': '`rest` 保存还没用的数字（0 没用，混在里面无害）',
        'rest.remove(n - 2)': '`n-2` 已经放好 → 从 `rest` 里删去',
        'self.dfs(2, res, n, rest)': '从下标 2 开始 dfs 搜索后面每个格子',
        'if now == n * 2 - 1': lambda S, B, ret: ('`now` 走到末尾 → ==全部填完==，返回 True' if S.now == S.n * 2 - 1
                                                  else f'`now = {S.now}` 还没到末尾 `{S.n * 2 - 1}` → 继续'),
        'if res[now]': lambda S, B, ret: (f'`res[{S.now}] = {S.res[S.now]}` 已被某次填充==闭合==占掉 → 直接跳过' if S.res[S.now]
                                          else f'`res[{S.now}]` 是空位 → 要从大到小枚举数字来填'),
        'return self.dfs(now + 1': '`res[{B.now}] = {B.res[B.now]}` 已被某次填充==闭合==占掉 → 跳过，直接看 `{B.now + 1}`',
        'for num in range(n - 1, 1, -1)': '`res[{now}]` 是空位，字典序最大 → ==从大到小==试 `num = {num}`',
        'if num in rest and': lambda S, B, ret: (
            f'`{S.num}` 还没用，闭合位置 `{S.now}+{S.num} = {S.now + S.num}` 在范围内且为空 → 可以填' if (S.num in S.rest and S.now + S.num < S.n * 2 - 1 and S.res[S.now + S.num] == 0)
            else f'`{S.num}` 已用过' if S.num not in S.rest
            else f'闭合位置 `{S.now + S.num}` 越界' if S.now + S.num >= S.n * 2 - 1
            else f'闭合位置 `{S.now + S.num}` 已被占 → 换更小的数'),
        'res[now] = res[now + num] = num': '同时填 `res[{now}]` 和 `res[{now + num}]` 为 `{num}`（两个相同数相距 `{num}`）',
        'rest.remove(num)': '`{num}` 用掉了 → 从 `rest` 删除',
        'if self.dfs(now + 1, res, n, rest):\n': '往后填下一格',
        'res[now] = res[now + num] = 0': '后面填不下去 → ==回溯==：`{num}` 放回 `rest`，两个位置清零，试更小的数',
        'if 1 in rest': lambda S, B, ret: ('大数都不行，试 `1`：它==没有闭合位置==，只占一格' if 1 in S.rest else '`1` 已用过 → 这一格无解，返回 False'),
        'res[now] = 1': '`res[{now}] = 1`',
        'rest.add(1)': '后面失败 → 把 `1` 放回 `rest`',
        'res[now] = 0': '清零这一格',
        'return False': '这一格所有数字都试过仍失败 → 返回 False，==回到上一层换更小的数==',
        'return True': lambda S, B, ret: ('填满了 → 返回 True' if S._line == 20 else '后面都成功 → 一路返回 True，先搜到的就是字典序最大'),
        'return res': '返回 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='先构造开头，再从大到小 DFS，第一个成功的就是最大',
        complexity='时间指数级（剪枝后很快），空间 `O(n)`',
        problem=['构造长度 `2n-1` 的序列：1 出现一次，2..n 各出现两次',
                 '==两个 i 之间的距离恰好是 i==（下标差为 i）',
                 '返回字典序最大的可行序列',
                 '示例：`n = 3` → `[3,1,2,3,2]`；本视频演示 `n = 5`'],
        quote='能构造出最大字典序的做法目前还没有想出来。好在本题的数据规模并不大，可以直接使用dfs搜索回溯。',
        quote_src='—— yiduobo 题解',
        idea=['以 `[n, n-2, ...]` 开头的序列总是合法 → 开头直接固定 `n` 和 `n-2`',
              '从前往后填格子：已填的格子跳过，否则从大到小试数字',
              '填 `num` 同时占 `now` 与 `now+num`，闭合位置要不越界、没被占',
              '数字 1 没有闭合位置，最后单独试'],
        result='得到字典序最大的序列 `[5,3,1,4,3,5,2,4,2]` ✓',
        summary=['时间指数级但剪枝强，空间 `O(n)`',
                 '易错点：填 `num` 要==同时==写两个位置，回溯也要两个都清零',
                 '易错点：1 只占一格，不能和其它数一起走“闭合位置”的逻辑',
                 '从大到小枚举 + 首个成功即返回 → 保证字典序最大'],
    ),
)
