#include <algorithm>
#include <iostream>
#include <array>
#include <cstdlib>
#include <ctime>
#include <unordered_map>
// #include <math.h>
using namespace std;
const int lenx = 20;
const int leny = 20;
const int depthmax = 3;

int eval[2][25] = {
    {999999, 900, 900, 900, 900, 700, 700, 700, 900, 300, 300, 50, 300, 300, 300, 300, 300, 250, 250, 200, 200, 200, 10, 300, 50},
    {-999999, -900, -900, -900, -900, -700, -700, -700, -900, -300, -300, -50, -300, -300, -300, -300, -300, -250, -250, -200, -200, -200, -10, -300, -50}};
int lines[32][5] = {
    {3, 3, 3, 3, 3},

    {3, 3, 3, 3, 0},
    {3, 0, 3, 3, 3},
    {3, 3, 0, 3, 3},
    {3, 3, 3, 0, 3},

    {3, 3, 3, 0, 0},
    {3, 0, 3, 3, 0},
    {3, 3, 0, 3, 0},

    {3, 3, 3, 3, 5},
    {3, 5, 3, 3, 3},
    {3, 3, 3, 5, 3},
    {3, 3, 5, 3, 3},

    {3, 3, 3, 0, 5},
    {3, 3, 3, 5, 0},
    {3, 3, 3, 5, 5},
    {3, 0, 3, 3, 5},
    {3, 3, 0, 3, 5},

    {3, 3, 0, 0, 0},
    {3, 0, 3, 0, 0},

    {3, 3, 0, 0, 5},
    {3, 3, 0, 5, 5},
    {3, 0, 3, 0, 5},
    {3, 0, 3, 5, 5},

    {3, 3, 5, 5, 5},
    {3, 3, 5, 0, 5},
    {3, 3, 5, 0, 0},
    {3, 3, 5, 3, 5},
    {3, 5, 3, 3, 5},

    {3, 0, 5, 0, 0},
    {3, 5, 0, 0, 0},
};
// void copy(int *maps, int *mapcopy)
// {
//     for (int x = 0; x < lenx; x++)
//     {
//         for (int y = 0; y < leny; y++)
//         {
//             mapcopy[x * leny + y] = maps[x * leny + y];
//         }
//     }
// }
// extern "C" __declspec(dllexport) void move(int *maps, int *mapcopy, int *point, int agentID)
// {
//     // copy(maps, mapcopy);
//     // // copy(maps, maps + lenx * leny, mapcopy);
//     mapcopy[point[0] * leny + point[1]] = agentID;
// }
extern "C" __declspec(dllexport) bool isDraw(int *maps)
{
    for (int x = 0; x < lenx; x++)
    {
        for (int y = 0; y < leny; y++)
        {
            if (maps[x * leny + y] == 0)
            {
                return true;
            }
        }
    }
    return false;
}

extern "C" __declspec(dllexport) int iswin(int *maps, int *point)
{

    int lineX[4] = {1, 1, 0, 1};
    int lineY[4] = {0, 1, 1, -1};
    int x = point[0];
    int y = point[1];
    int player = maps[x * leny + y];
    if (player != 0)
    {
        for (int i = 0; i < 4; i++)
        {
            int count = 1;
            for (int j = 1; j < 5; j++)
            {
                int vtx = x + lineX[i] * j;
                int vty = y + lineY[i] * j;
                if (vtx < 0 || vty < 0 || vtx >= lenx || vty >= leny)
                {
                    break;
                }
                if (maps[vtx * leny + vty] == player)
                {
                    count += 1;
                }
                else
                {
                    break;
                }
            }
            if (count == 5 && player == 1)
            {
                return 1;
            }
            else if (count == 5 && player == 2)
            {
                return 2;
            }
        }
    }

    return -1;
}
extern "C" __declspec(dllexport) int getLegalActions(int *maps, int *actions)
{

    int i = 0;
    for (int x = 0; x < lenx; x++)
    {
        for (int y = 0; y < leny; y++)
        {
            if (maps[x * leny + y] == 0)
            {
                actions[i * 2 + 0] = x;
                actions[i * 2 + 1] = y;
                i++;
            }
        }
    }
    return i;
}
extern "C" __declspec(dllexport) float getvalue(int line[], int head, int tail, int player)
{
    for (int i = 0; i < 5; ++i)
    {
        if (line[i] == player)
        {
            line[i] = 3;
        }
        else if (line[i] == 3 - player)
        {
            line[i] = 5;
        }
    }

    for (int i = 0; i < 32; ++i)
    {
        int *l = lines[i];
        bool isEqual = true;
        for (int j = 0; j < 5; ++j)
        {
            if (line[j] != l[j])
            {
                isEqual = false;
                break;
            }
        }
        if (isEqual)
        {
            if (i == 0 && tail == 4 && head == 4)
                return 0;
            else if (1 <= i && i <= 4)
            {
                if (tail == 4 && head == 4)
                    return 0;
            }
            else if (5 <= i && i <= 7)
            {
                if (tail == 4 && head == 4)
                    return 0;
                else if (head == 4)
                    return eval[player - 1][25 - 2];
            }
            else if (8 <= i && i <= 11)
            {
                if (tail == 4 && head == 4)
                    return 0;
                if ((i == 8 || i == 11) && head == 4)
                    return 0;
            }
            else if (12 <= i && i <= 16)
            {
                if (head == 4)
                    return 0;
            }
            else if (17 <= i && i <= 18)
            {
                if (tail == 4 && head == 4)
                    return 0;
                else if (head == 4)
                    return eval[player - 1][25 - 1];
            }
            else if (19 <= i && i <= 22)
            {
                if (head == 4)
                    return 0;
            }
            else if (23 <= i && i <= 27)
            {
                return eval[player - 1][25 - 1];
            }
            else if (i >= 28)
            {
                return eval[player - 1][25 - 3];
            }
            return eval[player - 1][i];
        }
    }
    return 0;
}

extern "C" __declspec(dllexport) float value(int *maps, int *point)
{
    int lineX[4] = {1, 1, 0, 1};
    int lineY[4] = {0, 1, 1, -1};
    int values[400] = {0};
    int k = 0;
    for (int x = 0; x < lenx; x++)
    {
        for (int y = 0; y < leny; y++)
        {
            int player = maps[x * leny + y];
            if (player != 0)
            {
                int i = 0, head = -1, tail = -1;
                int line[6];
                line[i] = player;

                for (int j = -1; j <= 5; j++)
                {
                    if (i = 0)
                        continue;
                    int vtx = x + lineX[i] * j;
                    int vty = y + lineY[i] * j;
                    if ((vtx < 0 || vty < 0 || vtx >= lenx || vty >= leny) && j == -1)
                        head = 4;
                    else if (j == -1 && maps[vtx * leny + vty] == 3 - player)
                        head = 4;
                    else if (j == -1 && maps[vtx * leny + vty] == player)
                    {
                        head = player;
                        break;
                    }
                    if (head == player)
                        break;
                    if ((vtx < 0 || vty < 0 || vtx >= lenx || vty >= leny) && j == 5)
                        tail = 4;
                    else if (j == 5 && maps[vtx * leny + vty] == 3 - player)
                        tail = 4;
                    if ((vtx < 0 || vty < 0 || vtx >= lenx || vty >= leny) && 1 <= j <= 4)
                    {
                        i++;
                        line[i] = 4;
                    }
                    else if (1 <= j <= 4)
                    {
                        i++;
                        line[i] = maps[vtx * leny + vty];
                    }

                    if (head == player)
                        continue;
                    int value = getvalue(line, head, tail, player);
                    values[k] = value;
                    k++;
                }
            }
        }
    }
    if (sizeof(values) / sizeof(values[0]) > 0)
    {
        int max_val = *std::max_element(values, values + 400);
        int min_val = *std::min_element(values, values + 400);

        if (max_val > std::abs(min_val))
        {
            return max_val;
        }
        else
        {
            return min_val;
        }
    }
    // return 0;
}
extern "C" __declspec(dllexport) float minmaxalphabeta(int *maps, int *point, int agentID, int depth, float alpha, float beta)
{

    // srand(static_cast<unsigned int>(time(nullptr)));
    if (depth == depthmax || isDraw(maps) == false || iswin(maps, point) != -1)
    {
        // return rand() % 2001 - 1000;
        return value(maps, point);
    }
    if (agentID == 2)
    {
        if (depth == depthmax)
            return value(maps, point);
        else
            return minmaxalphabeta(maps, point, 1, depth + 1, alpha, beta);
    }
    else
    {
        int tamp_arr[400][2];
        int *actions = (int *)tamp_arr;
        if (agentID == 1)
        {
            // cout << "234234" << endl;
            float maxEva = -999999999;
            int idx_ac = getLegalActions(maps, actions);
            for (int i = 0; i < idx_ac; i++)
            {
                int x = actions[i * 2 + 0], y = actions[i * 2 + 1];

                maps[x * leny + y] = agentID;
                float tamp = minmaxalphabeta(maps, point, agentID + 1, depth + 1, alpha, beta);
                maps[x * leny + y] = 0;
                maxEva = max(maxEva, tamp);
                alpha = max(alpha, maxEva);
                if (beta <= alpha)
                    break;
            }

            return maxEva;
        }
        else
        {
            float minEva = 999999999;
            int idx_ac = getLegalActions(maps, actions);
            for (int i = 0; i < idx_ac; i++)
            {
                int x = actions[i * 2 + 0], y = actions[i * 2 + 1];
                maps[x * leny + y] = agentID;
                float tamp = minmaxalphabeta(maps, point, agentID + 1, depth + 1, alpha, beta);
                maps[x * leny + y] = 0;
                minEva = min(minEva, tamp);
                beta = min(beta, minEva);
                if (beta <= alpha)
                    break;
            }
            return minEva;
        }
    }
}
extern "C" __declspec(dllexport) int add(int a, int b)
{
    return a + b;
}
// Function to print the map
// void printMap(int *map, int rows, int cols)
// {
//     for (int i = 0; i < rows; ++i)
//     {
//         for (int j = 0; j < cols; ++j)
//         {
//             cout << map[i * cols + j] << " ";
//         }
//         cout << endl;
//     }
// }

int main()
{
    // Example usage
    int maps[20][20] = {0};
    // int mapcopy[400][2];
    // int *a = (int *)mapcopy;
    int point[2] = {2, 3};
    // float d = minmaxalphabeta((int *)maps, (int *)point, 1, 1, -999999999, 999999999);
    float d = value((int *)maps, (int *)point);
    // printMap((int *)maps, 20, 20);
    // cout << int(d);
    return 0;
}