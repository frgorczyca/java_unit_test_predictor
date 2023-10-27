package org.dtu.analysis.control;

public class LoopsChanges4 {

    // No changes
    public static int stopAtPoint(int a) {
        int b = 0;
        for (int i = 0; i < a; i++) {
            if (i > 5) {
                break;
            }
            b += 1;
        }
        return b;
    }

    // Add more logic in outer loop
    // Should rerun tests where a > 0
    public static int innerLoop(int a) {
        int c = 0;
        for (int i = 0; i < a; i++) {
            c += 1;
            for (int j = 9; j < a; j++) {
                c += 1;
            }
        }
        return c;
    }
}
