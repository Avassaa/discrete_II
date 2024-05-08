#include <iostream>
using namespace std;
class GameOfLife {
        static void seperate_row(const int row_c) {
            cout<<endl;
            for(int i=0;i<row_c;i++) {
                cout<<"-----";
            }
            cout<<endl;
        }
        static int**  initialize_map(const int row,const int col) {
            int** game_table=(int**)malloc(sizeof(int*)*row);
            for(int i =0;i<row;i++) {
                game_table[i]=(int*)malloc(sizeof(int)*col);
            }
            for(int i =0;i<row;i++) {
                for(int j=0;j<col;j++) {
                    game_table[i][j]=(rand()%2);
                }
            }
            return game_table;
        }
        static void print_table(int rows,int cols,int** table) {
            seperate_row(rows);
            for(int i =0;i<rows;i++) {
                cout<<"|";
                for(int j =0;j<cols;j++) {
                    cout<<" "<<table[i][j]<<" |";
                }
                seperate_row(rows);
            }
        }
        static int count_alive_neighbors(int** table,int row,int col,int row_c,int col_c) {
            int count=0;
            for(int i =row-1;i<=row+1;i++) {
                for(int j =col-1;j<=col+1;j++) {
                    if((i<0 || j<0) || (i==row && j==col) || (i>=row_c || j >= col_c)) // TODO: row and col should not exceed their respective sizes.
                        continue;
                    if(table[i][j]==1)
                        count++;
                }

            }
            return count;
        }
    static void update_map(int**& map, int row, int col) {
            int** temp_map = new int*[row];
            for(int i = 0; i < row; ++i) {
                temp_map[i] = new int[col];
            }

            for(int i = 0; i < row; i++) {
                for(int j = 0; j < col; j++) {
                    int alive_neighbors = count_alive_neighbors(map, i, j, row, col);
                    if(map[i][j] == 1 && (alive_neighbors == 2 || alive_neighbors == 3))
                        temp_map[i][j] = 1;
                    else if (map[i][j] == 0 && alive_neighbors == 3)
                        temp_map[i][j] = 1;
                    else
                        temp_map[i][j] = 0;
                }
            }

            for(int i = 0; i < row; i++) {
                for(int j = 0; j < col; j++) {
                    map[i][j] = temp_map[i][j];
                }
            }

            for(int i = 0; i < row; ++i) {
                delete[] temp_map[i];
            }
            delete[] temp_map;
        }
public:
    static void start_game(int row ,int col,int iterations) {

            int ** table=initialize_map(row,col);
            for(int i =0;i<iterations;i++) {
                if(i==0) {
                    cout<<"Initial table:";
                }
                else {
                    cout<<"Iteration:"<<i<<endl;
                }
                print_table(row,col,table);
                for(int j =0;j<3;j++)
                    cout<<endl;
                update_map(table,row,col);
            }
        free(table);
        }



};

int main() {
    cout<<"Game of Life simulation baha"<<endl;
    GameOfLife::start_game(5,5,3);
    return 0;
}

