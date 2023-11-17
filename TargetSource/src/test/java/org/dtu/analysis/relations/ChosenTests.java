package org.dtu.analysis.relations;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class ChosenTests {

    @Test
    void GetA_Test() {
        assertEquals(1, Chosen.GetA());
    }

    @Test
    void GetB_Test() {
        assertEquals(2, Chosen.GetB());
    }

    @Test
    void GetC_Test() {
        assertEquals(3, Chosen.GetC());
    }

    @Test
    void GetD_Test() {
        assertEquals(4, Chosen.GetD());
    }

    @Test
    void GetE_Test() {
        assertEquals(5, Chosen.GetE());
    }

    @Test
    void SumAB_Test() {
        assertEquals(3, Chosen.SumAB());
    }

    @Test
    void SumAC_Test() {
        assertEquals(4, Chosen.SumAC());
    }

    @Test
    void SumBD_Test() {
        assertEquals(6, Chosen.SumBD());
    }

    @Test
    void SumDE_Test() {
        assertEquals(9, Chosen.SumDE());
    }

    @Test
    void SumEE_Test() {
        assertEquals(10, Chosen.SumEE());
    }

    @Test
    void SumTwo_AB_Test() {
        assertEquals(10, Chosen.SumTwo(0, 1));
    }

    @Test
    void SumTwo_AC_Test() {
        assertEquals(10, Chosen.SumTwo(0, 2));
    }

    @Test
    void SumTwo_BD_Test() {
        assertEquals(10, Chosen.SumTwo(1, 3));
    }

    @Test
    void SumTwo_DE_Test() {
        assertEquals(10, Chosen.SumTwo(3, 4));
    }

    @Test
    void SumTwo_EE_Test() {
        assertEquals(10, Chosen.SumTwo(4, 4));
    }
}
