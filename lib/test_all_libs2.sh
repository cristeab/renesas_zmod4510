#!/bin/bash
# =====================================================================
# Clean test of all ZMOD4510 libraries executed from the 'lib' directory
# Matches exactly: ./no2_o3-example output
# =====================================================================

# Check if we are actually standing in the 'lib' directory
if [ "$(basename "$(pwd)")" != "lib" ]; then
    echo "❌ Error: You must run this script from the 'lib' directory!"
    echo "Run: cd ~/renesas_zmod4510/lib && ./test_all_libs2.sh"
    exit 1
fi

echo "=== Complete ZMOD4510 Library Test via CMake ==="
echo "Script directory (libraries): $(pwd)"
echo "Build directory: $(dirname "$(pwd)")/build"
echo

LIB_DIR="$(pwd)"
BUILD_DIR="$(dirname "$LIB_DIR")/build"

# Ensure build directory exists
mkdir -p "$BUILD_DIR"

# Clean any leftover libraries in the root of lib/ from previous runs
rm -f lib_no2_o3.a lib_zmod4xxx_cleaning.a 2>/dev/null

# Scan subdirectories inside lib/ looking for source libraries
find . -mindepth 2 -name "lib_no2_o3.a" -not -path "*/old_root_libs/*" -exec dirname {} \; | sort | while read dir; do

    echo "────────────────────────────────────────────────────────"
    echo "Testing architecture from: $dir"

    # 1. Copy the tested libraries directly into the root of lib/
    cp "$dir"/lib_no2_o3.a "$LIB_DIR"/ 2>/dev/null
    cp "$dir"/lib_zmod4xxx_cleaning.a "$LIB_DIR"/ 2>/dev/null
    sync # Force disk synchronization

    # 2. Completely wipe the neighboring build/ directory to clear old cache
    rm -rf "$BUILD_DIR"/* 2>/dev/null

    # 3. Switch to the build directory for compilation
    cd "$BUILD_DIR" >/dev/null

    # 4. Run the CMake configuration
    if cmake -S .. -B . -DCMAKE_C_COMPILER=gcc-6 -DCMAKE_BUILD_TYPE=Release >/dev/null 2>&1; then
        
        # 5. Run the project compilation
        if make -j4 >/dev/null 2>&1; then
            echo "   ✅ CMake Compilation: SUCCESSFUL"
            sync 

            # 6. Target the specific example binary explicitly
            TARGET_BIN="./no2_o3-example"

            if [ ! -f "$TARGET_BIN" ]; then
                echo "   ❌ Error: Compilation succeeded, but $TARGET_BIN was not created."
            else
                # 7. EXECUTE THE BINARY AND CAPTURE LOGS VIA A TEMPORARY FILE
                TMP_LOG=$(mktemp)
                
                # Run with a 3-second timeout
                timeout 3s "$TARGET_BIN" > "$TMP_LOG" 2>&1
                STATUS=$?
                
                OUTPUT=$(cat "$TMP_LOG")
                rm -f "$TMP_LOG"

                # Handle specific ARM hardware termination statuses
                if [ $STATUS -eq 135 ]; then
                    OUTPUT="[System reported: Bus error (Memory bus conflict / file locked)]"
                elif [ $STATUS -eq 139 ]; then
                    OUTPUT="[System reported: Segmentation fault (Invalid memory access / wrong CPU architecture)]"
                fi

                echo "DEBUG - Status: $STATUS"
                echo "DEBUG - Program Output:"
                echo "----------------------------------------"
                echo "$OUTPUT"
                echo "----------------------------------------"

                # 8. EVALUATION: Check for your exact target hardware error strings
                if echo "$OUTPUT" | grep -q "Failed to write to the I2C device" && echo "$OUTPUT" | grep -q "Error during sensor initialization"; then
                    echo "   ✅ Binary execution ($TARGET_BIN): SUCCESSFUL (Architecture OK, matched I2C failure)"
                elif [ $STATUS -eq 0 ] || [ $STATUS -eq 124 ]; then
                    echo "   ✅ Binary execution ($TARGET_BIN): SUCCESSFUL (No Segfault / Running loop)"
                else
                    echo "   ❌ Binary execution: FAILED (Wrong architecture / Memory crash)"
                fi
            fi
        else
            echo "   ❌ CMake Compilation (make -j4): FAILED"
        fi
    else
        echo "   ❌ CMake Configuration: FAILED"
    fi

    # 9. Return to lib/ and clean up with a tiny safe delay
    cd "$LIB_DIR" >/dev/null
    sleep 0.2 # Gives the OS 200ms to completely release the binary from RAM
    rm -f lib_no2_o3.a lib_zmod4xxx_cleaning.a 2>/dev/null
    echo
done

echo "=== All CMake tests completed ==="
