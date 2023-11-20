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
        assertEquals(2115098112, Chosen.GetC());
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
    void IfElse_True_Test() {
        assertEquals(1, Chosen.IfElse(true));
    }

    @Test
    void IfElse_False_Test() {
        assertEquals(2, Chosen.IfElse(false));
    }

    @Test
    void NestedCalls_Test() {
        assertEquals(8, Chosen.NestedCall());
    }

    @Test
    void SumAB_Test() {
        assertEquals(3, Chosen.SumAB());
    }

    @Test
    void SumAC_Test() {
        assertEquals(2115098113, Chosen.SumAC());
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
    void SumTwo_AA_Test() {
        assertEquals(2, Chosen.SumTwo(0, 0));
    }

    @Test
    void SumTwo_AB_Test() {
        assertEquals(3, Chosen.SumTwo(0, 1));
    }

    @Test
    void SumTwo_AC_Test() {
        assertEquals(2115098113, Chosen.SumTwo(0, 2));
    }

    @Test
    void SumTwo_AD_Test() {
        assertEquals(5, Chosen.SumTwo(0, 3));
    }

    @Test
    void SumTwo_AE_Test() {
        assertEquals(6, Chosen.SumTwo(0, 4));
    }

    @Test
    void SumTwo_BA_Test() {
        assertEquals(3, Chosen.SumTwo(1, 0));
    }

    @Test
    void SumTwo_BB_Test() {
        assertEquals(4, Chosen.SumTwo(1, 1));
    }

    @Test
    void SumTwo_BC_Test() {
        assertEquals(2115098114, Chosen.SumTwo(1, 2));
    }

    @Test
    void SumTwo_BD_Test() {
        assertEquals(6, Chosen.SumTwo(1, 3));
    }

    @Test
    void SumTwo_BE_Test() {
        assertEquals(7, Chosen.SumTwo(1, 4));
    }

    @Test
    void SumTwo_CA_Test() {
        assertEquals(2115098113, Chosen.SumTwo(2, 0));
    }

    @Test
    void SumTwo_CB_Test() {
        assertEquals(2115098114, Chosen.SumTwo(2, 1));
    }

    @Test
    void SumTwo_CC_Test() {
        // Becomes negative due to overflow
        assertEquals(-64771072, Chosen.SumTwo(2, 2));
    }

    @Test
    void SumTwo_CD_Test() {
        assertEquals(2115098116, Chosen.SumTwo(2, 3));
    }

    @Test
    void SumTwo_CE_Test() {
        assertEquals(2115098117, Chosen.SumTwo(2, 4));
    }

    @Test
    void SumTwo_DA_Test() {
        assertEquals(5, Chosen.SumTwo(3, 0));
    }

    @Test
    void SumTwo_DB_Test() {
        assertEquals(6, Chosen.SumTwo(3, 1));
    }

    @Test
    void SumTwo_DC_Test() {
        assertEquals(2115098116, Chosen.SumTwo(3, 2));
    }

    @Test
    void SumTwo_DD_Test() {
        assertEquals(8, Chosen.SumTwo(3, 3));
    }

    @Test
    void SumTwo_DE_Test() {
        assertEquals(9, Chosen.SumTwo(3, 4));
    }

    @Test
    void SumTwo_EA_Test() {
        assertEquals(6, Chosen.SumTwo(4, 0));
    }

    @Test
    void SumTwo_EB_Test() {
        assertEquals(7, Chosen.SumTwo(4, 1));
    }

    @Test
    void SumTwo_EC_Test() {
        assertEquals(2115098117, Chosen.SumTwo(4, 2));
    }

    @Test
    void SumTwo_ED_Test() {
        assertEquals(9, Chosen.SumTwo(4, 3));
    }

    @Test
    void SumTwo_EE_Test() {
        assertEquals(10, Chosen.SumTwo(4, 4));
    }
}
