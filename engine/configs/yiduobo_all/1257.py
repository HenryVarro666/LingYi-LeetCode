CONFIG = dict(
    num=1257, title='最小公共区域', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='哈希表记录祖先链（LCA）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findSmallestRegion(self, regions, region1, region2):

        fa = {}
        for r in regions:
            for p in r[1:]:
                fa[p] = r[0]
        
        vis = set([region1])
        now = region1
        while now in fa:
            now = fa[now]
            vis.add(now)
        
        now = region2
        while now not in vis:
            now = fa[now]
        
        return now
''',
    call='''regions = [["Earth","NA","SA"],["NA","US","CA"],["US","NY","BO"],["CA","ON","QC"],["SA","BR"]]
Solution().findSmallestRegion(regions, "QC", "NY")''',
    expect='NA',
    views=[
        dict(type='map', var='fa', label='fa：子区域 → 父区域', h=170, font=24),
        dict(type='set', var='vis', label='vis：region1 到根的路径', h=150),
        dict(type='text', h=60, fn=lambda S: f"当前 `now = {S['now']}`" if 'now' in S else ''),
    ],
    watch=['region1', 'region2', 'now'],
    captions={
        'fa[p] = r[0]': '`{p}` 的父区域是 `{r[0]}`：每个区域只有一个父亲',
        'vis = set': '先把 `region1 = {region1}` 放进 vis，从它开始往上走',
        'while now in fa': lambda S, B, r: (f'`{S.now}` 在 fa 里（有父亲）→ 还能往上走' if S.now in S.fa
                                            else f'`{S.now}` 不在 fa 里：已走到根，路径记录完毕'),
        12: '往上走一步：`{B.now}` → `{now}`',
        17: '往上走一步：`{B.now}` → `{now}`',
        'vis.add(now)': '`{now}` 记入 vis：它是 region1 的祖先',
        'now = region2': '换 `region2 = {region2}`，从它往上走',
        'while now not in vis': lambda S, B, r: (f'`{S.now}` 不在 vis → 还不是 region1 的祖先，继续往上' if S.now not in S.vis
                                                 else f'`{S.now}` 已在 vis 中 → ==最先碰到的就是最近公共祖先=='),
        'return now': '答案：`{now}`',
    },
    cards=dict(
        one_liner='把区域关系看成树：一边走路径记下来，另一边撞上就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`regions[i]` 的第一个是父区域，其余是它直接包含的子区域',
                 '求同时包含 `region1`、`region2` 的最小区域',
                 '示例：Quebec / New York → `North America`（图中缩写为 QC / NY → NA）'],
        quote='题目可以认为是给出了一棵树，求树中两个节点的最近公共祖先。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `fa` 记录每个区域的父亲，把列表变成「向上指」的树',
              '从 `region1` 一路走到根，沿途记进哈希集合 `vis`',
              '再从 `region2` 往上走，第一个出现在 `vis` 里的就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（n 为区域总数）',
                 '`vis` 先放 `region1` 自己：它本身也可能就是公共祖先',
                 '适合单次查询；多次查询要用倍增等 LCA 方法',
                 '题目保证 region1、region2 都在树里，所以第二个循环不会越界'],
    ),
)
