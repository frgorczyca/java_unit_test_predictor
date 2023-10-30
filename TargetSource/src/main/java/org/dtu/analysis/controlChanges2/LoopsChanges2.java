package org.dtu.analysis.controlChanges2;

public class LoopsChanges2 {

    // Change stop value to 1
    // Should rerun all tests where a >= 3
    public static int stopAtPoint(int a) {
        int b = 0;
        for (int i = 1; i < a; i++) {
            if (i > 1) {
                break;
            }
            b += 1;
        }
        return b;
    }

    // Change inner loop start to 0
    // Should rerun all where a > 0
    public static int innerLoop(int a) {
        int c = 0;
        for (int i = 0; i < a; i++) {
            for (int j = 0; j < a; j++) {
                c += 1;
            }
        }
        return c;
    }
}
