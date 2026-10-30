def _txt(S):
    if 'limit' not in S:
        return '先建立相邻关系 `prev/next`，再用堆维护「理论最高」'
    if 'now_p' in S:
        return f"相邻限高建筑 `p={S['now_p']}`、`h={S['now_h']}`；峰顶 `max_h = max(h1,h2) + (间隔 - 高差) // 2`，取最大 `res = {S.get('res', 0)}`"
    done = {k: v for k, v in S['limit'].items() if v is not None}
    return f"每次弹出理论最矮的建筑，定死它的限高；已确定 `{done}`"


CONFIG = dict(
    num=1840, title='最高建筑高度', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='手写堆传播限高 + 相邻限高点峰顶公式',
    tags=['灵神题单', '难度分 2374'],
    code='''
class Solution(object):
    def maxBuilding(self, n, restrictions):

        prev = {}
        next = {}
        p_order = [1] + sorted([p for p, h in restrictions]) + [n + 1]
        for index in range(len(p_order)):
            if index > 0:
                prev[p_order[index]] = p_order[index - 1]
            if index < len(p_order) - 1:
                next[p_order[index]] = p_order[index + 1]

        heap = sorted([[h, p] for p, h in restrictions] + [[0, 1], [n, n + 1]], key=lambda d:d[0])
        pos = {}
        limit = {}
        for index in range(len(heap)):
            pos[heap[index][1]] = index
            limit[heap[index][1]] = None

        while len(heap) > 1:
            h, p = heap[0]
            limit[p] = h

            heap[0] = heap[-1]
            heap.pop()
            now = 0
            m = len(heap)
            #堆中删除操作，将要删除的位置now与堆数组末尾进行交换并从数组末尾删去
            while True: #调整新的now在堆中的位置
                left = now + now + 1
                left_flag = left < m and heap[left][0] < heap[now][0]
                
                right = now + now + 2
                right_flag = right < m and heap[right][0] < heap[now][0]

                if left_flag:
                    if right_flag:
                        if heap[left][0] < heap[right][0]:
                            heap[now], heap[left] = heap[left], heap[now]
                            pos[heap[now][1]] = now
                            now = left
                        else:
                            heap[now], heap[right] = heap[right], heap[now]
                            pos[heap[now][1]] = now
                            now = right
                    else:
                        heap[now], heap[left] = heap[left], heap[now]
                        pos[heap[now][1]] = now
                        now = left
                elif right_flag:
                    heap[now], heap[right] = heap[right], heap[now]
                    pos[heap[now][1]] = now
                    now = right
                else:
                    pos[heap[now][1]] = now
                    break

            #更新当前最矮建筑左侧建筑的理论最大高度
            if p > 1 and limit[prev[p]] is None:
                heap_pos = pos[prev[p]]
                delta = p - heap[heap_pos][1]
                if heap[heap_pos][0] > delta + h: 
                    #若成功更新，那么左侧建筑的理论最大高度是变小的，此时需要更新其在堆中的位置
                    heap[heap_pos][0] = delta + h
                    now = heap_pos
                    while now > 0:
                        fa = (now - 1) // 2
                        if heap[now][0] < heap[fa][0]:
                            heap[now], heap[fa] = heap[fa], heap[now]
                            pos[heap[now][1]] = now
                            now = fa
                        else:
                            break
                    pos[heap[now][1]] = now
            
            #更新当前最矮建筑右侧建筑的理论最大高度
            if p <= n and limit[next[p]] is None:
                heap_pos = pos[next[p]]
                delta = heap[heap_pos][1] - p
                if heap[heap_pos][0] > delta + h:
                    heap[heap_pos][0] = delta + h
                    now = heap_pos
                    while now > 0:
                        fa = (now - 1) // 2
                        if heap[now][0] < heap[fa][0]:
                            heap[now], heap[fa] = heap[fa], heap[now]
                            pos[heap[now][1]] = now
                            now = fa
                        else:
                            break
                    pos[heap[now][1]] = now
        
        limit[heap[0][1]] = heap[0][0]

        now_p = 1
        now_h = 0
        res = 0
        while now_p != n:
            next_p = next[now_p]
            next_h = limit[next_p]
            if next_p == n + 1: #对于假定右边界n + 1的特殊处理
                next_p -= 1
                next_h -= 1
            res = max(res, (next_p - now_p - 1 - (abs(next_h - now_h) - 1)) // 2 + max(now_h, next_h))
            now_p, now_h = next_p, next_h
        
        return res
''',
    call='Solution().maxBuilding(5, [[2,1],[4,1]])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=24, h=130),
        dict(type='heap', var='heap', fmt=lambda x: f'p{x[1]}:{x[0]}', h=330),
        dict(type='map', var='limit', fmt=lambda k, v: f'p{k}: ' + ('?' if v is None else str(v)), h=300),
    ],
    watch=['p', 'h', 'now_p', 'now_h', 'res'],
    captions={
        'prev = {}': '`prev/next`：记录每个限高点左、右相邻的限高点',
        'p_order =': '所有限高位置排序：`{p_order}`（首尾是哨兵位置 1 和 n+1），再逐个登记左右邻居',
        'for index in range(len(p_order))': '依次登记每个位置的左右邻居（`prev` / `next`）',
        'if index > 0': '`index = {index}`：有左邻居吗 → {"有" if index > 0 else "没有"}',
        'if index < len(p_order) - 1': '有右邻居吗 → {"有" if index < len(p_order) - 1 else "没有"}',
        'heap = sorted': '堆里放 `[理论高度, 位置]`，额外加入 `[0, 1]`（1 号必须为 0）和 `[n, n+1]`（右边界哨兵）',
        'for index in range(len(heap))': '登记每个建筑在堆里的下标 `pos`，`limit` 先都是未定 `?`',
        'while len(heap) > 1': '堆里还剩 `{len(heap)}` 个：继续「弹出理论最矮的建筑」',
        'h, p = heap[0]': '堆顶是理论最矮的建筑：位置 `p = {p}`，理论高度 `h = {h}`',
        'limit[p] = h': '它不会再被别人压低：==实际限高就是 `{h}`==，记入 `limit[{p}]`',
        'heap[0] = heap[-1]': '把它从堆里删掉：末尾元素补到堆顶，再逐层下沉（`pos` 同步更新）',
        'if p > 1 and limit[prev[p]]': '看左邻居 `{prev.get(p, "无")}`：还没定死吗 → {"是，可能被压低" if (p > 1 and limit[prev[p]] is None) else "否，跳过"}',
        'delta = p - heap': '左邻居离它 `delta = {delta}` 格，最多比 `h` 高 `delta`',
        'if heap[heap_pos][0] > delta + h': '理论高度 `{heap[heap_pos][0]}` 与 `delta + h = {delta + h}` 比较 → {"更高，要压低" if heap[heap_pos][0] > delta + h else "不更高，不用动"}',
        'heap[heap_pos][0] = delta + h': '邻居的理论高度被压低为 `{delta + h}`，再往上浮调整堆位置',
        'if p <= n and limit[next[p]]': '看右邻居 `{next.get(p)}`：还没定死吗 → {"是，可能被压低" if (p <= n and limit[next[p]] is None) else "否，跳过"}',
        'delta = heap[heap_pos][1] - p': '右邻居离它 `delta = {delta}` 格',
        'limit[heap[0][1]] = heap[0][0]': '堆里最后一个建筑的理论高度也就是实际限高',
        'now_p = 1': '开始算答案：从位置 1（高度 0）出发，逐对相邻限高点算峰顶',
        'res = 0': '`res` 记录最高的峰顶',
        'while now_p != n': '`now_p = {now_p}`：{"还没到 n，处理下一对限高点" if now_p != n else "到 n 了，结束"}',
        'next_p = next[now_p]': '下一个限高点位置 `next_p = {next_p}`',
        'next_h = limit[next_p]': '它的限高 `next_h = {next_h}`',
        'if next_p == n + 1': '`next_p = {next_p}`：{"是假想的右边界 n+1" if next_p == n + 1 else "是真实建筑"}',
        'next_p -= 1': '边界建筑 n+1 不存在，改成位置 `n`，高度同步减 1',
        'next_h -= 1': '`next_h` → {next_h}',
        'res = max': '峰顶 = `max(h1,h2) + (间隔 - 高差) // 2` → `res = {res}`',
        'now_p, now_h = next_p': '推进到下一个限高点 `p = {now_p}, h = {now_h}`',
        'return res': '最高建筑高度 `{ret}`',
    },
    skip=['next = {}', 'pos = {}', 'limit = {}', 'for index in range(len(p_order))', 'if index > 0', 'if index < len(p_order) - 1', 'prev[p_order', 'for index in range(len(heap))', 'heap_pos = pos', 'now_h = 0', 'next[p_order', 'pos[heap[index]', 'limit[heap[index]', 'heap.pop()', 'now = 0', 'm = len(heap)',
          'while True', 'left = now', 'right = now', 'left_flag', 'right_flag', 'heap[left][0] < heap[right][0]',
          'heap[now], heap[', 'pos[heap[now][1]] = now', 'now = left', 'now = right', 'now = heap_pos', 'while now > 0',
          'fa = ', 'heap[now][0] < heap[fa][0]', 'break', 'now = fa'],
    max_steps=90,
    cards=dict(
        one_liner='先让「理论最矮」的建筑定死限高并向两边传播，再用倒 V 公式求峰顶',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n` 栋建筑，1 号高度为 0，相邻高度差不超过 1',
                 '`restrictions[i] = [id, maxHeight]` 给部分建筑限高，求最高建筑的最大高度',
                 '本视频：`n=5, [[2,1],[4,1]]` → `2`'],
        quote='由于只会是较矮的建筑影响到较高建筑的最大高度，因此一个自然的想法就是每次选出剩余建筑中理论高度最矮的建筑。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 很大，不能逐栋建模，只处理限高建筑，另加位置 1（高 0）和 n+1（高 n）',
              '每次选理论最矮的：它的高度已经是实际限高，再用距离压低左右邻居',
              '需要定点更新，所以手写堆，并用 `pos` 记录每个建筑在堆里的下标',
              '相邻限高点 `(p1,h1)`、`(p2,h2)` 之间呈倒 V：峰顶 `max(h1,h2) + (p2-p1-|h1-h2|)//2`'],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '易错点：假想的右边界 `n+1` 不是真实建筑，算峰顶时要改成位置 `n`、高度减 1',
                 '更新邻居理论高度后必须上浮调整堆，并同步 `pos`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（上浮的父下标 `fa` 和峰顶公式共 3 处）',
                 '对比灵神：灵神用左右两次扫描代替手写堆，更短'],
    ),
)
