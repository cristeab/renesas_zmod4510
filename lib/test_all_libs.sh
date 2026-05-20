#!/bin/bash
# =============================================
# Čistý test všetkých ZMOD4510 knižníc
# =============================================

echo "=== Kompletný test všetkých ZMOD4510 knižníc ==="
echo "Priečinok: $(pwd)"
echo

find . -name "lib_no2_o3.a" -exec dirname {} \; | sort | while read dir; do
    
    echo "────────────────────────────────────────"
    echo "Testujem: $dir"
    
    cp -v "$dir"/lib_no2_o3.a . 2>/dev/null
    cp -v "$dir"/lib_zmod4xxx_cleaning.a . 2>/dev/null
    
    cat > test.c << 'EOF'
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
EOF

    rm -f test.o test_program 2>/dev/null
    
    if gcc-6 -c test.c -o test.o && gcc-6 -o test_program test.o *.a -lm 2>/dev/null; then
        echo "   ✅ Kompilácia ÚSPEŠNÁ"
        
        # Čisté spustenie bez otravného hlásenia
        timeout 3s ./test_program >/dev/null 2>&1
        STATUS=$?
        
        if [ $STATUS -eq 0 ]; then
            echo "   ✅ Spustenie ÚSPEŠNÉ"
        else
            echo "   ❌ Spustenie - Segmentation fault"
        fi
    else
        echo "   ❌ Kompilácia ZLYHALA"
    fi
    echo
done

echo "=== Všetky testy dokončené ==="
