#ifndef RANDOM_WALK
#define RANDOM_WALK

#include <bits/stdc++.h>
using namespace std;
struct Edge {
	int src, dst;
	Edge(int x, int y):src(x), dst(y){}
};
class RandomWalkGraph {
	private:
		int *walks;
		vector<int> nextIdx;
		vector<Edge> edgeList;
		int *headIdx, *degree;
		int numNodes;
	
		void addEdge(int src, int dst) {
			edgeList.push_back(Edge(src, dst));
			nextIdx.push_back(headIdx[src]);
			headIdx[src] = edgeList.size() - 1;
			degree[src] ++;

		}

		int dist(int src, int dst) {
			if (src == dst) return 0;
			if (src == -1) return 2;
			for (int i = headIdx[src]; i != -1; i = nextIdx[i])
				if (edgeList[i].dst == dst) return 1;
			return 2;
		}

		void simulateWalks(int node, int p, int q, int deno, int length) {
			if (degree[node] == 0) return;
			int srcNode = -1, curNode = node, targetNode;
			int selectedCount, selectedDir;
			int *selectedNodes; selectedNodes = new int[numNodes];
			srand(time(NULL));
			int selectedNode;
			for (int i = 0; i < length; i++) {
				int r; int selectedCount;
				do {
					selectedCount = 0;
					r = rand() % (deno * p + deno * q + p * q);
					if (r < deno * p) selectedDir = 2;
					else if (r < deno * p + deno * q) selectedDir = 0;
					else selectedDir = 1;
					for (int j = headIdx[curNode]; j != -1; j = nextIdx[j]) {
						// if (curNode == 144) printf("%d %d %d\n", edgeList[j].dst, dist(srcNode, edgeList[j].dst), srcNode);
						if (dist(srcNode, edgeList[j].dst) == selectedDir)
							selectedNodes[selectedCount++] = edgeList[j].dst;
					}
					if (selectedCount) {
						r = rand() % selectedCount;
						selectedNode = selectedNodes[r];
					}
					else selectedNode = srcNode;
					
				} while(selectedNode == -1 || selectedNode == curNode);
				
				// printf("%d ", selectedNode);
				// returnList.push_back(selectedNode);
				walks[length * node + i] = selectedNode;
				srcNode = curNode; curNode = selectedNode;
			}
			delete[] selectedNodes;
		}

	public:
		RandomWalkGraph(const char dir[], int n, bool directed = false):edgeList() {
			numNodes = n;
			int src, dst;
			walks = NULL;
			headIdx = new int[n]; degree = new int[n];
			for (int i = 0; i < numNodes; ++i) {headIdx[i] = -1; degree[i] = 0;}
			char str[1024];
			freopen(dir, "r", stdin);
			scanf("%[^\n]", str);
			while (scanf("%d, %d ", &src, &dst) != EOF) {
				addEdge(src, dst);
				if (!directed) addEdge(dst, src);
			}
		}
		int operator[](int idx) {
			return degree[idx];
		}
		void run(int p, int q, int deno, int length) {
			if (walks == NULL) walks = new int[numNodes * length];
			for (int i = 0; i < numNodes; ++i)
			{
				if (degree[i] > 0)
					simulateWalks(i, p, q, deno, length);
			}
		}
		int* getWalks(int p, int q, int deno, int length) {
			run(p, q, deno, length);
			return walks;
		}
		~RandomWalkGraph()
        {
            if(walks == NULL)
                delete []walks;
        }
};
#endif
