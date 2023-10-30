package org.dtu.analysis.controlChanges1;

public class LoopsChanges1 {

    // Change start value to 1
    // Should rerun all tests
    public static int stopAtPoint(int a) {
        int b = 0;
        for (int i = 1; i < a; i++) {
            if (i > 5) {
                break;
            }
            b += 1;
        }
        return b;
    }

    // Change counter start value to 1
    // Should rerun all tests
    public static int innerLoop(int a) {
        int c = 1;
        for (int i = 0; i < a; i++) {
            for (int j = 9; j < a; j++) {
                c += 1;
            }
        }
        return c;
    }
}
