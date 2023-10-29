package org.dtu.analysis.relations;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class RelationsTests {

    @Test
    void BasicClass_SetsAndReturnsId () {
        Basic b = new Basic();

        int id = 4;
        b.SetId(id);

        assertEquals(b.GetId(), id);
    }

    @Test
    void Offspring_SetsAndReturnsOffsetId () {
        int offset = 7;

        Offspring o = new Offspring(offset);

        int id = 5;
        o.SetId(id);

        assertEquals(o.GetOffsetId(),id + offset);
    }

    @Test
    void Composed_ReturnsIdSum() {
        Basic b = new Basic();

        int basicId = 4;
        b.SetId(basicId);

        int offset = 7;

        Offspring o = new Offspring(offset);

        int offspringId = 5;
        o.SetId(offspringId);

        Composed c = new Composed(b, o);

        assertEquals(c.GetIdSum(), basicId+offspringId+offset);
    }

    @Test
    void Composed_ReturnsLabel() {
        Basic b = new Basic();
        Offspring o = new Offspring(1);
        Composed c = new Composed(b, o);

        assertEquals(c.GetLabel(), BaseMapping.L1.label);
    }

}
