#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cuda_runtime.h>
#include "device_launch_parameters.h"
#include <curand.h>
#include <curand_kernel.h>

#define MAX_STEPS 100000

// On bourrine monte carto sur le GPU.
// Ca marche pas mais c'est fun.
__global__ void monteCarloMazeKernel(char* maze, int width, int height, int* results) {
    int threadId = threadIdx.x + blockIdx.x * blockDim.x;
    bool visited[MAX_STEPS] = { false };
    bool found = false;
    int pathLength = 0;
    int x = 1; // Point de départ en x (colonne)
    int y = 0; // Point de départ en y (ligne)
    curandState state;
    curand_init(1234 + threadId, 0, 0, &state);

    visited[y * width + x] = true; // Marquer la position de départ comme visitée

    for (int steps = 0; steps < MAX_STEPS; steps++) {
        int validDirections[4] = { -1, -1, -1, -1 };
        int numValidDirections = 0;

        for (int direction = 0; direction < 4; direction++) {
            int dx = 0, dy = 0;
            switch (direction) {
            case 0: dy = -1; break; // Nord
            case 1: dx = 1; break; // Est
            case 2: dy = 1; break; // Sud
            case 3: dx = -1; break; // Ouest
            }

            int newX = x + dx;
            int newY = y + dy;

            if (newX >= 0 && newX < width && newY >= 0 && newY < height &&
                maze[newY * width + newX] != '#' && !visited[newY * width + newX]) {
                validDirections[numValidDirections++] = direction;
            }
        }

        if (numValidDirections == 0) {
            results[threadId] = -1;
            return;
        }

        int chosenDirection = validDirections[int(curand_uniform(&state) * numValidDirections)];
        switch (chosenDirection) {
        case 0: y--; break;
        case 1: x++; break;
        case 2: y++; break;
        case 3: x--; break;
        }

        if (x >= 0 && x < width && y >= 0 && y < height && maze[y * width + x] != '#') {
            visited[y * width + x] = true;
            pathLength++;
        }

        if (x == width - 2 && y == height - 1) {
            found = true;
            break;
        }
    }

    if (found) {
        printf("%d: %d\n", threadId, pathLength);
        results[threadId] = pathLength;
    }
    else {
        results[threadId] = -1;
    }
}

std::vector<std::string> readMaze(const std::string& filename) {
    std::vector<std::string> maze;
    std::ifstream file(filename);
    std::string line;

    while (std::getline(file, line)) {
        maze.push_back(line);
    }

    return maze;
}

std::vector<char> linearizeMaze(const std::vector<std::string>& maze) {
    std::vector<char> linearMaze;
    for (const std::string& line : maze) {
        for (char c : line) {
            linearMaze.push_back(c);
        }
    }
    return linearMaze;
}

int main(int argc, char* argv[]) {
    std::vector<std::string> maze = readMaze("input");
    std::vector<char> linearMaze = linearizeMaze(maze);

    int width = maze[0].size();
    int height = maze.size();

    char* dev_maze;
    size_t size = linearMaze.size() * sizeof(char);
    cudaMalloc((void**)&dev_maze, size);
    cudaMemcpy(dev_maze, linearMaze.data(), size, cudaMemcpyHostToDevice);

    const int numThreads = 65535; // lol
    dim3 blockSize(512);
    dim3 gridSize((numThreads + blockSize.x - 1) / blockSize.x);

    int* dev_results;
    cudaMalloc((void**)&dev_results, numThreads * sizeof(int));

    monteCarloMazeKernel<<<gridSize, blockSize>>>(dev_maze, width, height, dev_results);

    int* host_results = new int[numThreads];
    cudaMemcpy(host_results, dev_results, numThreads * sizeof(int), cudaMemcpyDeviceToHost);

    int maxLength = 0;
    for (int i = 0; i < numThreads; i++) {
        if (host_results[i] > maxLength) {
            maxLength = host_results[i];
        }
    }
    std::cout << "Part 2: " << maxLength << std::endl;

    delete[] host_results;
    cudaFree(dev_results);
    cudaFree(dev_maze);

    return 0;
}
