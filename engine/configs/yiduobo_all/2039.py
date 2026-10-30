CONFIG = dict(
    num=2039, title='网络空闲的时刻', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 求距离 + 算最后一条回复', tags=['灵神题单', '广度优先搜索', '难度分 1865'],
    code='''
class Solution:
    def networkBecomesIdle(self, edges, patience):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        dis = {0: 0}
        q = [0]
        l = 0
        r = 1
        res = 0
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in dis:
                    dis[next] = dis[now] + 1
                    query_cnt = (dis[next] + dis[next] - 1) // patience[next] + 1
                    res = max(res, (query_cnt - 1) * patience[next] + dis[next] + dis[next])
                    q.append(next)
                    r += 1
        
        return res + 1
''',
    call='Solution().networkBecomesIdle([[0,1],[1,2],[2,3]], [0,2,1,3])',
    expect=10,
    views=[
        dict(type='text', size=28, h=70, fn=lambda S: (f"服务器 `{S['next']}`：dis = {S['dis'][S['next']]}，patience = {S['patience'][S['next']]}，发 `{S['query_cnt']}` 条，最后一次回复在 ==第 {(S['query_cnt']-1)*S['patience'][S['next']] + 2*S['dis'][S['next']]} 秒==") if 'query_cnt' in S and 'next' in S and S['next'] in S['dis'] else ''),
        dict(type='map', var='dis', label='dis：0 号到各服务器的距离', fmt=lambda k, v: f'{k}: {v}', font=28, h=130),
        dict(type='array', var='q', label='BFS 队列 q', window=('l', 'r - 1'), pointers={'l': 'blue'}, h=150),
        dict(type='array', var='patience', label='patience', h=150),
    ],
    watch=['now', 'next', 'query_cnt', ('res', 'res', 'green')],
    captions={
        'dis = {0: 0}': '主服务器 0 距离自己是 0，从它开始 BFS',
        'now = q[l]': '取出队头 `{now}`，看它的邻居',
        'if next not in dis': '`{next}` 在 dis 里吗？{next in dis}：==第一次到达时的层数就是最短距离==',
        'dis[next] = dis': '`dis[{next}] = dis[{now}] + 1 = {dis[next]}`：信息单程要走 {dis[next]} 秒，来回 `{2*dis[next]}` 秒',
        'query_cnt =': '第一次回复在 `2*dis = {2*dis[next]}` 秒到，之前的 `{2*dis[next]-1}` 秒内每 {patience[next]} 秒重发：共发 `(2*{dis[next]}-1)//{patience[next]} + 1` = =={query_cnt}== 条',
        'res = max': '最后一条发出时刻 `(query_cnt-1)*patience = {(query_cnt-1)*patience[next]}`，再加来回 `{2*dis[next]}` → ==第 {(query_cnt-1)*patience[next]+2*dis[next]} 秒==；`res` 取各服务器最大值 = {res}',
        'return res + 1': '最后一条消息在第 `{res}` 秒到达，==下一秒才空闲==：返回 `{res} + 1`',
    },
    skip=['g[x] = set()', 'g[y] = set()', 'if x not in g', 'if y not in g', 'g[x].add', 'g[y].add', 'for x, y in', 'g = {}', 'l = 0', 'r = 1', 'res = 0', 'l += 1', 'r += 1', 'q.append'],
    max_steps=80,
    cards=dict(
        one_liner='每台服务器互不影响：算出它最后一次收到回复的时间',
        complexity='时间 `O(n + E)`，空间 `O(n + E)`',
        problem=['服务器 0 是主服务器，其余服务器各发一条消息给它并等回复',
                 '没收到回复就每 `patience[i]` 秒重发一次，线路单程 1 秒/跳',
                 '求网络最早变空闲的秒数；示例链 0-1-2-3，`patience=[0,2,1,3]`'],
        quote='各个数据服务之间是互不影响的，只需要找出每个数据服务器接收最后一条回复的时间，其中的最大值就是网络中最后一个还有消息存在的时刻，那么这个时刻加上1就是最终答案了。',
        quote_src='—— yiduobo 题解',
        idea=['先 ==BFS 求每台服务器到 0 的距离 `dis`==',
              '第一次回复在 `2*dis` 秒到，这之前每 `patience` 秒重发，共 `(2*dis-1)//patience + 1` 条',
              '最后一次回复时间 = 最后一次发送时间 + `2*dis`；取最大值再 +1'],
        summary=['时间 `O(n + E)`：BFS 一遍，每台服务器 `O(1)` 计算',
                 '==是 `2*dis - 1` 不是 `2*dis`==：第 `2*dis` 秒回复已到，不再重发',
                 '答案要在最后一次到达的时刻上 ==+1==',
                 '原文为 Python 2 写法，其中整数除法 `/` 已改为 `//`'],
    ),
)
