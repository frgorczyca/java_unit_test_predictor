package org.dtu.analysis.control;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LoopsTest {

    @Test
    void stopAtPoint_minus_1000() {
        assertEquals(0, Loops.stopAtPoint(-1000));
    }

    @Test
    void stopAtPoint_minus_1() {
        assertEquals(0, Loops.stopAtPoint(-1));
    }

    @Test
    void stopAtPoint_0() {
        assertEquals(0, Loops.stopAtPoint(0));
    }

    @Test
    void stopAtPoint_1() {
        assertEquals(1, Loops.stopAtPoint(1));
    }

    @Test
    void stopAtPoint_3() {
        assertEquals(3, Loops.stopAtPoint(3));
    }

    @Test
    void stopAtPoint_6() {
        assertEquals(6, Loops.stopAtPoint(6));
    }

    @Test
    void stopAtPoint_10() {
        assertEquals(6, Loops.stopAtPoint(10));
    }

    @Test
    void stopAtPoint_1000() {
        assertEquals(6, Loops.stopAtPoint(1000));
    }

    @Test
    void innerLoop_minus_1000() {
        assertEquals(0, Loops.innerLoop(-1000));
    }

    @Test
    void innerLoop_minus_1() {
        assertEquals(0, Loops.innerLoop(-1));
    }

    @Test
    void innerLoop_zero() {
        assertEquals(0, Loops.innerLoop(0));
    }

    @Test
    void innerLoop_1() {
        assertEquals(0, Loops.innerLoop(1));
    }

    @Test
    void innerLoop_9() {
        assertEquals(0, Loops.innerLoop(9));
    }

    @Test
    void innerLoop_10() {
        assertEquals(10, Loops.innerLoop(10));
    }

    @Test
    void innerLoop_11() {
        assertEquals(22, Loops.innerLoop(11));
    }

    @Test
    void innerLoop_1000() {
        assertEquals(991000, Loops.innerLoop(1000));
    }
}