package org.dtu.analysis.controlChanges3;

public class LoopsChanges3 {

    // Change value added to 2
    // Should rerun tests where a > 0
    public static int stopAtPoint(int a) {
        int b = 0;
        for (int i = 0; i < a; i++) {
            if (i > 5) {
                break;
            }
            b += 2;
        }
        return b;
    }

    // Add more logic in inner loop
    // Should rerun tests where a >= 10
    public static int innerLoop(int a) {
        int c = 0;
        for (int i = 0; i < a; i++) {
            for (int j = 9; j < a; j++) {
                c += 1;
                c += 2;
            }
        }
        return c;
    }
}
