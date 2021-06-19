#ifndef NEGATIVE_SAMPLER
#define NEGATIVE_SAMPLER
#include <bits/stdc++.h>
class NegativeSampler {
	private:
		int *nodeList;
		int	curPos, totalNodes;

	public:
		NegativeSampler(int n)
		{
			curPos = 0; totalNodes = n;
			nodeList = new int[n];
			for (int i = 0; i < n; ++i)
				nodeList[i] = i;

			for (int i = 0; i < n; ++i)
			{
				int tag = rand() % n;
				int tmp = nodeList[tag];
				nodeList[tag] = nodeList[i];
				nodeList[i] = tmp;
			}
		}

		int *getSamples(int num) {
			int *returnValue = nodeList + curPos;
			curPos += num + rand() % num;
			if (curPos > totalNodes) {
				curPos %= totalNodes;
				returnValue = nodeList + curPos;
			}
			return returnValue;
		}
	
};

#endif
