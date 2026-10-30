"""Run a solution line by line and record snapshots of every frame's locals."""
import bisect
import collections
import copy
import functools
import heapq
import itertools
import math
import operator
import sys
import types
from typing import List, Optional, Dict, Tuple  # noqa: F401

FILENAME = '<solution>'
_uid = itertools.count(1)
_origin = {}  # uid -> (row, col) for nodes built from the input


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        self._uid = next_uid()

    def __repr__(self):
        return f'ListNode({self.val})'


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self._uid = next_uid()

    def __repr__(self):
        return f'TreeNode({self.val})'


class Node:  # LeetCode 138 style random-pointer node
    def __init__(self, x=0, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random
        self._uid = next_uid()

    def __repr__(self):
        return f'Node({self.val})'


def next_uid():
    return next(_uid)


_input_rows = itertools.count(0)


def L(vals, pos=-1):
    """Build a linked list; pos >= 0 makes the tail point to node[pos] (cycle)."""
    row = next(_input_rows)
    nodes = [ListNode(v) for v in vals]
    for i, nd in enumerate(nodes):
        _origin[nd._uid] = (row, i)
        if i + 1 < len(nodes):
            nd.next = nodes[i + 1]
    if pos >= 0 and nodes:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def Lnodes(head):
    out, seen = [], set()
    while head and id(head) not in seen:
        seen.add(id(head)); out.append(head); head = head.next
    return out


def Tr(vals):
    """Build a binary tree from LeetCode level-order list (None = missing)."""
    if not vals or vals[0] is None:
        return None
    it = iter(vals)
    root = TreeNode(next(it))
    q = collections.deque([root])
    while q:
        nd = q.popleft()
        try:
            v = next(it)
        except StopIteration:
            break
        if v is not None:
            nd.left = TreeNode(v); q.append(nd.left)
        try:
            v = next(it)
        except StopIteration:
            break
        if v is not None:
            nd.right = TreeNode(v); q.append(nd.right)
    return root


def tree_list(root):
    """TreeNode -> level-order list (for checking answers)."""
    out, q = [], collections.deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out


def list_vals(head):
    return [n.val for n in Lnodes(head)]


def base_namespace():
    ns = dict(
        ListNode=ListNode, TreeNode=TreeNode, Node=Node, L=L, Tr=Tr, tree_list=tree_list, list_vals=list_vals,
        List=List, Optional=Optional, Dict=Dict, Tuple=Tuple,
        defaultdict=collections.defaultdict, Counter=collections.Counter, deque=collections.deque,
        OrderedDict=collections.OrderedDict, collections=collections,
        heapq=heapq, heappush=heapq.heappush, heappop=heapq.heappop, heapify=heapq.heapify,
        heapreplace=heapq.heapreplace, heappushpop=heapq.heappushpop, nlargest=heapq.nlargest, nsmallest=heapq.nsmallest,
        bisect=bisect, bisect_left=bisect.bisect_left, bisect_right=bisect.bisect_right, insort=bisect.insort,
        math=math, inf=math.inf, gcd=math.gcd, comb=math.comb, isqrt=math.isqrt,
        functools=functools, cache=functools.cache, lru_cache=functools.lru_cache, reduce=functools.reduce,
        itertools=itertools, accumulate=itertools.accumulate, permutations=itertools.permutations,
        combinations=itertools.combinations, product=itertools.product, groupby=itertools.groupby,
        pairwise=getattr(itertools, 'pairwise', None), chain=itertools.chain, zip_longest=itertools.zip_longest,
        operator=operator, xor=operator.xor, ascii_lowercase='abcdefghijklmnopqrstuvwxyz',
        xrange=range,
    )
    return ns


class TooLong(Exception):
    pass


_SKIP_NAMES = {'<lambda>', '<listcomp>', '<dictcomp>', '<setcomp>', '<genexpr>'}


def _keep(k, v):
    if k.startswith('__'):
        return False
    if isinstance(v, (types.ModuleType, type, types.FunctionType, types.BuiltinFunctionType, types.MethodType,
                      functools.partial)):
        return False
    if callable(v) and not isinstance(v, (ListNode, TreeNode, Node)):
        return False
    return True


def _flatten_self(loc):
    out = {}
    for k, v in loc.items():
        if k == 'self' and hasattr(v, '__dict__'):
            for a, av in v.__dict__.items():
                if _keep(a, av):
                    out['self.' + a] = av
        elif _keep(k, v):
            out[k] = v
    return out


_SNAP_MAXLEN = None  # optional: keep only the first N items of very long lists in snapshots (config `snap_maxlen`)


def _cap_long(v):
    if _SNAP_MAXLEN and isinstance(v, list) and len(v) > _SNAP_MAXLEN:
        return v[:_SNAP_MAXLEN]
    return v


def _sync_repr(v):
    """readable state for threading primitives (they cannot be deep-copied)"""
    n = type(v).__name__
    try:
        if 'Semaphore' in n and hasattr(v, '_value'):
            return f'{n}({v._value})'
        if n == 'Event':
            return f'Event({"set" if v.is_set() else "clear"})'
        if n == 'Barrier':
            return f'Barrier(waiting={v.n_waiting})'
        if n == 'Condition':
            return 'Condition'
        if hasattr(v, 'locked') and callable(v.locked):
            return f'Lock({"locked" if v.locked() else "free"})'
    except Exception:
        return None
    return None


def snapshot(frame):
    chain = []
    f = frame
    while f is not None:
        if f.f_code.co_filename == FILENAME and f.f_code.co_name not in _SKIP_NAMES:
            chain.append(f)
        f = f.f_back
    chain.reverse()  # outermost first
    raw = [_flatten_self(dict(fr.f_locals)) for fr in chain]
    if _SNAP_MAXLEN:
        raw = [{k: _cap_long(v) for k, v in d.items()} for d in raw]
    try:
        locs = copy.deepcopy(raw)
    except Exception:
        locs = []
        for d in raw:
            dd = {}
            for k, v in d.items():
                try:
                    dd[k] = copy.deepcopy(v)
                except Exception:
                    dd[k] = _sync_repr(v) or repr(v)
            locs.append(dd)
    frames = []
    for fr, loc in zip(chain, locs):
        co = fr.f_code
        frames.append(dict(name=co.co_name, line=fr.f_lineno, locals=loc,
                           args=list(co.co_varnames[:co.co_argcount])))
    return frames


def run(code, call, max_events=6000, setup='', threads=False, trace_limit=None):
    """Execute `code`, then evaluate `call` (an expression, or statements whose last line is an expression)
    while tracing. Returns (result, events, ns). Each event: dict(kind, line, frames, ret, fname, thread).

    Opt-in extras (default off, so existing configs behave exactly as before):
      threads=True      also trace threads started by the call (threading.settrace); events carry the thread name
      trace_limit=N     after N events stop recording but let the code run to the end (ns['__truncated__'] = True)
    """
    import threading
    ns = base_namespace()
    exec(compile(code, FILENAME, 'exec'), ns)
    if setup:
        exec(compile(setup, '<setup>', 'exec'), ns)
    events = []
    state = {'stopped': False}

    def local(frame, event, arg):
        if state['stopped']:
            return None
        if event in ('line', 'return'):
            events.append(dict(kind=event, line=frame.f_lineno, frames=snapshot(frame),
                               ret=copy.deepcopy(arg) if event == 'return' else None,
                               fname=frame.f_code.co_name, thread=threading.current_thread().name))
            if trace_limit and len(events) >= trace_limit:
                state['stopped'] = True
                return None
            if len(events) > max_events:
                raise TooLong(f'more than {max_events} trace events; use a smaller input')
        return local

    def glob(frame, event, arg):
        if state['stopped']:
            return None
        if frame.f_code.co_filename == FILENAME and frame.f_code.co_name not in _SKIP_NAMES:
            return local
        return None

    body = call.strip().split('\n')
    pre, last = '\n'.join(body[:-1]), body[-1]
    sys.settrace(glob)
    if threads:
        threading.settrace(glob)
    try:
        if pre:
            exec(compile(pre, '<driver>', 'exec'), ns)
        result = eval(compile(last, '<driver>', 'eval'), ns)
    finally:
        sys.settrace(None)
        if threads:
            threading.settrace(None)
    ns['__truncated__'] = state['stopped']
    return result, events, ns
