#include <stdio.h>

extern void init_no2_o3_internal(void);
extern void init_no2_o3(void);
extern void calc_no2_o3(float no2, float o3);

int main(void)
{
    init_no2_o3_internal();
    init_no2_o3();
    calc_no2_o3(45.0f, 20.0f);
    printf("=== SUCCESS ===\n");
    return 0;
}
