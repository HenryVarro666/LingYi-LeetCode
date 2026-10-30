def _owners(S):
    co = S.get('self.chunk_owner') or []
    return {c: sorted(s) for c, s in enumerate(co) if s}


def _owned(S):
    oc = S.get('self.owned_chunk') or {}
    return {u: sorted(s) for u, s in oc.items()}


def _info(S):
    idle = sorted(S.get('self.idle_id') or [])
    return f"下一个全新 id：`next_id = {S.get('self.next_id', 1)}`　　空闲 id 堆：`{idle}`"


CONFIG = dict(
    num=1500, title='设计文件分享系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='两张哈希表 + 空闲 id 小顶堆',
    tags=['灵神题单'],
    code='''
class FileSharing(object):

    def __init__(self, m):
        self.chunk_owner = [set() for _ in range(m + 1)]
        self.owned_chunk = {}
        self.idle_id = []
        self.next_id = 1

    def join(self, ownedChunks):
        if self.idle_id:
            id = heapq.heappop(self.idle_id)
        else:
            id = self.next_id
            self.next_id += 1
        
        self.owned_chunk[id] = set(ownedChunks)
        for chunk in ownedChunks:
            self.chunk_owner[chunk].add(id)
        
        return id

    def leave(self, userID):
        heapq.heappush(self.idle_id, userID)
        for chunk in self.owned_chunk[userID]:
            self.chunk_owner[chunk].remove(userID)
        self.owned_chunk.pop(userID)

    def request(self, userID, chunkID):
        res = sorted(list(self.chunk_owner[chunkID]))
        
        if res:
            self.chunk_owner[chunkID].add(userID)
            self.owned_chunk[userID].add(chunkID)
        return res
''',
    call='''fs = FileSharing(4)
out = []
out.append(fs.join([1, 2]))
out.append(fs.join([2, 3]))
out.append(fs.join([4]))
out.append(fs.request(1, 3))
out.append(fs.request(2, 2))
fs.leave(1)
out.append(fs.request(2, 1))
fs.leave(2)
out.append(fs.join([]))
out''',
    expect=[1, 2, 3, [2], [1, 2], [], 1],
    views=[
        dict(type='map', var=_owned, label='owned_chunk（用户 → 拥有的块）', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='map', var=_owners, label='chunk_owner（块 → 拥有者）', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='heap', var='self.idle_id', label='idle_id（空闲 id，小顶堆）', h=140),
        dict(type='text', fn=_info, size=26, h=60),
    ],
    watch=[('userID', 'userID', 'blue'), ('chunkID', 'chunkID', 'pink'), ('res', 'res', 'green')],
    captions={
        'self.chunk_owner = [': '`chunk_owner[c]`：块 c 的拥有者集合，下标 1..m',
        'self.owned_chunk = {}': '`owned_chunk`：用户 → 他拥有的块集合',
        'self.idle_id = []': '`idle_id`：用户离开后空出来的 id，小顶堆 → 堆顶就是最小的空闲 id',
        'self.next_id = 1': '`next_id`：从未用过的最小 id',
        'if self.idle_id': lambda S, B, r: ('有空闲 id → 优先复用最小的空闲 id' if S['self.idle_id'] else '没有空闲 id → 用全新的 id'),
        'heapq.heappop(self.idle_id)': '弹出堆顶 = 最小的空闲 id：`id = {id}`',
        'id = self.next_id': '用全新 id：`id = {id}`',
        'self.next_id += 1': '`next_id` 往后挪一位 → {self.next_id}',
        'self.owned_chunk[id] = ': '记录用户 `{id}` 拥有的块：`{sorted(self.owned_chunk[id])}`',
        'for chunk in ownedChunks': '把用户 `{id}` 加入每个块的拥有者集合',
        'self.chunk_owner[chunk].add(id)': '块 `{chunk}` 的拥有者 → `{sorted(self.chunk_owner[chunk])}`',
        'return id': '`join` 返回 =={id}==',
        'heapq.heappush(self.idle_id': '用户 `{userID}` 离开：他的 id 进入空闲堆，之后 join 可复用',
        'for chunk in self.owned_chunk[userID]': '遍历他拥有的块，从每块的拥有者里剔除',
        'self.chunk_owner[chunk].remove(userID)': '块 `{chunk}` 不再有用户 `{userID}`：`{sorted(self.chunk_owner[chunk])}`',
        'self.owned_chunk.pop(userID)': '最后把用户 `{userID}` 从 `owned_chunk` 删除',
        'res = sorted': '块 `{chunkID}` 的拥有者排序后就是答案：==`{res}`==',
        'if res': lambda S, B, r: (f'有人拥有 → 用户 `{S.userID}` 成功下载，也变成块 `{S.chunkID}` 的拥有者' if S.res
                                   else '没人拥有这个块 → 返回空列表，什么都不更新'),
        'self.chunk_owner[chunkID].add(userID)': '块 `{chunkID}` 的拥有者 → `{sorted(self.chunk_owner[chunkID])}`',
        'self.owned_chunk[userID].add(chunkID)': '用户 `{userID}` 拥有的块 → `{sorted(self.owned_chunk[userID])}`',
        'return res': '`request` 返回 =={res}==',
    },
    cards=dict(
        one_liner='两张哈希表双向记账，再用小顶堆回收最小的空闲 id',
        complexity='join/leave `O(c log n)`，request `O(k log k)`',
        problem=['文件分享系统：用户 join（拿到最小可用 id）、leave、request 某个块',
                 '`join(ownedChunks)` 返回最小未被占用的 id；`request` 返回拥有该块的用户（升序），并让请求者也拥有它',
                 '本视频：`m=4`，依次 join、request、leave，返回 `[1,2,3,[2],[1,2],[],1]`'],
        quote='每个用户所拥有的文件以及每个文件的拥有者都需要记录下来，因此需要使用两个哈希数组记录……还需要一个堆来记录由于leave操作空闲下来的id。',
        quote_src='—— yiduobo 题解原文',
        idea=['`owned_chunk`：用户 → 块；`chunk_owner`：块 → 用户。两边==同步更新==',
              '`join`：堆非空取堆顶，否则用 `next_id` 并自增',
              '`leave`：从每个块的拥有者里剔除，再把 id 压回堆'],
        summary=['`leave` 要先拿到用户的块再删，不能先 pop 再遍历',
                 '`request` 只有在有人拥有该块时才更新两张表',
                 '返回的拥有者列表要排序（集合无序）',
                 '空闲堆保证 join 总拿到最小的可用 id',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
