#define DllExport   __attribute ((visibility("default")))

#include "negativeSampler.h"
#include "randomWalk.h"
#include "embeddings.h"
#include <bits/stdc++.h>
using namespace std;

inline double sigmoid(double x) {
	return 1 / (1 + exp(-x));
}
inline double vecDot(double *a, double *b, int dim) {
	double result = 0;
	for (int i = 0; i < dim; i++) result += a[i] * b[i];
	return result;
}
extern "C" {
    DllExport void link_detection(const char path[],
    							int n, int p, int q, int deno, int dim, int length,
    							int batchSize, int sampleSize, int epochs,
    							double lr, double *dstEmbedding);
}
void link_detection(const char path[],
					int n, int p, int q, int deno, int dim, int length,
					int batchSize, int sampleSize, int epochs,
					double lr, double *dstEmbedding) {

	RandomWalkGraph graph(path, n);
	NegativeSampler sampler(n);
	Embeddings embedding(n, dim);
	int *walks = NULL; double *grad = NULL;
	grad = new double[n * dim];

	cout << path << endl;
	int *samples; double lastLoss = 0; samples = new int[sampleSize];

	for (int epoch = 0; epoch < epochs; epoch++) {
		walks = graph.getWalks(p, q, deno, length);
		double loss = 0;
		// embedding.backPropagation(grad, lr);
		embedding.adamOptimizer(grad, lr);
		for (int j = 0; j < dim * n; j++) grad[j] = 0;
		for (int i = 0; i < n; i++) {
			if (graph[i] == 0)
				continue;
			for (int j = 0; j < length; j++) {
				int v = walks[i * length + j];
				// printf("%d %d\n", i, v);
				double x = vecDot(embedding[i], embedding[v], dim);
				double sig = sigmoid(-x);
				loss += log(sigmoid(x));
				for (int k = 0; k < dim; k++) {
					grad[i * dim + k] -= sig * embedding[v][k];
					grad[v * dim + k] -= sig * embedding[i][k];
				}
			}

			for (int j = 0; j < length; j++) {
				samples = sampler.getSamples(sampleSize);
				for (int k = 0; k < sampleSize; k++) {
					int sample = samples[k];
					sample = rand() % n;
					double x = vecDot(embedding[i], embedding[sample], dim);
					double sig = sigmoid(x);
					// printf("%f ", x * 100000);
					loss += log(sigmoid(-x));
					for (int l = 0; l < dim; l++) {
						grad[i * dim + l] += sig * embedding[sample][l];
						grad[sample * dim + l] += sig * embedding[i][l];
					}
				}
				// printf("\n");
			}
		}
		if((epoch+1) % 50 == 49)
		    lr /= 10;
		printf("epoch: %d  loss:%f\n", epoch, -1 * loss);
		// if (lastLoss - loss> 10000 && lastLoss != 0) break;
		lastLoss = loss;
	}
	embedding.copy(dstEmbedding);
}
