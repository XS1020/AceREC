#ifndef EMBEDDINGS
#define EMBEDDINGS
#include <bits/stdc++.h>
class Embeddings {
	private:
		double *embedding;
		int dimension, numNodes;
		double *adamM, *adamV;
		double randDouble() {
			int randInt[2];
			randInt[0] = rand(); randInt[1] = rand();
			double x = randInt[0] * 1.0 / randInt[1];
			return x;
		}

		void normalize() {
			double norm = 0;
			for (int i = 0; i < numNodes; i++) {
				norm = 0;
				for (int j = 0; j < dimension; j++)
					norm += embedding[i * dimension + j] * embedding[i * dimension + j];
				norm = sqrt(norm);
				for (int j = 0; j < dimension; j++)
					embedding[i * dimension + j] /= norm;
			}
		}
	public:
		Embeddings(int n, int dim) {
			srand(time(NULL));
			default_random_engine e(time(0));
			uniform_real_distribution<double> u(-0.5, 0.5);
			dimension = dim;
			numNodes = n;
			double mean = 0, maxValue = 0, minValue = 1e5;
			adamV = new double[n * dim]; adamM = new double[n * dim];

			for (int i = 0; i < n * dim; ++i)
				adamV[i] = adamM[i] = 0;
			embedding = new double[n * dimension];
			for (int i = 0; i < n * dim; i++) {
				// embedding[i] = randDouble();
				embedding[i] = u(e);
				mean += embedding[i];
				if (embedding[i] > maxValue) maxValue = embedding[i];
				if (embedding[i] < minValue) minValue = embedding[i];
			}
			// mean /= n * dim;
			// for (int i = 0; i < n * dim; i++) {
			// 	embedding[i] -= mean;
			// 	embedding[i] /= (maxValue - minValue);
			// }
			// normalize();
		}

		double* operator[](int idx) {
			return embedding + dimension * idx;
		}

		void backPropagation(double *grad, double lr) {
			for (int i = 0; i < numNodes * dimension; ++i) {
				embedding[i] -= grad[i] * lr;
			}
			//normalize();
		}
		void copy(double *dst) {
			for (int i = 0; i < numNodes * dimension; ++i)
				dst[i] = embedding[i];
		}
		void adamOptimizer(double *grad, double lr, double beta1 = 0.9, double beta2 = 0.999, double espsilon = 1e-8) {
			for (int i = 0; i < numNodes * dimension; i++) {
				adamM[i] = beta1 * adamM[i] + (1 - beta1) * grad[i];
				adamV[i] = beta2 * adamV[i] + (1 - beta2) * grad[i] * grad[i];
				embedding[i] -= lr * adamM[i] / (1 - beta1) / (sqrt(adamV[i] / (1 - beta2)) + espsilon);
			}
		}
};
#endif
