#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <regex>
// #include <math.h>

using namespace std;
const int lenx = 20;
const int leny = 20;
const int depthmax = 3;
const int maxsize = 12;
const int MININT = -999999999;
const int MAXINT = 999999999;
int evalState[lenx][leny];
void printMap(int *map, int rows, int cols);
void resetValue()
{
    for (int i = 0; i < lenx; i++)
    {
        for (int j = 0; j < leny; j++)
        {
            evalState[i][j] = 0;
        }
    }
}
int point[] = {
    4, 4, 4,
    8, 8, 8,
    8, 8, 8, 8, 8, 8,
    8,
    500, 500, 500, 500, 500, 500, 500,
    1000, 1000, 1000, 1000, 1000, 1000,
    100000};
char caseUser[][8] = {
    "11001", "10101", "10011",
    "00110", "01010", "01100",
    "11100", "11010", "10110", "01101", "01011", "00111",
    "01110",
    "011100", "011010", "010110", "001110", "1010101", "1011001", "1001101", // đánh 2 đường nữa là thắng
    "01111", "10111", "11011", "11101", "11101", "11110",
    "11111"};
char caseAI[][8] = {
    "22002", "20202", "20022",
    "00220", "02020", "02200",
    "22200", "22020", "20220", "02202", "02022", "00222",
    "02220",
    "022200", "022020", "020220", "002220", "2020202", "2022002", "2002202",
    "02222", "20222", "22022", "22202", "22202", "22220",
    "22222"};
int defenseScore[] = {0, 1, 9, 81, 729, 6534};    // bảng điểm phòng thủ
int attackScore[] = {0, 3, 24, 192, 1536, 12288}; // bảng điểm tấn công

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

    int countrow = 1;
    int coutcolum = 1;
    int coutcrossleft = 1;
    int coutcrossright = 1;
    int i = point[0];
    int j = point[1];
    int type = maps[i * leny + j];
    int lx = 19, ly = 19;
    if (type != 0)
    {
        int x = i;
        // Kiểm tra cột
        while ((x > 0) && (maps[(x - 1) * leny + j] == type))
        {
            coutcolum++;
            x--;
        }

        x = i;
        while ((x < lx) && (maps[(x + 1) * leny + j] == type))
        {
            coutcolum++;
            x++;
        }

        // Kiểm tra hàng
        int y = j;
        while ((y > 0) && (maps[i * leny + y - 1] == type))
        {
            countrow++;
            y--;
        }

        y = j;
        while ((y < ly) && (maps[i * leny + y + 1] == type))
        {
            countrow++;
            y++;
        }

        // Kiểm tra chéo trái
        y = j;
        x = i;
        while (((y > 0) && (x > 0)) && (maps[(x - 1) * leny + y - 1] == type))
        {
            coutcrossleft++;
            y--;
            x--;
        }

        y = j;
        x = i;
        while (((y < ly) && (x < lx)) && (maps[(x + 1) * leny + y + 1] == type))
        {
            coutcrossleft++;
            y++;
            x++;
        }

        // Kiểm tra chéo phải
        y = j;
        x = i;
        while (((y < ly) && (x > 0)) && (maps[(x - 1) * leny + y + 1] == type))
        {
            coutcrossright++;
            y++;
            x--;
        }

        y = j;
        x = i;
        while (((y > 0) && (x < lx)) && (maps[(x + 1) * leny + y - 1] == type))
        {
            coutcrossright++;
            y--;
            x++;
        }
        if (
            countrow == 5 || coutcolum == 5 || coutcrossleft == 5 || coutcrossright == 5)
            if (type == 1)
                return 1;
            else
                return 2;
    }
    return -1;
}

extern "C" __declspec(dllexport) void evaluateEachmaps(int *maps, int player)
{
    resetValue();
    int x, y, i, countAI, countUser;
    /*Kiểm tra theo hàng
     * -----
     * -----
     * -----
     * */
    for (x = 0; x < lenx; x++)
    {
        for (y = 0; y < leny - 4; y++)
        {
            countAI = 0;
            countUser = 0;
            /*đếm số ô người chơi và AI đã đánh ở đoạn từ y đến y+4*/
            for (i = 0; i < 5; i++)
            { // duyệt đoạn
                if (maps[x * leny + y + i] == 2)
                    countAI++;
                else if (maps[x * leny + y + i] == 1)
                    countUser++;
            }
            /*Nếu ở đoạn này một trong hai không đánh ô nào và người còn lại có đánh ít nhất 1 ô*/
            if (countAI * countUser == 0 && countAI != countUser)
            {
                for (i = 0; i < 5; i++)
                { // duyệt đoạn
                    if (maps[x * leny + y + i] == 0)
                    { // nếu ô này ko ai đánh
                        if (countAI == 0)
                        { // nếu ở đoạn này AI không đánh ô nào cả
                            if (player == 2)
                            {                                                   // nếu lượt chơi hiện tại là của AI
                                evalState[x][y + i] += defenseScore[countUser]; // thì cộng điểm phòng ngự ở ô này
                            }
                            else
                                evalState[x][y + i] += attackScore[countUser]; // ngược lại, thì tăng điểm tấn công ở ô này
                        }
                        else if (countUser == 0)
                        { // nếu ở đoạn này User không đánh ô nào cả
                            if (player == 1)
                            {                                                 // nếu lượt chơi hiện tại là của User
                                evalState[x][y + i] += defenseScore[countAI]; // thì cộng điểm phòng ngự ở ô này
                            }
                            else
                                evalState[x][y + i] += attackScore[countAI]; // ngược lại,cộng điểm tấn công của ô này
                        }
                        if (countAI == 4 || countUser == 4)
                        {                             // Nếu một trong hai người chơi có nước 4
                            evalState[x][y + i] *= 2; // thì lượng giá ô này lên gấp đôi
                        }
                    }
                }
            }
        }
    }
    /*Kiểm tra theo cột
     * |||||||
     * |||||||
     * |||||||
     * */
    for (x = 0; x < lenx - 4; x++)
    {
        for (y = 0; y < leny; y++)
        {
            countAI = 0;
            countUser = 0;
            for (i = 0; i < 5; i++)
            {
                if (maps[(x + i) * leny + y] == 2)
                    countAI++;
                else if (maps[(x + i) * leny + y] == 1)
                    countUser++;
            }
            if (countAI * countUser == 0 && countAI != countUser)
            {
                for (i = 0; i < 5; i++)
                {
                    if (maps[(x + i) * leny + y] == 0)
                    {
                        if (countAI == 0)
                        {
                            if (player == 2)
                            {
                                evalState[x + i][y] += defenseScore[countUser];
                            }
                            else
                                evalState[x + i][y] += attackScore[countUser];
                        }
                        else if (countUser == 0)
                        {
                            if (player == 1)
                            {
                                evalState[x + i][y] += defenseScore[countAI];
                            }
                            else
                                evalState[x + i][y] += attackScore[countAI];
                        }
                        if (countAI == 4 || countUser == 4)
                        {
                            evalState[x + i][y] *= 2;
                        }
                    }
                }
            }
        }
    }

    /*Kiểm tra theo đường chéo chính
     * \\\\\\
     * \\\\\\
     * \\\\\\
     * */
    for (x = 0; x < lenx - 4; x++)
    {
        for (y = 0; y < leny - 4; y++)
        {
            countAI = 0;
            countUser = 0;
            for (i = 0; i < 5; i++)
            {
                if (maps[(x + i) * leny + y + i] == 2)
                    countAI++;
                else if (maps[(x + i) * leny + y + i] == 1)
                    countUser++;
            }
            if (countAI * countUser == 0 && countAI != countUser)
            {
                for (i = 0; i < 5; i++)
                {
                    if (maps[(x + i) * leny + y + i] == 0)
                    {
                        if (countAI == 0)
                        {
                            if (player == 2)
                            {
                                evalState[x + i][y + i] += defenseScore[countUser];
                            }
                            else
                                evalState[x + i][y + i] += attackScore[countUser];
                        }
                        else if (countUser == 0)
                        {
                            if (player == 1)
                            {
                                evalState[x + i][y + i] += defenseScore[countAI];
                            }
                            else
                                evalState[x + i][y + i] += attackScore[countAI];
                        }
                        if (countAI == 4 || countUser == 4)
                        {
                            evalState[x + i][y + i] *= 2;
                        }
                    }
                }
            }
        }
    }

    /*Kiểm tra theo đường chéo phụ*/
    /* //////
     * //////
     * //////
     * */
    for (x = 4; x < lenx; x++)
    {
        for (y = 0; y < leny - 4; y++)
        {
            countAI = 0;
            countUser = 0;
            for (i = 0; i < 5; i++)
            {
                if (maps[(x - i) * leny + y + i] == 2)
                    countAI++;
                else if (maps[(x - i) * leny + y + i] == 1)
                    countUser++;
            }
            if (countAI * countUser == 0 && countAI != countUser)
            {
                for (i = 0; i < 5; i++)
                {
                    if (maps[(x - i) * leny + y + i] == 0)
                    {
                        if (countAI == 0)
                        {
                            if (player == 2)
                            {
                                evalState[x - i][y + i] += defenseScore[countUser];
                            }
                            else
                                evalState[x - i][y + i] += attackScore[countUser];
                        }
                        else if (countUser == 0)
                        {
                            if (player == 1)
                            {
                                evalState[x - i][y + i] += defenseScore[countAI];
                            }
                            else
                                evalState[x - i][y + i] += attackScore[countAI];
                        }
                        if (countAI == 4 || countUser == 4)
                        {
                            evalState[x - i][y + i] *= 2;
                        }
                    }
                }
            }
        }
    }
}
extern "C" __declspec(dllexport) int lengthNum(int a)
{
    if (a == 0)
        return 1;
    if (a < 0)
        a *= -1;
    int dem = 0;
    while (a > 0)
    {
        a /= 10;
        dem++;
    }
    return dem;
}
extern "C" __declspec(dllexport) int getLegalActions(int *maps, int *actions, int player)

{
    evaluateEachmaps(maps, player);
    int size = maxsize; // số phần tử tối đa được phép lấy
    int maxValueList[maxsize];
    int maxCellList[maxsize][2];
    // khởi tạo giá trị
    for (int i = 0; i < size; i++)
    {
        maxValueList[i] = MININT;
        maxCellList[i][0] = -1;
        maxCellList[i][1] = -1;
    }

    for (int x = 0; x < lenx; x++)
    {
        for (int y = 0; y < leny; y++)
        {
            int value = evalState[x][y];
            /*Tìm list những ô tối ưu để đánh*/
            for (int i = size - 1; i >= 0; i--)
            {
                if (maxValueList[i] <= value && value != 0)
                {
                    /* sắp xếp theo thứ tự giảm dần */
                    for (int j = 0; j < i; j++)
                    {                                          // cập nhật những phần tử trước i
                        maxValueList[j] = maxValueList[j + 1]; // cập nhật điểm
                        maxCellList[j][0] = maxCellList[j + 1][0];
                        maxCellList[j][1] = maxCellList[j + 1][1];
                    }
                    // cập nhật phần tử i
                    maxValueList[i] = value;
                    maxCellList[i][0] = x;
                    maxCellList[i][1] = y;
                    break;
                }
            }
        }
    }
    // add vào list những phần tử có số điểm lớn nhất có độ lớn gần bằng nhau(ex: 981, 857, 80, 15 => chỉ chọn 981 và 857)
    int maxLength = lengthNum(maxValueList[size - 1]); // length của số lớn nhất
    int difference[6] = {0, 2, 8, 32, 128, 512};       // chênh lệch theo từng cấp độ dài so với phần tử lớn nhất

    int k = 0;
    actions[k * 2 + 0] = maxCellList[size - 1][0]; // add vào phần tử có điểm lớn nhất
    actions[k * 2 + 1] = maxCellList[size - 1][1];
    k++;

    for (int i = size - 2; i >= 0; i--)
    { // add vào các phần tử còn lại phù hợp điều kiện
        if (maxValueList[size - 1] - maxValueList[i] <= difference[maxLength])
        { // chỉ chấp nhận chênh lệch so với pt lớn nhất trong khoảng quy định

            actions[k * 2 + 0] = maxCellList[i][0];
            actions[k * 2 + 1] = maxCellList[i][1];
        }
        else
            break;
    }

    return k;
}

int count(const char *text, const char *find)
{
    int i = 0;
    const char *p = text;
    const char *q = find;
    while (*p != '\0')
    {
        const char *r = p;
        while (*r == *q && *q != '\0')
        {
            ++r;
            ++q;
        }
        if (*q == '\0')
        {
            ++i;
        }
        ++p;
        q = find;
    }
    return i;
}
extern "C" __declspec(dllexport) float value(int *maps)
{

    char rem[5000];
    rem[0] = '\0';
    char num_str[10];

    // check hàng và cột (|,__)
    for (int i = 0; i < lenx; i++)
    {
        for (int j = 0; j < leny; j++)
        {
            strcat(rem, itoa(maps[i * leny + j], num_str, 10));
        }
        strcat(rem, ";");
        for (int j = 0; j < leny; j++)
        {
            strcat(rem, itoa(maps[j * leny + i], num_str, 10));
        }
        strcat(rem, ";");
    }
    // check nửa trên đường chéo phải ( \ )
    for (int i = 0; i < lenx - 4; i++)
    {
        for (int j = 0; j < leny - i; j++)
        {

            strcat(rem, itoa(maps[j * leny + i + j], num_str, 10));
        }
        strcat(rem, ";");
    }
    // check nửa dưới đường chéo phải ( \ )
    for (int i = lenx - 5; i > 0; i--)
    {
        for (int j = 0; j < leny - i; j++)
        {
            strcat(rem, itoa(maps[(i + j) * leny + j], num_str, 10));
        }
        strcat(rem, ";");
    }
    // check nửa trên đường chéo trái ( / )
    for (int i = 4; i < lenx; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            strcat(rem, itoa(maps[(i - j) * leny + j], num_str, 10));
        }
        strcat(rem, ";");
    }
    // check nửa dưới đường chéo trái ( / )
    for (int i = lenx - 5; i > 0; i--)
    {
        for (int j = leny - 1; j >= i; j--)
        {
            strcat(rem, itoa(maps[j * leny + i + leny - j - 1], num_str, 10));
        }
        strcat(rem, ";\n");
    }
    // cout << rem;
    char find1[8], find2[8];
    int diem = 0;
    // Tính điểm của trạng thái
    for (int i = 0; i < 27; i++)
    {                                         // duyệt các đường chiến lược
        strcpy(find1, caseAI[i]);             // duyệt những đường chiến lược của AI
        strcpy(find2, caseUser[i]);           // duyệt những đường chiến lược của User
        diem += point[i] * count(rem, find1); // cộng vào điểm lượng giá của AI
        diem -= point[i] * count(rem, find2); // trừ đi điểm lượng giá của User
    }
    return diem;
}
extern "C" __declspec(dllexport) float minmaxalphabeta(int *maps, int *point, int agentID, int depth, float alpha, float beta)
{

    // srand(static_cast<unsigned int>(time(nullptr)));
    if (depth > depthmax || isDraw(maps) == false || iswin(maps, point) != -1)
    {
        // return rand() % 2001 - 1000;
        return value(maps);
    }
    if (agentID == 2)
    {
        if (depth == depthmax)
            // return rand() % 2001 - 1000;
            return value(maps);
        else
            return minmaxalphabeta(maps, point, 1, depth + 1, alpha, beta);
    }
    else
    {
        int tamp_arr[maxsize][2];
        int *actions = (int *)tamp_arr;
        if (agentID == 2)
        {
            // cout << "234234" << endl;
            float maxEva = MININT;
            int idx_ac = getLegalActions(maps, actions, agentID);
            for (int i = 0; i < idx_ac; i++)
            {
                int x = actions[i * 2 + 0], y = actions[i * 2 + 1];

                maps[x * leny + y] = agentID;
                point[0] = x;
                point[1] = y;
                float tamp = minmaxalphabeta(maps, point, agentID + 1, depth + 1, alpha, beta);
                maps[x * leny + y] = 0;
                maxEva = max(maxEva, tamp);
                alpha = max(alpha, maxEva);
                if (beta <= alpha)
                    break;
            }
            return maxEva;
        }
        else if (agentID == 1)
        {
            float minEva = MAXINT;
            int idx_ac = getLegalActions(maps, actions, agentID);
            for (int i = 0; i < idx_ac; i++)
            {
                int x = actions[i * 2 + 0], y = actions[i * 2 + 1];
                maps[x * leny + y] = agentID;
                point[0] = x;
                point[1] = y;
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
    return -1;
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
// void print(int map[][20])
// {
//     for (int i = 0; i < 20; ++i)
//     {
//         cout << i << "\t";
//     }
//     cout << endl;
//     cout << endl;
//     for (int i = 0; i < 20; ++i)
//     {
//         cout << i << " ";
//         for (int j = 0; j < 20; ++j)
//         {
//             cout << map[i][j] << "\t";
//         }
//         cout << endl;
//     }
//     cout << endl;
// }
int main()
{
    // int map[20][20] = {0};
    // map[8][11] = 1;
    // map[9][12] = 2;
    // map[10][13] = 2;
    // map[10][12] = 1;
    // map[11][12] = 1;
    // int *maps = (int *)map;
    // int acti[maxsize][2];
    // int *action = (int *)acti;
    // // cout << getLegalActions(maps, action, 1);
    // evaluateEachmaps(maps, 2);
    // print(map);
    // print(evalState);
    return 1;
}

// g++ -shared -o brain.dll brain.cpp