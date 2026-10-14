"""Q6: Lexicographically smallest topological order; report a cycle if present."""
import sys
import heapq

def find_cycle(graph, remaining):
    color, parent = {}, {}
    for start in remaining:
        if color.get(start, 0): continue
        stack = [(start, iter(graph[start]))]
        color[start] = 1
        while stack:
            node, children = stack[-1]
            try: nxt = next(children)
            except StopIteration:
                color[node] = 2; stack.pop(); continue
            if nxt not in remaining: continue
            if color.get(nxt, 0) == 0:
                parent[nxt] = node; color[nxt] = 1
                stack.append((nxt, iter(graph[nxt])))
            elif color[nxt] == 1:
                cycle = [nxt]; cur = node
                while cur != nxt:
                    cycle.append(cur); cur = parent[cur]
                cycle.append(nxt); cycle.reverse()
                return cycle
    return []

def main():
    data = sys.stdin.read().splitlines()
    try:
        n, e = map(int, data[0].split())
        names = [data[i+1].strip() for i in range(n)]
        if len(set(names)) != n: raise ValueError("Module names must be unique")
        known = set(names)
        graph = {name: [] for name in names}
        indegree = {name: 0 for name in names}
        for line in data[n+1:n+1+e]:
            source, dependency = line.split()
            if source not in known or dependency not in known: raise ValueError("Unknown module")
            # Edge dependency -> source means dependency must load first.
            if source not in graph[dependency]:
                graph[dependency].append(source)
                indegree[source] += 1
        heap = [name for name in names if indegree[name] == 0]
        heapq.heapify(heap); order = []
        while heap:
            node = heapq.heappop(heap); order.append(node)
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0: heapq.heappush(heap, nxt)
        if len(order) == n:
            print(*order)
        else:
            remaining = {name for name in names if indegree[name] > 0}
            cycle = find_cycle(graph, remaining)
            print("CYCLE")
            print(*cycle)
    except (ValueError, IndexError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
