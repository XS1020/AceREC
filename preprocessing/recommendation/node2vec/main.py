import os
import ctypes
import pickle
import numpy as np
import pandas as pd

if __name__ == "__main__":
    module = ctypes.CDLL("./linkDetection.so")

    root = "data/"
    paths = []
    for _, _, files in os.walk(root):
        paths = [file for file in files if file.endswith(".csv")]

    p = 5
    q = 1
    denominator = 2
    dim = 256
    length = 10
    batch_size = 1024
    sample_size = 20
    epochs = 100
    threshold = 0.5
    lr = ctypes.c_double(0.01)

    for filename in paths:

        if os.path.exists("embeddings/" + filename + ".pkl"):
            continue

        edge_path = root + filename
        print(edge_path)

        data_frame = pd.read_csv(edge_path , encoding="utf-8").to_numpy()
        n = int(data_frame.max()) + 1

        print(n)

        path = ((len(edge_path) + 1) * ctypes.c_char)()
        embedding = (n * dim * ctypes.c_double)()
        for i, c in enumerate(edge_path):
            path[i] = bytes(edge_path[i], 'utf-8')
        path[len(edge_path)] = bytes(chr(0), 'utf-8')
        print("[INFO] Start C++")
        module.link_detection(path, n, p, q, denominator, dim, length, batch_size, sample_size, epochs, lr, embedding)
        print("[INFO] Finish C++")
        embedding = list(map(float, embedding))
        embedding = np.array(embedding, dtype=np.float32).reshape([n, dim])
        with open("embeddings/"+filename+".pkl", "wb") as f:
            pickle.dump(embedding, f)
