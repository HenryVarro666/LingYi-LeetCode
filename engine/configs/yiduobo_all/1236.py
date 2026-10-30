A = 'http://news.yahoo.com/news/topics/'
B = 'http://news.yahoo.com/news'
C = 'http://news.yahoo.com/sports'
D = 'http://news.yahoo.com/tech'
G = 'http://news.google.com'
GRAPH = {A: [B, G], B: [A, C], G: [A], C: [B, D], D: []}


def _short(u):
    return u.replace('http://', '').replace('news.yahoo.com', 'yahoo').replace('news.google.com', 'google')


def _tail(u):
    return u.rstrip('/').split('/')[-1] if u.count('/') > 2 else u.split('/')[2]


def _host(u):
    return u.split('/', 3)[2]


def _cap_if(S, B, ret):
    nx, now = S['next'], S['now']
    if nx in S['vis']:
        return f'`{_short(nx)}` ==已访问过== → 跳过，避免重复爬取'
    if _host(nx) != _host(now):
        return f'域名 `{_host(nx)}` ≠ `{_host(now)}`（和起点不同）→ ==不爬=='
    return f'`{_short(nx)}` 没访问过，域名同为 `{_host(nx)}` → 加入队列'


CONFIG = dict(
    num=1236, title='网络爬虫', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS + 域名过滤',
    code='''
class Solution(object):
    def crawl(self, startUrl, htmlParser):

        q = [startUrl]
        vis = set([startUrl])

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in htmlParser.getUrls(now):
                if next not in vis and now.split('/', 3)[2] == next.split('/', 3)[2]:
                    vis.add(next)
                    q.append(next)
                    tail += 1
        
        return q
''',
    setup=f'''
GRAPH = {GRAPH!r}
class HtmlParser:
    def getUrls(self, url):
        return GRAPH[url]
''',
    call=f'Solution().crawl({A!r}, HtmlParser())',
    expect=[A, B, C, D],
    views=[
        dict(type='array', var=lambda S: [_tail(u) for u in S['q']] if 'q' in S else None,
             label='q（BFS 队列，也是最终答案；蓝 = head 指向的当前页面）', cell=140, pointers={'head': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if 'now' in S and S['q'][i] == S['now'] else None),
        dict(type='set', var='vis', label='vis（已访问）', fmt=lambda x: _short(x), font=20, h=230),
        dict(type='text', h=120, fn=lambda S: (f"当前页面 `{_short(S['now'])}`" + (f"，看到链接 `{_short(S['next'])}`" if 'next' in S and S.get('_line', 0) >= 10 else '')) if 'now' in S else ''),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), 'now', ('len(q)', 'len(q)', 'green')],
    captions={
        'q = [startUrl]': '队列从起点开始：`q = [startUrl]`',
        'vis = set': '`vis` 记录已经入队的地址，防止重复',
        'head, tail': '`head` 指向下一个要处理的，`tail` = 队列长度',
        'while head < tail': lambda S, B, r: f'`head = {S.head} < tail = {S.tail}`：队里还有没处理的 → 继续' if S.head < S.tail else f'`head = {S.head} = tail`：队列处理完 → 结束',
        'now = q[head]': lambda S, B, r: f'取出队首页面 `{_short(S.now)}`',
        'head += 1': '`head` → {head}，这一页算处理中',
        'for next in': '遍历这一页 `getUrls` 返回的链接',
        'if next not in vis': _cap_if,
        'vis.add': lambda S, B, r: f'标记 `{_short(S.next)}` 已访问',
        'q.append': lambda S, B, r: f'`{_short(S.next)}` 入队，成为答案的一员',
        'tail += 1': '`tail` → {tail}',
        'return q': '队列本身就是答案：`{len(q)}` 个页面',
    },
    cards=dict(
        one_liner='从起点 BFS，只爬同域名、没访问过的链接',
        complexity='时间 `O(V+E)`（域名比较另计），空间 `O(V)`',
        problem=['给起点 `startUrl` 和 `htmlParser.getUrls(url)`，爬出所有和起点==同一域名==的链接',
                 '域名 = `http://` 后到第一个 `/` 之前的部分，答案顺序任意',
                 '本视频：从 `news.yahoo.com/news/topics/` 出发，`news.google.com` 域名不同不爬'],
        quote='bfs的问题。从startUrl开始进行爬取，对于当前爬取到的地址，若其没有被访问过，且其域名与startUrl相同，那么就将其加入到bfs队列中。bfs完成后，整个bfs队列即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列既当 BFS 的工作队列，又当答案：入队的就是爬到的',
              '用 `head` 下标代替出队，`q` 不删元素',
              '`split("/", 3)[2]` 取出域名，和 `next` 的域名比较'],
        summary=['时间 `O(V+E)`，空间 `O(V)`',
                 '==先判 vis 再判域名都行==，关键是入队时就标记，避免同一页重复入队',
                 '起点的域名取 `now` 的就行：同域名的页面传递下来都等于起点域名',
                 '原文开头 `#class HtmlParser` 只是接口注释，已省略；setup 里补了一个小 HtmlParser'],
    ),
)
