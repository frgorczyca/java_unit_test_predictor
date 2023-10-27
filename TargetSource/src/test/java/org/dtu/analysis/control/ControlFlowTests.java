package org.dtu.analysis.control;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ControlFlowTests {

    @Test
    void boolCheck_boolIsTrue() {
        assertEquals(1, Conditions.boolCheck(true));
    }

    @Test
    void boolCheck_boolIsFalse() {
        assertEquals(0, Conditions.boolCheck(false));
    }

    @Test
    void greaterThanZero_minus_1000() {
        assertEquals(1001, Conditions.greaterThanZero(-1000));
    }

    @Test
    void greaterThanZero_minus_1() {
        assertEquals(2, Conditions.greaterThanZero(-1));
    }

    @Test
    void greaterThanZero_0() {
        assertEquals(1, Conditions.greaterThanZero(0));
    }

    @Test
    void greaterThanZero_1() {
        assertEquals(1, Conditions.greaterThanZero(1));
    }

    @Test
    void greaterThanZero_1000() {
        assertEquals(1000, Conditions.greaterThanZero(1000));
    }

    @Test
    void elseIf_minus_1000() {
        assertEquals(-1, Conditions.elseIf(-1000));
    }

    @Test
    void elseIf_minus_1() {
        assertEquals(-1, Conditions.elseIf(-1));
    }

    @Test
    void elseIf_0() {
        assertEquals(0, Conditions.elseIf(0));
    }

    @Test
    void elseIf_1() {
        assertEquals(1, Conditions.elseIf(1));
    }

    @Test
    void elseIf_1000() {
        assertEquals(1, Conditions.elseIf(1000));
    }
}
